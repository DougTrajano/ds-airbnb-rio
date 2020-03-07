import pandas as pd
import numpy as np
import ast
from tqdm import tqdm
import math
import json


def get_data(origin="calendar"):
    """
    This function can download the data from Airbnb repo files (http://insideairbnb.com/get-the-data.html).

    Input
    - origin (str, optional): The file name from airbnb data repository. Choose between calendar, listings or reviews.

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

def processing(dataset, del_features=False, cat_features=False, fillna=False):
    """
    This function make all the processing step on listings.csv extracted from airbnb.

    Input
    - dataset (DataFrame, required): The DataFrame loaded from listings.csv.
    - del_features (bool, optional): Delete textual features that we won't work with.
    - cat_features (bool, optional): Encoding for categorical features.
    - fillna (bool, optional): Send True if you like to convert nan values in 0 (zeros).

    Output
    - datset (DataFrame): The dataset processed.
    """
    dataset = dataset.to_dict(orient="records")
    new_dataset = []
    bool_cols = ["is_location_exact", "host_is_superhost", "host_identity_verified",
                 "instant_bookable"]
    
    # procesing each record
    with tqdm(total=len(dataset)) as pbar:
        for each in dataset:
            # irrelevant features
            each = _irrelevant_features(each)
            
            each["property_type"] = _property_type(each["property_type"])
            each["host_response_rate"] = _host_response_rate(each["host_response_rate"])
            each["price"] = _price(each["price"])
            each["weekly_price"] = _price(each["weekly_price"])
            each["monthly_price"] = _price(each["monthly_price"])
            each["security_deposit"] = _price(each["security_deposit"])
            each["cleaning_fee"] = _price(each["cleaning_fee"])
            each["extra_people"] = _price(each["extra_people"])

            host_verifications = _host_verifications(
                each["host_verifications"])
            if isinstance(host_verifications, dict):
                each = {**each, **host_verifications}
            del each["host_verifications"]

            amenities = _amenities(each["amenities"])
            if isinstance(amenities, dict):
                each = {**each, **amenities}
            del each["amenities"]

            for col in bool_cols:
                each[col] = _bool_convert(each[col])
                
            if del_features:
                del_features = ['name', 'description', 'access', 'house_rules',
                                'host_about', 'host_neighbourhood', 'neighbourhood']
                each = _del_features(each, del_features)
                
            if cat_features:
                each = _encoder(each)
            # add processed record
            new_dataset.append(each)
            pbar.update(1)
    new_dataset = pd.DataFrame(new_dataset)
    if fillna:
        new_dataset.fillna(0, inplace=True)
    return new_dataset


def _property_type(value):
    if value in ["Apartment", "House", "Condominium", "Loft", "Guest suite"]:
        return value
    elif value == "Serviced apartment":
        return "Apartment"
    elif value == ["Guesthouse", "Townhouse", "Tiny house", "Earth house"]:
        return "House"
    elif value == ["Boutique hotel", "Aparthotel", "Hostel"]:
        return "Hotel"
    else:
        return "Others"


def _bool_convert(value):
    if value == "t":
        return 1
    elif value == "f":
        return 0
    else:
        return np.nan


def _host_response_rate(value):
    try:
        value = value.replace("%", "")
        value = int(value)
    except:
        value = np.nan
    finally:
        return value


def _host_verifications(value):
    hosts = {}
    value_lst = ast.literal_eval(value)
    try:
        for each in value_lst:
            key_name = "host_verifications_" + each
            hosts[key_name] = 1
    except:
        hosts = np.nan
    return hosts


def _amenities(value):
    try:
        value = value.replace('"', '')
        value = value.replace('{', '["')
        value = value.replace('}', '"]')
        value = value.replace(',', '","')
        value = ast.literal_eval(value)
    except:
        value = np.nan
    finally:
        try:
            new_value = []
            for each in value:
                each = each.replace(" ", "_")
                each = each.lower()
                new_value.append(each)

            amenities = {}
            for each in new_value:
                key_name = "amenities_" + each
                amenities[key_name] = 1
        except:
            amenities = np.nan
    return amenities


def _price(value):
    if isinstance(value, str):
        value = value.replace("$", "")
        value = value.split(".")[0]
        value = value.replace(",", "")
        value = int(value)
    else:
        value = np.nan
    return value


def _del_features(value, del_features):    
    for col in del_features:
        try:
            del value[col]
        except:
            pass
    return value

def _irrelevant_features(value):
    cols_to_remove = ["city", "calendar_updated", "bed_type", "availability_60", "availability_90", 
                      "availability_365", "calendar_last_scraped", "calculated_host_listings_count_entire_homes", 
                      "country", "country_code", "experiences_offered", "first_review", "has_availability", 
                      "host_acceptance_rate", "host_has_profile_pic", "host_id", "host_location", "host_name", 
                      "host_picture_url", "host_since", "host_thumbnail_url", "host_total_listings_count", 
                      "host_url", "id", "interaction", "is_business_travel_ready", "jurisdiction_names", 
                      "last_review", "last_scraped", "latitude", "longitude", "license", "listing_url", 
                      "market", "maximum_minimum_nights", "maximum_nights", "maximum_nights_avg_ntm", 
                      "medium_url", "minimum_maximum_nights", "minimum_minimum_nights","minimum_nights", 
                      "minimum_nights_avg_ntm", "neighborhood_overview", "neighbourhood_cleansed", 
                      "neighbourhood_group_cleansed", "notes","number_of_reviews", "number_of_reviews_ltm", 
                      "picture_url", "require_guest_phone_verification", "require_guest_profile_picture", 
                      "requires_license", "review_scores_accuracy", "review_scores_checkin", "review_scores_cleanliness", 
                      "review_scores_communication", "review_scores_location", "review_scores_rating", 
                      "review_scores_value", "reviews_per_month", "scrape_id", "smart_location", "space", 
                      "square_feet", "state", "street", "summary", "thumbnail_url", "transit", 
                      "xl_picture_url", "zipcode"]  
    value = _del_features(value, cols_to_remove)
    return value

def _encoder(value):
    filename = "cat_features_encoding.json"
    with open(filename, 'r') as filename:
        encoding = json.load(filename)
        
    for col in encoding.keys():        
        for i in encoding[col]:
            if value[col] == i:
                value[col] = encoding[col][i]             
        
    return value


def create_encoder(dataset, cat_features):
    """
    This function can create a Label Encoder for categorical features.
    
    A json file called "cat_features_encoding.json" will be saved on folder's script. This file can be used on _encoder function.

    Input
    - dataset (DataFrame, required): The DataFrame loaded from listings.csv.
    - cat_features (list, required): The categorical features list that you want to convert in numeric values.

    Output
    - encoding (dict): A dictionary with the encoder created. The same content of json file.
    """
    encoding = {}
    filename = "cat_features_encoding.json"
    for col in cat_features:
        temp = {}
        n_values = dataset[col].unique()
        i = 0
        for n in n_values:
            temp[str(n)] = i
            i += 1
        encoding[col] = temp
    
    # save json file encoder
    with open(filename, 'w') as filename:
        json.dump(encoding, filename)
        
    return encoding