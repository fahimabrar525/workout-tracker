import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
BASIC_AUTH = os.environ.get("BASIC_AUTH")

GENDER = "male"
WEIGHT_KG = 80
HEIGHT_CM = 178
AGE = 28

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_text = input("Tell me which exercise you did?: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)

today = datetime.now()
formatted_date = today.strftime("%d/%m/%Y")
formatted_time = today.strftime("%X")

sheet_endpoint = "https://api.sheety.co/7a5614c09907f01012a8c97bf468b538/workoutTracking/workouts"

basic_headers = {
    "Authorization": BASIC_AUTH
}

for exercise in result["exercises"]:
    sheet_params = {
        "workout": {
            "date": formatted_date,
            "time": formatted_time,
            "exercise": exercise["user_input"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(url=sheet_endpoint, json=sheet_params, headers=basic_headers)
    print(sheet_response.text)
