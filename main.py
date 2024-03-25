from flask import Flask, jsonify
from service.insuranceResp import InsuranceResponse
import base64
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from models.VehicleDetails import VehicleDetails
from google.cloud import bigquery
from datetime import datetime
import os      
import llm_generate
from flask import Flask,flash,request,session,redirect,render_template
from vertexai.preview.generative_models import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Ai-SquAd'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload_files", methods=["POST"])
def upload_files():
    carBrandModel = request.form.get('carBrandModel')
    licensePlate = request.form.get('licensePlate')
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        carPrompt = []
        for file in files:
          if not allowed_file(file.filename):
            return "Received image file is not supported"
          else :
            fileBytes  = file.stream.read()
            imagebytes = Image.from_bytes(fileBytes) 
            Part.from_data(data=base64.b64decode(fileBytes),mime_type="image/"+file.filename.rsplit('.', 1)[1].lower())
            carPrompt.append(imagebytes)
            
        return llm_generate.generateContent(carBrandModel,licensePlate,carPrompt)
    
        
@app.route("/")
def index():
    client = bigquery.Client()
    selectQuery = ('select distinct brand,model from cap-ai-squad.SQUAD_DS.spares_info order by brand')
    query_job = client.query(selectQuery)  
    spares_rs = query_job.result()  
    
    vehicleDetails = []
    for row in spares_rs:
        vehicleDetails.append(VehicleDetails(row[0],row[1]))
    
    return render_template('home.html',vehicleDetails=vehicleDetails)

@app.route("/raiseClaim",methods=["POST"])
def raiseClaim():
    carBrandModel = request.form.get('carBrandModel')
    totalSparesCost = request.form.get('totalSparesCost')
    licensePlate = request.form.get('licensePlate')
    client = bigquery.Client()
    selectQuery = ("select distinct user_id from SQUAD_DS.users_info where License_Plate = '" + licensePlate + "'")
    query_job = client.query(selectQuery)  
    rows = query_job.result()  
    
    userId= ''
    for row in rows:
        userId=row[0]
    
    return render_template('raiseClaim.html',totalSparesCost=totalSparesCost,userId=userId,carBrandModel=carBrandModel)

@app.route("/submitClaim", methods=["POST"])
def submitClaim():    

    userId = request.form.get("userId")
    claimDate = request.form.get("claimDate")
    
    licensePlate = request.form.get("licensePlate")
    description = request.form.get("description")
    insurancePolicyStatus = request.form.get("insurancePolicyStatus")
    insuranceCompany = request.form.get("insuranceCompany")
    insuranceNumber = request.form.get("insuranceNumber")
    insuranceExpiryDate = request.form.get("insuranceExpiryDate")
    includedCoverages = request.form.get("includedCoverages")
    policyRenewalDate = request.form.get("policyRenewalDate")
        
    msg = "Claim details added successfully" 
    return redirect('/')
    

if __name__ == '__main__':
    app.run(debug=False, port=server_port, host='0.0.0.0')    
    