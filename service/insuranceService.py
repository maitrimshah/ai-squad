app = Flask(__name__)
from flask import Flask, jsonify
import InsuranceResponse
    
@app.route("/raiseClaim",methods=["POST"])
def raiseClaim():
    totalSparesCost = request.form.get('totalSparesCost')
    return render_template('raiseClaim.html',totalSparesCost=totalSparesCost)

@app.route('/submitClaim', methods=['POST'])
def submitClaim(request):    
    
    bigDataQuery = "insert into cap-ai-squad.SQUAD_DS.claims_info (Claim Number,User Id,Claim Date,Claim Amount,Coverage Amount,License Plate,Description,Insurance Policy Status,Insurance Company,Insurance Number,Insurance Expiry Date,Included Coverages,Policy Renewal Date) VALUES ( '" + request.User_Id + "','" + request.claimDate + "','" + request.claimAmount + "','" + request.coverageAmount+ "','" +request.licensePlate+ "','" +request.description+ "','" +request.insurancePolicyStatus+ "','" +request.insuranceCompany+ "','" +request.insuranceNumber+ "','" +request.insuranceExpiryDate+ "','" +request.includedCoverages+ "','" +request.policyRenewalDate+ "')" 
  
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