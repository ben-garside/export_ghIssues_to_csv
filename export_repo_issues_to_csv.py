"""
Exports Issues from a specified repository to a CSV file

Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import csv
import requests


GITHUB_USER = ''
GITHUB_PASSWORD = ''
REPO = ''  # format is username/repo
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues' % REPO
AUTH = (GITHUB_USER, GITHUB_PASSWORD)


def write_issues(response):
    '''output a list of issues to csv'''
    if not r.status_code == 200:
        raise Exception(r.status_code)
    for issue in r.json():
        labels = ''
        for label in issue['labels']:
            labels = labels + ', ' + label['name']
        labels = labels[2:]
        if issue['milestone'] is None:
            issue_milestone = ''
        else:
            issue_milestone = issue['milestone']['title']
        if issue['assignee'] is None:
            issue_assignee = ''
        else:
            issue_assignee = issue['assignee']['login']
        csvout.writerow([issue['number'],
                         issue['title'],
                         issue['user']['login'],
                         issue['created_at'],
                         issue['updated_at'],
                         labels,
                         issue['state'],
                         issue_milestone,
                         issue_assignee])

r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
csvfile = '%s-issues.csv' % (REPO.replace('/', '-'))
csvout = csv.writer(open(csvfile, 'w', newline=''))
csvout.writerow(('id', 'Title', 'Opened By', 'Created At', 'Updated At', 'Labels', 'State', 'Milestone', 'Assignee'))
write_issues(r)
#more pages? examine the 'link' header returned
if 'link' in r.headers:
    pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                r.headers['link'].split(',')]])
    while 'last' in pages and 'next' in pages:
        r = requests.get(pages['next'], auth=AUTH)
        write_issues(r)
        if pages['next'] == pages['last']:
            break