import sys
import time
import requests

def build_url(user, strt, finish): #build the request for the jira API
    """Build the request URL inputs: cmd, username, start, finish"""
    url = 'https://camgian.atlassian.net/rest/api/latest/search?jql='
    qry = 'worklogAuthor%20%3D%20jhicks%20AND%20worklogDate%20>%3D%20"2018%2F01%2F01"%20AND%20worklogDate%20<%3D%20"2018%2F01%2F15"&fields=worklog'
    req = url + qry
    return req

def main():
    """Main function"""

    usrName = sys.argv[1]
    passWrd = sys.argv[2]
    startDate = sys.argv[3]
    finishDate = sys.argv[4]

    #request to get all issues with work logged between dates
    #query: worklogAuthor = jhicks AND worklogDate >= "2018/01/01" AND worklogDate <= "2018/01/15"
    resp = requests.get(build_url(usrName, startDate, finishDate), auth = (usrName, passWrd)).json()

    #sort through dates and print out times for each project
    print('Author: ' + resp['issues'][0]['fields']['worklog']['worklogs'][0]['author']['key'])
    print('Date: ' + resp['issues'][0]['fields']['worklog']['worklogs'][0]['created'])
    print('Time: ' + resp['issues'][0]['fields']['worklog']['worklogs'][0]['timeSpent'])
    return 0

if __name__=='__main__':
    sys.exit(main())