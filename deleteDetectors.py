import requests
import json
import sys

realm1 = ''
token1 = ''

#listOfDetectors=['EW9muroAcAA']

def getV1Detectors():
    results = []
    try:
        headers = {'X-SF-TOKEN':token1,'Content-Type':'application/json'}
        url = 'https://api.'+realm1+'.signalfx.com/v1/detector?limit=1000'        
        resp = requests.get(url=url,headers=headers).json()
        print('response->',resp)
        if resp['count'] >0:
            for result in resp['rs']:
                print('result id->',result)
                results.append(result)
    except Exception as e:
        print(e)
    return results

def getV2Detectors():
    results = []
    try:
        headers = {'X-SF-TOKEN':token1,'Content-Type':'application/json'}
        url = 'https://api.'+realm1+'.signalfx.com/v2/detector?limit=1000'
        resp = requests.get(url=url,headers=headers).json()
        if resp['count'] > 0:
            for result in resp['results']:
                print(result['id'],',name:',result['name'])
                results.append(result['id'])

    except Exception as e:
        print(e)
    return results

def deleteV1Detector(detectorId):
    print('Working with Detector ID: ',detectorId)
    respText = ''

    try:
        headers = {'X-SF-TOKEN':token1,'Content-Type':'application/json'}
        url = 'https://api.'+realm1+'.signalfx.com/v1/detector/'+detectorId
        respText = requests.delete(url=url,headers=headers)
        print('RespText->',respText)
        
    except Exception as e:
        print('Error in deleting data: ',e)


def deleteV2Detector(detectorId):
    print('Working with Detector ID: ',detectorId)
    respText = ''

    try:
        headers = {'X-SF-TOKEN':token1,'Content-Type':'application/json'}
        url = 'https://api.'+realm1+'.signalfx.com/v2/detector/'+detectorId
        respText = requests.delete(url=url,headers=headers)
        print('RespText->',respText)
        
    except Exception as e:
        print('Error in deleting data: ',e)
        

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python exportDashboardGroup.py SF_REALM1 SF_TOKEN1')
    realm1 = sys.argv[1]
    token1 = sys.argv[2]


    if realm1 == '' or token1 == '':
        print('Missing arguments in usage. Aborting')
        sys.exit(0)

    v1_detectorList = []
    v1_detectorList = getV1Detectors()

    v2_detectorList = []
    v2_detectorList = getV2Detectors()

    for detector in v1_detectorList:
        deleteV1Detector(detector)

    for detector in v2_detectorList:
        deleteV2Detector(detector)



