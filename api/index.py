from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
from api.async_wovi import availableSlots, getJWT, partyIDlookup, locationLookup
import pytz
import asyncio

app = Flask(__name__)

# Route for rendering the home page
@app.route('/')
async def home():
    # Render the index.html template and pass partyIDlookup for dropdown menu
    return render_template('index.html', partyIDlookup=partyIDlookup)

# API endpoint for fetching available slots
@app.route('/api/availability', methods=['POST'])
async def availables():
    # Get JSON data from POST request
    postData = request.json

    # Extract maxDays and locations from JSON data
    maxDays = int(postData.get('days'))
    locations = postData.get('locations')

    # Get JWT token asynchronously
    jwt = await getJWT()

    # Create tasks to fetch available slots for each location asynchronously
    tasks = [availableSlots(jwt, partyIDlookup[location],
                            location, maxDays) for location in locations]

    # Gather results from all tasks asynchronously
    results = await asyncio.gather(*tasks)

    # Return results as JSON response
    return jsonify(results)
