import re
import telebot
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from messagesender import message_sender
from eventlistener import run_event_listener
from redisconnector import *

token = '6532561146:AAGvEUL_A4rN3GKzwGr5Bu5dUpZrC9DQAhQ'

# run event listener in background
thread = threading.Thread(target=run_event_listener)
thread.daemon = True
thread.start()

# run message sender in background
# thread = threading.Thread(target=message_sender)
# thread.daemon = True
# thread.start()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['sub'])
def start(message):
    mess = message.text
    user_id = message.chat.id
    url_match = re.search(r'https?://[^\s]+', mess)
    repo_url = url_match.group(0) if url_match else None
    events_part = mess.split(repo_url)[-1].strip() if repo_url else mess
    events = [event.strip() for event in events_part.split(',')]
    create_subscription(user_id, repo_url.replace('github.com', 'api.github.com/repos') + '/events', events)
    bot.send_message(message.chat.id, f'Подписка на события репозитория {repo_url} успешно создана.', parse_mode='html')


@bot.message_handler(commands=['unsub'])
def start(message):
    repo_url = message.text
    user_id = message.chat.id
    unsubscribe(user_id, repo_url.replace('github.com', 'api.github.com/repos') + 'events')
    bot.send_message(message.chat.id, f'Подписка на события репозитория {repo_url} успешно удалена.', parse_mode='html')


@bot.message_handler()
def get_user_text(message):
    bot.send_message(message.chat.id, "Не удается распознать сообщение, пожалуйста повторите.", parse_mode='html')


def scheduled_message():
    subscribers = get_subscriptions(2)
    sending_collection = []

    for record in subscribers:
        repo_url = record.split(';')[1]
        user_id = record.split(';')[0]
        message = read_and_delete_event(repo_url)
        events = get_subscribed_event_list(record)
        if message is None: continue
        event_collection = {'repo_url': repo_url, 'user_id': user_id, 'message': message, 'events': events}
        sending_collection.append(event_collection)
    if len(sending_collection) == 0: return
    for send_items in sending_collection:
        for event in send_items['message']:
            if event['type'] in send_items['events']:
                bot.send_message(send_items['user_id'], json.dumps(event))


scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_message, 'interval', seconds=10)
scheduler.start()

bot.polling(none_stop=True)
