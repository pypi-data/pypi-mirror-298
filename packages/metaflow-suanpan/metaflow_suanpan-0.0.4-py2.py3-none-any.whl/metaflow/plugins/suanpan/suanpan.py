import base64
import json
import os
import re
import shlex
import sys
from collections import defaultdict
from hashlib import sha1
from math import inf
from typing import List, Tuple
import uuid
import copy
from metaflow import JSONType, current
from metaflow.decorators import flow_decorators
from metaflow.exception import MetaflowException
from metaflow.graph import DAGNode, FlowGraph
from metaflow.includefile import FilePathClass
from metaflow.metaflow_config import (
    ARGO_EVENTS_EVENT,
    ARGO_EVENTS_EVENT_BUS,
    ARGO_EVENTS_EVENT_SOURCE,
    ARGO_EVENTS_INTERNAL_WEBHOOK_URL,
    ARGO_EVENTS_SERVICE_ACCOUNT,
    ARGO_EVENTS_WEBHOOK_AUTH,
    ARGO_WORKFLOWS_CAPTURE_ERROR_SCRIPT,
    ARGO_WORKFLOWS_ENV_VARS_TO_SKIP,
    ARGO_WORKFLOWS_KUBERNETES_SECRETS,
    ARGO_WORKFLOWS_UI_URL,
    AWS_SECRETS_MANAGER_DEFAULT_REGION,
    AZURE_KEY_VAULT_PREFIX,
    AZURE_STORAGE_BLOB_SERVICE_ENDPOINT,
    CARD_AZUREROOT,
    CARD_GSROOT,
    CARD_S3ROOT,
    DATASTORE_SYSROOT_AZURE,
    DATASTORE_SYSROOT_GS,
    DATASTORE_SYSROOT_S3,
    DATATOOLS_S3ROOT,
    DEFAULT_METADATA,
    DEFAULT_SECRETS_BACKEND_TYPE,
    GCP_SECRET_MANAGER_PREFIX,
    KUBERNETES_FETCH_EC2_METADATA,
    KUBERNETES_LABELS,
    KUBERNETES_NAMESPACE,
    KUBERNETES_NODE_SELECTOR,
    KUBERNETES_SANDBOX_INIT_SCRIPT,
    KUBERNETES_SECRETS,
    S3_ENDPOINT_URL,
    S3_SERVER_SIDE_ENCRYPTION,
    SERVICE_HEADERS,
    SERVICE_INTERNAL_URL,
    UI_URL,
)
from metaflow.metaflow_config_funcs import config_values
from metaflow.mflog import BASH_SAVE_LOGS, bash_capture_logs, export_mflog_env_vars
from metaflow.parameters import deploy_time_eval
from metaflow.plugins.kubernetes.kubernetes import (
    parse_kube_keyvalue_list,
    validate_kube_labels,
)
from metaflow.plugins.kubernetes.kubernetes_jobsets import KubernetesArgoJobSet
from metaflow.unbounded_foreach import UBF_CONTROL, UBF_TASK
from metaflow.util import (
    compress_list,
    dict_to_cli_options,
    to_bytes,
    to_camelcase,
    to_unicode,
)


