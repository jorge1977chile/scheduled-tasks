import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

api_key = os.environ.get("OWM")
account_sid = os.environ.get("SID")
auth_token = os.environ.get("TOKEN")
cel = os.environ.get("CEL")

weather_params = {
    "lat":-33.4569,
    "lon":-70.6483,
    "appid" : api_key,
    "cnt":4,
}

response=requests.get(OWM_Endpoint, params=weather_params)
weather_data=response.json()
 
will_rain=False

for hour_data in weather_data["list"]:
    condition_code=hour_data["weather"][0]["id"]
    if int(condition_code)<700:
        will_rain=True


if will_rain==False:

    https_proxy=os.environ.get("https_proxy")
    if https_proxy:
        proxy_client = TwilioHttpClient()
        proxy_client.session.proxies = {'https': https_proxy}
        client = Client(account_sid, auth_token, http_client=proxy_client)
    else:
        client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Vas a tener un día soleado",
        from_="+12706333576",
        to=cel,
    )

    print(message.body
