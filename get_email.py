from models import Email
import requests


email = Email(
    id = 0,
    name = "das ding",
    description = "die beschreibung",
    price = 10.01,
    url= "http://www.google.de",
    user= "ich",
    mailtext= "Der text der email",
    mailaddress = "milde@hs-fulda.de"
    )

print(email)



url = 'http://localhost:3000/email'
headers = {"Content-Type": "application/json; charset=utf-8"}
response = requests.get(url)

print(response.text)
print("Status Code", response.status_code)
print("JSON Response ", response.json() )
