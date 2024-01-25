from redisconnector import *

token = '6532561146:AAGvEUL_A4rN3GKzwGr5Bu5dUpZrC9DQAhQ'


def message_sender():
    from apscheduler.schedulers.background import BackgroundScheduler
    import telebot

    bot = telebot.TeleBot(token)

    def scheduled_message():
        subscribers = get_subscriptions(2)
        sending_collection = []
        for record in subscribers:
            repo_url = record.split(';')[1]
            user_id = record.split(';')[0]
            events = get_subscribed_event_list(record)
            message = read_and_delete_event(repo_url)
            if message is None: continue
            event_collection = {'repo_url': repo_url, 'user_id': user_id, 'message': message, 'events': events}
            sending_collection.append(event_collection)

        for send_items in sending_collection:
            for event in send_items['message']:
                if event['type'] in send_items['events']:
                    bot.send_message(send_items['user_id'], json.dumps(event))

    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_message, 'interval', seconds=10)  # Adjust the interval as needed
    scheduler.start()

    try:
        bot.polling()
    except Exception as e:
        print(e)


