class InsuranceResponse :
    
    def __init__(self,claimNumber,userId,claimDate,claimAmount,coverageAmount,licensePlate,
                 description,insurancePolicyStatus,insuranceCompany,insuranceNumber,insuranceExpiryDate,
                 includedCoverages,policyRenewalDate):
        self.claimNumber = claimNumber
        self.userId = userId
        self.claimDate = claimDate
        self.claimAmount = claimAmount
        self.coverageAmount = coverageAmount
        self.licensePlate = licensePlate
        self.description = description
        self.insurancePolicyStatus = insurancePolicyStatus
        self.insuranceCompany = insuranceCompany
        self.insuranceNumber = insuranceNumber
        self.insuranceExpiryDate = insuranceExpiryDate
        self.includedCoverages = includedCoverages
        self.policyRenewalDate = policyRenewalDate