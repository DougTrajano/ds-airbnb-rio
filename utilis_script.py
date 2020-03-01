import pandas as pd

def get_data(origin="calendar"):
    """
    This function can download the data from Airbnb repo files (http://insideairbnb.com/get-the-data.html).

    Input
    - origin (str): The file name from airbnb data repository. Choose between calendar, listings or reviews.

    Output
    - df (Pandas.DataFrame): The DataFrame with dataset loaded.
    """
    if origin == "calendar":
        url = "http://data.insideairbnb.com/brazil/rj/rio-de-janeiro/2019-11-22/data/calendar.csv.gz"
    elif origin == "listings":
        url = "http://data.insideairbnb.com/brazil/rj/rio-de-janeiro/2019-11-22/data/listings.csv.gz"
    elif origin == "reviews":
        url = "http://data.insideairbnb.com/brazil/rj/rio-de-janeiro/2019-11-22/data/reviews.csv.gz"
    else:
        raise ValueError(
            '{} is invalid. Please select between "calendar", "listings" or "reviews"'.format(origin))
    
    df = pd.read_csv(url, low_memory=False)
    return df
