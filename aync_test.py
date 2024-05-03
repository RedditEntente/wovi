import asyncio
import time
import requests
import aiohttp

async def main():
    # Create clients for both the library
    aiohttp_client = aiohttp.ClientSession()
    url = url = 'https://www.wovi.com.au/bookings/'

    try:
        # Send 100 asynchronous GET requests using HTTPX
        start_time = time.perf_counter()
        tasks = [requests.get(url) for _ in range(2)]
        end_time = time.perf_counter()
        print(f"Requests: {end_time - start_time:.2f} seconds")

        # Send 100 asynchronous GET requests using AIOHTTP
        start_time = time.perf_counter()
        tasks = [aiohttp_client.get(url) for _ in range(2)]
        await asyncio.gather(*tasks)
        end_time = time.perf_counter()
        print(f"AIOHTTP: {end_time - start_time:.2f} seconds")
    finally:
        # Close client sessions
        await aiohttp_client.close()

asyncio.run(main())