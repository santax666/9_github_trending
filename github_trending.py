import requests
import datetime
import json


def get_date_one_week_ago():
    days_in_week = 7
    now_date = datetime.date.today()
    count_days_ago = datetime.timedelta(days=days_in_week)
    date_ago = now_date - count_days_ago
    return date_ago.strftime("%Y-%m-%d")


""" --- send_get_request(url, param) ---
Функция вызывается 2 раза, поэтому разные url и param переносить внутрь функции
нежелательно. Если скрипт будет импортирован в другой проект, то есть большая
вероятность, что эта функция будет использована - url и param в ней будут лишни
    --- send_get_request(url, param) --- """


def send_get_request(url, param):
    response = requests.get(url, params=query_param)
    return response.json()


def get_trending_repositories(json_data):
    trending_repos = []
    repos_trend_count = 20
    for repo in json_data['items'][:repos_trend_count:]:
        name = repo['name']
        url = repo['issues_url']
        issues_count = repo['open_issues_count']
        if issues_count:
            open_issues = get_open_issues_amount(url)
        else:
            open_issues = []
        repo_info = (name, url, open_issues,)
        trending_repos.append(repo_info)
    return trending_repos


def get_open_issues_amount(issues_url):
    open_issues = []
    url = issues_url.replace('{/number}', '')
    issues_content = send_get_request(url, None)
    for issue in issues_content:
        html_url = issue['html_url']
        state = issue['state']
        if ("/issues/" in html_url) and (state == 'open'):
            title = issue['title']
            issue_info = (html_url, title,)
            open_issues.append(issue_info)
    return open_issues


def output_trending_repos(trending_repos):
    for repo_count, repo in enumerate(trending_repos, 1):
        open_issues_count = len(repo[2])
        print()
        print("{0}) Проект: {1}, открытых issues: {2}"
              .format(repo_count, repo[0], open_issues_count))
        if open_issues_count:
            for issue in repo[2]:
                print(issue)


if __name__ == '__main__':
    query_param = {'order': 'desc', 'sort': 'stars',
                   'q': 'created:>' + get_date_one_week_ago()}
    query_url = 'https://api.github.com/search/repositories'

    repos_json_content = send_get_request(query_url, query_param)
    trending_repos = get_trending_repositories(repos_json_content)
    output_trending_repos(trending_repos)
