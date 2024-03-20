from datetime import datetime
import os      
import llm_generate
from flask import Flask, flash, request, redirect, render_template

app = Flask(__name__)
os.urandom(12)

# Allowed extension 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload_files", methods=["POST"])
def upload_files():
    brandModel = request.form.get('cars')
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
          if not allowed_file(file.filename):
            return "Received image file is not supported"
        
        llm_response = llm_generate.generateContent(brandModel,files)
  
        if llm_response[0]:
            print('car_details')
            print(llm_response[0])
        
        if llm_response:
            print('spare_parts')
            print(llm_response)
            return render_template('models.html',car_details=llm_response[0],spare_parts=llm_response)
        
        return "Sever response is not available."
        
    
@app.route("/")
def index():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    
    