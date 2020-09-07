# Auto Emby Accounts

Use python requests to add and configure new accounts on an Emby server.

## Notice

>I'm an inexperienced coder and even more inexperienced when it comes to API requests. Use this script at your own risk.

## Requirements

* Python 3
  * requests
* An Emby account with administrator privileges

## Usage

To get the script started, you need a couple inputs. First, and the most important, would be the `config.py` file.

### Configuration

`config.py` will have comments above the definition that will explain what each setting does.

```python
# Different Logging Levels
#     4: DEBUG
#     3: INFO
#     2: WARNING
#     1: ERROR
#     0: CRITICAL
log_level = 3

# When set true, if the script finds a user that already exists,
# the script will attempt to change the policy of that user,
# and add the emby connect account to that user.
overwrite = False

# The url to your Emby server
emby_base_url = 'http://localhost:8096'

# Login info for an account on your Emby server that has admin privileges
# Username
emby_admin_uname = ''
# Password
emby_admin_passwd = ''

# The script will avoid doing anything to these users AND admin_uname
avoid_users = [
    'Python',
    'Admin1122'
]

# number of seconds before the first request will timeout.
timeout = 2

# Determine whether or not to output in tsv format. Will be text if False
tsv_out = True

# If all thats provided is a connect username, this prefix will be put at
# the start of the username on the server
user_prefix = '!'

# These are the user policy changes that will be made. Can be empty
user_policy = {
    # 'IsAdministrator':                  False,          # True|False
    # 'IsHidden':                         True,           # True|False
    # 'IsHiddenRemotely':                 True,           # True|False
    # 'IsDisabled':                       False,          # True|False
    # 'MaxParentalRating':	              None,           # int|None
    # 'BlockedTags':	                    [],             # string[]
   ...
}
```

### Adding Users

To define the usernames of the accounts, create a file named `in.txt` and use the following format, values comma separated.

```text
test, ConnectUsername1
ConnectUsername2
```

 With the first line in `in.txt`, the script will create a user named **test** and attempt to link **ConnectUsername1** to that account.

The second line will create a user named **!ConnectUsername2** and attempt to link **ConnectUsername2** to that account. The "!" can be changed in the config under user_prefix

The account password will be a random 20 character alphanumeric string.

## Output

Outupt of this script, in `out.txt` or `out.tsv`, should look something like this

```tsv
---------------[2020-09-07 03:18:33.671850]---------------
LocalUser69420	EmbyConnect123	1WabMUMnaaXylCfIGrnx
```

Values are tab separated. The leftmost value is the username *on the emby server*, while the second value is the *emby connect username*. The third value is the *password* for the account on the server.
