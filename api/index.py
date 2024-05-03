from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
from api.async_wovi import availableSlots, getJWT, partyIDlookup, locationLookup
# from api.wovi import availableSlots, getJWT, partyIDlookup, locationLookup
import pytz
import asyncio

app = Flask(__name__)


@app.route('/')
async def home():
    return render_template('index.html', partyIDlookup=partyIDlookup)


@app.route('/api/availability', methods=['POST'])
async def availables():
    postData = request.json

    maxDays = int(postData.get('days'))
    locations = postData.get('locations')
    jwt = await getJWT()
    # jwt = getJWT()
    tasks = [availableSlots(jwt, partyIDlookup[location],
                            location, maxDays) for location in locations]

    results = await asyncio.gather(*tasks)
    print(results)
    return jsonify(results)

# @app.route('/')
# def home():
#     print(os.listdir())
#     return json.dumps(os.listdir())
#     # return "hello"

# @app.route('/about')
# def about():
#     return 'About'
