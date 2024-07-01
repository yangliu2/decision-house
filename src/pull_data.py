""" Get house data from Zillow using rapidapi """
# https://rapidapi.com/developer/dashboard
# https://rapidapi.com/s.mahmoud97/api/zillow56/playground/

import requests
import requests_cache
from typing import Dict
import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


def search_house(location: str) -> Dict:
	"""Initial search using zipcode as the location

	:param location: zipcode location
	:type location: str
	:return: result json as dictionary
	:rtype: Dict
	"""	
	time.sleep(1)

	url = os.getenv("RAPIDAPI_SEARCH_URL")

	querystring = {"location": location,
					"output": "json",
					"status": "forSale",
					"sortSelection": "priorityscore",
					"listing_type": "by_agent",
					"doz": "any"}

	headers = {
		"x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
		"x-rapidapi-host": os.getenv("RAPIDAPI_HOST")
	}

	session = requests_cache.CachedSession("data/request_cache",
											expire_after=3600)

	response = session.get(url, headers=headers, params=querystring)

	response_dict = response.json()

	return response_dict


def get_detail(zpid: str) -> Dict:
	""" Get detailed data using zpid

	:param zpid: zillow zpid
	:type zpid: str
	:return: detailed house info in json dictionary
	:rtype: Dict
	"""
	time.sleep(1)

	url = os.getenv("RAPIDAPI_PROPERTY_URL")

	querystring = {"zpid": zpid}

	headers = {
		"x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
		"x-rapidapi-host": os.getenv("RAPIDAPI_HOST")
	}

	session = requests_cache.CachedSession("data/request_cache",
											expire_after=None)

	response = session.get(url, headers=headers, params=querystring)

	response_dict = response.json()

	return response_dict


def main():

    output = Path("data/search_response.json")
    
    zipcode = "78750"
    response_dict = search_house(location=zipcode)
    
    # zpid = 29372295
    # response_dict = get_detail(zpid=zpid)
    
    with output.open("w", encoding="utf8") as file:
        json.dump(response_dict, file)


if __name__ == "__main__":
    main()
