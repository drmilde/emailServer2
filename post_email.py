from models import Email
import requests


email = Email(
    id = 0,
    name = "Badehose",
    description = "habe ich schon bekommen von Dir.",
    price = 1.23,
    url= "http://www.google.de",
    user= "Jan-Torsten",
    mailtext= "Dies sind ein paar Testmails.",
    #mailaddress = "milde@hs-fulda.de"
    mailaddress = "Claudia.Milde@web.de"
    )

print(email)



url = 'http://localhost:3000/email'
headers = {"Content-Type": "application/json; charset=utf-8"}
for x in range(1,5):
    email.id = x
    response = requests.post(url, headers=headers, json=email.to_json())

print(response.text)
print("Status Code", response.status_code)
print("JSON Response ", response.json() )
