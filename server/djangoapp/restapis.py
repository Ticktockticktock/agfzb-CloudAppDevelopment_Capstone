import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def get_request(url, **kwargs): 
    try:
        # Call get method of requests library with URL and parameters
        if kwargs.get("api_key"):
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=params, 
                                    auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)

    # print(response)
    
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], 
                                   full_name=dealer["full_name"], id=dealer["id"], 
                                   lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])

            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
    # - Parse JSON results into a DealerReview object list
    results = []

    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    print(json_result)

    if json_result.get("result"):
        # Get the row list in JSON as dealers
        dealers = json_result["result"]

        for dealer in dealers:
            dealer_obj = DealerReview(dealership=dealer["dealership"], name=dealer["name"], 
                        purchase=dealer["purchase"], review=dealer["review"])

            if "purchase_date" in dealer:
                dealer_obj.purchase_date = dealer["purchase_date"]
            if "car_make" in dealer:
                dealer_obj.car_make = dealer["car_make"]
            if "car_model" in dealer:
                dealer_obj.car_model = dealer["car_model"]
            if "car_year" in dealer:
                dealer_obj.car_year = dealer["car_year"]

            try:
                # print("dealer being analized: {}".format(dealer_obj.name))
                temp_sent = analyze_review_sentiments(dealer_obj.review)
                dealer_obj.sentiment = temp_sent
            except:
                dealer_obj.sentiment = "Neutral"

            results.append(dealer_obj)
        
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/170a6796-7450-4f40-90b4-d41037b83eec'
    api_key="e4l7K99G8t-oJ7c0hN0OQUzAuBjmD_hBnlJnIQgpaPiZ" 

    authenticator = IAMAuthenticator(api_key) 

    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 

    natural_language_understanding.set_service_url(url) 

    response = natural_language_understanding.analyze( 
                            text=dealerreview ,
                            features=Features(sentiment=SentimentOptions(
                                        targets=[dealerreview]))).get_result() 

    label=json.dumps(response, indent=2) 
    # print("anlysys response: {}".format(label))
    label = response['sentiment']['document']['label'] 

    return(label) 




