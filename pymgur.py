
import sys
if sys.platform == "linux" or sys.platform == "linux2":
    from mss.linux import MSS as mss
elif sys.platform == "darwin":
    from mss.darwin import MSS as mss
elif sys.platform == "win32":
    from mss.windows import MSS as mss
import time
import mss.tools
import requests
import json
import pyperclip
import yaml

screenshotType= 'default';
imgurConfFile = 'imgurConf.yaml'
imgurConf = {}

img_filename = time.strftime("%a-%d-%b-%Y_%H:%M:%S", time.gmtime()) + ".png"

if(len(sys.argv) > 1):
    screenshotType = sys.argv[1]

def loadConfig():
    with open(imgurConfFile, 'r') as stream:
        imgurConf = yaml.safe_load(stream)


def takeScreenshot(screenshotType):
    loadConfig()

    if ('default' in screenshotType):
        with mss.mss() as sct:
            file = sct.shot(output=img_filename)
    elif ('-d' in screenshotType):
        with mss.mss() as sct:
            time.sleep(5)
            file = sct.shot(output=img_filename)
    elif ('-i' in screenshotType):
        with mss.mss() as sct:
            file = sct.shot(output='imgur.png')
        upload()
            
def upload():
    time.sleep(5)
    print(imgurConf)
    imageUploadAPI = "https://api.imgur.com/3/upload"
    imageUploadPayload = {'image' : open('imgur.png', 'rb').read() }
    imageUploadHeaders = {'Authorization' : 'Bearer {}'.format(imgurConf['access_token']) }

    req = requests.post(imageUploadAPI, data=imageUploadPayload, headers=imageUploadHeaders)
    imageUploadResponse = json.loads(req.text)


    if(imageUploadResponse['status'] == 200 and imageUploadResponse['success'] == True):
        userResponse = {}
        userResponse['link'] = imageUploadResponse['data']['link']
        userResponse['deleteHash'] = imageUploadResponse['data']['deletehash']
        userResponse['account_id'] = imageUploadResponse['data']['account_id']

        print(json.dumps(userResponse, indent=4, sort_keys=True))
        pyperclip.copy(userResponse['link'])
        print('\n\rDu har imgur-länken i clipboard, bara att pastea järnet!')


takeScreenshot(screenshotType)
