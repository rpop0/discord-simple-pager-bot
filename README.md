# Pager bot for Discord
Simple pager bot for discord using python.

## Set up

### Prerequisites
* A MongoDB Database
* Python 3.10

### Installing
* Create a virtual environment.
* Install requirements.txt file in the virtual environ,ent.
* Create a file named `environment.env` at the folder's root.
* Export the environment variables and run the `main.py` script.

### Alternative: Docker install
* Create the docker image using `docker build -t image_name .`
* Run the docker image using `docker --restart always --env-file ./environment.env -d image_name`

### .env file
The `.env` file should look like this:
```
BOT_TOKEN=<BOT_TOKEN>
PAGER_DB_CONN=<MONGO-CONNECTION-STRING-WITH-USERNAME-AND-PASSWORD>
PAGERDB_NAME=<DB-NAME>
PAGER_DB_COL_NAME=<COLLECTION-NAME>
GUILD_ID=<GUILD-ID>
```