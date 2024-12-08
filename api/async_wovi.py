import logging
import pytz
import time
import json
import aiohttp
import asyncio
import requests
from datetime import datetime

# Dictionary to map party IDs to locations
partyIDlookup = {'Beenleigh': 72491, 'Beenleigh (Hail Damage)': 93625, 'Brisbane': 72492, 'Brisbane (Hail Damage)': 73693, 'Bundaberg': 72493, 'Cairns': 72494,
                 'Gold Coast': 72495, 'Gold Coast (Hail Damage)': 93626, 'Mackay': 72496, 'Rockhampton': 72497, 'Sunshine Coast': 72498, 'Toowoomba': 72499, 'Townsville': 72500}

# Reverse dictionary to map party IDs to locations
locationLookup = {partyIDlookup[key]: key for key in partyIDlookup}

# Configure logging
logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", datefmt='%d/%m/%Y %H:%M:%S',
                    level=logging.DEBUG, handlers=[logging.StreamHandler()])

# Function to asynchronously retrieve JWT
async def getJWT():
    jwt = ""
    url = 'https://www.wovi.com.au/bookings/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                html = await response.text()

                # Extract JWT token from HTML response
                jwt = html.split("INIT.TOKEN='")[1].split("'")[0]
                logging.info("JWT successfully found")
                # logging.info(f"JWT : {jwt}")
            except:
                logging.info("JWT couldn't be found")

            return jwt

# Function to validate JWT
def validateJWT(jwt):

    headers = {
        'Authorization': f'Bearer {jwt}',
    }

    params = {
        'includeAvailable': 'true',
        'includeBooked': 'true',
        'includeCancelled': 'true',
        'includePending': 'true',
        'includeQuery': 'true',
        'startDate': '2024-05-06T15:38:54',
    }

    response = requests.get(
        'https://api.dealersolutions.com.au/QIS/Locations/72492/BookingSlotsCountByDate',
        params=params,
        headers=headers,
    )

    # Check if response text is empty to determine validity of JWT
    if len(response.text) == 0:
        return "invalid"
    else:
        return "valid"

