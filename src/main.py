from fastapi import FastAPI, HTTPException
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
    country:str,
    starting_page:int|None,
    result_per_page:int|None,
    total_result:int|None
    ):

    try:
        log.info('endpoint_get_adzuna_job Called')
        response = get_adzuna_job(
            output_bucket=output_bucket,
            execution_datetime=execution_datetime,
            country=country,
            starting_page=starting_page,
            result_per_page=result_per_page,
            total_result=total_result
            )    
        return {"message": "job done", "details": response}
    
    except Exception as e:
        log.error(f"Error in endpoint_get_adzuna_job: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
   