class Suanpanflows(object):
    def __init__(
        self,
        name,
        graph: FlowGraph,
        flow,
        code_package_sha,
        code_package_url,
        metadata,
        flow_datastore,
        environment,
        event_logger,
        monitor,
    ):
        self.name = name
        self.graph = graph
        self.flow = flow
        self.code_package_sha = code_package_sha
        self.code_package_url = code_package_url
        self.metadata = metadata
        self.flow_datastore = flow_datastore
        self.environment = environment
        self.event_logger = event_logger
        self.monitor = monitor
        self.parameters = self._process_parameters()
        self._workflow_template = self._compile_workflow_template()

    def __str__(self):
        return str(self._workflow_template)

    def to_json(self):
        return self._workflow_template

    @staticmethod
    def _sanitize(name):
        # return name.replace("_", "-")
        return name

    def _process_parameters(self):
        parameters = {}
        has_schedule = self.flow._flow_decorators.get("schedule") is not None
        seen = set()
        for var, param in self.flow._get_parameters():
            # Throw an exception if the parameter is specified twice.
            norm = param.name.lower()
            if norm in seen:
                raise MetaflowException(
                    "Parameter *%s* is specified twice. "
                    "Note that parameter names are "
                    "case-insensitive." % param.name
                )
            seen.add(norm)

            if param.kwargs.get("type") == JSONType or isinstance(
                param.kwargs.get("type"), FilePathClass
            ):
                # Special-case this to avoid touching core
                param_type = str(param.kwargs.get("type").name)
            else:
                param_type = str(param.kwargs.get("type").__name__)

            is_required = param.kwargs.get("required", False)
            # Throw an exception if a schedule is set for a flow with required
            # parameters with no defaults. We currently don't have any notion
            # of data triggers in Argo Workflows.

            if "default" not in param.kwargs and is_required and has_schedule:
                raise MetaflowException(
                    "The parameter *%s* does not have a default and is required. "
                    "Scheduling such parameters via Argo CronWorkflows is not "
                    "currently supported." % param.name
                )
            default_value = deploy_time_eval(param.kwargs.get("default"))
            # If the value is not required and the value is None, we set the value to
            # the JSON equivalent of None to please argo-workflows. Unfortunately it
            # has the side effect of casting the parameter value to string null during
            # execution - which needs to be fixed imminently.
            if not is_required or default_value is not None:
                default_value = json.dumps(default_value)
            parameters[param.name] = dict(
                name=param.name,
                value=default_value,
                type=param_type,
                description=param.kwargs.get("help"),
                is_required=is_required,
            )
        return parameters

    def _compile_workflow_template(self):
        annotations = {
            "metaflow/flow_name": self.flow.name,
        }
        return (
            SuanpanTemplate()
            .add_node(
                self.flow.name,
                self.code_package_url,
                self._dag_templates(),
                self.parameters,
            )
            .to_json()
        )

    # Visit every node and yield the uber DAGTemplate(s).
    def _dag_templates(self):
        def _visit(
            node,
            exit_node=None,
            templates=None,
            dag_tasks=None,
            parent_foreach=None,
        ):  # Returns Tuple[List[Template], List[DAGTask]]
            """ """
            # Every for-each node results in a separate subDAG and an equivalent
            # DAGTemplate rooted at the child of the for-each node. Each DAGTemplate
            # has a unique name - the top-level DAGTemplate is named as the name of
            # the flow and the subDAG DAGTemplates are named after the (only) descendant
            # of the for-each node.

            # Emit if we have reached the end of the sub workflow
            if dag_tasks is None:
                dag_tasks = []
            if templates is None:
                templates = []
            if exit_node is not None and exit_node is node.name:
                return templates, dag_tasks
            if node.name == "start":
                # Start node has no dependencies.
                dag_task = DAGTask(self._sanitize(node.name))
            elif (
                node.is_inside_foreach
                and self.graph[node.in_funcs[0]].type == "foreach"
                and not self.graph[node.in_funcs[0]].parallel_foreach
                # We need to distinguish what is a "regular" foreach (i.e something that doesn't care about to gang semantics)
                # vs what is a "num_parallel" based foreach (i.e. something that follows gang semantics.)
                # A `regular` foreach is basically any arbitrary kind of foreach.
            ):
                # Child of a foreach node needs input-paths as well as split-index
                # This child is the first node of the sub workflow and has no dependency

                parameters = [
                    Parameter("input-paths").value("{{inputs.parameters.input-paths}}"),
                    Parameter("split-index").value("{{inputs.parameters.split-index}}"),
                ]
                dag_task = DAGTask(self._sanitize(node.name)).arguments(
                    Arguments().parameters(parameters)
                )
            elif node.parallel_step:
                # This is the step where the @parallel decorator is defined.
                # Since this DAGTask will call the for the `resource` [based templates]
                # (https://argo-workflows.readthedocs.io/en/stable/walk-through/kubernetes-resources/)
                # we have certain constraints on the way we can pass information inside the Jobset manifest
                # [All templates will have access](https://argo-workflows.readthedocs.io/en/stable/variables/#all-templates)
                # to the `inputs.parameters` so we will pass down ANY/ALL information using the
                # input parameters.
                # We define the usual parameters like input-paths/split-index etc. but we will also
                # define the following:
                # - `workerCount`:  parameter which will be used to determine the number of
                #                   parallel worker jobs
                # - `jobset-name`:  parameter which will be used to determine the name of the jobset.
                #                   This parameter needs to be dynamic so that when we have retries we don't
                #                   end up using the name of the jobset again (if we do, it will crash since k8s wont allow duplicated job names)
                # - `retryCount`:   parameter which will be used to determine the number of retries
                #                   This parameter will *only* be available within the container templates like we
                #                   have it for all other DAGTasks and NOT for custom kubernetes resource templates.
                #                   So as a work-around, we will set it as the `retryCount` parameter instead of
                #                   setting it as a {{ retries }} in the CLI code. Once set as a input parameter,
                #                   we can use it in the Jobset Manifest templates as `{{inputs.parameters.retryCount}}`
                # - `task-id-entropy`: This is a parameter which will help derive task-ids and jobset names. This parameter
                #                   contains the relevant amount of entropy to ensure that task-ids and jobset names
                #                   are uniquish. We will also use this in the join task to construct the task-ids of
                #                   all parallel tasks since the task-ids for parallel task are minted formulaically.
                parameters = [
                    Parameter("input-paths").value("{{inputs.parameters.input-paths}}"),
                    Parameter("num-parallel").value(
                        "{{inputs.parameters.num-parallel}}"
                    ),
                    Parameter("split-index").value("{{inputs.parameters.split-index}}"),
                    Parameter("task-id-entropy").value(
                        "{{inputs.parameters.task-id-entropy}}"
                    ),
                    # we cant just use hyphens with sprig.
                    # https://github.com/argoproj/argo-workflows/issues/10567#issuecomment-1452410948
                    Parameter("workerCount").value(
                        "{{=sprig.int(sprig.sub(sprig.int(inputs.parameters['num-parallel']),1))}}"
                    ),
                ]
                if any(d.name == "retry" for d in node.decorators):
                    parameters.extend(
                        [
                            Parameter("retryCount").value("{{retries}}"),
                            # The job-setname needs to be unique for each retry
                            # and we cannot use the `generateName` field in the
                            # Jobset Manifest since we need to construct the subdomain
                            # and control pod domain name pre-hand. So we will use
                            # the retry count to ensure that the jobset name is unique
                            Parameter("jobset-name").value(
                                "js-{{inputs.parameters.task-id-entropy}}{{retries}}",
                            ),
                        ]
                    )
                else:
                    parameters.extend(
                        [
                            Parameter("jobset-name").value(
                                "js-{{inputs.parameters.task-id-entropy}}",
                            )
                        ]
                    )

                dag_task = DAGTask(self._sanitize(node.name)).arguments(
                    Arguments().parameters(parameters)
                )
            else:
                # Every other node needs only input-paths
                parameters = [
                    Parameter("input-paths").value(
                        compress_list(
                            [
                                "argo-{{workflow.name}}/%s/{{tasks.%s.outputs.parameters.task-id}}"
                                % (n, self._sanitize(n))
                                for n in node.in_funcs
                            ],
                            # NOTE: We set zlibmin to infinite because zlib compression for the Argo input-paths breaks template value substitution.
                            zlibmin=inf,
                        )
                    )
                ]
                # NOTE: Due to limitations with Argo Workflows Parameter size we
                #       can not pass arbitrarily large lists of task id's to join tasks.
                #       Instead we ensure that task id's for foreach tasks can be
                #       deduced deterministically and pass the relevant information to
                #       the join task.
                #
                #       We need to add the split-index and root-input-path for the last
                #       step in any foreach scope and use these to generate the task id,
                #       as the join step uses the root and the cardinality of the
                #       foreach scope to generate the required id's.
                if (
                    node.is_inside_foreach
                    and self.graph[node.out_funcs[0]].type == "join"
                ):
                    if any(
                        self.graph[parent].matching_join
                        == self.graph[node.out_funcs[0]].name
                        and self.graph[parent].type == "foreach"
                        for parent in self.graph[node.out_funcs[0]].split_parents
                    ):
                        parameters.extend(
                            [
                                Parameter("split-index").value(
                                    "{{inputs.parameters.split-index}}"
                                ),
                                Parameter("root-input-path").value(
                                    "{{inputs.parameters.input-paths}}"
                                ),
                            ]
                        )

                dag_task = (
                    DAGTask(self._sanitize(node.name))
                    .dependencies(
                        [self._sanitize(in_func) for in_func in node.in_funcs]
                    )
                    .arguments(Arguments().parameters(parameters))
                )

            dag_tasks.append(dag_task)
            # End the workflow if we have reached the end of the flow
            if node.type == "end":
                return [
                    Template(self.flow.name).dag(DAGTemplate().tasks(dag_tasks))
                ] + templates, dag_tasks
            # For split nodes traverse all the children
            if node.type == "split":
                for n in node.out_funcs:
                    _visit(
                        self.graph[n],
                        node.matching_join,
                        templates,
                        dag_tasks,
                        parent_foreach,
                    )
                return _visit(
                    self.graph[node.matching_join],
                    exit_node,
                    templates,
                    dag_tasks,
                    parent_foreach,
                )
            # For foreach nodes generate a new sub DAGTemplate
            # We do this for "regular" foreaches (ie. `self.next(self.a, foreach=)`)
            elif node.type == "foreach":
                foreach_template_name = self._sanitize(
                    "%s-foreach-%s"
                    % (
                        node.name,
                        "parallel" if node.parallel_foreach else node.foreach_param,
                        # Since foreach's are derived based on `self.next(self.a, foreach="<varname>")`
                        # vs @parallel foreach are done based on `self.next(self.a, num_parallel="<some-number>")`,
                        # we need to ensure that `foreach_template_name` suffix is appropriately set based on the kind
                        # of foreach.
                    )
                )

                # There are two separate "DAGTask"s created for the foreach node.
                # - The first one is a "jump-off" DAGTask where we propagate the
                # input-paths and split-index. This thing doesn't create
                # any actual containers and it responsible for only propagating
                # the parameters.
                # - The DAGTask that follows first DAGTask is the one
                # that uses the ContainerTemplate. This DAGTask is named the same
                # thing as the foreach node. We will leverage a similar pattern for the
                # @parallel tasks.
                #
                foreach_task = (
                    DAGTask(foreach_template_name)
                    .dependencies([self._sanitize(node.name)])
                    .template(foreach_template_name)
                    .arguments(
                        Arguments().parameters(
                            [
                                Parameter("input-paths").value(
                                    "argo-{{workflow.name}}/%s/{{tasks.%s.outputs.parameters.task-id}}"
                                    % (node.name, self._sanitize(node.name))
                                ),
                                Parameter("split-index").value("{{item}}"),
                            ]
                            + (
                                [
                                    Parameter("root-input-path").value(
                                        "argo-{{workflow.name}}/%s/{{tasks.%s.outputs.parameters.task-id}}"
                                        % (node.name, self._sanitize(node.name))
                                    ),
                                ]
                                if parent_foreach
                                else []
                            )
                            + (
                                # Disabiguate parameters for a regular `foreach` vs a `@parallel` foreach
                                [
                                    Parameter("num-parallel").value(
                                        "{{tasks.%s.outputs.parameters.num-parallel}}"
                                        % self._sanitize(node.name)
                                    ),
                                    Parameter("task-id-entropy").value(
                                        "{{tasks.%s.outputs.parameters.task-id-entropy}}"
                                        % self._sanitize(node.name)
                                    ),
                                ]
                                if node.parallel_foreach
                                else []
                            )
                        )
                    )
                    .with_param(
                        # For @parallel workloads `num-splits` will be explicitly set to one so that
                        # we can piggyback on the current mechanism with which we leverage argo.
                        "{{tasks.%s.outputs.parameters.num-splits}}"
                        % self._sanitize(node.name)
                    )
                )
                dag_tasks.append(foreach_task)
                templates, dag_tasks_1 = _visit(
                    self.graph[node.out_funcs[0]],
                    node.matching_join,
                    templates,
                    [],
                    node.name,
                )

                # How do foreach's work on Argo:
                # Lets say you have the following dag: (start[sets `foreach="x"`]) --> (task-a [actual foreach]) --> (join) --> (end)
                # With argo we will :
                # (start [sets num-splits]) --> (task-a-foreach-(0,0) [dummy task]) --> (task-a) --> (join) --> (end)
                # The (task-a-foreach-(0,0) [dummy task]) propagates the values of the `split-index` and the input paths.
                # to the actual foreach task.
                templates.append(
                    Template(foreach_template_name)
                    .inputs(
                        Inputs().parameters(
                            [Parameter("input-paths"), Parameter("split-index")]
                            + ([Parameter("root-input-path")] if parent_foreach else [])
                            + (
                                [
                                    Parameter("num-parallel"),
                                    Parameter("task-id-entropy"),
                                    # Parameter("workerCount")
                                ]
                                if node.parallel_foreach
                                else []
                            )
                        )
                    )
                    .outputs(
                        Outputs().parameters(
                            [
                                # non @parallel tasks set task-ids as outputs
                                Parameter("task-id").valueFrom(
                                    {
                                        "parameter": "{{tasks.%s.outputs.parameters.task-id}}"
                                        % self._sanitize(
                                            self.graph[node.matching_join].in_funcs[0]
                                        )
                                    }
                                )
                            ]
                            if not node.parallel_foreach
                            else [
                                # @parallel tasks set `task-id-entropy` and `num-parallel`
                                # as outputs so task-ids can be derived in the join step.
                                # Both of these values should be propagated from the
                                # jobset labels.
                                Parameter("num-parallel").valueFrom(
                                    {
                                        "parameter": "{{tasks.%s.outputs.parameters.num-parallel}}"
                                        % self._sanitize(
                                            self.graph[node.matching_join].in_funcs[0]
                                        )
                                    }
                                ),
                                Parameter("task-id-entropy").valueFrom(
                                    {
                                        "parameter": "{{tasks.%s.outputs.parameters.task-id-entropy}}"
                                        % self._sanitize(
                                            self.graph[node.matching_join].in_funcs[0]
                                        )
                                    }
                                ),
                            ]
                        )
                    )
                    .dag(DAGTemplate().tasks(dag_tasks_1))
                )

                join_foreach_task = (
                    DAGTask(self._sanitize(self.graph[node.matching_join].name))
                    .dependencies([foreach_template_name])
                    .arguments(
                        Arguments().parameters(
                            (
                                [
                                    Parameter("input-paths").value(
                                        "argo-{{workflow.name}}/%s/{{tasks.%s.outputs.parameters.task-id}}"
                                        % (node.name, self._sanitize(node.name))
                                    ),
                                    Parameter("split-cardinality").value(
                                        "{{tasks.%s.outputs.parameters.split-cardinality}}"
                                        % self._sanitize(node.name)
                                    ),
                                ]
                                if not node.parallel_foreach
                                else [
                                    Parameter("num-parallel").value(
                                        "{{tasks.%s.outputs.parameters.num-parallel}}"
                                        % self._sanitize(node.name)
                                    ),
                                    Parameter("task-id-entropy").value(
                                        "{{tasks.%s.outputs.parameters.task-id-entropy}}"
                                        % self._sanitize(node.name)
                                    ),
                                ]
                            )
                            + (
                                [
                                    Parameter("split-index").value(
                                        # TODO : Pass down these parameters to the jobset stuff.
                                        "{{inputs.parameters.split-index}}"
                                    ),
                                    Parameter("root-input-path").value(
                                        "{{inputs.parameters.input-paths}}"
                                    ),
                                ]
                                if parent_foreach
                                else []
                            )
                        )
                    )
                )
                dag_tasks.append(join_foreach_task)
                return _visit(
                    self.graph[self.graph[node.matching_join].out_funcs[0]],
                    exit_node,
                    templates,
                    dag_tasks,
                    parent_foreach,
                )
            # For linear nodes continue traversing to the next node
            if node.type in ("linear", "join", "start"):
                return _visit(
                    self.graph[node.out_funcs[0]],
                    exit_node,
                    templates,
                    dag_tasks,
                    parent_foreach,
                )
            else:
                raise Exception(
                    "Node type *%s* for step *%s* is not currently supported by "
                    "Argo Workflows." % (node.type, node.name)
                )

        # Generate daemon tasks

        templates, _ = _visit(node=self.graph["start"], dag_tasks=None)
        return templates


