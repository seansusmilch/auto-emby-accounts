# Auto Emby Accounts

Use python requests to add and configure new accounts on an Emby server.

## Notice

>I'm an inexperienced coder and even more inexperienced when it comes to API requests. Use this script at your own risk.

## Requirements

* Python (I've only tested 3.8.2) with the following modules
  * requests
  * json

## Usage

This script takes action on 3 files `in.txt`,`out.txt`, and `secrets.py` which need to be in the same directory as `auto-emby-accts.py`.

To define your server url and api token, make a file named `secrets.py` in the same directory as `auto-emby-accts.py` with this format

```python
base_url = ""   # put the url your emby server here (Ex: "http://localhost:8096")
api_token = ""  # put the static api token for your server here (Ex: "ac4e8d00c23842f39e6f793383152360")
```

To define the usernames of the accounts, create a file named `in.txt` and use the following format, values comma separated.

```text
test, testConnectUsername
testConnectUsername
```

 With the first line in `in.txt`, the script will create a user named **test** and attempt to link **testConnectUsername** to that account.

The second line will create a user named **!testConnectUsername** (notice the "!" at the beginning) and attempt to link **testConnectUsername** to that account.

The account password will be a random 20 character alphanumeric string.

## Output

Outupt of this script, in `out.txt`, should look something like this

```text
!test	testConnectUsername K46uLsbhQ6EhZY2a7OK9
test2	testConnectUsername2    LCM4Pyl2AFc7gr8zQwi4	-CONNECTERROR-
-----------------------------
```

Values are tab separated. The leftmost value is the username *on the emby server*, while the second value is the *emby connect username*. The third value is the password for the account on the server. Any values past this should be error messages. A line of dashes will print after each run, given that no uncaught exceptions occured.

## Errors

I have not extensively tested for every possible error but here are some that can occur.

```text
-CONNECTERROR-                              out.txt error. The script could not link an account to emby connect. The account may be already linked on the server, or the connect username is invalid.
-CREATEERROR-                               out.txt error. This shouldn't be able to be written to out.txt
...already exists! Skipping...              Console error. There is an account on the emby server that has the username trying to be added.
API token is invalid. Stopping...           Console error. Your API token in secrets.py is invalid.
```

### Emby User Settings

Here's a list of user settings explicitly changed by this script. A screenshot of what the user settings page will look like is also down there. These settings are to suit my own needs but can be edited in `auto-emby-accts.py` under the section that begins with the comment `# CHANGE POLICY`

|   Feature    |   Value    |
|-------|-------|
|IsAdministrator|False|
|IsHidden|True|
|IsHiddenRemotely|True|
|IsDisabled|False|
|EnableRemoteControlOfOtherUsers|False|
|EnableSharedDeviceControl|False|
|EnableRemoteAccess|True|
|EnableLiveTvManagement|False|
|EnableLiveTvAccess|False|
|EnableContentDeletion|False|
|EnableContentDownloading|True|
|EnableSubtitleDownloading|False|
|EnableSubtitleManagement|False|
|EnableSyncTranscoding|False|
|EnableMediaConversion|False|
|EnablePublicSharing|False|

![alt text](https://i.imgur.com/uYbYqMk.png)
