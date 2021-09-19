from fastapi import FastAPI
import requests
import gocardless_pro
from datetime import date
import calendar
import os
from dotenv import load_dotenv
import json

load_dotenv()  # take environment variables from .env.

title = "Karma Computing Recuring Revenue"
description = """
View recuring revenue. <small>[Code](https://github.com/KarmaComputing/reccuring-revenue/settings)</small> 🚀

# See also

## Accounts & Cashflow

- [Accounts & Cashflow](https://balance.dokku.karmacomputing.co.uk/docs) ([Code](https://github.com/KarmaComputing/balance))

## Time Invested API

- [Ad-Hoc support](https://time.karmacomputing.co.uk/) ([Code](https://github.com/KarmaComputing/time-api))

"""

app = FastAPI(description=description)


@app.get("/")
def monthly_revenue():

    year = date.today().year
    month = date.today().strftime("%m")
    last_day = calendar.monthrange(year, int(month))[1]

    monthly_revenue = 0

    with open("./endpoints/endpoints.json") as fp:
        endpoints = json.load(fp)
        for endpoint in endpoints:
            url = f"{endpoint['url']}"
            url = eval(f"f'{url}'")
            response = requests.get(url).json()

            if len(endpoint["revenue_key"]) == 1:
                revenue = response[endpoint["revenue_key"][0]]
            else:
                count = 1
                data = response[endpoint["revenue_key"][0]]
                while count < len(endpoint["revenue_key"]):
                    data = data[endpoint["revenue_key"][count]]
                    count += 1
                revenue = data
            if endpoint["times-by-100"]:
                revenue = int(revenue * 100)
            else:
                revenue = int(revenue)
            monthly_revenue += revenue

    # GoCardless revenue
    client = gocardless_pro.Client(
        access_token=os.getenv("GOCARDLESS_ACCESS_TOKEN"),
        environment=os.getenv("GOCARDLESS_ENVIRONMENT"),  # noqa
    )  # noqa

    payouts = client.payouts.list(
        params={
            "limit": 500,
            "created_at[gt]": f"{year}-{month}-01T10:00:00.000Z",
            "created_at[lt]": f"{year}-{month}-{last_day}T10:00:00.000Z",
        }
    ).records
    revenue_gocardless = 0
    for payout in payouts:
        revenue_gocardless += payout.amount

    monthly_revenue = (monthly_revenue + revenue_gocardless) / 100

    result = {"monthly_revenue": monthly_revenue}
    return result
