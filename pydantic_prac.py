from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Annotated

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
class Patient(BaseModel):
    name: Annotated[str, Field( max_length=100,title="Name", description="Name must be a string with a maximum length of 100 characters",example="John Doe")]
    email: EmailStr
    linkdin_url: AnyUrl
    age:Annotated[int, Field( gt=0, description="Age must be a positive integer",strict=True)]
    conditions: Optional[List[str]]= None
    contact_info: Dict[str, str]=Field(max_length=2, description="Contact info should contain phone and email")
    height:float
    weight:float
    address: Address #nested pydantic model
    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        valid_domains = ['example.com', 'test.com']
        domain = value.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
    @field_validator('name',mode='after')
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    @model_validator(mode='after')
    @classmethod
    def emerency_contact_required(cls, model):
        if model.age>60 and ('emergency_contact' not in model.__dict__ or not model.__dict__['emergency_contact']):
            raise ValueError("Emergency contact is required")
        return model

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.conditions)
    print(patient.contact_info)
    print(patient.email)
    print(patient.linkdin_url)
    print(f"BMI: {patient.bmi}")
    print(patient.address.state)
    print("inserting patient")

address_dict = {'street': '123 Main St', 'city': 'Anytown', 'state': 'CA', 'zip_code': '12345'}
patient_address = Address(**address_dict)

patient_info={'name': "John Doe", 'age': 30, 'conditions': ["Diabetes", "Hypertension"], 'contact_info': {'phone': '123-456-7890', 'email': 'john.doe@example.com'}, 'email': 'john.doe@example.com', 'linkdin_url': 'https://www.linkedin.com/in/johndoe', 'height': 1.75, 'weight': 70, 'address': patient_address}
patient1 = Patient(**patient_info)
insert_patient(patient1)

temp=patient1.model_dump() # convert pydantic model to dict
print(temp)
temp1 =patient1.model_dump_json() # convert pydantic model to json
print(temp1)
temp2=patient1.model_dump(include={'name','age'}) # convert pydantic model to dict with only name and age
print(temp2)