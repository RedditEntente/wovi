# Wovi Booking Monitor

The Wovi Booking Monitor is a Python-based web scraping tool designed to provide users with real-time updates on available slots for bookings on the Wovi platform. Leveraging the power of web scraping, this tool offers users the convenience of monitoring booking availability within a specified timeframe, eliminating the need for manual checking and ensuring timely booking opportunities.

## Demo

https://flask-python-template.vercel.app/

## How it Works

This example uses the Web Server Gateway Interface (WSGI) with Flask to enable handling requests on Vercel with Serverless Functions.

## Running Locally using Gunicorn

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
