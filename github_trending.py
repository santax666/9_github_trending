import requests
import datetime
import json


def get_date_ago():
    number_days_ago = 7
    now_date = datetime.date.today()
    days_ago = datetime.timedelta(days=number_days_ago)
    date_ago = now_date - days_ago
    return date_ago.strftime("%Y-%m-%d")


def get_request(url, req_type):
    if req_type == 'repo':
        query_param = {'order': 'desc', 'sort': 'stars',
                       'q': 'created:>'+get_date_ago()}
        query_url = 'https://api.github.com/search/repositories'
    else:
        query_param = None
        query_url = url.replace('{/number}', '')
    repos = requests.get(query_url, params=query_param)
    return repos.text


def json_data_parse(json_str, req_type):
    json_data = json.loads(json_str)
    if req_type == 'repo':
        json_data = json_data["items"]
    return json_data


def get_trending_repos_info(data):
    trending_repos = []
    repos_trend_count = 20
    for repo in data[:repos_trend_count:]:
        name = repo['name']
        stars = repo['stargazers_count']
        url = repo['issues_url']
        repo_info = (name, stars, url,)
        trending_repos.append(repo_info)
    return trending_repos


def get_open_issues_amount(issues_url):
    open_issues = []
    all_issues = get_request(issues_url, 'issues')
    issues_info = json_data_parse(all_issues, 'issues')
    for issue in issues_info:
        html_url = issue['html_url']
        state = issue['state']
        if ("/issues/" in html_url) and (state == 'open'):
            title = issue['title']
            issue_info = (html_url, title,)
            open_issues.append(issue_info)
    return open_issues


if __name__ == '__main__':
    all_repos = get_request(None, 'repo')
    repos_info = json_data_parse(all_repos, 'repo')
    trending_repos = get_trending_repos_info(repos_info)

    for repo_count, repo in enumerate(trending_repos, 1):
        open_issues = get_open_issues_amount(repo[2])
        open_issues_count = len(open_issues)
        print()
        print(repo_count, ") Проект:", repo[0], ", звезд -", repo[1],
              ", открытых issues -", open_issues_count, ':')
        for issue in open_issues:
            print(issue)
