import json
import logging as log
import random
import string
import sys
from datetime import datetime
from os import mkdir, path

import requests

from config import (emby_admin_passwd, emby_admin_uname, avoid_users,
                    emby_base_url, log_level, overwrite, timeout, tsv_out,
                    user_policy, user_prefix)

switcher = {
    4: log.DEBUG,
    3: log.INFO,
    2: log.WARNING,
    1: log.ERROR,
    0: log.CRITICAL
}

dir = path.split(path.abspath(__file__))
dir = dir[0]
log_path = f'{dir}/logs'
if not path.exists(log_path):
    mkdir(log_path)
# log setup

log.basicConfig(
    filename=f'{dir}/logs/{path.basename(path.splitext(__file__)[0])}.log',
    level=switcher.get(log_level, log.DEBUG),
    datefmt="%Y-%m-%d %H:%M:%S",
    format='%(asctime)s - %(levelname)s - %(message)s'
    )
cons = log.StreamHandler()
cons.setLevel(switcher.get(log_level, log.DEBUG))
fmt = log.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
cons.setFormatter(fmt)
log.getLogger('').addHandler(cons)
log.debug('Started script!')


out_file = f'{dir}/out.' + 'tsv' if tsv_out else 'txt'

def add_user(username, connect, 
    passwd = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20)),
    base_url = emby_base_url,
    admin_uname = emby_admin_uname,
    admin_passwd = emby_admin_passwd):
    '''
    username: the username for the new user
    passwd: the password for the new user
    connect: the emby connect account username/email
    base_url: the direct url to the emby server
    api_token: static api token for the emby server
    '''

    # make sure username is not the same as admin username
    if username == admin_uname or username in avoid_users:
        log.warning(f'{username} is set to be avoided! Skipping...')
        return

    log.info(f'Creating user for {username},{connect}')

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        'X-Emby-Client': "Requests Python",
        'X-Emby-Device-Name': "Python",
        "X-Emby-Client-Version": "4.4.2.0",
        "X-Emby-Device-Id": "12345678-1234-1234-1234-123456789012"
    }

    # Authenticate as admin

    raw_data = {
        'username': admin_uname,
        'Pw': admin_passwd
    }

    try:
        res = requests.post(f'{base_url}/Users/AuthenticateByName', params=raw_data, headers=headers, timeout=timeout)
    except requests.exceptions.ConnectionError:
        log.error(f'Cannot establish connection to base_url! Stopping... base_url={base_url}')
        sys.exit(1)

    try:
        data = json.loads(res.text)
        headers.update({
            'X-Emby-Token': data['AccessToken']
            })
        log.info('Successfully authenticated as admin')
    except json.decoder.JSONDecodeError:
        if 'Invalid username' in res.text:
            log.error('Admin username or password is incorrect! Stopping...')
        else:
            log.error('Error occurred authenticating as admin. Stopping...')
            log.error(f'{res.status_code} - {res.text}')
        sys.exit(1)

    #
    # CREATE NEW USER
    #

    raw_data = {
        'name': username
    }

    res = requests.post(f'{base_url}/Users/New', params=raw_data, headers=headers)
    new_id = ''
    try:
        data = json.loads(res.text)
        new_id = data['Id']
        log.info(f'Created new user')

    except json.decoder.JSONDecodeError:
        if ' already exists' in res.text:
            if not overwrite:
                log.info(f'{username} already exists and overwrite is off. Skipping...')
                return
            else:
                # reset password if overwrite is on
                log.warning(f'{username} already exists. Will attempt to overwrite settings.')

                # get list of users
                res = requests.get(f'{base_url}/Users', headers=headers)
                try:
                    data = json.loads(res.text)
                    for user in data:
                        if user['Name'] == username:
                            new_id = user['Id']
                            break
                except json.decoder.JSONDecodeError:
                    log.error(f'Error getting list of users! Skipping {username} {res.status_code} - {res.text}')

                raw_data = {
                    'resetPassword': True
                }
                res = requests.post(f'{base_url}/Users/{new_id}/Password', params=raw_data, headers=headers)

        elif 'Access token is invalid or expired.' == res.text:
            log.error('API token is invalid. Stopping...')
            sys.exit(1)
        else:
            log.error(f'Unknown error making {username}! Stopping... Status code={res.status_code} Response={res.text}')
            sys.exit(1)
    
    #
    #   SET PASSWORD
    #

    if passwd == 0:
        passwd = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))

    raw_data = {
        'CurrentPw': '',
        'NewPw': passwd
        }

    res = requests.post(f'{base_url}/Users/{new_id}/Password', params=raw_data, headers=headers)
    if res.status_code > 299:
        log.warning(f'Authenticating {username} unsuccessful. Stopping... {res.status_code} - {res.text}')
        sys.exit(1)
    else:
        log.info(f'Successfully set password to {passwd}')

    #
    #   CHANGE POLICY
    #

    res = requests.post(f'{base_url}/Users/{new_id}/Policy', params=user_policy, headers=headers)
    if res.status_code > 299:
        log.error(f'Error occurred when changing policy! Stopping... {res.status_code} - {res.text}')
        sys.exit(1)
    log.info('Successfully set policy.')

    #
    # LINK EMBY CONNECT ACCOUNT
    #

    raw_data = {
        'ConnectUsername': connect
    }

    res = requests.post(f'{base_url}/Users/{new_id}/Connect/Link', params=raw_data, headers=headers)
    if res.status_code > 299:
        log.warning(f'Connect link unsuccessful for {username}:{connect}. {res.status_code} - {res.text}')
    else:
        log.info('Successfully linked Emby connect account.')

    #
    # APPEND TO OUT.TXT
    # 
    
    with open(out_file, 'a+', encoding='utf-8') as file:
        log.info(f'Writing output to {out_file}')
        file.seek(0)
        if len(file.read(10)) > 0:
            file.write('\n')
        file.write(f'{username}\t{connect}\t{passwd}')
        file.close()
        

if __name__ == '__main__':
    with open(out_file, 'a+', encoding='utf-8') as file:
        file.seek(0)
        if len(file.read(10)) > 0:
            file.write('\n')
        file.write(f'---------------[{datetime.now()}]---------------')
        file.close()

    # Get input from in.txt
    in_file = f'{dir}/in.txt'
    if not path.isfile(in_file):
        log.error(f'Cant get input from {in_file}. Stopping...')
        sys.exit(1)

    new_users = []
    with open(f'{dir}/in.txt', 'a+') as file:
        log.info(f'Getting new users from {in_file}')
        file.seek(0)
        for line in file.readlines():
            new_users.append(line.strip().split(','))
        file.close()
    for user in new_users:
        
        if len(user) == 1:
            add_user(f'{user_prefix}{user[0].strip()}', user[0].strip())
        elif len(user) == 2:
            add_user(user[0].strip(), user[1].strip())
        else:
            log.error(f'Input file is in the wrong format! Skipping line={user}')
            continue
