# ACM @ UIUC Lambda Functions

This monorepo houses the Lambda functions that enable membership signup and user provisioning.

`aad-enroll.py` runs as an AWS Lambda function and invites users to the `acm.illinois.edu` Azure AD tenant when they become a paid member through the site. 

`aad-enroll` uses the custom Stripe Lambda layer to provide integration with Stripe and verify Stripe tokens.

`stripe-checkout.py` runs as an AWS Lambda function and generates Stripe checkout sessions for the membership signup flow. 

Commits to the `main` branch are automatically deployed to the respective AWS Lambda function.
