# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2NzUxODA2LCJpYXQiOjE2ODY3NDgyMDYsImp0aSI6IjIyNDhmZmQzNmU1MDQ0NDliYWIzYzUyNjViZTk1NmM4IiwidXNlcl9pZCI6MX0.dTMtK8fGxGYPkkoE9AORJzDlaZzDATtbD9TOvniPRhA
import requests
import json

url = "http://127.0.0.1:8000/api/addcontact/"

payload = json.dumps({
  "name": "abcd",
  "phone_number": "12334"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2NzUxODA2LCJpYXQiOjE2ODY3NDgyMDYsImp0aSI6IjIyNDhmZmQzNmU1MDQ0NDliYWIzYzUyNjViZTk1NmM4IiwidXNlcl9pZCI6MX0.dTMtK8fGxGYPkkoE9AORJzDlaZzDATtbD9TOvniPRhA'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
