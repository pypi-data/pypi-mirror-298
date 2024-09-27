import base64
import configparser
import json
import os
import platform
import re
import sys
from hashlib import sha1
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
from base64 import b64decode, b64encode
from datetime import datetime

import requests

from metaflow import JSONType, Run, current, decorators, parameters
from metaflow._vendor import click
from metaflow.client.core import get_metadata
from metaflow.exception import (
    MetaflowException,
    MetaflowInternalError,
    MetaflowNotFound,
)
from metaflow.metaflow_config import (
    ARGO_WORKFLOWS_UI_URL,
    KUBERNETES_NAMESPACE,
    SERVICE_VERSION_CHECK,
    UI_URL,
)
from metaflow.package import MetaflowPackage

# TODO: Move production_token to utils
from metaflow.plugins.aws.step_functions.production_token import (
    load_token,
    new_token,
    store_token,
)
from metaflow.plugins.environment_decorator import EnvironmentDecorator
from metaflow.plugins.kubernetes.kubernetes_decorator import KubernetesDecorator
from metaflow.tagging_util import validate_tags
from metaflow.util import get_username, to_bytes, to_unicode, version_parse

from .suanpan import Suanpanflows

VALID_NAME = re.compile(r"^[a-z0-9]([a-z0-9\.\-]*[a-z0-9])?$")

unsupported_decorators = {
    "snowpark": "Step *%s* is marked for execution on Snowpark with Argo Workflows which isn't currently supported.",
    "slurm": "Step *%s* is marked for execution on Slurm with Argo Workflows which isn't currently supported.",
    "nvidia": "Step *%s* is marked for execution on Nvidia with Argo Workflows which isn't currently supported.",
}


class IncorrectProductionToken(MetaflowException):
    headline = "Incorrect production token"


class RunIdMismatch(MetaflowException):
    headline = "Run ID mismatch"


class IncorrectMetadataServiceVersion(MetaflowException):
    headline = "Incorrect version for metaflow service"


class ArgoWorkflowsNameTooLong(MetaflowException):
    headline = "Argo Workflows name too long"


class UnsupportedPythonVersion(MetaflowException):
    headline = "Unsupported version of Python"


@click.group()
def cli():
    pass


@cli.group(help="Commands related to suanpan.")
@click.option(
    "--name",
    default=None,
    type=str,
    help="Argo Workflow name. The flow name is used instead if "
    "this option is not specified.",
)
@click.pass_obj
def suanpan(obj, name=None):
    obj.check(obj.graph, obj.flow, obj.environment, pylint=obj.pylint)
    (
        obj.workflow_name,
        obj.token_prefix,
        obj.is_project,
    ) = resolve_workflow_name(obj, name)


@suanpan.command(help="Cerate a json file")
@click.pass_obj
def create(
    obj,
):
    for node in obj.graph:
        for decorator, error_message in unsupported_decorators.items():
            if any([d.name == decorator for d in node.decorators]):
                raise MetaflowException(error_message % node.name)

    obj.echo("Creating json file for *%s* " % obj.workflow_name, bold=True)

    flow = make_flow(
        obj,
        obj.workflow_name,
    )

    # print(flow.to_json())
    with open('graph.json', 'w', encoding='utf-8') as f:
        json.dump(flow.to_json(), f, ensure_ascii=False)

    obj.echo_always("CREATE FINISH", err=False, no_bold=True)
    



def read_config():
    config = configparser.ConfigParser()
    config_path = os.path.expanduser('~/.suanpan')
    
    if not os.path.exists(config_path):
        print(f"Config file not found at {config_path}")
        return None
    config.read(config_path)
    print(config.sections())
    xuelang_config = config['xuelang']
    return xuelang_config.get('username'), xuelang_config.get('password'), xuelang_config.get('url')

def get_public_key_and_salt(url):
    response = requests.get(f"{url}/api/v1/publicKey")
    if response.status_code == 200:
        data = response.json()
        print(data)
        if data.get('success'):
            return data['data']['publicKey'], data['data']['salt']
        else:
            print("Error:", data.get('message'))
    else:
        print("Request failed with status code:", response.status_code)
    return None, None



def encrypt_password(str_to_encrypt, public_key_base64):
    # 解码base64格式的公钥
    public_key_der = b64decode(public_key_base64)
    
    # 从DER格式加载公钥
    public_key = serialization.load_der_public_key(
        public_key_der,
        backend=default_backend()
    )
    
    # 使用公钥进行RSA加密
    encrypted_bytes = public_key.encrypt(
        str_to_encrypt.encode('utf-8'),
        padding.PKCS1v15()  # 使用PKCS1填充
    )
    
    # 将加密后的字节转换为base64字符串
    encrypted_base64 = b64encode(encrypted_bytes).decode('utf-8')
    
    return encrypted_base64

