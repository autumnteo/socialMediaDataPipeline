# socialMediaDataPipeline


## Purpose
In this project, we pull data from twitter and/or reddit, perform some data transformation before storing it in a (sqlite) database.

This project is for me to learn how to apply good coding principles when building data pipelines.


## Prerequisites

1. [Python3](https://www.python.org/downloads/)
2. [sqlite3](https://www.sqlite.org/download.html)
3. [Reddit app](https://www.geeksforgeeks.org/how-to-get-client_id-and-client_secret-for-python-reddit-api-registration/). You'll need a reddit API token **`REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, & REDDIT_USER_AGENT`**.
4. [Twitter API token](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api), You'll need a twitter API token **`BEARER_TOKEN`**.
5. [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)


## Setup

Create a `.env` in the project's root directory, with the following content
```txt
REDDIT_CLIENT_ID=<reddit-client-id>
REDDIT_CLIENT_SECRET=<replace-with-your->reddit-client-secret>
REDDIT_USER_AGENT=<reddit-user-agent>
BEARER_TOKEN=<twitter-bearer-token>
```


Run the following commands are to be run via the terminal, from your project root directory.

```bash
python3 -m venv venv # Create a venv
. venv/bin/activate # activate venv
pip install -r requirements.txt # install requirements
make ci # Run tests, check linting, & format code
make reset-db # Creates DB schemas
make reddit-pipeline # pipeline reddit data
make twitter-elt # pipeline twitter data
make db # open the db to check ELT-ed data 
```

```sqlite
select source, count(*) from social_posts group by 1;
.exit
```

Set up git hooks. Create a pre-commit file, as shown below.

```bash
echo -e '
#!/bin/sh
make ci
' > .git/hooks/pre-commit
chmod ug+x .git/hooks/*
```

## Make commands

We have some make commands to make things run better, please refer to the [Makefile](./Makefile) to see them.