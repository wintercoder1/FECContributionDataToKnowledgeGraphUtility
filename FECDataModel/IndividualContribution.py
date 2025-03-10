from FECDataModel.CodeMaps.AmendmentIndicatorMap import amendment_indicator_map
from FECDataModel.CodeMaps.EntityTypeMap import entity_type_map
from FECDataModel.CodeMaps.ReportTypeMap import report_type_map
from FECDataModel.CodeMaps.TransactionTypeMap import transaction_type_map

class IndividualContribution:
    def __init__(self, 
                 committee_id,
                 amendment_indicator_code,
                 report_type_code,
                 transaction_pgi,
                 image_num,
                 transaction_type_code,
                 entity_type_code,
                 contributor_name,
                 city,
                 state,
                 zip_code,
                 employer,
                 occupation,
                 transaction_date,
                 transaction_amount,
                 other_id,
                 tran_id,
                 file_num,
                 memo_cd,
                 memo_text,
                 fec_record_number):
        
        self.committee_id = committee_id

        # Amendment indicator code.
        if amendment_indicator_code in  amendment_indicator_map:
            amendment = amendment_indicator_map[amendment_indicator_code]
        else:
            amendment = amendment_indicator_code
        self.amendment_indicator = amendment

        # Report type map.
        if report_type_code in report_type_map:
            report = report_type_map[report_type_code]
        else:
            report = report_type_code
        self.report_type = report
        
        self.transaction_primary_general_indicator = transaction_pgi
        self.image_number = image_num

        # Transaction type map.
        if transaction_type_code in transaction_type_map:
            transaction_type = transaction_type_map[transaction_type_code]
        else:
            transaction_type = transaction_type_code
        self.transaction_type = transaction_type

        # Entity type map.
        if entity_type_code in entity_type_map:
            entity_type = entity_type_map[entity_type_code]
        else:
            entity_type = entity_type_code
        self.entity_type = entity_type

        self.contributor_name = contributor_name
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.employer = employer
        self.occupation = occupation
        self.transaction_date = transaction_date
        self.transaction_amount = transaction_amount
        self.other_id = other_id
        self.transaction_id = tran_id
        self.file_number = file_num
        self.memo_code = memo_cd
        self.memo_text = memo_text
        self.fec_record_number = fec_record_number
    
    def printContribution(self):
        print(self.committee_id )
        print(self.amendment_indicator)
        print(self.report_type)
        print(self.transaction_primary_general_indicator)
        print(self.image_number)
        print(self.transaction_type)
        print(self.entity_type)
        print(self.contributor_name)
        print(self.city)
        print(self.state)
        print(self.zip_code)
        print(self.employer)
        print(self.occupation)
        print(self.transaction_date)
        print(self.transaction_amount)
        print(self.other_id )
        print(self.transaction_id)
        print(self.file_number)
        print(self.memo_code )
        print(self.memo_text)
        print(self.fec_record_number)
        print()
        print()

    def __str__(self):
        return f"Contribution: {self.fec_record_number} - {self.contributor_name} contributed ${self.transaction_amount} to committee {self.committee_id} on {self.transaction_date}"
    
# class IndividualContribution:

#     def __init__(self, transaction_id: int, amount: int, to_organization: IndividualContribution, from_individual: Individual, memo = ''):
#         self.id = transaction_id
#         self.amount = amount
#         self.to_organization = to_organization
#         self.from_individual = from_individual
#         self.memo = memo

#     def __str__(self):
#         str = f"{self.from_individual.name} contributed {self.amount} to the organization {self.to_organization.id}"
#         return str