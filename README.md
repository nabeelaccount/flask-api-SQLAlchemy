# Flask API Postgres

There are a number of ways of using and testing out this application. 


## Running the application locally

Prerequeists
- You have a running Postgres Server with a database  "transactions".
- You've created a file named .env with a key DATABASE_URL and the value as the database URL in the following format. Please make sure not to commit this file to GitHub or Docker.
```
'DATABASE_URL=postgresql://user:password@postgres-database-endpoint:5432/transactions'
```
This command assumes the Postgres has a database named transactions

Now lets begin! I recommend you create a python virtual environment. You can create the virtual environments by running the following:
```
python3 -m venv env
source env/bin/activate
```

You the require to install all the module dependencies required by the application. Please run the following:
```
python3 -m pip install -r requirements.txt 
```

You should now be able to run the application by running:
```
flask run
```

You may recieve the following message, this is what is expected and it's totally fine for development:
"""
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 960-226-082
"""

You can then send a POST request to the database using the API through the following command:
```
curl --header "Content-Type: application/json" \
-X POST http://<someip>/api/transaction/ \
--data '{"transactionId":"0f7e46df-c685-4df9-9e23-e75e7ac8ba7a",
"amount": "99.99","timestamp":"2009-09-28T19:03:12Z"}'
```

You can also use Postman or Insomnia to run your POST request.


## Running the application in a Docker container

Once you've pushed the image:
```
docker build . -t your-account-name/fask-api-sqlalchemy
```

You can run the image inside a docker container as follows:
```
docker run -p 5000:5000 --env-file .env your-account-name/fask-api-sqlalchemy
```


Develop database driven REST API with Python: https://betterdatascience.com/develop-database-driven-rest-api-with-python-in-10-minutes/


## Running the application in a Docker compose

To start the application you should run:
```
docker compose up -flask_db
```

Check the database server is running locally using:
```
psql -h localhost -p 5432 -U postgres postgres
```

Then build the image by running:
```
docker compose build
```

Once this is complete and successful, it's now time to run the flask API application:
```
docker compose up flask_app
```

Excenllent example can be found here: https://github.com/FrancescoXX/flask-crud-live

