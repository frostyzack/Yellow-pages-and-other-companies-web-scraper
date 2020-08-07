import requests
from requests.auth import HTTPBasicAuth
import json

API_KEY = "Your API KEY"
# Scrape Job Listings on Reed.co.uk Job Search API
def reed_api_json(key):
    endpoints = []
    reed_listing_data = []
    keywords = ["Marketing+Director", "App+Developer", "Web+Developer", "Marketing+Analyst", "Marketing+Lead", "Marketing+Executive"]
    for keyword in keywords:
        endpoint = "https://www.reed.co.uk/api/1.0/search?keywords="+keyword+"&location=united+kingdom"
        endpoints.append(endpoint)
        #print(endpoints)
        for endpoint in endpoints:
            response = requests.get(endpoint, auth=(API_KEY, None))
            response = response.text
            json_data = json.loads(response)
        #print(data["totalResults"])
        for result in json_data["results"]:
            reed_listing_data.append(
                {"Name": result["employerName"], "Job Title": result["jobTitle"], "Website": result["jobUrl"]})

    return reed_listing_data

data = reed_api_json(API_KEY)
for item in data:
    print("Listing: " + item["Name"] + " -- " + item["Job Title"] + " -- " + item["Website"])
