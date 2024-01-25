from time import sleep
import requests
from redisconnector import get_subscriptions, add_new_event
import json


# Эта функция запускается в beckgraund и бесконечно выполняется заполняя список событий в redis
def get_repository_events():
    def filter_events(events):
        _events = []
        for event in events:
            if event['type'] in ['PullRequestEvent', 'PushEvent', 'IssuesEvent']:
                _events.append(event)
        return _events

    while True:
        repositories = get_subscriptions(1)
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"}
        for repo_url in repositories:
            response = requests.get(repo_url, headers=headers)
            if response.status_code != 200:
                print(repo_url)
                print(response.status_code)
                continue
            filtered_events = filter_events(response.json())
            print(filtered_events)
            add_new_event(repo_url, json.dumps(filtered_events))
        sleep(600)


def run_event_listener():
    while True:
        get_repository_events()
        sleep(600)
