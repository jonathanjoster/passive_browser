# Passive browser

\* works on crontab, accumulating your favorite account's latest tweets.

## Setup

```
conda install tweepy
conda install linebot
```

Additinally, don't forget to add keys.json to your project directory.

## Usage

Command `crontab -e` then append this below:

```
# this cron works every hour
* * */1 * * /abs/path/to/your/python abs/path/to/main.py > /var/log/passive_browser.log 1> /dev/null
```