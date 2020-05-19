import requests
import json
import sys

realm1 = ''
realm2 = ''

token1 = ''
token2 = ''

fileName = ''

def exportDashboardGroup(groupId):
	print('Working with Dashboard Group ID: ',groupId)
	respText = ''

	try:
		headers = {'X-SF-TOKEN':token1,'Content-Type':'application/json','charset':'utf-8'}
		url = 'https://api.'+realm1+'.signalfx.com/v1/page/'+groupId+'?export=true'
		respText = requests.get(url=url,headers=headers).json()
		print('..Retrieved Dashboard Group..')
	except Exception as e:
		print('Error in retrieving data: ',e)
	
	try:
		url = 'https://api.'+realm2+'.signalfx.com/v1/import'
		headers['X-SF-TOKEN']=token2
		resp = requests.post(url=url,headers=headers,data=respText['export'])
		print('..Imported Dashboard Group with response..',resp.status_code)
		print('..Group ID created: ',resp.text,' ..')
	except Exception as e:
		print('Error in importing to new org: ',e)



if __name__ == "__main__":
	if len(sys.argv) != 6:
		print('Usage: python exportDashboardGroup.py SF_REALM1 SF_TOKEN1 SF_REALM2 SF_TOKEN2 DASHBOARD_GROUPS_FILE')
	realm1 = sys.argv[1]
	token1 = sys.argv[2]
	realm2 = sys.argv[3]
	token2 = sys.argv[4]
	fileName = sys.argv[5]

	if realm1 == '' or realm2 == '' or token1 == '' or token2 == '':
		print('Missing arguments in usage. Aborting')
		sys.exit(0)

	dashboardGroups = []
	with open(fileName) as f:
		dashboardGroups = f.readlines()
	
	for group in dashboardGroups:
		exportDashboardGroup(group.strip('\n'))



