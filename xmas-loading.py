from config import create_api
import datetime
import calendar
from time import sleep
import logging


FILE_NAME = 'last-percentage.txt'


def retrieve_last_percentage(file_name):
    """Retrieve last percentage value tweeted

    Args:
        file_name (string): Name of file used to store percentage value

    Returns:
        integer: Last percentage value tweeted
    """
    f_read = open(file_name, 'r')
    last_seen_percentage = f_read.read().strip()
    f_read.close()
    return int(last_seen_percentage)


def store_last_percentage(last_seen_percentage,file_name):
    """Store lastest percentage tweeted

    Args:
        last_seen_percentage (integer): Latest percentage calculated
        file_name (string): Name of file used to store percentage value
    """
    f_write = open(file_name, 'w')
    f_write.write('%d' % last_seen_percentage)
    f_write.close()


def percentage_complete(today):
    """Calculates the progess of reaching Christmas day
    in a percentage value

    Args:
        today (datetime): Today's date

    Returns:
        int32: Percentage progress rounded to the nearest
        percentage point
    """
    if today >= datetime.date(today.year,12,26):
        christmas_date = datetime.date(today.year+1,12,25)
    else:
        christmas_date = datetime.date(today.year,12,25)

    if calendar.isleap(today.year):
        days_in_year = 366
    else:
        days_in_year = 365

    days_until_xmas = christmas_date-today
    percentage = round((days_in_year - int(days_until_xmas.days))/days_in_year*100)

    if today.month == 12 and today.day == 25:
        percentage = 100
    else:
        if percentage == 100:
            percentage = 99

    if today.month == 12 and today.day == 26:
        percentage = 0
    else:
        if percentage == 0:
            percentage = 1

    return percentage


def generate_progress_bar(percentage):
    """Generates the progress bar that can be used in
    a tweet

    Args:
        percentage (integer): Percentage progress to Christmas day

    Returns:
        string: Progress base using present emojis to visually
        show the progress of reaching Christmas day
    """
    presents = (percentage//10)*"\U0001F381"
    empty_blocks = (10-percentage//10)*"🔲"
    tweet = f"{presents}{empty_blocks} {percentage}%"
    return tweet


def update_status(twitter_api, tweet):
    """Tweets string to Twitter account

    Args:
        twitter_api (Twitter API): Twitter API used with Tweepy
        tweet (string): Tweet contents to be tweeted
    """
    twitter_api.update_status(tweet)
    logging.info(f"Percentage updated.")


def main():
    logging.info("Creating API...")
    twitter_api = create_api()
    
    while True:
        logging.info("Checking progress percentage...")
        today = datetime.date.today()
        percentage = percentage_complete(today)            
        last_percentage = retrieve_last_percentage(FILE_NAME)

        if today == datetime.date(today.year,12,25):
            update_status(twitter_api, generate_progress_bar(100))
            store_last_percentage(0, FILE_NAME)
        elif today == datetime.date(today.year,12,26):
            update_status(twitter_api, generate_progress_bar(0))
        elif percentage > last_percentage:
            update_status(twitter_api, generate_progress_bar(percentage))
            store_last_percentage(percentage, FILE_NAME)
        else:
            logging.info("Progress percentage unchanged...")
            
        sleep(60*60*24/2)

if __name__ == "__main__":
    main()