class SuanpanTemplate(object):
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(
            os.path.join(current_dir, 'config_template.json'), encoding='utf-8'
        ) as f:
            self.config_template = json.load(f)
        with open(
            os.path.join(current_dir, 'vscode_node_template.json'), encoding='utf-8'
        ) as f:
            self.vscode_node_template = json.load(f)


    def add_node(self, flow_name, code_package_url, dag_templates, parameters):

        processes = {}
        connections = []
        # print(dag_templates[0].to_json())
        name_uuid = {}
        dag_template = dag_templates[0].to_json()
        # print(dag_template)
        for task in dag_template["dag"]["tasks"]:
            print(task['name'])
            random_uuid = str(uuid.uuid4()).replace('-', '')

            node_template = copy.deepcopy(self.vscode_node_template)
            node_template['metadata']['label'] = task['name']
            node_template['metadata']['sublabel'] = task['name']

            custom_env = {
                'step': task['name'],
                'main_file': os.path.basename(sys.argv[0]),
                'code_package_url': code_package_url,
                'params': parameters,
                'last_step_num': len(task['dependencies']),
            }
            # print("=============")
            # print(parameters)
            # print("=============")
            if task['name'] == 'start':
                for param_name, param in parameters.items():
                    print("param['value']========", param['value'])
                    param_uuid = str(uuid.uuid4()).replace('-', '')
                    node_template['metadata']['def']['params']['mf-' + param_name]={
                        "type": "string",
                        "controlInstUuid": param_uuid,
                        "value": param['value'],
                    }
                    node_template['metadata']['ui']['tabs']['params']['controls'].append(
                    {
                                "uuid": param_uuid,
                                "type": "string",
                                "label": {
                                    "zh_CN": param['name'],
                                    "en_US": param['name']
                                },
                                "placeholder": {
                                    "zh_CN": "值",
                                    "en_US": "value"
                                },
                            }
                    )

            node_template['metadata']['def'][
                'dockerCmd'
            ] =  f"export CUSTOM_ENV='{json.dumps(custom_env, ensure_ascii=False)}'"
            # if task['name'] == 'train':
            #     node_template['metadata']['def']['dockerCmd'] += ' && pip install --upgrade torch==1.12.1+cu116 torchvision==0.13.1+cu116 --extra-index-url https://download.pytorch.org/whl/cu116'
            #     node_template['metadata']['def']['dockerCmd'] += ' && pip install --no-cache-dir -r /code/requirements.txt'
            # else:
            #         node_template['metadata']['def']['dockerCmd'] += ' && pip install boto3'

            

            node_template['metadata']['def']['dockerCmd'] += " && sh /code/run.sh"
            # print("11111111", node_template['metadata']['def']['dockerCmd'])
            processes[random_uuid] = node_template
            name_uuid[task['name']] = random_uuid
            in_port_id = 1
            for dependency in task['dependencies']:
                connections.append(
                    {
                        "src": {
                            "process": name_uuid[dependency],
                            "port": "out1",
                        },
                        "tgt": {
                            "process": random_uuid,
                            "port": f"in{in_port_id}",
                        },
                        "metadata": {
                            "path": "M439.5,307 L455.5,307 L475.25,307 L475.25,270 L495,270 L511,270",
                            "custom": False,
                        },
                    }
                )
                if in_port_id > 1:
                    processes[random_uuid]['metadata']['def']['ports'].append(
                        {
                            "uuid": f"in{in_port_id}",
                            "id": str(uuid.uuid4()).replace('-', ''),
                            "description": {"en_US": "input data", "zh_CN": "输入数据"},
                            "display": True,
                            "type": "data",
                            "subType": "json",
                            "ioType": "in",
                            "options": ["json"],
                            "angle": 180,
                        }
                    )
                in_port_id += 1
        self.config_template["processes"] = processes
        self.config_template["connections"] = connections
        return self

    def to_json(self):
        return self.config_template

    def __str__(self):
        return json.dumps(self.config_template, indent=4, ensure_ascii=False)


