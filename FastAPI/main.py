import json
from typing import Annotated
from pathlib import Path as FilePath
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()
DATA_FILE = FilePath(__file__).with_name('patients.json')


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Unique identifier for the patient", example='P001')]
    name: Annotated[str, Field(..., description="Name of the patient", example='John Doe')]
    city: Annotated[str, Field(..., description="City of the patient", example='New York')]
    age: Annotated[int, Field(..., gt=0, lt=120,  description="Age of the patient", example=30)]
    gender: Annotated[str, Field(..., description="Gender of the patient", example='Male')]
    height: Annotated[float, Field(..., description="Height of the patient", example=1.75)]
    weight: Annotated[float, Field(..., description="Weight of the patient", example=70.5)]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= self.bmi < 25:
            return 'Normal weight'
        elif 25 <= self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
        
class PatientUpdate(BaseModel):
    name: Annotated[str, Field(..., description="Name of the patient", example='John Doe')]
    city: Annotated[str, Field(..., description="City of the patient", example='New York')]
    age: Annotated[int, Field(..., gt=0, lt=120,  description="Age of the patient", example=30)]
    gender: Annotated[str, Field(..., description="Gender of the patient", example='Male')]
    height: Annotated[float, Field(..., description="Height of the patient", example=1.75)]
    weight: Annotated[float, Field(..., description="Weight of the patient", example=70.5)]
    

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

def load_data():
    if not DATA_FILE.exists():
        return {}

    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail='patients.json contains invalid JSON') from exc

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.get('/view')
def view():
    data = load_data()

    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example='P001')):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description = "Sort on the basis of name, age, bmi"), order: str = Query(..., description = "Sort in ascending order or descending order")):
    valid_sort_by = ['name', 'age', 'bmi']
    
    if sort_by not in valid_sort_by:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value. Must be one of {valid_sort_by}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order value. Must be 'asc' or 'desc'")
    
    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=(order == 'desc'))
    
    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    data[patient.id] = patient.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(content={'message': 'Patient created successfully'}, status_code=201)   

@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    updated_patient = Patient(id=patient_id, **patient_update.model_dump())
    data[patient_id] = updated_patient.model_dump(exclude={'id'})
    save_data(data)
    
    return {'message': 'Patient updated successfully'}

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]
    save_data(data)
    
    return {'message': 'Patient deleted successfully'}