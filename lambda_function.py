import json
import requests
import os 

# Test Comment

def get_access_token():
    url = "https://login.microsoftonline.com/c8d9148f-9a59-4db3-827d-42ea0c2b6e2e/oauth2/v2.0/token"
    body = {
        'client_id': os.environ['AAD_CLIENT_ID'],
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials',
        'client_secret': os.environ["AAD_CLIENT_SECRET"]
    }
    x = requests.post(url, data=body)
    return x.json()

def get_user_exists(token, email):
    emails = email.split("@")
    netid, domain = emails[0], emails[1]
    formatted = "https://graph.microsoft.com/v1.0/users/{}_illinois.edu%23EXT%23@acmillinois.onmicrosoft.com".format(netid, domain)
    headers = {
        "Authorization": "Bearer " + token,
        "Content-type": "application/json"
    }
    x = requests.get(formatted, headers = headers)
    return (x.status_code == 200)
    

def lambda_handler(event, context):
    email = ""
    try:
        body = event["body"]
        parsedBody = json.loads(body)
        email = parsedBody['data']['object']['customer_details']['email']
    except:
        return {
            "statusCode": 404,
            "body": "No email found."
        }
    url = "https://graph.microsoft.com/v1.0/invitations"
    body = {
        "invitedUserEmailAddress": email,
        "inviteRedirectUrl": "https://acm.illinois.edu"
    }
    token = get_access_token()['access_token']
    if get_user_exists(token, email):
        return {
            'statusCode': 201,
            'body': "User already exists. No need to invite again."
        }
    headers = {
        "Authorization": "Bearer " + token,
        "Content-type": "application/json"
    }
    x = requests.post(url, json = body, headers = headers)
    resp = x.json()
    resp["Status"] = "Done."
    if x.status_code == 201:
        return {
            'statusCode': 200,
            'body': "Done!"
        }
    return {
        'statusCode': x.status_code,
        'body': str(resp)
    }
