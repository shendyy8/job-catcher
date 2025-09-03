from fastapi import FastAPI
from functionality.adzuna import get_adzuna_job
from classes.logger import Logger

app = FastAPI()
log = Logger().get_logger()

@app.get("/")
def home() -> dict:
    log.info('Hello World')
    return {"message":"hello-world"}

@app.get("/adzuna_job")
def endpoint_get_adzuna_job(
    output_bucket:str,
    execution_datetime:str|None,
    country:str
    ):

    response = get_adzuna_job(
        output_bucket=output_bucket,
        execution_datetime=execution_datetime,
        country=country
        )

    return response