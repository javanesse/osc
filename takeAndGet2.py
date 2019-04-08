#!/usr/bin/env python

import requests
import shutil
import time
import sys

BASEURL = 'http://192.168.107.1/osc/'


resp = requests.get(BASEURL + 'info')
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /osc/info/ {}'.format(resp.status_code))

print('Manufacturer: {}'.format(resp.json()["manufacturer"]))
print('Model: {}'.format(resp.json()["model"]))
print('Firmware: {}'.format(resp.json()["firmwareVersion"]))
print('Serial: {}'.format(resp.json()["serialNumber"]))


resp = requests.post(BASEURL + 'state')
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /osc/state/ {}'.format(resp.status_code))

print('batteryLevel: {}'.format(resp.json()["state"]["batteryLevel"]*100))




data = {"name": "camera.startSession", "parameters": {} }

resp = requests.post(BASEURL + 'commands/execute', json=data)
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('camera.startSession: {}'.format(resp.status_code))


sessionId = (resp.json()["results"]["sessionId"])
print ('SessionId: {}'.format(sessionId))


# GET LAST IMAGE
data = {"name": "camera.listImages", "parameters": { "entryCount": 1} }
resp = requests.post(BASEURL + 'commands/execute', json=data)
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('camera.listImages: {}'.format(resp.status_code))
oldname = (resp.json()["results"]["entries"][0]["name"])


# TAKE A NEW IMAGE

print ('Say cheese!')

data = {"name": "camera.takePicture", "parameters": { "sessionId": sessionId} }
resp = requests.post(BASEURL + 'commands/execute', json=data)
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('camera.takePicture: {}'.format(resp.status_code))

print ('Click!')

# WAIT FOR LAST IMAGE TO CHANGE

# IF YOU ARE USING PYTHON V.2
"""
for x in range(1, 30):
    sys.stdout.write('.')
    sys.stdout.flush()
    data = {"name": "camera.listImages", "parameters": { "entryCount": 1} }
    resp = requests.post(BASEURL + 'commands/execute', json=data)
    name = (resp.json()["results"]["entries"][0]["name"])
    if (name!=oldname): 
        break
    time.sleep(0.5)

print ('')
"""

for x in xrange(1, 30):
    sys.stdout.write('.')
    sys.stdout.flush()
    data = {"name": "camera.listImages", "parameters": { "entryCount": 1} }
    resp = requests.post(BASEURL + 'commands/execute', json=data)
    name = (resp.json()["results"]["entries"][0]["name"])
    if (name!=oldname): 
        break
    time.sleep(0.5)

print ('')


# NEW IMAGE CHANGED

uri = (resp.json()["results"]["entries"][0]["uri"])

#print ('uri: {}'.format(uri))


# GET NEW IMAGE

data = {"name": "camera.getImage", "parameters": { "fileUri": uri} }

resp = requests.post(BASEURL + 'commands/execute', json=data)
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('camera.getImage: {}'.format(resp))


# SAVE NEW IMAGE
# IF YOU ARE USING PYTHON V.2
"""
resp.raw.decode_content = True

with open(name,'wb') as ofh:
	for chunk in resp:
            ofh.write(chunk)
        
print ('Image stored as: {}'.format(name))
"""

resp.raw.decode_content = True

with open(name,'w') as ofh:
	for chunk in resp:
            ofh.write(chunk)
        
print ('Image stored as: {}'.format(name))



