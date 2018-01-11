import sys
import time
import requests

def build_url(cmd, user, strt, finish): #build the request for the jira API
    """Build the request URL inputs: cmd, username, start, finish"""
    return 0

def main():
    """Main function"""

    usrName = sys.argv[1]
    passWrd = sys.argv[2]
    startDate = sys.argv[3]
    finishDate = sys.argv[4]

    #request to get all issues with work logged between dates
    #query: worklogAuthor = jhicks AND worklogDate >= "2018/01/01" AND worklogDate <= "2018/01/15"
    resp = requests.get(build_url('search', usrName, startDate, finishDate), auth = (usrName, passWrd))
    #resp = requests.get('https://camgian.atlassian.net/rest/api/latest/search?jql=worklogAuthor%20%3D%20jhicks%20AND%20worklogDate%20>%3D%20"2018%2F01%2F01"%20AND%20worklogDate%20<%3D%20"2018%2F01%2F15"', auth = ('ajoiner', 'Lis@1676')).json()

    #sort through dates and print out times for each project

    return 0

if __name__=='__main__':
    sys.exit(main())