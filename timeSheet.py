import sys
from datetime import datetime
import requests

def build_url(user, strt, finish): #build the request for the jira API
    """Build the request URL inputs: cmd, username, start, finish"""
    url = 'https://camgian.atlassian.net/rest/api/latest/search?jql='
    cstrt = strt.strftime('%Y%%2F%m%%2F%d')
    cfinish = finish.strftime('%Y%%2F%m%%2F%d')
    
    qry = 'worklogAuthor%20%3D%20' + user + '%20AND%20worklogDate%20>%3D%20"' + cstrt + '"%20AND%20worklogDate%20<%3D%20"' + cfinish + '"&fields=worklog,labels'
    req = url + qry
    return req

def main():
    """Main function"""

    usrName = sys.argv[1]
    passWrd = sys.argv[2]
    startDate = datetime.strptime(sys.argv[3], '%Y/%m/%d')
    finishDate = datetime.strptime(sys.argv[4], '%Y/%m/%d')
    proj = ['ERDC2B', 'RIF', 'FinTech', 'ERDC', 'CBM', 'Point72', 'Fincantieri']
    work = [0,0,0,0,0,0,0]

    #request to get all issues with work logged between dates
    #query: worklogAuthor = jhicks AND worklogDate >= "2018/01/01" AND worklogDate <= "2018/01/15"
    resp = requests.get(build_url(usrName, startDate, finishDate), auth = (usrName, passWrd)).json()

    numIssues = resp['total']
    #Loop through the total number of issues in the query
    for x in range(0, numIssues):
        numLogs = resp['issues'][x]['fields']['worklog']['total']

        #loop through the total number of work logs in the issue
        for y in range(0, numLogs):
            cmtDate = datetime.strptime(resp['issues'][x]['fields']['worklog']['worklogs'][y]['created'][:10], '%Y-%m-%d')

            #check for only logs within the time window
            if cmtDate >= startDate and cmtDate <= finishDate:
                lab = resp['issues'][x]['fields']['labels']
                for i in range(0, len(proj)):
                    for j in range(0, len(lab)):
                        if lab[j] == proj[i]:
                            #add time to correct project
                            work[i] = work[i] + int(resp['issues'][x]['fields']['worklog']['worklogs'][y]['timeSpentSeconds'])

    for num in range(0, len(proj)):
        print('Project {0} has {1} seconds'.format(proj[num], work[num]))

if __name__=='__main__':
    sys.exit(main())