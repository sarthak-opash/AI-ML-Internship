import json
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get('/view')
def view():
    data = load_data()

    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example='P001')):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    return {'message': 'Patient not found'}