from fastapi import FastAPI
from functionality.adzuna import get_adzuna_job

app = FastAPI()

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