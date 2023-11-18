# How far can I go (shows how far u can travel from starting airport based on budget.)
# Using Kayaks Flight Search API

import requests
import json
from datetime import date
import requests
from keys import RAPID_API_KEY
import pandas as pd


def getFlightsUnderBudget(budget=1000, starting_airport="ATL", travel_date=date.today()):
    baseurl = "https://sky-scrapper.p.rapidapi.com/api/v1/"
    airportCheckUrl = "flights/searchAirport"
    searchFlightsEverywhereUrl = "flights/searchFlightEverywhere"

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "sky-scrapper.p.rapidapi.com"
    }

    # GET SKYID FOR STARTING AIRPORT
    querystring = {"query": starting_airport}
    airport_response = requests.get(baseurl + airportCheckUrl, headers=headers, params=querystring)
    airports = airport_response.json()["data"]
    skyId = airports[0]["skyId"]
    for airport in airports:
        if airport["skyId"].lower() == starting_airport.lower():
            skyId = airport["skyId"]
            break
    print(skyId)
    
    # Get countries with flights from starting airport under budget
    querystring = {"originSkyId":skyId,"travelDate":travel_date}
    all_flight_countries_response = requests.get(baseurl + searchFlightsEverywhereUrl, headers=headers, params=querystring)
    filteredFlights = []
    for country in all_flight_countries_response.json()["data"]:
        print(country["Meta"])
        if country["Meta"]["Price"] < budget:
            temp = (country["Meta"]["CountryId"], country["Meta"]["CountryNameEnglish"], country["Meta"]["Price"])
            filteredFlights.append(temp)

    # Create dataframe with filtered flights
    df = pd.DataFrame(filteredFlights, columns=["CountryId", "CountryNameEnglish", "Price"])
    print(df)
    return df


getFlightsUnderBudget()
