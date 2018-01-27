import sys
from datetime import datetime, timedelta, date
import requests

def build_url(user, strt, finish): #build the request for the jira API
    """Build the request URL inputs: cmd, username, start, finish"""
    url = 'https://camgian.atlassian.net/rest/api/latest/search?jql='
    cstrt = strt.strftime('%Y%%2F%m%%2F%d')
    cfinish = finish.strftime('%Y%%2F%m%%2F%d')
    
    qry = 'worklogAuthor%20%3D%20' + 'jhicks' + '%20AND%20worklogDate%20>%3D%20"' + cstrt + '"%20AND%20worklogDate%20<%3D%20"' + cfinish + '"&fields=worklog,labels'
    req = url + qry
    return req

def build_date(pCode, begin, end):
    """Builds dict with a list of dates and projects between begin and end"""
    dates = {}
    duration = int(str((end - begin).days))
    for d in range(0, duration + 1):
        dates[(begin + timedelta(days=d))] = pCode
    return dates

def main():
    """Main function"""

    usrName = sys.argv[1]
    passWrd = sys.argv[2]
    startDate = datetime.strptime(sys.argv[3], '%Y/%m/%d')
    finishDate = datetime.strptime(sys.argv[4], '%Y/%m/%d')
    proj = [['ERDC2B', 0], ['RIF', 0], ['FinTech', 0], ['ERDC', 0], ['CBM', 0], ['Point72', 0], ['Fincantieri', 0]]
    work = [0, 0, 0, 0, 0, 0, 0]
    workLog = build_date(proj, startDate, finishDate)

    #request to get all issues with work logged between dates
    #query: worklogAuthor = jhicks AND worklogDate >= "2018/01/01" AND worklogDate <= "2018/01/15"
    resp = requests.get(build_url(usrName, startDate, finishDate), auth = (usrName, passWrd)).json()

    numIssues = resp['total']
    #Loop through the total number of issues in the query
    for x in range(0, numIssues):
        numLogs = resp['issues'][x]['fields']['worklog']['total']

        #loop through the total number of work logs in the issue
        for y in range(0, numLogs):
            cmtDate = datetime.strptime(resp['issues'][x]['fields']['worklog']['worklogs'][y]['started'][:10], '%Y-%m-%d')

            #check for only logs within the time window
            if cmtDate >= startDate and cmtDate <= finishDate:
                lab = resp['issues'][x]['fields']['labels']
                #Loop through the labels on the issue until we find one of the proj labels
                for i in range(0, len(proj)):
                    for j in range(0, len(lab)):
                        if lab[j] == proj[i][0]:
                            #add time to correct date and project in workLog
                            workLog[cmtDate][i][1] += int(resp['issues'][x]['fields']['worklog']['worklogs'][y]['timeSpentSeconds'])

    for a in workLog:
        print (a.strftime('%Y/%m/%d') + ': ' + str(workLog[a]))

if __name__=='__main__':
    sys.exit(main())