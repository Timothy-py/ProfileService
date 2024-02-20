from contextlib import asynccontextmanager
import logging


from fastapi import FastAPI
from mangum import Mangum
import boto3


from app.models import profile
from app.core.database import engine
from app.routes.profile_route import profile_router


client = boto3.client('sns', "eu-north-1")


@asynccontextmanager
async def lifespan(app: FastAPI):
    client.subscribe(
        TopicArn="arn:aws:sns:eu-north-1:620335327632:user-verified",
        Endpoint=f"http://localhost:7000/api/v1/profile",  # Replace with actual URL
        Protocol="https"
    )


app = FastAPI(
    title="Profile Service",
    description="Thelima profile service",
    version="1.0.0",
)

profile.Base.metadata.create_all(bind=engine)

handler = Mangum(app)


# Index health check
@app.get('/')
def index():
    return {"message": "Profile service"}


app.include_router(profile_router)

# TODO: To receive Profile creation event from Authentication service
# TODO: To receive tokenized user card details from Payment service to add to a user profile