class WorkflowTemplate(object):
    # https://argoproj.github.io/argo-workflows/fields/#workflowtemplate

    def __init__(self):
        tree = lambda: defaultdict(tree)
        self.payload = tree()
        self.payload["apiVersion"] = "argoproj.io/v1alpha1"
        self.payload["kind"] = "WorkflowTemplate"

    def metadata(self, object_meta):
        self.payload["metadata"] = object_meta.to_json()
        return self

    def spec(self, workflow_spec):
        self.payload["spec"] = workflow_spec.to_json()
        return self

    def to_json(self):
        return self.payload

    def __str__(self):
        return json.dumps(self.payload, indent=4)


class ObjectMeta(object):
    # https://argoproj.github.io/argo-workflows/fields/#objectmeta

    def __init__(self):
        tree = lambda: defaultdict(tree)
        self.payload = tree()

    def annotation(self, key, value):
        self.payload["annotations"][key] = str(value)
        return self

    def annotations(self, annotations):
        if "annotations" not in self.payload:
            self.payload["annotations"] = {}
        self.payload["annotations"].update(annotations)
        return self

    def generate_name(self, generate_name):
        self.payload["generateName"] = generate_name
        return self

    def label(self, key, value):
        self.payload["labels"][key] = str(value)
        return self

    def labels(self, labels):
        if "labels" not in self.payload:
            self.payload["labels"] = {}
        self.payload["labels"].update(labels or {})
        return self

    def name(self, name):
        self.payload["name"] = name
        return self

    def namespace(self, namespace):
        self.payload["namespace"] = namespace
        return self

    def to_json(self):
        return self.payload

    def __str__(self):
        return json.dumps(self.to_json(), indent=4)


