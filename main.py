import uvicorn
from fastapi import FastAPI

from t1_company.run_api import run_api

app: FastAPI = run_api()

if __name__ == '__main__':
    uvicorn.run("main:app", port=6080, host="0.0.0.0", reload=True)
