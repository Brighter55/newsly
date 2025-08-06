# NEWSLY
Welcome to my first real, deployed, full-stack project.

I'm the kind of person who struggles to keep up with our constantly changing world. There’s just so much happening every day, and it takes so much time to grasp all the information from just typically reading news.

So I created NEWSLY — a website that asks for your email and sends you daily, AI-summarized news straight to your inbox.

You can check it out [here!](https://www.new-sly.com/)

# Demo

I've also created an under-1-minute demo video to demonstrate how NEWSLY works. Click the image!

<a href="https://www.youtube.com/watch?v=LoZgC0YxILY"><img width="1100" alt="newsly website" src="https://i.imgur.com/LdGDFE2.png"></a>

# Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [How it Works](#how-it-works)
- [License](#license)

# Features
- User will get a daily email containing summarized-news classified by categories the user has chosen.
- User will get a sql database table containing Users' email address and categories in which they picked.
- User will get a noSQL database collection containing news summaries, summarized from **OpenAI**.
- User will get an "index.html" webpage that works on getting users' email and categories needed for latter procedures.
- User will get auto-generated "full_summary.html" webpages that display the summary of each news article.
- User will get responsive webpages that work on most devices.

# Installation
- Set up locally
    1. Clone the repository and install the dependencies

        ````bash
        git clone https://github.com/Brighter55/newsly.git
        cd newsly
        pip install -r requirements.txt
        ````
    2. Change .env file to yours (You will need to upload this to the deployment service)
        ````bash
        code .env
        ````
        Your .env should look like this (To get these API keys/token, you will have to sign up/host the services)
        ````bash
        POSTGRESDB_URI = "postgresql://[username]:[password]@localhost:5432/[database_name]"
        MONGODB_URI = "mongodb://localhost:27017/"
        THENEWSAPI_TOKEN = "..."  # thenewsapi.com will provide API token for you
        OPENAI_API_KEY = "..."  # OPENAI will provide API key for you
        MAILTRAP_TOKEN = "Bearer ..."  # MAILTRAP will provide token for you
        ````
    3. Adjust fetch_and_send.py to your domain
        ````bash
        url = "https://bulk.api.mailtrap.io/api/send"
        for user in users:
            html_body = ""
            for category in user["categories"]:
                for bodies_category in html_bodies_data:
                    if category == bodies_category:
                        for body in html_bodies_data[category]:
                            html_body = html_body + body
            html_message = create_html_message(html_body, user["categories"], utc_yesterday)
            payload = {
                "from": {
                    "email": "noreply@new-sly.com",  # Change
                    "name": "Newsly Summarizer AI",
                },
                "to": [
                    {
                        "email": user["email"],
                    }
                ],
                "subject": f"Your Newsly for {utc_yesterday}",
                "html": html_message,
                "category": "Summaries",
            }
            headers = {
                "Authorization": os.getenv("MAILTRAP_TOKEN"),
                "Content-Type": "application/json"
            }
            requests.request("POST", url, headers=headers, json=payload)

        ````
    4. To run the webpages, navigate to register_and_summary/
        ```bash
        cd register_and_summary
        python app.py
        ````

    5. To manually send email to users, navigate to daily_task/
        ````bash
        cd ..  # if you are in register_and_summary/
        cd daily_task
        python fetch_and_send.py
        ````

- Set up Online
    1. Clone the repository

        ````bash
        git clone https://github.com/Brighter55/newsly.git
        cd newsly
        ````
    2. Change .env file to yours (You will need to upload this to the deployment service)
        ````bash
        code .env
        ````
        Your .env should look like this (To get these API keys/token, you will have to sign up/host the services)
        ````bash
        POSTGRESDB_URI = "..."  # Your hosted platform will provide connection string for you
        MONGODB_URI = "..."  # Your hosted platform will provide connection string for you
        THENEWSAPI_TOKEN = "..."  # thenewsapi.com will provide API token for you
        OPENAI_API_KEY = "..."  # OPENAI will provide API key for you
        MAILTRAP_TOKEN = "Bearer ..."  # MAILTRAP will provide token for you
        ````
    3. Adjust fetch_and_send.py to your domain
        ````bash
        url = "https://bulk.api.mailtrap.io/api/send"
        for user in users:
            html_body = ""
            for category in user["categories"]:
                for bodies_category in html_bodies_data:
                    if category == bodies_category:
                        for body in html_bodies_data[category]:
                            html_body = html_body + body
            html_message = create_html_message(html_body, user["categories"], utc_yesterday)
            payload = {
                "from": {
                    "email": "noreply@new-sly.com",  # Change
                    "name": "Newsly Summarizer AI",
                },
                "to": [
                    {
                        "email": user["email"],
                    }
                ],
                "subject": f"Your Newsly for {utc_yesterday}",
                "html": html_message,
                "category": "Summaries",
            }
            headers = {
                "Authorization": os.getenv("MAILTRAP_TOKEN"),
                "Content-Type": "application/json"
            }
            requests.request("POST", url, headers=headers, json=payload)

        ````
    4. Deploy! *Note: I personally use Render as my deploying site because it can deploy my web service and my CRON worker in one
        1. Deploy your website (app.py)
        2. Deploy your CRON job (fetch_and_send.py) and set it to run at 12 AM UTC daily

# Technologies Used
## Front-end
- **HTML**
- **CSS**
- **Javascript**
## Back-end
- Language and framework: **Python (Flask)**
- Libraries: **sqlalchemy, pymongo, newspaper3k, openai, ...**
- Databases: **PostgresDB (Supabase)** and **MongoDB (Mongo Atlas)**
## Deployment
- Deploying and CRON services: **Render**

# Project Structure
````plaintext
newsly/
│
│── daily_task/
│  ├── fetch_and_send.py
│  └── helper.py
│
│── register_and_summary/
│   ├──static/
│   │   ├──/images
│   │   ├──script.js
│   │   ├──style.css
│   │   └──summary_style.css
│   ├── templates/
│   │    ├──full_summary.html
│   │    └──index.html
│   └── app.py
│
├── LICENSE
│
├── README.md
│
├── requirements.txt
│
├── .env
│
└── .gitignore

````

# How it Works
## app.py
Once the user has submitted their email, "/" route in **app.py** will do the second check if the user has provided valid email and if they have chosen at least one category. It will also check if the email the user provided has already existed in the **postgresDB**. If any of these fails, registration will be rejected and an error pop up would show on user's screen. Finally, if all of the tests have been satisfied, user's email will be stored in database, waiting to be referenced by **fetch_and_send.py**.

## fetch_and_send.py
1. Once the script has been called whether by CRON job or manual call, the program will get top news' links using **The News API** and store it as a python object (dictionary). Consequently, the program will loop through our data, and each link, we will use **newspaper3k** library to scrape the website content and send it to **openai** to summarize news and format them in JSON, and finally at the end of the loop, we will store the JSON summaries in **MongoDB**

2. This part is all about preparing to send emails to recipients. To get nice presentation of the summaries, we need to send email content as in html form. We will loop through our target day summaries stored in **MongoDB** to, for each summary, make html body for it and store in python object, waiting to be constructed as a whole html message. Next we will have to extract recipients' email and their chosen categories stored in **PostgresDB** and store it in a list of recipients for later use.

3. We will loop through the list of recipients to, firstly, create a category-personalized html message for them by looping through recipients' category, and if the recipients' category matches the category you are matching, concatenate all of that category's content html body to central html body that will hold all of categories' body.
Next we will call **create_html_message** function to construct the html message. And lastly, we will send it through **mailtrap** api service

# License
This project is licensed under the [MIT License](LICENSE)
