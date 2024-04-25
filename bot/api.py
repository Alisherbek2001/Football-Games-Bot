import requests
from environs import Env

env = Env()
env.read_env()
BASE_URL = env.str('URL')
import json


def create_user(fullname, telegram_id, phone):
    response = requests.post(f"{BASE_URL}/api/user/",
                             data={'fullname': fullname, 'telegram_id': telegram_id, 'phone': phone})
    return 'OK'


def get_team(telegram_id):
    response = requests.get(f"{BASE_URL}/api/team/id/{telegram_id}/")
    return json.loads(response.text)


def update_team(id, telegram_id, name):
    response = requests.put(f"{BASE_URL}/api/team/{id}/", data={'name': name, 'telegram_id': telegram_id})
    return response.status_code


def delete_team(team_id):
    response = requests.delete(f"{BASE_URL}/api/team/{team_id}")
    return 'ok'


def create_team(name, captain):
    respone = requests.post(f"{BASE_URL}/api/team/", data={'name': name, 'captain': captain})
    return 'ok'


def get_member(telegram_id):
    response = requests.get(f"{BASE_URL}/api/member/{telegram_id}/")
    return json.loads(response.text)


def create_member(name, phone_number, number, captain):
    respone = requests.post(f"{BASE_URL}/api/member/",
                            data={'name': name, 'phone_number': phone_number, 'number': number, 'captain': captain})
    return 'ok'

def update_member(member_id,name,phone_number,number):
    response = requests.put(f"{BASE_URL}/api/memberid/{member_id}/", data={'name':name,'phone_number':phone_number,'number':number})
    return response.status_code
def delete_member(member_id):
    response = requests.delete(f"{BASE_URL}/api/memberid/{member_id}")
    return 'deleted'
