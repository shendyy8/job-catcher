# API wrapper for Adzuna

import requests
from dotenv import load_dotenv
import os
import json
import pycountry
from typing import Optional
import pandas as pd 

load_dotenv()

# can be made into query builder class
class Adzuna():

  def __init__(self, starting_page:int=1, result_per_page:int=50):
    self.base_url = os.environ['ADZUNA_BASE_URL']
    self.app_id = os.environ['ADZUNA_APP_ID']
    self.app_key = os.environ['ADZUNA_APP_KEY']
    self.country = None
    self.starting_page = starting_page
    self.result_per_page = result_per_page

  def set_country(self, country):
    country = str(pycountry.countries.lookup(country).alpha_2).lower()
    self.country = country

  def search_job(
      self,
      keyword:Optional[str]=None,
      title:Optional[str]=None,
      additional_query:Optional[str]=None,
      result_count:int=100
      ):
    
    if self.country is None:
      raise ValueError('Set Country First!')
    
    # base query
    base_query = f"?app_id={self.app_id}&app_key={self.app_key}"
    base_query += f"&results_per_page={self.result_per_page}"
    base_query += '&category=it-jobs&salary_include_unknown=1'

    # config by parameter
    base_query += f'&what={keyword}' if keyword else ''
    base_query += f'title_only={title}' if title else ''
    base_query += additional_query if additional_query else ''

    content_result = []
    for i , _ in enumerate(range(0,result_count,self.result_per_page)):
        
      # Call
      current_page = self.starting_page + i
      base_uri = f"{self.base_url}/{self.country}/search/{current_page}"
      response = requests.get(base_uri+base_query, timeout=600)
      contents = json.loads(response.content)

      for r in contents['results']:
        content = {}
        content['id'] = r['id']
        content['created'] = r['created']
        content['company'] = r['company']['display_name']
        content['location'] = r['location']['display_name']
        content['country'] = self.country
        content['contract_type'] = r.get('contract_type', r.get('contract_time'))
        content['title'] = r['title']
        content['salary_max'] = r.get('salary_max')
        content['salary_min'] = r.get('salary_min')
        content['description'] = r['description']
        content['redirect_url'] = r['redirect_url']

        content_result.append(content)
      
      if len(contents['results']) < self.result_per_page:
        break

    return pd.DataFrame(content_result)
    