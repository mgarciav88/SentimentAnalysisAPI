# SentimentAnalysisAPI
Small test project of fastAPI + AWS Comprehend for sentiment analysis

To start, setup AWS credentials. This can be done either as part of .aws/credentials when running locally.

The project is configured so that it can run with a custom profile, whose name is defined in the .env and passed as an 
environment variable.

To start the API, simply run:

python main.py

The API can be accessed via localhost:8080 as configured.
