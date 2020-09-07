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

api_token = '3e77f677c7cf44f29034106330e5922b'
base_url = 'http://localhost:8096'

admin_uname = ''
admin_passwd = ''

# The script will avoid doing anything to these users AND admin_uname
avoid_users = [
    'Python',
]

# number of seconds before the first request will timeout.
timeout = 2

# Determine whether or not to output in tsv format. Will be text if False
tsv_out = True

# If all thats provided is a connect username, this prefix will be put at
# the start of the username on the server
user_prefix = '!'

# These are the user policy changes that will be made. 
user_policy = {
    'IsAdministrator':                  False,          # True|False
    'IsHidden':                         True,           # True|False
    'IsHiddenRemotely':                 True,           # True|False
    'IsDisabled':                       False,          # True|False
    # 'MaxParentalRating':	            None,           # int|None
    # 'BlockedTags':	                    [],             # string[]
    # 'EnableUserPreferenceAccess':	    True,           # True|False
    # 'AccessSchedules':	                [],             # [Configuration.AccessSchedule{...}]
    # 'BlockUnratedItems':	            [],             # string[Movie, Trailer, Series, Music, Game, Book, LiveTvChannel, LiveTvProgram, ChannelContent, Other]
    'EnableRemoteControlOfOtherUsers':  False,          # True|False
    'EnableSharedDeviceControl':        True,           # True|False
    'EnableRemoteAccess':               True,           # True|False
    'EnableLiveTvManagement':           False,          # True|False
    'EnableLiveTvAccess':               False,          # True|False
    'EnableMediaPlayback':	            True,           # True|False
    'EnableAudioPlaybackTranscoding':	True,           # True|False
    'EnableVideoPlaybackTranscoding':	True,           # True|False
    'EnablePlaybackRemuxing':	        True,           # True|False
    'EnableContentDeletion':            False,          # True|False
    # 'EnableContentDeletionFromFolders': [],             # string[]
    'EnableContentDownloading':         True,           # True|False
    'EnableSubtitleDownloading':        False,          # True|False
    'EnableSubtitleManagement':         False,          # True|False
    'EnableSyncTranscoding':            False,          # True|False
    'EnableMediaConversion':            False,          # True|False
    # 'EnabledDevices':	                [],             # string[]
    'EnableAllDevices':	                True,           # True|False
    # 'EnabledChannels':	                [],             # string[]
    'EnableAllChannels':	            True,           # True|False
    # 'EnabledFolders':                   [],             # string[]
    'EnableAllFolders':                 True,           # True|False
    # 'InvalidLoginAttemptCount':	        10,             # int
    'EnablePublicSharing':              False,          # True|False
    # 'BlockedMediaFolders':              [],             # string[]
    # 'BlockedChannels':	                [],             # string[]
    # 'RemoteClientBitrateLimit':	        12,             # int
    # 'AuthenticationProviderId':	        '',             # string
    # 'ExcludedSubFolders':	            [],             # string[]
    # 'DisablePremiumFeatures':	        False           # True|False
}
