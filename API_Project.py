# Fast API is a framework to build api's in python.
#uvicorn is a webserver implementation. 
#this will help us run our api in server - uvicorn filename:app 

from fastapi import FastAPI

app = FastAPI()

shipments = []

@app.get("/")
def home():
    return {"message": "Shipment API is running"}

@app.get("/shipments")
def get_shipments():
    return shipments

@app.post("/shipments")
def add_shipment(shipment: dict):
    shipments.append(shipment)
    return {"message": "Shipment added", "data": shipment}
