Challenges:
this week, I had to configure and setup github codespace as my gitpod credit has been exhausted.
This week I switched back to using gitpod, but I forgot to uncomment the 'REACT_APP_BACKEND_URL' env variable in the docker compose file, for gitpod instead I was using that of codespace. this was throwing errors until I resolved it.

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
- Press "commandj+shift+P" to open command pallete and type *codespaces* and select, **Manage user secret**
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

## Creating Cognito User Group 
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

# Integration with AWS Amplify
AWS Amplify is a low-code solution SDK for a bunch of serverless application, a frontend JS library and also used to provision backend resources. It a hosting platform. To use the Cognito client-side is by using the Amplify JavaScript library.

## Install the AWS Amplify library
- fronm the **frontend-react-js**, run the command `npm i aws-amplify --save`
- We used '--save' to save it as a dependency because we need it to login in prod. If it was only required during development, we use '--save-dev'

## Hook up Cognito Pool to our app
- copy and paste the command, `import { Amplify } from 'aws-amplify'` into App.js
- configure Amplify by pasting this block of code below the amplify import statement.
```
    Amplify.configure({
    "AWS_PROJECT_REGION": process.env.REACT_APP_AWS_PROJECT_REGION,
    "aws_cognito_identity_pool_id": process.env.REACT_APP_AWS_COGNITO_IDENTITY_POOL_ID,
    "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
    "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
    "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID,
    "oauth": {},
    Auth: {
        // We are not using an Identity Pool
        // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
        region: process.env.REACT_AWS_PROJECT_REGION,           // REQUIRED - Amazon Cognito Region
        userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,         // OPTIONAL - Amazon Cognito User Pool ID
        userPoolWebClientId: process.env.REACT_APP_AWS_USER_POOLS_WEB_CLIENT_ID,   // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
        }
    });
```
- Copy the block below and add them under the ***environment*** section of the **docker-compose.yml** file
```
    REACT_APP_AWS_PROJECT_REGION: "${AWS_DEFAULT_REGION}"
    REACT_APP_AWS_COGNITO_REGION: "${AWS_DEFAULT_REGION}"
    REACT_APP_AWS_USER_POOLS_ID: "${AWS_USER_POOLS_ID}"
    REACT_APP_AWS_CLIENT_ID: "${AWS_APP_CLIENT_ID}"
```
- export each as env variable
```
    export REACT_APP_AWS_PROJECT_REGION="$<YOUR_CHOOSEN_REGION>"
    gp env REACT_APP_AWS_PROJECT_REGION="$<YOUR_CHOOSEN_REGION>"

```
- repeat for each of the variables
- get the **AWS_APP_CLIENT_ID** and **AWS_USER_POOL_ID** from the cognito user group we created

# Conditionally show components based on whether user is logged in or logged out
## Homepage
- import amplify into the **HomeFeedPage.js** `import { Auth } from 'aws-amplify';`
- set a state `const [user, setUser] = React.useState(null);` To be able to manage the users as variables or objects.
- replace the *CheckAuth* function with this block
```
    // check if we are authenicated
    const checkAuth = async () => {
    Auth.currentAuthenticatedUser({
        // Optional, By default is false. 
        // If set to true, this call will send a 
        // request to Cognito to get the latest user data
        bypassCache: false 
    })
    .then((user) => {
        console.log('user',user);
        return Auth.currentAuthenticatedUser()
    }).then((cognito_user) => {
        setUser({
            display_name: cognito_user.attributes.name,
            handle: cognito_user.attributes.preferred_username
        })
    })
    .catch((err) => console.log(err));
    };
```

- replace `import Cookies from 'js-cookie'` in *ProfileInfo.js* with `import { Auth } from 'aws-amplify'`
- replace the *signOut* function block with this:
```
    const signOut = async () => {
        try {
            await Auth.signOut({ global: true });
            window.location.href = "/"
        } catch (error) {
            console.log('error signing out: ', error);
        }
    }
```

