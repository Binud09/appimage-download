import os
import argparse
import urllib.request
import json
from pathlib import Path
import stat


def getResponse(url):
    operUrl = urllib.request.urlopen(url)
    if(operUrl.getcode()==200):
        data = operUrl.read()
        print(data)
        jsonData = json.loads(data)
    else:
        print("Error receiving data", operUrl.getcode())
    return jsonData


def downloader(url, id):
    print('Beginning file download')
    print('Downloading')
    home = str(Path.home())
    download_path = os.path.join(home, 'Applications', id)
    print(download_path)
    urllib.request.urlretrieve(url, download_path)
    
    st = os.stat(download_path)
    os.chmod(download_path, st.st_mode | stat.S_IEXEC)
    print('Downloading Completed')

def installAppImage(id):
  root_url = 'https://raw.githubusercontent.com/Bonani19/finalproject/master/appimages.scraper-master/results/'
  appImage_url = root_url + id
  appImage_json_url = appImage_url + "/AppImageInfo.json"
  print(appImage_json_url)
  #get data from url
  jsonData = getResponse(appImage_json_url)
  #convert url data into json
  jsonData = json.dumps(jsonData, sort_keys=True)
  jsonData = json.loads(jsonData)
  appImage_file_url = jsonData['file']['referring_url']
  print(appImage_file_url)
  downloader(appImage_file_url, id)


def removeAppImage(id):
    os.remove(id)
    print('Removed')


parser = argparse.ArgumentParser(description="Manage AppImage",
                                 prog='AppImage',
                                 usage='sudo appimage [options] ')
parser.add_argument('-i',
                    '--install',
                    nargs='+',
                    help="To install AppImage -i <package id>")

parser.add_argument('-r',
                    '--remove',
                    nargs='+',
                    help="To remove AppImage -r <package id>")

args = parser.parse_args()

if args.install:
    print("Install")
    appImage_id = args.install[0]
    print(appImage_id)
    installAppImage(appImage_id)
elif args.remove:
    appImage_id = args.remove[0]
    removeAppImage(appImage_id)
else:
    print('No Argument')
    print('--help for Usage')
