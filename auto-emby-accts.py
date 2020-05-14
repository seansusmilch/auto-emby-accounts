import json
import random
import string
from os import path
from secrets import api_token, base_url

import requests


def add_user(username, passwd, connect, base_url, api_token):
    '''
    username, the username for the new user
    passwd, the password for the new user
    connect, the emby connect account username/email
    base_url, the direct url to the emby server
    api_token, static api token for the emby server
    '''

    api_json = {"X-Emby-Token": {api_token}}
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
    msg = ""

    #
    # CREATE NEW USER
    #

    raw_data = {
        'name': username
    }
    raw_data.update(api_json)

    res = requests.post(base_url+'/Users/New', params=raw_data, headers=headers)
    if res.status_code > 300:
        msg += "-CREATEERROR-"
    try:
        data = json.loads(res.text)
    except json.decoder.JSONDecodeError as e:
        if ' already exists' in res.text:
            print(username, ' already exists! Skipping...')
        elif 'Access token is invalid or expired.' == res.text:
            print("API token is invalid. Stopping...")
        else:
            print('error: ' + res.text)
            print(username, ' unknown error when creating! Skipping...')
        return
    newId = data['Id']
    print(username, ' create user ', res.status_code)

    #
    # UPDATE PASSWORD
    # 

    device = {
        'X-Emby-Client': "Requests Python",
        'X-Emby-Device-Name': "Python",
        "X-Emby-Client-Version": "4.4.2.0",
        "X-Emby-Device-Id": "12345678-1234-1234-1234-123456789012"
    }
    raw_data = {
        "username": username,
        "Pw": ""
    }
    raw_data.update(device)
    res = requests.post(base_url+'/Users/AuthenticateByName', params=raw_data, headers=headers)
    if res.status_code > 300:
        msg += "-AUTHERROR-"
    
    data = json.loads(res.text)
    temp_token = data['AccessToken']
    # need access token to use in place of api token because static api tokens cannot change user passwords
    raw_data = {
        "X-Emby-Token": temp_token,
        "CurrentPw": "",
        "NewPw": passwd
    }
    raw_data.update(device)
    res = requests.post(base_url+'/emby/Users/'+newId+'/Password', params=raw_data, headers=headers)
    print(username, ' add password ', passwd, ' ', res.status_code)
    if res.status_code > 300:
        msg += "-PASSWORDERROR-"

    #
    # CHANGE POLICY
    # 

    raw_data = {
        "IsAdministrator": False,
        "IsHidden": True,
        "IsHiddenRemotely": True,
        "IsDisabled": False,
        # MaxParentalRating	integer($int32, nullable)
        # BlockedTags	[string]
        # EnableUserPreferenceAccess	boolean
        # AccessSchedules	[Configuration.AccessSchedule{...}]
        # BlockUnratedItems	[string($enum)(Movie, Trailer, Series, Music, Game, Book, LiveTvChannel, LiveTvProgram, ChannelContent, Other)]
        "EnableRemoteControlOfOtherUsers": False,
        "EnableSharedDeviceControl": False,
        "EnableRemoteAccess": True,
        "EnableLiveTvManagement": False,
        "EnableLiveTvAccess": False,
        # EnableMediaPlayback	boolean
        # EnableAudioPlaybackTranscoding	boolean
        # EnableVideoPlaybackTranscoding	boolean
        # EnablePlaybackRemuxing	boolean
        "EnableContentDeletion": False,
        # EnableContentDeletionFromFolders	[string]
        "EnableContentDownloading": True,
        "EnableSubtitleDownloading": False,
        "EnableSubtitleManagement": False,
        "EnableSyncTranscoding": False,
        "EnableMediaConversion": False,
        # EnabledDevices	[string]
        # EnableAllDevices	boolean
        # EnabledChannels	[string]
        # EnableAllChannels	boolean
        # "EnabledFolders": "",
        # "EnableAllFolders": False,
        # InvalidLoginAttemptCount	integer($int32)
        "EnablePublicSharing": False,
        # "BlockedMediaFolders": "",
        # BlockedChannels	[string]
        # RemoteClientBitrateLimit	integer($int32)
        # AuthenticationProviderId	string
        # ExcludedSubFolders	[string]
        # DisablePremiumFeatures	boolean
    }
    raw_data.update(api_json)
    res = requests.post(base_url+'/emby/Users/'+newId+'/Policy', params=raw_data, headers=headers)
    print(username, ' update policy ', res.status_code)
    if res.status_code > 300:
        msg += "-POLICYERROR-"

    #
    # ADD EMBY CONNECT ACCOUNT
    #

    raw_data = {
        "ConnectUsername": connect
    }
    raw_data.update(api_json)
    res = requests.post(base_url+'/emby/Users/'+newId+'/Connect/Link', params=raw_data, headers=headers)
    print(username, ' add emby connect ', res.status_code)
    if res.status_code > 300:
        msg += "-CONNECTERROR-"
        

    #
    # APPEND TO OUT.TXT
    # 

    with open(dir + '/out.txt', 'a+', encoding='utf-8') as outfile:
        outfile.seek(0)
        if len(outfile.read(10)) > 0:
            outfile.write('\n')
        outfile.write(username + '\t' + connect + '\t' + passwd + ('\t'+msg if msg else ''))
        outfile.close()





# get users from in.txt

dir = path.split(path.abspath(__file__))
dir = dir[0]

newUsrs = []
with open(dir + '/in.txt', 'a+') as intxt:
    print('Getting new users from\n' + dir + '/in.txt')
    intxt.seek(0)
    for line in intxt.readlines():
        newUsrs.append(line.rstrip().split(','))
    intxt.close()

# run the add_user function for each new user with a password

newUsrName = connect = ""
for user in newUsrs:

    # new passwd
    passwd = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))
    print(passwd)

    if len(user) == 1:
        connect = user[0]
        username = '!' + user[0]
    elif len(user) == 2:
        connect = user[1]
        username = user[0]
    else:
        print('yo shit in the wrong format (in.txt)')
    add_user(username, passwd, connect, base_url, api_token)

with open(dir + '/out.txt', 'a+', encoding='utf-8') as outfile:
    outfile.write('\n-----------------------------')
    outfile.close()