# Function to map location names to their party IDs
def locationID():
    data = [{"AddressLine1": "Unit 2 18 Spanns Road ", "AddressLine2": "Beenleigh Queensland 4207 ", "BookingSlotType": 0, "BuildingName": 0, "ClientNo": 20941, "DisplayName": "Beenleigh", "EmailAddress": "adminqis@wovi.com.au", "GoogleLocation": "2/18 Spanns Rd, Beenleigh QLD 4207, Australia", "HasAvailableBookingSlots": 1, "Latitude": -27.71272659, "Longitude": 153.18797300, "Name": "Queensland Inspection Services - Beenleigh", "PartyID": 72491, "PhoneNumber": "1300 722 411", "Suburb": "Beenleigh"}, {"AddressLine1": "Unit 2 18 Spanns Road ", "AddressLine2": "Beenleigh Queensland 4207 ", "BookingSlotType": 0, "BuildingName": 0, "ClientNo": 29979, "DisplayName": "Beenleigh - HAIL ONLY", "EmailAddress": "adminqis@wovi.com.au", "GoogleLocation": "2/18 Spanns Rd, Beenleigh QLD 4207, Australia", "HasAvailableBookingSlots": 0, "Latitude": -27.71270180, "Longitude": 153.18791200, "Name": "Queensland Inspection Services - Beenleigh (Hail Damage)", "PartyID": 93625, "PhoneNumber": "1300 722 411", "Suburb": "Beenleigh"}, {"AddressLine1": "110 Lamington Avenue ", "AddressLine2": "Eagle Farm Queensland 4009 ", "BookingSlotType": 1, "BuildingName": "Manheim", "ClientNo": 20942, "DisplayName": "Brisbane", "EmailAddress": "adminqis@wovi.com.au", "GoogleLocation": "110 Lamington Ave, Eagle Farm QLD 4009, Australia", "HasAvailableBookingSlots": 1, "Latitude": -27.42882538, "Longitude": 153.08181760, "Name": "Queensland Inspection Services - Brisbane", "PartyID": 72492, "PhoneNumber": "1300 722 411", "Suburb": "Eagle Farm"}, {"AddressLine1": "110 Lamington Avenue ", "AddressLine2": "Eagle Farm Queensland 4009 ", "BookingSlotType": 1, "BuildingName": 0, "ClientNo": 21450, "DisplayName": "Brisbane - HAIL ONLY", "EmailAddress": "adminqis@wovi.com.au", "GoogleLocation": "110 Lamington Ave, Eagle Farm QLD 4009, Australia", "HasAvailableBookingSlots": 0, "Latitude": -27.42835808, "Longitude": 153.08236690, "Name": "Queensland Inspection Services - Brisbane (Hail Damage)", "PartyID": 73693, "PhoneNumber": "1300 722 411", "Suburb": "Eagle Farm"}, {"AddressLine1": "Unit 1 52 Enterprise Street ", "AddressLine2": "Bundaberg Queensland 4670 ", "BookingSlotType": 2, "BuildingName": 0, "ClientNo": 20943, "DisplayName": "Bundaberg", "EmailAddress": "adminqis@wovi.com.au", "GoogleLocation": "1/52 Enterprise St, Svensson Heights QLD 4670, Australia", "HasAvailableBookingSlots": 0, "Latitude": -24.88859940, "Longitude": 152.33004760, "Name": "Queensland Inspection Services - Bundaberg", "PartyID": 72493, "PhoneNumber": "1300 722 411", "Suburb": "Bundaberg"}, {"AddressLine1": "Unit 4 261 McCormack Street ", "AddressLine2": "Manunda Queensland 4870 ", "BookingSlotType": 2, "BuildingName": 0, "ClientNo": 20944, "DisplayName": "Cairns", "EmailAddress": "adminqis@wovi.com.au", "GoogleLocation": "4/261 McCormack St, Manunda QLD 4870, Australia", "HasAvailableBookingSlots": 1, "Latitude": -16.91494751, "Longitude": 145.74478150, "Name": "Queensland Inspection Services - Cairns", "PartyID": 72494, "PhoneNumber": "1300 722 411", "Suburb": "Manunda"}, {"AddressLine1": "Unit 10 52-54 Township Drive ", "AddressLine2": "Burleigh Heads Queensland 4220 ", "BookingSlotType": 0, "BuildingName": 0, "ClientNo": 20945, "DisplayName": "Burleigh Heads", "EmailAddress": "adminqis@wovi.com.au", "GoogleLocation": "10/52-54 Township Dr, Burleigh Heads QLD 4220, Australia", "HasAvailableBookingSlots": 1, "Latitude": -28.11281395, "Longitude": 153.43267820, "Name": "Queensland Inspection Services - Gold Coast", "PartyID": 72495, "PhoneNumber": "1300 722 411", "Suburb": "Burleigh Heads"}, {
        "AddressLine1": "Unit 10 52-54 Township Drive ", "AddressLine2": "Burleigh Heads Queensland 4220 ", "BookingSlotType": 0, "BuildingName": 0, "ClientNo": 29980, "DisplayName": "Burleigh Heads - HAIL ONLY", "EmailAddress": "adminqis@wovi.com.au", "GoogleLocation": "52/54 Township Dr, Burleigh Heads QLD 4220, Australia", "HasAvailableBookingSlots": 0, "Latitude": -28.11305809, "Longitude": 153.43284610, "Name": "Queensland Inspection Services - Gold Coast (Hail Damage)", "PartyID": 93626, "PhoneNumber": "1300 722 411", "Suburb": "Burleigh Heads"}, {"AddressLine1": "74 Gordon Street ", "AddressLine2": "Mackay Queensland 4740 ", "BookingSlotType": 0, "BuildingName": "GOODYEAR", "ClientNo": 20946, "DisplayName": "Mackay", "EmailAddress": "adminqis@wovi.com.au", "GoogleLocation": "74 Gordon St, Mackay QLD 4740, Australia", "HasAvailableBookingSlots": 0, "Latitude": -21.14207458, "Longitude": 149.17886350, "Name": "Queensland Inspection Services - Mackay", "PartyID": 72496, "PhoneNumber": "1300 722 411", "Suburb": "Mackay"}, {"AddressLine1": "17 Derby Street ", "AddressLine2": "Rockhampton City Queensland 4700 ", "BookingSlotType": 2, "BuildingName": 0, "ClientNo": 20947, "DisplayName": "Rockhampton City", "EmailAddress": "adminqis@wovi.com.au", "GoogleLocation": "17 Derby St, Rockhampton City QLD 4700, Australia", "HasAvailableBookingSlots": 0, "Latitude": -23.38359642, "Longitude": 150.51347350, "Name": "Queensland Inspection Services - Rockhampton", "PartyID": 72497, "PhoneNumber": "1300 722 411", "Suburb": "Rockhampton City"}, {"AddressLine1": "Unit 4 33 Enterprise Street ", "AddressLine2": "Kunda Park Queensland 4556 ", "BookingSlotType": 2, "BuildingName": 0, "ClientNo": 20948, "DisplayName": "Sunshine Coast", "EmailAddress": "adminqis@wovi.com.au", "GoogleLocation": "4/33 Enterprise St, Kunda Park QLD 4556, Australia", "HasAvailableBookingSlots": 1, "Latitude": -26.66751480, "Longitude": 153.02972410, "Name": "Queensland Inspection Services - Sunshine Coast", "PartyID": 72498, "PhoneNumber": "1300 722 411", "Suburb": "Kunda Park"}, {"AddressLine1": "Unit 9 11-15 Gardner Court ", "AddressLine2": "Toowoomba Queensland 4350 ", "BookingSlotType": 2, "BuildingName": 0, "ClientNo": 20949, "DisplayName": "Toowoomba", "EmailAddress": "adminqis@wovi.com.au", "GoogleLocation": "9/11-15 Gardner Ct, Wilsonton QLD 4350, Australia", "HasAvailableBookingSlots": 1, "Latitude": -27.54732704, "Longitude": 151.90476990, "Name": "Queensland Inspection Services - Toowoomba", "PartyID": 72499, "PhoneNumber": "1300 722 411", "Suburb": "Toowoomba"}, {"AddressLine1": "647-651 Ingham Road ", "AddressLine2": "Bohle Queensland 4818 ", "BookingSlotType": 2, "BuildingName": 0, "ClientNo": 20950, "DisplayName": "Townsville", "EmailAddress": "adminqis@wovi.com.au", "GoogleLocation": "647-651 Ingham Rd, Mount St John QLD 4818, Australia", "HasAvailableBookingSlots": 1, "Latitude": -19.26039505, "Longitude": 146.73892210, "Name": "Queensland Inspection Services - Townsville", "PartyID": 72500, "PhoneNumber": "1300 722 411", "Suburb": "Bohle"}]
    locationID = {}

    # Iterate over data to create a mapping of location names to their party IDs
    for record in data:
        locationID[record["Name"].split("- ")[-1]] = record["PartyID"]
    return locationID