class WorkflowSpec(object):
    # https://argoproj.github.io/argo-workflows/fields/#workflowspec
    # This object sets all Workflow level properties.

    def __init__(self):
        tree = lambda: defaultdict(tree)
        self.payload = tree()

    def automount_service_account_token(self, mount=True):
        self.payload["automountServiceAccountToken"] = mount
        return self

    def arguments(self, arguments):
        self.payload["arguments"] = arguments.to_json()
        return self

    def archive_logs(self, archive_logs=True):
        self.payload["archiveLogs"] = archive_logs
        return self

    def entrypoint(self, entrypoint):
        self.payload["entrypoint"] = entrypoint
        return self

    def onExit(self, on_exit_template):
        if on_exit_template:
            self.payload["onExit"] = on_exit_template
        return self

    def parallelism(self, parallelism):
        # Set parallelism at Workflow level
        self.payload["parallelism"] = int(parallelism)
        return self

    def pod_metadata(self, metadata):
        self.payload["podMetadata"] = metadata.to_json()
        return self

    def priority(self, priority):
        if priority is not None:
            self.payload["priority"] = int(priority)
        return self

    def workflow_metadata(self, workflow_metadata):
        self.payload["workflowMetadata"] = workflow_metadata.to_json()
        return self

    def service_account_name(self, service_account_name):
        # https://argoproj.github.io/argo-workflows/workflow-rbac/
        self.payload["serviceAccountName"] = service_account_name
        return self

    def templates(self, templates):
        if "templates" not in self.payload:
            self.payload["templates"] = []
        for template in templates:
            self.payload["templates"].append(template.to_json())
        return self

    def hooks(self, hooks):
        # https://argoproj.github.io/argo-workflows/fields/#lifecyclehook
        if "hooks" not in self.payload:
            self.payload["hooks"] = {}
        for k, v in hooks.items():
            self.payload["hooks"].update({k: v.to_json()})
        return self

    def to_json(self):
        return self.payload

    def __str__(self):
        return json.dumps(self.to_json(), indent=4)


