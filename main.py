import tweepy
import json
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage

WORKING_DIR = os.getcwd()

KEYS_FILE_PATH = os.path.join(WORKING_DIR, 'keys.json')
if not os.path.exists(KEYS_FILE_PATH):
    raise FileNotFoundError('keys file not found!')
with open(KEYS_FILE_PATH, 'r') as f:
    keys = json.load(f)

# Twitter APIの認証情報
consumer_key = keys['consumer_key']
consumer_secret = keys['consumer_secret']
access_token = keys['access_token']
access_token_secret = keys['access_token_secret']

# LINE Notify APIのアクセストークン
# line_access_token = keys['line_access_token']
# LINE Messaging APIのアクセストークン
channel_access_token = keys['channel_access_token']
user_id = keys['user_id']

# Twitter APIの認証
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Twitter APIクライアントの作成
api = tweepy.API(auth)

# specify account id
screen_names = ['jaguring1', 'narita_yusuke']

for screen_name in screen_names:
    log_path = os.path.join(WORKING_DIR, 'logs/' f'{screen_name}.log')
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            latest_tweet_id = f.readline().strip()
    else:
        with open(log_path, 'w'):
            latest_tweet_id = ''

    # 指定したアカウントの最新ツイートを取得
    if latest_tweet_id == '':
        latest_tweets = api.user_timeline(screen_name=screen_name, count=3)
    else:
        latest_tweets = api.user_timeline(screen_name=screen_name, since_id=latest_tweet_id)
    print(f'found {len(latest_tweets)} tweet(s)')

    records = []
    for tweet in latest_tweets:
        # ツイートのテキストとURLを取得
        tweet_text = tweet.text
        tweet_url = f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}'

        # LINEに送信するメッセージを作成
        # message = f'@{screen_name}\'s latest tweet:\n{tweet_text}\n{tweet_url}'
        message = f'@{screen_name}\'s latest tweet:\n{tweet_text}'

        # line notify
        # line_notify_api = 'https://notify-api.line.me/api/notify'
        # headers = {'Authorization': f'Bearer {line_access_token}'}
        # data = {'message': message}
        # response = requests.post(line_notify_api, headers=headers, data=data)

        # line bot
        line_bot_api = LineBotApi(channel_access_token)
        messages = TextSendMessage(text=message)
        line_bot_api.push_message(user_id, messages=messages)
        
        # store id for logging
        records.append(tweet.id_str)

    # 最新ツイートIDを更新
    with open(log_path, 'r') as f:
        old_tweets_ids = list(map(lambda id: id.strip(), f.readlines()))
    with open(log_path, 'w') as f:
        f.writelines(map(lambda id: id+'\n', records + old_tweets_ids))

print('Execution completed')
