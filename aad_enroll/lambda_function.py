import json
import requests
import os 
import stripe

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
    secret = os.environ['ENDPOINT_SECRET']
    try:
        if event["queryStringParameters"]["test"]:
            print("Using test key")
            secret = os.environ['TEST_ENDPOINT_SECRET']
    except:
        secret = os.environ['ENDPOINT_SECRET']
    try:
        body = event["body"]
        stripeEvent = stripe.Webhook.construct_event(body, event['headers']['stripe-signature'], secret)
    except Exception as e:
        print("Exception: ", e)
        return {
            'statusCode': 421,
            'body': "Invalid Payload."
        }
    if
    try:
        parsedBody = json.loads(body)
        cancel_url = parsedBody['data']['object']['cancel_url']
        success_url = 
        if cancel_url != "https://acm.illinois.edu/#/membership" || success_url != "https://acm.illinois.edu/#/paid":
            return {
                "statusCode": 200,
                "body": "Not a subscription event."
            }
        email = parsedBody['data']['object']['customer_details']['email']
        print("Inviting: ", email)
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
        print("Email already exists, not inviting: ", email)
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
        print("Invited : ", email)
        return {
            'statusCode': 200,
            'body': "Done!"
        }
    else:
        print("Error ", x.status_code, "inviting: ", email, " ", json.dumps(resp))
    return {
        'statusCode': x.status_code,
        'body': str(resp)
    }
