from dotenv import load_dotenv
import pandas as pd 
from datetime import datetime
from classes.adzuna_wrapper import Adzuna
from google.cloud import storage
from io import BytesIO

# Setup Credentials & Secrets
load_dotenv()


def get_adzuna_job(output_bucket:str, execution_datetime:str|None=None, country:str='gb'):
  
  # Setup variables
  exc_dt = datetime.now()
  exc_date = execution_datetime or exc_dt.strftime("%Y-%m-%d %H:%M:%S")
  exc_date_object = datetime.strptime(exc_date, "%Y-%m-%d %H:%M:%S")

  time_string = f"{exc_date_object.hour}{exc_date_object.minute}{exc_date_object.strftime("%S")}"
  date_string = exc_date_object.strftime("%Y%m%d")

  filename = f"adzuna/{date_string}/job_{country}_{time_string}.parquet"
  adzuna = Adzuna()
  buffer = BytesIO()
  adzuna.set_country(country)

  # Search for Job
  df = adzuna.search_job(result_count=50)

  df["created"] = pd.to_datetime(df["created"], utc=True)
  df['execution_datetime'] = exc_date_object
  df["filename"] = filename
  
  df.to_parquet(buffer, engine='pyarrow', compression='snappy', index=False)
  buffer.seek(0)

  # Setup Storage Client
  client = storage.Client()
  bucket = client.get_bucket(output_bucket)
  blobs = bucket.blob(filename)
  blobs.upload_from_file(buffer, content_type="application/octet-stream")

  return {"message": f"Data successfuly uploaded into {output_bucket}/{filename}"}