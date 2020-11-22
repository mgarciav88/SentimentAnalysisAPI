import os

from dotenv import load_dotenv, find_dotenv
import boto3
from fastapi import FastAPI, HTTPException, Depends

from schemas import SingleRequest, BatchRequest, SentimentResponse, BatchResponse
from utils import select_dominant_language, select_batch_dominant_language

load_dotenv(find_dotenv())

app = FastAPI(
    title="Sentiment Analysis",
    version="1.0",
    description="Sentiment Analysis API using AWS Comprehend",
)


def aws_connect():
    try:
        session = boto3.Session(profile_name=os.getenv('AWS_PROFILE', 'default'))
        yield session.client(service_name='comprehend')
    finally:
        print('Close if this was necessary')


@app.get("/")
def default_response():
    return {"Hello World"}


@app.post("/single_analysis", response_model=SentimentResponse)
def single_analysis_response(body: SingleRequest, comprehend=Depends(aws_connect)):
    language_response = comprehend.detect_dominant_language(Text=body.text)
    language_obj = select_dominant_language(language_response)
    language = language_obj.get('LanguageCode')
    analysis_response = comprehend.detect_sentiment(Text=body.text, LanguageCode=language)
    response_body = {
        'sentiment': analysis_response.get('Sentiment'),
        'score': analysis_response.get('SentimentScore'),
        'language': language,
    }

    if (score := language_obj.get('Score')) < 0.7:
        response_body.update({'message': f"Language confidence is low, value computed of {score}"})

    return response_body


@app.post("/batch_analysis", response_model=BatchResponse)
def detect_language(body: BatchRequest, comprehend=Depends(aws_connect)):
    language_response = comprehend.batch_detect_dominant_language(TextList=body.text_list)
    language = select_batch_dominant_language(language_response)
    if language is None:
        raise HTTPException(status_code=400, detail="More than one language detected, make sure all phrases belong to "
                                                    "the same language")

    analysis_response = comprehend.batch_detect_sentiment(TextList=body.text_list, LanguageCode=language)
    response_list = [{
        'sentiment': response.get('Sentiment'),
        'score': response.get('SentimentScore'),
        'language': language,
    } for response in analysis_response.get('ResultList')]

    return {'response': response_list}
