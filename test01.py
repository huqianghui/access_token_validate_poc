import requests
import jwt
import requests

def get_token(client_id, client_secret, tenant_id):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "api://XXXX/.default"}

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return None

client_id = ""
client_secret = ""
tenant_id = ""

token = get_token(client_id, client_secret, tenant_id)
print(token)

# Decode the token without verification
payload = jwt.decode(token,options={"verify_signature": True})

# Print the payload
print(payload)

from aad_token_verify import get_verified_payload

payload = get_verified_payload(token, 
                               tenant_id=tenant_id, 
                               audience_uris=["cd5347aa-d60d-49f7-9877-e036b25c9f94"])

