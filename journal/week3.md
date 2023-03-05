# Week 3 — Decentralized Authentication
## Creating Cognito user pool
- Log in to your aws cognito console
- go to **Users pool**
- by default 'Cognito user pool' is is selected.
- check 'User name' and 'Email' 
- under 'User name requirements' select 'Allow users to sign in with a preferred user name'
- click 'Next'
- select 'No MFA' and leave the rest at default
- click 'Next'
- select 'name' under the 'Additional required attributes' dropdown under 'Required attributes' and leave the rest at default
- click 'Next' 
- select an email you have verified with Amazon SES
- Click 'Next' 
- Give your user pool a name and select 'Use the Cognito Hosted UI'
- Leave the other settings at default and click to create.
