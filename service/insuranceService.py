app = Flask(__name__)
from flask import Flask, jsonify
import InsuranceResponse
    
@app.route('/fetchUserDetails', methods=['POST'])
def fetchUserDetails(request):    
    
    bigDataQuery = "insert into cap-ai-squad.SQUAD_DS.users_info (User_Id,Vehicle_Type,Type_Of_Damage,Date_Of_Accident,Car_Model_Name,Car_Brand_Name,Vehicle_Registration_Number,Policy_Holder_FirstName,Policy_Holder_LastName,License_Plate,Mobile_Number,Email_Address,PAN,Birth_Date) VALUES ( '" + request.User_Id + "','" + request.Vehicle_Type + "','" + request.Type_Of_Damage + "','" + request.Date_Of_Accident+ "','" +request.Car_Model_Name+ "','" +request.Car_Brand_Name+ "','" +request.Vehicle_Registration_Number+ "','" +request.Policy_Holder_FirstName+ "','" +request.Policy_Holder_LastName+ "','" +request.License_Plate+ "','" +request.Mobile_Number,request.Email_Address+ "','" +request.PAN+ "','" +request.Birth_Date+ "')" 
  
    client = bigquery.Client()
    query_job = client.query(bigDataQuery)  # API request
    
    spares_details = query_job.result()  # Waits for query to finish
    rows = query_job.result()  # Waits for query to finish
    
    user_details = []
    for row in user_details:
        user_details.append(UserDetais(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14]))
    
    ############################ TO DO     ##########################
    # add later the logic to check whether it is a valid claim or not
    ############################ TO DO     ##########################
    
    return user_details;

if __name__ == '__main__':
    app.run(debug=True)