class Template(object):
    # https://argoproj.github.io/argo-workflows/fields/#template

    def __init__(self, name):
        tree = lambda: defaultdict(tree)
        self.payload = tree()
        self.payload["name"] = name

    def dag(self, dag_template):
        self.payload["dag"] = dag_template.to_json()
        return self

    def steps(self, steps):
        if "steps" not in self.payload:
            self.payload["steps"] = []
        # steps is a list of lists.
        # hence we go over every item in the incoming list
        # serialize it and then append the list to the payload
        step_list = []
        for step in steps:
            step_list.append(step.to_json())
        self.payload["steps"].append(step_list)
        return self

    def inputs(self, inputs):
        self.payload["inputs"] = inputs.to_json()
        return self

    def outputs(self, outputs):
        self.payload["outputs"] = outputs.to_json()
        return self

    def metadata(self, metadata):
        self.payload["metadata"] = metadata.to_json()
        return self

    def to_json(self):
        return self.payload

    def resource(self, action, manifest, success_criteria, failure_criteria):
        self.payload["resource"] = {}
        self.payload["resource"]["action"] = action
        self.payload["setOwnerReference"] = True
        self.payload["resource"]["successCondition"] = success_criteria
        self.payload["resource"]["failureCondition"] = failure_criteria
        self.payload["resource"]["manifest"] = manifest
        return self

    def __str__(self):
        return json.dumps(self.payload, indent=4)


