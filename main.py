from fastapi import FastAPI,Path,HTTPException,Query
import json
def load_data():
    with open("patients.json","r") as f:
        data = json.load(f)
    return data

app = FastAPI()
@app.get("/")
def hello_world():
    return {"message": "patient management system API"}

@app.get("/about")
def about():
    return {"message": "A fully functional patient management system API built with FastAPI."}

@app.get("/view")
def view_patients():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str=Path(..., description="The ID of the patient to retrieve",example='P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str=Query(...,description="sort on the basis of height,weight,bmi"),order: str=Query("asc",description="order of sorting asc or dsc")):
    valid_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {valid_fields}")
    if order not in ["asc", "dsc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Valid orders are: 'asc' or 'dsc'")
    
    data=load_data()
    sort_order=True if order=="dsc" else False

    sorted_data=sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return  sorted_data