from contextlib import asynccontextmanager
import json
import logging
import requests


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import boto3


from app.models import profile
from app.core.database import engine
from app.routes.profile_route import profile_router


client = boto3.client('sns', "us-east-1")
AUTH_SERVICE_TOPIC_ARN="arn:aws:sns:us-east-1:577204341211:authentication-service-topic"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan function listening for notifications...")
    client.subscribe(
        TopicArn=AUTH_SERVICE_TOPIC_ARN,
        Endpoint=f"https://profileservice-os6x.onrender.com/api/v1/profile/sns",  # Replace with actual URL
        Protocol="https",
    )


app = FastAPI(
    title="Profile Service",
    description="Thelima profile service",
    version="1.0.0",
)

profile.Base.metadata.create_all(bind=engine)


# Index health check
@app.get('/')
def index():
    return {"message": "Profile service"}


# SNS
@app.post('/profile/sns')
async def subscribe(request: Request):
    headers = request.headers
    body = await request.body()
    amazon_message_type = headers.get('x-amz-sns-message-type')

    # Confirm subscription to the SNS topic
    if amazon_message_type == 'SubscriptionConfirmation':
        print("Processing subscription confirmation")
        try:
            data = json.loads(body.decode('utf-8'))
            subscribe_url = data.get('SubscribeURL')

            if subscribe_url:
                response = requests.get(url=subscribe_url)
                print('Subscription to SNS topic confirmed: %s', response)
                logging.info('Subscription to SNS topic confirmed: %s', response)
            else:
                logging.warning('Subscribe URL not found')
        except json.JSONDecodeError:
            logging.error('Invalid JSON data received')
        
        return JSONResponse(status_code=200)
    
    # Consume message from SNS topic
    elif amazon_message_type == 'Notification':
        print("Processing notification")
        print("Raw body %s" % body)
        print("Processed body %s" % body.decode('utf-8'))
        return JSONResponse(status_code=200)

app.include_router(profile_router)

# TODO: To receive Profile creation event from Authentication service
# TODO: To receive tokenized user card details from Payment service to add to a user profile