## SignIn Page
- open **SigninPage.js** and replace `import Cookies from 'js-cookie'` with `import { Auth } from 'aws-amplify';`
- replace lines 15-26 with this block
```
    const onsubmit = async (event) => {
    setErrors('')
    event.preventDefault(); 
        Auth.signIn(email, password)
        .then(user => {
            localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
            window.location.href = "/"
        })
        .catch(error => {
          if (error.code == 'UserNotConfirmedException') {
          window.location.href = "/confirm"
        }
        setErrors(error.message)
    });
    return false
  }
```
- `do docker-compose up` to try the feature so far.
- click to signin and you should get an error, **'username and password doesn't exist'**
- go to cognito console and create a user manually. choose the old console to see an option not to confirm user.
- we need to use aws cli to force-change password for the created user.
```
    aws cognito-idp admin-set-user-password \
    --user-pool-id <your-user-pool-id> \
    --username <username> \
    --password <password> \
    --permanent
```
- copy the user-pool-id from the console and run the command.
- login with the user you created. 

## Signup Page
- goto the **SignupPage.js** and replace the import line 7 with `import { Auth } from 'aws-amplify';`
- replace lines 18-29 with the code in it. Replace all ni **setCognitoErrors** with `setErrors`

## Setup Confirmation Page
- replace line 7 with `import { Auth } from 'aws-amplify';`
- replace lines 23-53 with 
```
    const resend_code = async (event) => {
        setErrors('')
        try {
        await Auth.resendSignUp(email);
        console.log('code resent successfully');
        setCodeSent(true)
        } catch (err) {
        // does not return a code
        // does cognito always return english
        // for this to be an okay match?
        console.log(err)
        if (err.message == 'Username cannot be empty'){
            setCognitoErrors("You need to provide an email in order to send Resend Activiation Code")   
        } else if (err.message == "Username/client id combination not found."){
            setCognitoErrors("Email is invalid or cannot be found.")   
        }
        }
    }

    const onsubmit = async (event) => {
        event.preventDefault();
        setErrors('')
        try {
        await Auth.confirmSignUp(email, code);
        window.location.href = "/"
        } catch (error) {
        setErrors(error.message)
        }
        return false
    }

    let el_errors;
    if (errors){
        el_errors = <div className='errors'>{errors}</div>;
    }
```
- Re-build docker and go to the signup page to comfirm your implementation

## Recovery page
This page is handles a case of a user forgeting his/her password
- open **RecoverPage.js** 
- paste this import statement `import { Auth } from 'aws-amplify';`
- next is this block of code which have been replaced
```
    const onsubmit_send_code = async (event) => {
        event.preventDefault();
        setErrors('')
        Auth.forgotPassword(username)
        .then((data) => setFormState('confirm_code') )
        .catch((err) => setErrors(err.message) );
        return false
    }
    const onsubmit_confirm_code = async (event) => {
        event.preventDefault();
        setErrors('')
        if (password == passwordAgain){
        Auth.forgotPasswordSubmit(username, code, password)
        .then((data) => setFormState('success'))
        .catch((err) => setErrors(err.message) );
        } else {
        setErrors('Passwords do not match')
        }
        return false
    }
  ```

  # Cognito JWT Server side Authorization
  In the **SigninPage.js**, we saved *authorization token in our local storage. See the block of code below.
  ```
        Auth.signIn(email, password)
        .then(user => {
            localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
            window.location.href = "/"
        })
  ```
- To protect our api endpoint, we need to request for this token from the user making the api call.
- Our homepage endpoint is in line 23 in the *HomeFeedPage.js*
  `const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/home``
- copy this header block and add to the **`const loadData`** block(lines 21-36) of the *HomeFeedPage.js* file. 
```headers: {
    Authorization: `Bearer ${localStorage.getItem("access_token")}`
  }
```
- update your cors to allow header by copying this block to replace lines 95-101
```
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'], 
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)
```
## Reading the authorization token in backend (flask)
- In your **app.py** do `from flask import request`
- copy `print(request.headers.get('Authorization'))` and paste in the **def data_home()** block of the **app.py** file. Or use,
```
import sys

app.logger.debug(
    request.headers.get('Authorization')
)
``` to verify that it's being passed to the backend. However remove the block of code because you don't want people to have access to it.
