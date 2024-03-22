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
    carModel = request.form.get('model')
    carBrand = request.form.get('brand')
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
          if not allowed_file(file.filename):
            return "Received image file is not supported"
          else :
            imageList = []
            for file in files:
                fileBytes  = file.stream.read()
                imagebytes = Image.from_bytes(fileBytes)
                imageList.append(imagebytes)
                #flash(file.name + " uploaded successfully")
        
        llm_generate.generateContent(carModel,imageList)
    
        
@app.route("/")
def index():
    client = bigquery.Client()
    selectQuery = ('select brand,model from cap-ai-squad.SQUAD_DS.spares_info where model in (select distinct model from cap-ai-squad.SQUAD_DS.spares_info group by model)')
    query_job = client.query(selectQuery)  
    spares_rs = query_job.result()  
    
    vehicleDetails = []
    for row in spares_rs:
        vehicleDetails.append(VehicleDetails(row[0],row[1]))
    
    return render_template('home.html',vehicleDetails=vehicleDetails)

@app.route("/raiseClaim",methods=["POST"])
def raiseClaim():
    totalSparesCost = request.form.get('totalSparesCost')
    return render_template('raiseClaim.html',totalSparesCost=totalSparesCost)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)