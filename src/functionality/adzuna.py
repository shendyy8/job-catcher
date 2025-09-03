from dotenv import load_dotenv
import pandas as pd 
from datetime import datetime
from classes.adzuna_wrapper import Adzuna
from classes.logger import Logger
from google.cloud import storage
from io import BytesIO

# Setup Credentials & Secrets
load_dotenv()
log = Logger().get_logger()

def get_adzuna_job(
    output_bucket:str, 
    execution_datetime:str|None=None, 
    country:str='gb', 
    starting_page:int|None=1,
    result_per_page:int|None=50,
    total_result:int|None=50
    ):
  
  
  # Setup variables
  exc_dt = datetime.now()
  exc_date = execution_datetime or exc_dt.strftime("%Y-%m-%d %H:%M:%S")
  exc_date_object = datetime.strptime(exc_date, "%Y-%m-%d %H:%M:%S")

  time_string = f"{exc_date_object.strftime("%H")}{exc_date_object.strftime("%M")}{exc_date_object.strftime("%S")}"
  date_string = exc_date_object.strftime("%Y%m%d")

  filename = f"adzuna/{date_string}/job_{country}_{time_string}.parquet"
  adzuna = Adzuna()
  buffer = BytesIO()
  adzuna.set_country(country)
  adzuna.starting_page = starting_page or 1
  adzuna.result_per_page = result_per_page or 50

  log.info('get_adzuna_job: Setting up variable Done')

  # Search for Job

  df = adzuna.search_job(result_count= total_result or 50)

  df["created"] = pd.to_datetime(df["created"], utc=True)
  df['execution_datetime'] = exc_date_object
  df["filename"] = filename
  
  df.to_parquet(buffer, engine='pyarrow', compression='snappy', index=False)
  buffer.seek(0)
  log.info(f'get_adzuna_job: Searching Job to Adzuna Done')

  # Setup Storage Client
  client = storage.Client()
  bucket = client.get_bucket(output_bucket)
  blobs = bucket.blob(filename)
  blobs.upload_from_file(buffer, content_type="application/octet-stream")
  
  log.info(f'get_adzuna_job: Uploading Data to {output_bucket}/{filename} Done')

  return f"Data successfuly uploaded into {output_bucket}/{filename}"