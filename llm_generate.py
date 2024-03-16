import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
import json

def generate_content():
  print('Calling LLM')
  vertexai.init(project="cap-ai-squad", location="us-central1")
  model = GenerativeModel("gemini-1.0-pro-vision-001")
  responses = model.generate_content(
    """I am car assistant sales man. Can you give me the list of all the parts name of all the car available in India. Provide the list of parts in json format with json key as company_name, part_name, car_name, model_name, model_number and part_color with json value as string or comma seperated string. Output json with no nested objects. Wrap json array with [ ] brackets. Return only the valid json string.""",
    generation_config={
        "max_output_tokens": 1024,
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 32
    },
    safety_settings={
          generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    },
    stream=True,
  )
  content = ''
  for response in responses:
    content = content + response.text
  json_string = _clean_json(content)
  print(json_string)
  json_data = {}
  json_data = json.loads(json_string)
  return json_data
def _clean_json(content: str):
  return content.strip().removeprefix('```').strip().removeprefix('json').removeprefix('JSON').strip().removesuffix('```')