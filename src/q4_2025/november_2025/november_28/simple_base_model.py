from random import choice
from typing import Optional, Union
from pydantic import BaseModel, Field, field_validator

password_list = ['simple', 'complex', 'simpleComplex']

customFunc = lambda x: choice(password_list)

result = customFunc(5)

print(result)


# User
class User(BaseModel):

    # Define some attributes
    name: str
    email_id: str
    age: int =  Field(default=18)
    password: Optional[str] = Field(default=choice(password_list))
    

    # Method
    @field_validator('email_id')
    @classmethod
    def acceptable_email(cls, v: str) -> str:

        # Allowable domains
        allowable_domains = ['gmail.com', 'yahoo.com', 'outlook.org', 'hotmail.com', 'aol.com']

        id, domain = v.split('@')

        if domain not in allowable_domains:
            raise ValueError("Not a proper email.")
        
        elif '@' not in v:
            raise ValueError("Not a proper email.")
        
        return v

    # Method
    @field_validator('age')
    @classmethod
    def minimum_age(cls, v: int) -> int:
        # Control Flow
        if v < 21:
            raise ValueError("Minimum age requirement has not been met.")

        return v
    
    # Method
    @field_validator('age')
    @classmethod
    def maximum_age(cls, v: int) -> int:
        if v > 65:
            raise ValueError("Maximum age detected. Not eligible for entry.")

        return v

# Dictionary
user_attrs = {
    'name' : 'charlie',
    'email_id' : 'charlie@gmail.com',
    'age' : 64
}

# User object
user = User(**user_attrs)

print(user)

# Convert the objects into JSON
user_as_json = user.model_dump()

print(user_as_json)