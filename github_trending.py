import requests
import datetime
import json


def get_date_ago():
    number_days_ago = 7
    now_date = datetime.date.today()
    days_ago = datetime.timedelta(days=number_days_ago)
    date_ago = now_date - days_ago
    return date_ago.strftime("%Y-%m-%d")


def get_content_of_response(url, param):
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
    issues_data = get_content_of_response(url, None)
    for issue in issues_data:
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
                   'q': 'created:>' + get_date_ago()}
    query_url = 'https://api.github.com/search/repositories'

    all_repos = get_content_of_response(query_url, query_param)
    trending_repos = get_trending_repositories(all_repos)
    output_trending_repos(trending_repos)