class Inputs(object):
    # https://argoproj.github.io/argo-workflows/fields/#inputs

    def __init__(self):
        tree = lambda: defaultdict(tree)
        self.payload = tree()

    def parameters(self, parameters):
        if "parameters" not in self.payload:
            self.payload["parameters"] = []
        for parameter in parameters:
            self.payload["parameters"].append(parameter.to_json())
        return self

    def to_json(self):
        return self.payload

    def __str__(self):
        return json.dumps(self.payload, indent=4)


class Outputs(object):
    # https://argoproj.github.io/argo-workflows/fields/#outputs

    def __init__(self):
        tree = lambda: defaultdict(tree)
        self.payload = tree()

    def parameters(self, parameters):
        if "parameters" not in self.payload:
            self.payload["parameters"] = []
        for parameter in parameters:
            self.payload["parameters"].append(parameter.to_json())
        return self

    def to_json(self):
        return self.payload

    def __str__(self):
        return json.dumps(self.payload, indent=4)


class Parameter(object):
    # https://argoproj.github.io/argo-workflows/fields/#parameter

    def __init__(self, name):
        tree = lambda: defaultdict(tree)
        self.payload = tree()
        self.payload["name"] = name

    def value(self, value):
        self.payload["value"] = value
        return self

    def default(self, value):
        self.payload["default"] = value
        return self

    def valueFrom(self, value_from):
        self.payload["valueFrom"] = value_from
        return self

    def description(self, description):
        self.payload["description"] = description
        return self

    def to_json(self):
        return self.payload

    def __str__(self):
        return json.dumps(self.payload, indent=4)


