from models.Spares import Spares
import pandas as pd
from google.cloud import bigquery
import base64
import vertexai
import json
from vertexai.preview.generative_models import GenerativeModel, Part, Image
import vertexai.preview.generative_models as generative_models

def generateContent(carModel,imageList):#typeOfVehicle,imageList):
   
  vertexai.init(project="cap-ai-squad", location="us-west1")
  model = GenerativeModel("gemini-1.0-pro-vision-001")
  
# if typeOfVehicle == '4 Wheelers':
  prompt = "Can you identify the damages of the " + carModel + " car in attached images and provide the list of damaged spare parts in json format with json key as  part_name and json value as comma separated string. Output json with no nested objects.Wrap json array with [ ] brackets. Return only the valid json string. Also make sure the json values that exactly matches with any of the values from below list : Air Filter,Bonnet/Hood,Dashboard,Dicky,Disc Brake Front,Disc Brake Rear,Door Panel,Front Brake Pads,Front Bumper,Front Windshield Glass,Fuel Filter,Oil Filter,Rear Brake Pads,Rear Bumper,Rear Windshield Glass,Side View Mirror,Steering Wheel,Fender (Left or Right),Rear Door (Left or Right),Front Door (Left or Right),Tail Light (Left or Right),Headlight (Left or Right)."
#  elif typeOfVehicle == '3 Wheelers':
#   prompt = "Identify the damaged spare parts names from the attached images of " + brandModel + " and provide the list of damaged spare parts in json format with json key as  part_name and json value as comma separated string. Output json with no nested objects.Wrap json array with [ ] brackets. Return only the valid json string. Also make sure the json values that exactly matches with any of the values from below list : Air filter, Alternator,Ball joints,Battery,Body panels,Brake calipers,Brake drums,Brake lines,Brake pads,Brake shoes,Camshaft,Carburetor,Clutch,Connecting rod,Cooling fan,Crankshaft,Cylinder head,Dashboard,Differential,Engine,Exhaust system,Front suspension,Fuel pump,Fuel tank,Gearbox,Headlights,Taillights,Horn,Ignition coil,Indicators,Instruments,Master cylinder,Mirrors,Oil filter,Oil pump,Piston and rings,Radiator,Rear suspension,Seats,Spark plugs,Starter motor,Steering rack,Tie rods,Timing chain,Tyres,Transmission,Voltage regulator,Wheels,Windows,Wiring harness."
# elif typeOfVehicle == '2 Wheelers':
#   prompt = "Identify the damaged spare parts names from the attached images of " + brandModel + " and provide the list of damaged spare parts in json format with json key as  part_name and json value as comma separated string. Output json with no nested objects.Wrap json array with [ ] brackets. Return only the valid json string. Also make sure the json values that exactly matches with any of the values from below list : Piston,Cylinder Head,Cylinder Block,Crankshaft,Connecting Rod,Cam Chain,Timing Chain,Oil Filter,Air Filter,Spark Plug,Clutch Plates,Gearbox,Final Drive Chain,Front Sprocket,Rear Sprocket,Battery.Starter Motor,Alternator,Regulator Rectifier,Ignition Coil,CDI Unit,Headlight Assembly,Taillight Assembly,Turn Signal Indicators,Horn,Front Fork Assembly,Rear Shock Absorber,Swingarm,Brake Parts,Front Brake Pads,Rear Brake Pads,Front Brake Master Cylinder,Rear Brake Master Cylinder,Brake Disc,Brake Lines,Front Panel,Side Panels,Rear Panel,Seat Assembly,Leg Shield,Floorboard,Fuel Tank,Fuel Pump,Fuel Injector,Radiator,Fan,Engine Oil,Brake Fluid,Coolant"
  
  contents = [
    prompt
  ]
  
  for image in imageList :
    contents.append(image)

  responses = model.generate_content(contents,
     generation_config={
        "max_output_tokens": 2048,
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32
    },
    safety_settings={
          generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    },
    stream=False,
  )
  content = _clean_json(responses.text)  
  sparePartNames = json.loads(content)
  
  csvPartValuesForQuery = ''
  for sparePartName in sparePartNames:
      csvPartValuesForQuery =  csvPartValuesForQuery +  "'" + sparePartName.get('part_name') + "'," 
  csvPartValuesForQuery = csvPartValuesForQuery[:-1]
    
  bigDataQuery = "select Spares_Sub_Type,Spares_Cost from cap-ai-squad.SQUAD_DS.spares_info where model  = '" + carModel + "' and initcap(spares_sub_type) in (" + csvPartValuesForQuery + ")"
  
  client = bigquery.Client()
  query_job = client.query(bigDataQuery)  
  
  rs = query_job.result() 
  
  totalCost = 0;
  spareParts = []
  for row in rs:
    spareParts.append(Spares(row[0],row[1]))
    totalCost = totalCost + row[1]    
  
  if spare_part_details:
      print('spare_part_details')
      print(spare_part_details)
      return render_template('models.html',spare_part_details=spare_part_details,brand=carBrand,model=carModel,totalSparesCost=totalCost)
        
  return "Sever response is not available."
  
def _clean_json(content: str):
  return content.strip().replace('json','').replace('JSON','').replace('```','').strip()