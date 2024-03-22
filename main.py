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
    brand = request.form.get('brand')
    model = request.form.get('model')
    colorOfVehicle = request.form.get('colorOfVehicle')
    typeOfVehicle = request.form.get('typeOfVehicle')
    brandModel = request.form.get('brand') + ' ' + request.form.get('model')
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
          if not allowed_file(file.filename):
            return "Received image file is not supported"
          else :
            for file in files:
                fileBytes  = file.stream.read()
                imagebytes = Image.from_bytes(fileBytes)
                imageList = []
                imageList.append(imagebytes)
                flash(file.name + " uploaded successfully")
        
        spare_part_details = llm_generate.generateContent(brandModel,typeOfVehicle,imageList)
        
        if spare_part_details:
            print('spare_part_details')
            print(spare_part_details)
            return render_template('models.html',spare_part_details=spare_part_details,brand=brand,model=model,typeOfVehicle=typeOfVehicle,colorOfVehicle=colorOfVehicle)
        
        return "Sever response is not available."
        
@app.route("/")
def index():
    client = bigquery.Client()
    selectQuery = ('select distinct type_Of_Vehicle from cap-ai-squad.SQUAD_DS.spares_info order by type_Of_Vehicle')
    query_job = client.query(selectQuery)  
    spares_rs = query_job.result()  
    
    vehicleDetails = []
    for row in spares_rs:
        vehicleDetails.append(VehicleDetails('','',row[0],''))
    
    return render_template('home.html',vehicleDetails=vehicleDetails)
    
@app.route("/getBrand", methods=["GET"])
def getBrand():
    typeOfVehicle = request.form.get('typeOfVehicle')
    client = bigquery.Client()
    selectQuery = ("select distinct brand from cap-ai-squad.SQUAD_DS.spares_info where type_of_vehicle='"+typeOfVehicle+""order by type_Of_Vehicle')
    query_job = client.query(selectQuery)  
    spares_rs = query_job.result()  
    
    vehicleDetails = []
    for row in spares_rs:
        vehicleDetails.append(VehicleDetails('','',row[0],''))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)