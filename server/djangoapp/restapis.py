import requests
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/7b954983-308f-4ffd-a67c-79bd753f6e83"
api_key = "COUZ50Z10XAzLQi_aZsOF5bcAtjjqWj6MpiVpOok8reA"
authenticator = IAMAuthenticator(api_key)
natural_language_understanding = NaturalLanguageUnderstandingV1(
                        version='2021-08-01', authenticator=authenticator)
natural_language_understanding.set_service_url(url)
            
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if 'params' in kwargs:
            # Call get method of requests library with URL and parameters
            response = natural_language_understanding.analyze(language='en', features=Features(keywords=KeywordsOptions(sentiment=True,limit=1)), return_analyzed_text = True, text=kwargs["params"]["text"])
            status_code = response.get_status_code()
            print("With status {} ".format(status_code))
            print(response.get_result())
            if response.get_result().get('keywords'):
                json_data = response.get_result().get('keywords')[0].get('sentiment').get('label')
                print("INPUT TEXT: ", kwargs["params"]["text"])
                print("JSON DATA: ", json_data)
            else:
                json_data = ""
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
            status_code = response.status_code
            print("With status {} ".format(status_code))
            json_data = json.loads(response.text)
    
    except Exception as e:
        # If any error occurs
        print("Network exception occurred: ", e.message)
    print(json_data)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf (url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]["data"]["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            print("REVIEW TO BE SENT FOR NLU:", dealer_doc["review"])
            # Create a CarDealer object with values in `doc` object
            dealer_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"], purchase=dealer_doc["purchase"],
                                   review=dealer_doc["review"], purchase_date=dealer_doc["purchase_date"], car_make=dealer_doc["car_make"],
                                   car_model=dealer_doc["car_model"],
                                   car_year=dealer_doc["car_year"], sentiment=analyze_review_sentiments(dealer_doc["review"]),
                                   id=dealer_doc["id"])
            results.append(dealer_obj)
    return results

def get_dealers_by_state_from_cf(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    params = dict()
    params["text"] = dealerreview
    params["version"] = "2021-03-25"
    params["features"] = "sentiment"
    params["return_analyzed_text"] = True
    #url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/7b954983-308f-4ffd-a67c-79bd753f6e83"
    url='www.ibm.com'
    json_result = get_request(url, api_key=api_key, params=params)
    return json_result

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print(json_payload)
    print("POST to {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        status_code = response.status_code
        print(response.text)
        print("With status {} ".format(status_code))
    except:
        # If any error occurs
        print("Network exception occurred")

