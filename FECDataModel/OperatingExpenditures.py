from FECDataModel.CodeMaps.AmendmentIndicatorMap import amendment_indicator_map
from FECDataModel.CodeMaps.DisbursementCategoryMap import disbursement_category_code_map
from FECDataModel.CodeMaps.EntityTypeMap import entity_type_map
from FECDataModel.CodeMaps.ReportTypeMap import report_type_map

from datetime import date

class OperatingExpenditures:
    def __init__(self, 
                 committee_id,
                 amendment_indicator_code,
                 report_year,
                 report_type_code,
                 image_number,
                 line_number,
                 form_type,
                 schedule_type,
                 payee_name,
                 city,
                 state,
                 zip_code,
                 transaction_date,
                 transaction_amount,
                 transaction_pgi,
                 purpose,
                 category,
                 disbursement_category_code,
                 memo_code,
                 memo_text,
                 entity_type_code,
                 fec_record_number,
                 file_number,
                 tran_id,
                 back_ref_tran_id):
        
        self.committee_id = committee_id

        # Amendment indicator code.
        if amendment_indicator_code in  amendment_indicator_map:
            amendment = amendment_indicator_map[amendment_indicator_code]
        else:
            amendment = amendment_indicator_code
        self.amendment_indicator = amendment

        self.report_year = report_year

        # Report type map.
        if report_type_code in report_type_map:
            report = report_type_map[report_type_code]
        else:
            report = report_type_code
        self.report_type = report

        self.image_number = image_number
        self.line_number = line_number
        self.form_type = form_type
        self.schedule_type = schedule_type
        self.payee_name = payee_name
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.transaction_date = transaction_date
        self.transaction_amount = transaction_amount
        self.transaction_primary_general_indicator = transaction_pgi
        self.purpose = purpose

        self.category = category

        # Disbursement Category Code Description
        if disbursement_category_code in disbursement_category_code_map:
            category_desc = disbursement_category_code_map[disbursement_category_code]
        else: 
            category_desc = disbursement_category_code
        self.disbursement_category_description = category_desc

        # Memo code.
        self.memo_code = memo_code
        if memo_code == 'X':
            memo_text = """'X' indicates that the amount is NOT to be included in the itemization total."""
        self.memo_text = memo_text

        # Entity type map.
        if entity_type_code in entity_type_map:
            entity_type = entity_type_map[entity_type_code]
        else:
            entity_type = entity_type_code
        self.entity_type = entity_type

        self.fec_record_number = fec_record_number # Sub ID
        self.file_number = file_number
        self.transaction_id = tran_id
        self.back_reference_transaction_id = back_ref_tran_id
    
    def printOperatingExpendature(self):
        print(self.committee_id)
        print(self.amendment_indicator)
        print(self.report_year)
        print(self.report_type)
        print(self.image_number)
        print(self.line_number)
        print(self.form_type)
        print(self.schedule_type)
        print(self.payee_name)
        print(self.city)
        print(self.state)
        print(self.zip_code)
        print(self.transaction_date)
        print(self.transaction_amount)
        print(self.transaction_primary_general_indicator)
        print(self.purpose)
        print(self.category)
        print(self.disbursement_category_description)
        print(self.memo_code)
        print(self.memo_text)
        print(self.entity_type)
        print(self.fec_record_number)
        print(self.file_number)
        print(self.transaction_id)
        print(self.back_reference_transaction_id)
        print()
        print()

    def __str__(self):
        return f"Operating Expenditure: {self.sub_id} - {self.committee_id} paid ${self.transaction_amount} to {self.payee_name} on {self.transaction_date} for {self.purpose}"