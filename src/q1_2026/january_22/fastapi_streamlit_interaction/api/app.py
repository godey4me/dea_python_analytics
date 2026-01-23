from fastapi import FastAPI
from uvicorn import run

# Custom module
from data_retrieval import student_data_array, heart_data_array

# Application object
app = FastAPI(title="Data Serving", 
              description="The data will be served for interaction with a front end service."
              )


"""
Routes
"""

@app.get(path="/")
def home():
    return {
        'message': 'Welcome to the data serving API'
    }

@app.get(path="/heart_data")
def heart_data():
    return heart_data_array

@app.get(path="/student_data")
def student_data():
    return student_data_array

# Uvicorn run
run(app=app, host='0.0.0.0', port=8580)