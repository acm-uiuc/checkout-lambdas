# PayPal Azure AD Integration
PayPal-Azure AD integration for user provisioning.

This webhook runs as an AWS Lambda function and invites users to the `acm.illinois.edu` Azure AD tenant when they become a paid member through the site. 

Commits to the `main` branch are automatically deployed to the AWS Lambda function.
