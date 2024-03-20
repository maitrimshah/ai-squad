import base64
import vertexai
import json
from vertexai.preview.generative_models import GenerativeModel, Part, Image
from werkzeug.utils import secure_filename
import vertexai.preview.generative_models as generative_models

def generateContent(brandModel,files):
#  print('Calling LLM')
#  print(brandModel)
#  print(files)
  
  #flash('All images successfully uploaded')
  for file in files:
    fileBytes  = file.stream.read()
    imagebytes = Image.from_bytes(fileBytes)
    filename = secure_filename(file.filename)
#    print('----imagebytes----')
#    print(imagebytes)
#    print('----filename----')
#    print(filename)
  
  vertexai.init(project="cap-ai-squad", location="us-west1")
  model = GenerativeModel("gemini-1.0-pro-vision-001")
  prompt = """Return a json with json value as string or a comma separated string values containing correct and exact full spare parts which are damaged in the car in the attached image.
Also specify the rear/front/left/right in the spare part names if there is the possibility of those words in the names"""    
  
  responses = model.generate_content(
    [prompt, imagebytes],
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
  print('responses.text')
  print(responses.text)
  data = json.loads(responses.text)
  print('data')
  print(data)
  #parts  = str(data["External Damaged Parts"]).strip().removeprefix('[').removesuffix(']').replace("'","")
  #partsArray  = parts.split(',')
    
 # subQuery = ""    
 # for parts in partsArray:
  #  subQuery =  subQuery +  "lower(spares_sub_type) like %"  + parts + "% or "
       
#  finalSubQuery  = " ".join(subQuery.split(' ')[:-2])
#  bqQuery = 'SELECT car_model,spares_sub_type,spares_cost FROM cap-ai-squad.SQUAD_DS.spares_costs where car_model = ' + brandModel +' and (' + finalSubQuery + ')'    
#  print('---bqQuery---')
#  print(bqQuery)
################ to do write down code here to use Bigquery SDK to return response from BQ Table ##############
            
# generation_model = TextGenerationModel.from_pretrained("text-bison@001")
# promptText = f"""
# Give summary of cost for search response {response} in Table format also add total for each json element"
# Final Cost : 
# finalCost =  generation_model.predict(
# promptText, temperature=0.5, top_k=40, top_p=0.8
# ).text

  return render_template('index.html',CostTable =bqQuery)

def _clean_json(content: str):
  return content.strip().removeprefix('```').strip().removeprefix('json').removeprefix('JSON').strip().removesuffix('```')
