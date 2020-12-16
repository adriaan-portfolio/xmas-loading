from config import create_api
import datetime
import calendar


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
    today = datetime.date.today()
    percentage = percentage_complete(today)
    tweet = generate_progress_bar(today, percentage)
    #twitter_api = create_api()
    #twitter_api.update_status(tweet)


if __name__ == "__main__":
    main()