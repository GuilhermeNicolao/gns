import requests
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost"
AUTHORIZATION_CODE = ""

# Se sua conta for Brasil use:
# TOKEN_URL = "https://accounts.zoho.com.br/oauth/v2/token"

TOKEN_URL = "https://accounts.zoho.com/oauth/v2/token"

# 🚀 REQUISIÇÃO

payload = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "code": AUTHORIZATION_CODE
}

response = requests.post(TOKEN_URL, data=payload)

# 📋 RESULTADO

if response.status_code == 200:
    data = response.json()
    print("\n✅ Sucesso!\n")
    print("Access Token:")
    print(data.get("access_token"))
    print("\nRefresh Token (GUARDE ESSE!):")
    print(data.get("refresh_token"))
    print("\nExpira em:", data.get("expires_in"), "segundos")
else:
    print("\n❌ Erro:")
    print(response.status_code)
    print(response.text)