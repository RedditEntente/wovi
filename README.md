# Wovi Booking Monitor

The Wovi Booking Monitor is a Python-based web scraping tool designed to provide users with real-time updates on available slots for bookings on the Wovi platform. Leveraging the power of web scraping, this tool offers users the convenience of monitoring booking availability within a specified timeframe, eliminating the need for manual checking and ensuring timely booking opportunities.

## Demo

https://wovi.vercel.app

## How it Works

This example uses the Web Server Gateway Interface (WSGI) with Flask to enable handling requests on Vercel with Serverless Functions.

## Running Locally using Poetry & Gunicorn

```bash
poetry install
poetry run gunicorn -b localhost:3000 api.index:app
```

## Export dependencies to a requirements.txt file

```
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

## Running Locally to test Vercel Deployment

```bash
npm i -g vercel
vercel dev
```

Your Flask application is now available at `http://localhost:3000`.

## Directory Structure
    .
    ├── api
    │   ├── static
    │   │   └── custom.css
    │   ├── templates
    │   │   └── index.html
    │   ├── async_wovi.py
    │   └── index.py
    ├── static
    │   └── custom.css
    ├── aync_test.py
    ├── poetry.lock
    ├── pyproject.toml
    ├── requirements.txt
    └── vercel.json

## Running async_wovi.py Directly to Output to Terminal

Before running the Python script, configure the refresh time, location, and maximum number of days within the main block of async_wovi.py:

```python
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

        # Pauses the execution for the specified refresh time before fetching slots again
        time.sleep(REFRESH_TIME)
```

To run the script and output the results to the terminal, use the following commands:

```bash
pip install -r requirements.txt
python api/async_wovi.py 
```

