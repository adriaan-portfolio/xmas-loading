from config_tweepy import create_api
from config_dropbox import create_dropbox_api
import datetime
import calendar
from time import sleep
import logging
import dropbox

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

FILE_NAME = 'last-percentage.txt'

def read_file(dbx, from_file):
    """Read file from Dropbox 

    Args:
        dbx (Dropbox object): Dropbox object generated from API token
        from_file (string): File location in Dropbox accounts

    Returns:
        int32: Percentage value
    """
    _, f = dbx.files_download(from_file)
    percentage = f.content
    percentage = percentage.decode('utf-8')
    return int(percentage)


def write_file(dbx, last_percentage_file, to_file_location):
    """Write file to dropbox account

    Args:
        dbx (dropbox object): Dropbox object generated with API token
        last_percentage_file (file): Name of file that will be uploaded
        to_file_location (string): Dropbox location where file is written to
    """
    with open(last_percentage_file, 'rb') as f:
        dbx.files_upload(f.read(), to_file_location, mode=dropbox.files.WriteMode.overwrite)


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
    
    return percentage


def generate_progress_bar(today,percentage):
    """Generates the progress bar that can be used in
    a tweet

    Args:
        today (datetime): Today's date
        percentage (integer): Percentage progress to Christmas day

    Returns:
        string: Progress base using present emojis to visually
        show the progress of reaching Christmas day
    """
    if today == datetime.date(today.year,12,25):
        presents = 10*'\U0001F381'
        tweet = f"{presents} {percentage}%"
    elif today == datetime.date(today.year,12,26):
        empty_blocks = 10*"🔲"
        tweet = f"{empty_blocks} {percentage}%"
    else:
        presents = (percentage//10)*"\U0001F381"
        empty_blocks = (10-percentage//10)*"🔲"
        tweet = f"{presents}{empty_blocks} {percentage}%"
    return tweet


def main():
    logging.info("Creating Twitter API...")
    twitter_api = create_api()
    
    while True:
        logging.info("Checking progress percentage...")
        today = datetime.date.today()
        logging.info("Creating Dropbox object...")
        dbx = create_dropbox_api()
        percentage = percentage_complete(today)
        logging.info("Retrieving last percentage tweeted...")            
        last_percentage = read_file(dbx, f"/{FILE_NAME}")
        if percentage > last_percentage:
            logging.info("Updating percentage value...")
            tweet = generate_progress_bar(today, percentage)
            twitter_api.update_status(tweet)
            store_last_percentage(percentage, FILE_NAME)
            write_file(dbx, FILE_NAME, f"/{FILE_NAME}")
            logging.info(f"Percentage updated to {percentage}%")
        else:
            logging.info("Last and current percentage the same, no action required.")
        sleep(60*60*24/2)

if __name__ == "__main__":           
    main()