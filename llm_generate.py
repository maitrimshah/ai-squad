from google.cloud import aiplatform
from models.Spares import Spares
import pandas as pd
from google.cloud import bigquery
import base64
import vertexai
import json
from flask import Flask,flash,request,session,redirect,render_template
from vertexai.preview.generative_models import GenerativeModel, Part, Image
import vertexai.preview.generative_models as generative_models
    
def generateContent(carBrandModel,licensePlate,carPrompt):
   
  vertexai.init(project="cap-ai-squad",location="europe-west1")
  model =  GenerativeModel("gemini-1.0-pro-vision")
  
  prompt = "You are auto Expert for Indian Cars,based on the images uploaded of '" + carBrandModel +  """',can you identify which spare parts of the car are damaged in below json format { "External Damaged Parts": [], "Internal Damaged Parts": [], "Fixes for the External Damaged Parts": [], "Fixes for the Internal Damaged Parts": []}. Also make sure identified damaged part should exactly match with one of values from below list in format, { "External Damaged Parts": [Bonnet/Hood,Disc Brake Front], "Internal Damaged Parts": [Front Brake Pads,Filter], "Fixes for the External Damaged Parts": [], "Fixes for the Internal Damaged Parts": []} Air Filter,Bonnet/Hood,Dashboard,Dicky,Disc Brake Front,Disc Brake Rear,Door Panel,Front Brake Pads,Front Bumper,Front Windshield Glass,Fuel Filter,Oil Filter,Rear Brake Pads,Rear Bumper,Rear Windshield Glass,Side View Mirror,Steering Wheel,Fender (Left or Right),Rear Door (Left or Right),Front Door (Left or Right),Tail Light (Left or Right),Headlight (Left or Right)."""
  
  print(prompt)
  carPrompt.append(prompt)

  responses  = model.generate_content(carPrompt,
    generation_config={
        "max_output_tokens": 2048,
        "temperature": 0,
        "top_p": 0,
        "top_k": 22
    },                                      
    safety_settings={
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    },
    stream=False,                                  
  ) 
  
  data = json.loads(_clean_json(responses.text))
  parts1 = str(data["External Damaged Parts"]).strip().replace('[','').replace(']','').replace("'","")
  parts2 = str(data["Internal Damaged Parts"]).strip().replace('[','').replace(']','').replace("'","")
  
  parts = parts1 + parts2
  
  partsarray  = parts.split(',')

  print(partsarray)
  subQuery = ''
  for parts in partsarray:
      subQuery =  subQuery +  "'" + parts + "'," 
  subQuery = subQuery[:-1]
  
  bqQuery = "select Spares_Sub_Type part_name,Spares_Cost part_cost from cap-ai-squad.SQUAD_DS.spares_info where concat(brand,'"+ " " +"',model) = '" + carBrandModel + "' and initcap(spares_sub_type) in (" + subQuery + ")"
    
  client = bigquery.Client()
  query_job = client.query(bqQuery)  
  rows = query_job.result()  

  totalSparesCost = 0
  spareParts = []
  for row in rows:
    spareParts.append(Spares(row[0],row[1]))  
    totalSparesCost = totalSparesCost + row[1]    
         
  if spareParts:
    print('spare_part_details')
    print(spareParts)
    
  return render_template('models.html',spare_part_details=spareParts,carBrandModel=carBrandModel,totalSparesCost=totalSparesCost,licensePlate=licensePlate)
  
def _clean_json(content: str):
  return content.strip().replace('json','').replace('JSON','').replace('```','').strip()