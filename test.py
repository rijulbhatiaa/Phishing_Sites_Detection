# import uvicorn
# from fastapi import FastAPI
# import joblib,os

# app = FastAPI()

# #pkl
# phish_model = open('phishing.pkl','rb')
# phish_model_ls = joblib.load(phish_model)

# # ML Aspect
# @app.get('/predict/{feature}')
# async def predict(features):
# 	X_predict = []
# 	X_predict.append(str(features))
# 	y_Predict = phish_model_ls.predict(X_predict)
# 	if y_Predict == 'bad':
# 		result = "This is a Phishing Site"
# 	else:
# 		result = "This is not a Phishing Site"

# 	return (features, result)
# if __name__ == '__main__':
# 	uvicorn.run(app,host="127.0.0.1",port=8000)


import uvicorn
from fastapi import FastAPI, HTTPException
import joblib
import requests
from requests.exceptions import RequestException
import requests
from requests.exceptions import RequestException, HTTPError, Timeout
import re
app = FastAPI()

# Load phishing detection model
phish_model = joblib.load('phishing.pkl')

# Function to check if URL is valid
def is_valid_url(url):
    try:
        # Ensure the URL has a valid format
        if not re.match(r'http[s]?://', url):
            url = 'http://' + url

        response = requests.get(url, allow_redirects=True, timeout=10)
        # Consider the URL valid if the status code is in the 200-399 range
        if 200 <= response.status_code < 400:
            return True
        else:
            return False
    except (RequestException, HTTPError, Timeout) as e:
        # Print the error for debugging purposes
        # print(f"Error for URL {url}: {e}")
        return False

# Endpoint for predicting phishing status
@app.get('/predict/')
async def predict(url: str):
    if not is_valid_url(url):
        raise HTTPException(status_code=400, detail="URL is not valid or not reachable")

    X_predict = [url]
    y_predict = phish_model.predict(X_predict)
    
    if y_predict[0] == 'bad':
        result = "This is a Phishing Site"
    else:
        result = "This is not a Phishing Site"

    return {"URL": url, "Prediction": result}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
