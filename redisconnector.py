import json

import redis

# database 0 using for store repo_url & user_id: [events list]
# database 1 using for store repo_url: response_data
subscriptions_db = redis.Redis(host='redis', port=6379, db=0)
data_db = redis.Redis(host='redis', port=6379, db=1)


def create_subscription(subscriber_id, repo_url, events: list):
    subscriptions_db.delete(f'{subscriber_id};{repo_url}')
    for event in events: subscriptions_db.rpush(f'{subscriber_id};{repo_url}', event)


def unsubscribe(subscriber_id, repo_url):
    subscriptions_db.delete(f'{subscriber_id};{repo_url}')


def add_new_event(repo_url, event_data):
    data_db.set(repo_url, event_data)


def get_subscribed_event_list(key):
    events_list = subscriptions_db.lrange(key, 0, -1)
    events_list = [item.decode('utf-8') for item in events_list]
    return events_list


# provide 1 if you want to get repositories list
# provide 0 if you want to get user id list
# provide 2 if you want to get user; repo pair
def get_subscriptions(number: int):
    all_keys = subscriptions_db.keys("*")
    data_list = []
    for key in all_keys:
        if number != 2:
            data_list.append(key.decode().split(';')[number])
        else:
            data_list.append(key.decode())
    return data_list


def read_and_delete_event(repo_url):
    new_event = data_db.get(repo_url)
    if new_event is None: return None
    data_db.delete(repo_url)
    return json.loads(new_event)
