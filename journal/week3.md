Challenges:
this week I had to configure and setup github code space as my gitpod credit has been exhausted.
## Setup and configure guthub codespace to install aws cli
- open your repository
- click on 'code' then 'codespace' tab and click on the '+' icon to launch new codespace.
- In the codespace, goto command pallet (cmd + shift + P)
- select 'Codespace: Add Devcontainer... -> create new config -> backend...
- check AWS CLI and click 'OK'
- after creation, delete **docker-compose.yml** file in the ***.devcontainer*** directory.
- copy the contents of the ***devcontainer.json*** file into the new file created.
- go to the command pallete, type rebuild and select to rebuild codespace.
- after rebuid this will install the the packages including aws cli

## Setup AWS Credentials
- Press "commandj+shift+P" to open command pallete and type *codespaces* and select, **Manage user secrete**
- Select **Manage on Github** -> New secret
- provide the credentials and specify a repository to link to aws.
- Save and rebuild codespace.
- copy this code block and paste in the ***devcontainer.json*** file and rebuild
```
    "remoteEnv": {
            "AWS_CLI_AUTO_PROMPT": "on-partial"
        },
```
- cd into the ***frontend-react-js** and run `npm install`
- run `docker compose up` from the root directory
- the frontend will be unable to communicate with the backend because we still have gitpod config in the **docker-compose.yml** file
- copy the following block of code and past into the file and comment that of the gitpod out.
```
    FRONTEND_URL: "https://${CODESPACE_NAME}-3000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
    BACKEND_URL: "https://${CODESPACE_NAME}-4567.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
    REACT_APP_BACKEND_URL: "https://${CODESPACE_NAME}-4567.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
```


# Week 3 — Decentralized Authentication
Authentication is establishing that you are who you say you are.

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
