import requests
import json
import sys

realm1 = ''
realm2 = ''

token1 = ''
token2 = ''

#listOfDetectors=['EW9muroAcAA']

def getNewUserId(oldUserId):
    print('Working with User ID: ',oldUserId)
    respText = ''
    
    try:
        headers = {'X-SF-TOKEN':token1,'Content-Type':'application/json'}
        url = 'https://api.'+realm1+'.signalfx.com/v2/organization/member/'+oldUserId
        respText = requests.get(url=url,headers=headers).json()
        email = respText['email']
        #print('RespText->',type(respText))
        print('User Email->',email)
        
    except Exception as e:
        print('Error in retrieving data: ',e)
        return None
        
    try:
        url = 'https://api.'+realm2+'.signalfx.com/v2/organization/member?query=email:'+email
        headers['X-SF-TOKEN']=token2
        resp = requests.get(url=url,headers=headers).json()
        #print('Response->',resp)
        if resp['count'] > 0:
            newUserId = resp['results'][0]['id']
            print('newUserId: ',newUserId)
            return newUserId
        else:
            print('No user matched in the new org')
        
    except Exception as e:
        print('Error in getting new User ID: ',e)
        
    return None

def getNewTeamId(oldTeamId):
    print('Working with Team ID: ',oldTeamId)
    respText = ''
    
    try:
        headers = {'X-SF-TOKEN':token1,'Content-Type':'application/json'}
        url = 'https://api.'+realm1+'.signalfx.com/v2/team/'+oldTeamId
        respText = requests.get(url=url,headers=headers).json()
        name = respText['name']
        #print('RespText->',type(respText))
        print('Team name->',name)
        
    except Exception as e:
        print('Error in retrieving data: ',e)
        return None
        
    try:
        url = 'https://api.'+realm2+'.signalfx.com/v2/team?name='+name
        headers['X-SF-TOKEN']=token2
        resp = requests.get(url=url,headers=headers).json()
        #print('Response->',resp)
        if resp['count'] > 0:
            newTeamId = resp['results'][0]['id']
            print('newTeamId: ',newTeamId)
            return newTeamId
        else:
            print('No team matched in the new org')
        
    except Exception as e:
        print('Error in getting new Team ID: ',e)
    return None

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

def exportDetector(detectorId):
    print('Working with Detector ID: ',detectorId)
    respText = ''

    try:
        headers = {'X-SF-TOKEN':token1,'Content-Type':'application/json'}
        url = 'https://api.'+realm1+'.signalfx.com/v2/detector/'+detectorId
        respText = requests.get(url=url,headers=headers).json()
        #print('RespText->',type(respText))
        
        #print('Detector->',json.dumps(respText, indent=2))
        
        users = respText['authorizedWriters']['users']
        teams = respText['authorizedWriters']['teams']
        
        newUsers = []
        newTeams = []
        
        for user in users:
            newUserId = getNewUserId(user)
            if newUserId != None:
                newUsers.append(newUserId)
                
        for team in teams:
            newTeamId = getNewTeamId(team)
            if newTeamId != None:
                newTeams.append(newTeamId)        
        
        respText['authorizedWriters']['users'] = newUsers
        respText['authorizedWriters']['teams'] = newTeams
        
        respText.pop('id')
        #respText.pop('created')
        #respText.pop('creator')
        
        newnotificationTeams = []
        newlinkTeams = []
        deleteNotifications = []
        
        for rule in respText['rules']:
            for notification in rule['notifications']:
                if notification['type'] == 'Team':
                    print('In notifications...')
                    newTeam = getNewTeamId(notification['team'])
                    if newTeam == None:
                        deleteNotifications.append(notification)
                    else:
                        print('old team->',notification['team'],'...new team->',newTeam)
                        notification['team'] = newTeam
        
        for rule in respText['rules']:
            for notification in deleteNotifications:
                print('deleting notification..',notification)
                rule['notifications'].remove(notification)
        
        
        
        newLinkTeams = []
        for team in respText['teams']:
            print('In linking teams...')
            newTeam = getNewTeamId(team)
            if newTeam != None:
                print('old team->',team,'...new team->',newTeam)
                newLinkTeams.append(newTeam)
            
        respText['teams'] = newLinkTeams
       
        
        
    except Exception as e:
        print('Error in retrieving data: ',e)
        
    try:
        url = 'https://api.'+realm2+'.signalfx.com/v2/detector'
        headers['X-SF-TOKEN']=token2
        resp = requests.post(url=url,headers=headers,json=respText)
        print('Response->',resp.text)
        print('Status Code->',resp.status_code)
        if resp.status_code != 200:
            print('Error in Detector creation for Detector Body->',json.dumps(respText, indent=2))
    except Exception as e:
        print('Error in importing to new org: ',e)
        

if __name__ == "__main__":
	if len(sys.argv) != 5:
		print('Usage: python exportDashboardGroup.py SF_REALM1 SF_TOKEN1 SF_REALM2 SF_TOKEN2')
	realm1 = sys.argv[1]
	token1 = sys.argv[2]
	realm2 = sys.argv[3]
	token2 = sys.argv[4]
	

	if realm1 == '' or realm2 == '' or token1 == '' or token2 == '':
		print('Missing arguments in usage. Aborting')
		sys.exit(0)

	v2_detectorList = []
	v2_detectorList = getV2Detectors()
	
	for detector in v2_detectorList:
		exportDetector(detector)



