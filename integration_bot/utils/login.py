import os
import requests

def login() -> str:
  api_url:str = "https://integration.utt.fr/api/auth/login"
  payload:dict = {"email": os.getenv('BOT_WEBSITE_EMAIL'), "password": os.getenv('BOT_WEBSITE_PASSWORD')}
  response = requests.post(api_url, json=payload, verify=False)
  if response.status_code == 200:
    return response.json().get('data', {}).get('token', '')
  else:
    raise Exception(f"Login failed with status code {response.status_code}: {response.text}")