class DAGTemplate(object):
    # https://argoproj.github.io/argo-workflows/fields/#dagtemplate

    def __init__(self):
        tree = lambda: defaultdict(tree)
        self.payload = tree()

    def tasks(self, tasks):
        if "tasks" not in self.payload:
            self.payload["tasks"] = []
        for task in tasks:
            self.payload["tasks"].append(task.to_json())
        return self

    def to_json(self):
        return self.payload

    def __str__(self):
        return json.dumps(self.payload, indent=4)


class DAGTask(object):
    # https://argoproj.github.io/argo-workflows/fields/#dagtask

    def __init__(self, name):
        tree = lambda: defaultdict(tree)
        self.payload = tree()
        self.payload["name"] = name

    def arguments(self, arguments):
        self.payload["arguments"] = arguments.to_json()
        return self

    def dependencies(self, dependencies):
        self.payload["dependencies"] = dependencies
        return self

    def template(self, template):
        # Template reference
        self.payload["template"] = template
        return self

    def inline(self, template):
        # We could have inlined the template here but
        # https://github.com/argoproj/argo-workflows/issues/7432 prevents us for now.
        self.payload["inline"] = template.to_json()
        return self

    def with_param(self, with_param):
        self.payload["withParam"] = with_param
        return self

    def to_json(self):
        return self.payload

    def __str__(self):
        return json.dumps(self.payload, indent=4)


class Arguments(object):
    # https://argoproj.github.io/argo-workflows/fields/#arguments

    def __init__(self):
        tree = lambda: defaultdict(tree)
        self.payload = tree()

    def parameters(self, parameters):
        if "parameters" not in self.payload:
            self.payload["parameters"] = []
        for parameter in parameters:
            self.payload["parameters"].append(parameter.to_json())
        return self

    def to_json(self):
        return self.payload

    def __str__(self):
        return json.dumps(self.payload, indent=4)