def get_cookie(url, username, encrypted_password):
    headers = {'Content-Type': 'application/json'}
    payload = {
        'username': username,
        'password': encrypted_password
    }
    response = requests.post(f"{url}/api/v1/getCookie", json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return response
        else:
            print("Error:", data.get('message'))
    else:
        print("Request failed with status code:", response.status_code)
    return None


def parse_set_cookie(set_cookie_header):
    cookies = {}
    name_value_pair = set_cookie_header.split('; ')[0]
    print('name_value_pair', name_value_pair)
    name, value = name_value_pair.split('=')
    cookies[name] = value
    return cookies

def generate_cookie_string(cookies):
    return '; '.join([f"{name}={value}" for name, value in cookies.items()])

def create_suanpan_app(base_url, cookie_string, name):
    headers = {'Cookie': cookie_string, 'Content-Type': 'application/json'}
    with open('./graph.json', 'r') as f:
        graphJson = json.load(f)
    payload = {
        "name": name,
        "type": "algo",
        "description": "",
        "graphJson": graphJson
    }
    response = requests.post(f"{base_url}/app/append", json=payload, headers=headers)
    if response.status_code == 200:
        print("Response from create_suanpan_app:")
        print(response.text)
    else:
        print("Create suanpan app request failed with status code:", response.status_code)


@suanpan.command(help="")
@click.pass_obj
def deploy(
    obj,
):
    obj.echo("Deploying *%s* to Suanpan Workflows..." % obj.workflow_name, bold=True)
    username, password, base_url = read_config()
    publicKey, salt = get_public_key_and_salt(base_url)
    print(publicKey, '????',salt)
    if publicKey or salt:
        print(f"Public Key: {publicKey}")
        print(f"Salt: {salt}")
        encrypted_password = encrypt_password(salt+password, publicKey)
        response = get_cookie(base_url, username, encrypted_password)
        if response:
            # 解析 Set-Cookie 头
            set_cookie_header = response.headers.get('Set-Cookie')
            if set_cookie_header:
                parsed_cookies = parse_set_cookie(set_cookie_header)
                cookie_string = generate_cookie_string(parsed_cookies)
                print(f"Generated Cookie String: {cookie_string}")
                
                # 发送带有Cookie的后续请求
                create_suanpan_app(base_url, cookie_string, obj.workflow_name + datetime.now().strftime("%Y%m%d%H%M%S"))
            else:
                print("cookie error")
        else:
            print("cookie error")


    

def resolve_workflow_name(obj, name):
    
    project = current.get("project_name")
    obj._is_workflow_name_modified = False
    if project:
        if name:
            raise MetaflowException(
                "--name is not supported for @projects. Use --branch instead."
            )
        workflow_name = current.project_flow_name
        project_branch = to_bytes(".".join((project, current.branch_name)))
        
        token_prefix = (
            "mfprj-%s"
            % to_unicode(base64.b32encode(sha1(project_branch).digest()))[:16]
        )
        is_project = True
        # Argo Workflow names can't be longer than 253 characters, so we truncate
        # by default. Also, while project and branch allow for underscores, Argo
        # Workflows doesn't (DNS Subdomain names as defined in RFC 1123) - so we will
        # remove any underscores as well as convert the name to lower case.
        # Also remove + and @ as not allowed characters, which can be part of the
        # project branch due to using email addresses as user names.
        if len(workflow_name) > 253:
            name_hash = to_unicode(
                base64.b32encode(sha1(to_bytes(workflow_name)).digest())
            )[:8].lower()
            workflow_name = "%s-%s" % (workflow_name[:242], name_hash)
            obj._is_workflow_name_modified = True
        if not VALID_NAME.search(workflow_name):
            workflow_name = sanitize_for_argo(workflow_name)
            obj._is_workflow_name_modified = True
    else:
        if name and not VALID_NAME.search(name):
            raise MetaflowException(
                "Name '%s' contains invalid characters. The "
                "name must consist of lower case alphanumeric characters, '-' or '.'"
                ", and must start and end with an alphanumeric character." % name
            )

        workflow_name = name if name else current.flow_name
        token_prefix = workflow_name
        is_project = False

        if len(workflow_name) > 253:
            msg = (
                "The full name of the workflow:\n*%s*\nis longer than 253 "
                "characters.\n\n"
                "To deploy this workflow to Argo Workflows, please "
                "assign a shorter name\nusing the option\n"
                "*argo-workflows --name <name> create*." % workflow_name
            )
            raise ArgoWorkflowsNameTooLong(msg)

        if not VALID_NAME.search(workflow_name):
            workflow_name = sanitize_for_argo(workflow_name)
            obj._is_workflow_name_modified = True

    return workflow_name, token_prefix.lower(), is_project


def make_flow(
    obj,
    name,
):

    decorators._init_step_decorators(
        obj.flow, obj.graph, obj.environment, obj.flow_datastore, obj.logger
    )

    # Save the code package in the flow datastore so that both user code and
    # metaflow package can be retrieved during workflow execution.
    obj.package = MetaflowPackage(
        obj.flow, obj.environment, obj.echo, obj.package_suffixes
    )
    package_url, package_sha = obj.flow_datastore.save_data(
        [obj.package.blob], len_hint=1
    )[0]

    return Suanpanflows(
        name,
        obj.graph,
        obj.flow,
        package_sha,
        package_url,
        obj.metadata,
        obj.flow_datastore,
        obj.environment,
        obj.event_logger,
        obj.monitor,
    )


def sanitize_for_argo(text):
    """
    Sanitizes a string so it does not contain characters that are not permitted in Argo Workflow resource names.
    """
    return (
        re.compile(r"^[^A-Za-z0-9]+")
        .sub("", text)
        .replace("_", "")
        .replace("@", "")
        .replace("+", "")
        .lower()
    )
