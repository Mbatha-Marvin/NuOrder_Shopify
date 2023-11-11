from pprint import pprint
import pycountry
import json
from geopy.geocoders import Nominatim


# Opening JSON file
with open(
    "/home/mbatha-marvin/Downloads/Documents/WorkProjects/MasterclassGitHub/NuOrder_Shopify/App/Data/NuOrder.json"
) as json_file:
    data = json.load(json_file)


def getBillingAddress(nuouder_data):
    country_details = pycountry.countries.search_fuzzy(
        nuouder_data["billing_address"]["country"]
    )
    city_to_find = nuouder_data["billing_address"]["city"]

    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    city_details = geolocator.geocode(city_to_find)
    print(city_to_find)
    print(city_details.latitude)
    print(city_details.longitude)

    billing_address = {
        "billing_address": {
            "first_name": nuouder_data["retailer"]["retailer_name"].split(" ")[0],
            "address1": nuouder_data["billing_address"]["line_1"],
            "phone": None,
            "city": "Tyler",
            "zip": "75703",
            "province": None,
            "country": country_details[0].name,
            "last_name": nuouder_data["retailer"]["retailer_name"].split(" ")[1],
            "address2": None,
            "company": None,
            "latitude": city_details.latitude,
            "longitude": city_details.longitude,
            "name": nuouder_data["retailer"]["retailer_name"],
            "country_code": country_details[0].alpha_2,
            "province_code": None,
        }
    }
    pprint(billing_address)


getBillingAddress(data)
