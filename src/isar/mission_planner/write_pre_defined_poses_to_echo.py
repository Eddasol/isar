import json
from isar.config.predefined_poses.predefined_poses import predefined_poses
from math import acos
from time import sleep
from isar.services.service_connections.request_handler import RequestHandler
from isar.services.auth.azure_credentials import AzureCredentials
from azure.identity import DefaultAzureCredential
import logging
from isar.config.settings import settings
from json import dumps
from requests import Response
from dotenv import load_dotenv
from isar.config.log import setup_logger
from requests.exceptions import HTTPError


def from_q_to_ang(orientation):
        qw = orientation.w
        angle = 2 * acos(qw) if orientation.z >= 0 else -2 * acos(qw)
        x = 0
        y = 0
        z = 1
        return x, y, z, angle

def write_all_pre_poses():
    installation_code = "KAA"

    for key in predefined_poses:
        if key[0:2] == "A-":
            installation_code = "JSV"
        elif key[0:2] != "A-" and installation_code == "JSV": 
            installation_code = "JCA"

        tag = key
        name = 'default'
        pose_x = predefined_poses[key].position.x
        pose_y = predefined_poses[key].position.y
        pose_z = predefined_poses[key].position.z
        rot_x, rot_y, rot_z, angle = from_q_to_ang(predefined_poses[key].orientation)
        body = {'installationCode': installation_code,
        'tag': tag,
        'name': name,
        'markerToolPosition': '',
        'position': {
            'e': pose_x,
            'n': pose_y,
            'u': pose_z
        },
        'lookDirectionNormalized': {
            'e': rot_x,
            'n': rot_y,
            'u': rot_z
        },
        'tiltDegClockwise': angle,
        'isDefault': False
        }
        
        print(installation_code,": ", tag)
        write_pose(body)


def recalculate_all_angles():
    installation_code = "KAA"

    for key in predefined_poses:
        if key[0:2] == "A-":
            installation_code = "JSV"
        elif key[0:2] != "A-" and installation_code == "JSV":
            installation_code = "JCA"

        tag = key

        rot_x, rot_y, rot_z, angle = from_q_to_ang(predefined_poses[key].orientation)

        body = {
        'name': None,
        'markerToolPosition': None,
        'position': None,
        'lookDirectionNormalized': {
            'e': rot_x,
            'n': rot_y,
            'u': rot_z
        },
        'tiltDegClockwise': angle,
        'isDefault': None
        }

        pose_id = get_id(installation_code, tag)
        
        print(installation_code,": ", tag)
        modify_pose(pose_id, body)


def write_pose(body: dict):
    """
    Takes in a dictionary that contains info needed in the api to post pose
    """        

    client_id: str = settings.ECHO_CLIENT_ID
    scope: str = settings.ECHO_APP_SCOPE
    request_scope: str = f"{client_id}/{scope}"

    token: str = credentials.get_token(request_scope).token
    url: str = f"{settings.ECHO_API_URL}/robots/pose"
    body_json = dumps(body)
    
    # If 403 error. Try hardcoding token
    # token = ''
    headers = {"accept": "text/plain", "Authorization": f"Bearer {token}", "Content-Type": "text/json"}
    print(url,'\n')
    print(headers, '\n')
    print(body_json, '\n')
    try:
        response: Response = request_handler.post(
            url=url,
            headers=headers,
            data=body_json
        )
    except HTTPError as e:
        print(f"{body['tag']} has issues")


def modify_pose(pose_id: int, body: dict):
    """
    Takes in a dictionary that contains info needed in the api to post pose
    """

    client_id: str = settings.ECHO_CLIENT_ID
    scope: str = settings.ECHO_APP_SCOPE
    request_scope: str = f"{client_id}/{scope}"

    token: str = credentials.get_token(request_scope).token
    url: str = f"{settings.ECHO_API_URL}/robots/pose/{pose_id}"

    # If 403 error. Try hardcoding token
    # token = ''
    headers = {"accept": "text/plain", "Authorization": f"Bearer {token}", "Content-Type": "text/json"}
    body_json = dumps(body)

    try:
        response: Response = request_handler.patch(
            url=url,
            headers=headers,
            data=body_json
        )
    except HTTPError as e:
        print(f"{body['tag']} has issues")


def get_id(installationCode: str, tag: str):
    client_id: str = settings.ECHO_CLIENT_ID
    scope: str = settings.ECHO_APP_SCOPE
    request_scope: str = f"{client_id}/{scope}"

    token: str = credentials.get_token(request_scope).token
    url: str = f"{settings.ECHO_API_URL}/robots/pose/?InstallationCode={installationCode}&Tags={tag}"
    try:
        response: Response = request_handler.get(
            url=url,
            headers={"Authorization": f"Bearer {token}"},
        )
    except Exception as e:
        print(e)
    return response.json()[0]["poseId"]



if __name__=="__main__":
    load_dotenv()
    setup_logger()
    request_handler: RequestHandler = RequestHandler()
    credentials: DefaultAzureCredential = (AzureCredentials.get_azure_credentials())
    logger = logging.getLogger("api")
    write_all_pre_poses()