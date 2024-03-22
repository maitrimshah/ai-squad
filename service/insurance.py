app = Flask(__name__)
from flask import Flask, jsonify
import InsuranceResponse

@app.route('/submitClaim', methods=['POST'])
def submitClaim(request):    
    
    bigDataQuery = "insert into cap-ai-squad.SQUAD_DS.claims_info (User_Id,Claim_Date,Claim_Amount,Coverage_Amount,License_Plate,Description,Insurance_Policy_Status,Insurance_Company,Insurance_Number,Insurance_Expiry_Date,Included_Coverages,Policy_Renewal_Date) VALUES ( '" + request.User_Id + "','" + request.Claim_Date + "','" + request.Claim_Amount + "','" + request.Coverage_Amount+ "','" +request.License_Plate+ "','" +request.Description+ "','" +request.Insurance_Policy_Status+ "','" +request.Insurance_Company+ "','" +request.Insurance_Number+ "','" +request.Insurance_Expiry_Date+ "','" +request.Included_Coverages+ "','" +request.Policy_Renewal_Date+ "')" 
  
    client = bigquery.Client()
    query_job = client.query(bigDataQuery)  
    
    spares_details = query_job.result() 
    rows = query_job.result()  
    
    user_details = []
    for row in user_details:
        user_details.append(InsuranceResponse(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]))
        d1 = datetime.strptime(row[10], "%Y/%m/%d")
        d2 = datetime.strptime(datetime.datetime.now(), "%Y/%m/%d")
        if d2-d1 < 0 :
            msg = "Policy has already expired" 
        else :
            msg = "Claim details added successfully" + "Policy renewal date is " + row[12]
            
    return render_template('models.html',msg=msg)

if __name__ == '__main__':
    app.run(debug=True)