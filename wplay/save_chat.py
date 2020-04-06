'''
This code is copied by https://github.com/EliteAndroidApps/WhatsApp-GD-Extractor.


EliteAndroidApps/WhatsApp-GD-Extractor is licensed under the
GNU General Public License v3.0
'''

# region IMPORTS
from pathlib import Path
from configparser import ConfigParser
import json
import os
import re
import requests

from wplay.utils.Logger import Logger
# endregion

# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


def getGoogleAccountTokenFromAuth():
    payload : dict = {'Email': gmail, 'Passwd': passw, 'app': client_pkg,
               'client_sig': client_sig, 'parentAndroidId': devid}
    request = requests.post(
        'https://android.clients.google.com/auth', data=payload)
    token = re.search('Token=(.*?)\n', request.text)
    if token:
        return token.group(1)
    else:
        quit(request.text)


def getGoogleDriveToken(token):
    payload : dict = {
        'Token': token,
        'app': pkg,
        'client_sig': sig,
        'device': devid,
        'google_play_services_version': client_ver,
        'service': 'oauth2:https://www.googleapis.com/auth/drive.appdata https://www.googleapis.com/auth/drive.file',
        'has_permission': '1'
    }
    request = requests.post(
        'https://android.clients.google.com/auth', data=payload)
    token = re.search('Auth=(.*?)\n', request.text)
    if token:
        return token.group(1)
    else:
        quit(request.text)


def rawGoogleDriveRequest(bearer, url):
    headers : dict = {'Authorization': 'Bearer ' + bearer}
    request : dict = requests.get(url, headers=headers)
    return request.text


def downloadFileGoogleDrive(bearer, url, local):
    if not os.path.exists(os.path.dirname(local)):
        os.makedirs(os.path.dirname(local))
    if os.path.isfile(local):
        os.remove(local)
    headers : dict = {'Authorization': 'Bearer ' + bearer}
    request = requests.get(url, headers=headers, stream=True)
    request.raw.decode_content = True
    if request.status_code == 200:
        with open(local, 'wb') as asset:
            for chunk in request.iter_content(1024):
                asset.write(chunk)
    print('Downloaded: "' + local + '".')


def gDriveFileMap():
    global bearer
    data = rawGoogleDriveRequest(
        bearer, 'https://www.googleapis.com/drive/v2/files')
    jres = json.loads(data)
    backups = [] #  type : list
    for result in jres['items']:
        if result['title'] == 'gdrive_file_map':
            backups.append((result['description'],
                            rawGoogleDriveRequest(
                                bearer,
                                result['downloadUrl'])))
    if len(backups) == 0:
        quit('Unable to locate google drive file map for: ' + pkg)
    return backups


def getConfigs():
    global gmail, passw, devid, pkg, sig, client_pkg, client_sig, client_ver
    config = ConfigParser()
    try:
        config.read('settings.cfg')
        gmail = input("enter WhatsApp backup Email: ")  # type : str
        passw = input("enter password: ")  # type : str
        devid = config.get('auth', 'devid')
        pkg = config.get('app', 'pkg')
        sig = config.get('app', 'sig')
        client_pkg = config.get('client', 'pkg')
        client_sig = config.get('client', 'sig')
        client_ver = config.get('client', 'ver')
    except(ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        quit('The "settings.cfg" file is missing or corrupt!')


def jsonPrint(data):
    print(json.dumps(json.loads(data), indent=4, sort_keys=True))


def localFileLog(md5):
    logfile = 'logs' / 'files.log'  # type : str
    if not os.path.exists(os.path.dirname(logfile)):
        os.makedirs(os.path.dirname(logfile))
    with open(logfile, 'a') as log:
        log.write(md5 + '\n')


def localFileList():
    logfile = 'logs' / 'files.log'  # type : str
    if os.path.isfile(logfile):
        flist = open(logfile, 'r')
        return [line.split('\n') for line in flist.readlines()]
    else:
        open(logfile, 'w')
        return localFileList()


def createSettingsFile():
    with open('settings.cfg', 'w') as cfg:
        cfg.write('[auth]\ngmail = alias@gmail.com\npassw = yourpassword\ndevid = 0000000000000000\n\n[app]\npkg = com.whatsapp\nsig = 38a0f7d505fe18fec64fbf343ecaaaf310dbd799\n\n[client]\npkg = com.google.android.gms\nsig = 38918a453d07199354f8b19af05ec6562ced5788\nver = 9877000')


def getSingleFile(data, asset):
    data = json.loads(data)
    for entries in data:
        if entries['f'] == asset:
            return entries['f'], entries['m'], entries['r'], entries['s']


def getMultipleFiles(data, folder):
    files = localFileList()
    data = json.loads(data)
    for entries in data:
        if any(entries['m'] in lists for lists in files) is \
                False or 'database' in entries['f'].lower():
            local = folder + os.path.sep + entries['f'].replace("/", os.path.sep)
            if os.path.isfile(local) and 'database' not in local.lower():
                quit('Skipped: "' + local + '".')
            else:
                downloadFileGoogleDrive(
                    bearer,
                    'https://www.googleapis.com/drive/v2/files/' + entries['r'] + '?alt=media',
                    local)
                localFileLog(entries['m'])


def runMain(mode, asset, bID):
    global bearer
    if not os.path.isfile('settings.cfg'):
        createSettingsFile()
    getConfigs()
    bearer = getGoogleDriveToken(getGoogleAccountTokenFromAuth())
    drives = gDriveFileMap()
    if mode == 'info':
        for i, drive in enumerate(drives):
            if len(drives) > 1:
                print("Backup: " + str(i))
            jsonPrint(drive[0])
    elif mode == 'list':
        for i, drive in enumerate(drives):
            if len(drives) > 1:
                print("Backup: " + str(i))
            jsonPrint(drive[1])
    elif mode == 'pull':
        try:
            drive = drives[bID]
        except IndexError:
            quit("Invalid backup ID: " + str(bID))
        target = getSingleFile(drive[1], asset)
        try:
            f = target[0]
            m = target[1]
            r = target[2]
        except TypeError:
            quit('Unable to locate: "' + asset + '".')
        local = 'WhatsApp'+ os.path.sep + f.replace("/", os.path.sep)
        if os.path.isfile(local) and 'database' not in local.lower():
            quit('Skipped: "' + local + '".')
        else:
            downloadFileGoogleDrive(
                bearer,
                'https://www.googleapis.com/drive/v2/files/' + r + '?alt=media',
                local)
            localFileLog(m)
    elif mode == 'sync':
        for i, drive in enumerate(drives):
            folder = 'WhatsApp'
            if len(drives) > 1:
                print('Backup: ' + str(i))
                folder = 'WhatsApp-' + str(i)
            getMultipleFiles(drive[1], folder)