# Function to asynchronously fetch available slots
async def availableSlots(jwt, partyID, location, maxDays):
    headers = {
        'Authorization': f'Bearer {jwt}',
    }

    params = {
        'includeAvailable': 'true',
        'includeBooked': 'true',
        'includeCancelled': 'true',
        'includePending': 'true',
        'includeQuery': 'true',
        'startDate': datetime.now(pytz.timezone('Australia/Brisbane')).isoformat().split('.')[0],
    }

    today = datetime.strptime(datetime.now(pytz.timezone(
        'Australia/Brisbane')).strftime('%Y-%m-%d'), '%Y-%m-%d')

    availableDates = []
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.dealersolutions.com.au/QIS/Locations/{partyID}/BookingSlotsCountByDate', params=params,
                               headers=headers) as response:
            jsonData = await response.text()

            # Extract available dates from JSON response within the specified range
            availableDates = [date["Date"].split("T")[0] for date in json.loads(jsonData) if (
                date["Available"] != 0 and (2 < (datetime.strptime(date["Date"], '%Y-%m-%dT%H:%M:%S') - today).days <= maxDays))]
            
    # Log available slots for the location within the next maxDays days
    logging.info(
        f'Avaiable slots for {locationLookup[partyID]} ({partyID}) within the next {maxDays} days is {availableDates} ')

    return {"availableSlots": availableDates, "timeFetched": datetime.now(pytz.timezone('Australia/Brisbane')).strftime('%Y-%m-%d %H:%M:%S'),  "location": location}

# Main block of code that will be executed when the script is run directly
if __name__ == "__main__":
    # Constant defining the time interval for refreshing data (in seconds)
    REFRESH_TIME = 60
    # Maximum number of days to look ahead for available slots
    MAX_DAYS = 100
    # Location for which slots will be checked
    LOCATION = 'Brisbane'

    # Infinite loop to continuously fetch available slots
    while (True):
        # Asynchronously fetches a JSON Web Token (jwt) for authentication
        jwt = asyncio.run(getJWT())

        # Asynchronously fetches available slots using the obtained jwt, party ID for the specified location,
        # location name, and maximum number of days to look ahead
        results = asyncio.run(availableSlots(jwt, partyIDlookup[LOCATION], LOCATION, MAX_DAYS))

        # Pauses the execution for the specified refresh time before fetching slots 
        time.sleep(REFRESH_TIME)

