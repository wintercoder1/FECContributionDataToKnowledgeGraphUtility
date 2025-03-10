from FECDataModel.CodeMaps.AmendmentIndicatorMap import amendment_indicator_map
from FECDataModel.CodeMaps.EntityTypeMap import entity_type_map
from FECDataModel.CodeMaps.ReportTypeMap import report_type_map
from FECDataModel.CodeMaps.TransactionTypeMap import transaction_type_map

from datetime import date

class CommitteeToOtherCommitteeContribution:
    def __init__(self, 
                 committee_id,
                 amendment_indicator_code,
                 report_type_code,
                 transaction_primary_general_indicator,
                 image_num,
                 transaction_type_code,
                 entity_type_code,
                 name,
                 city,
                 state,
                 zip_code,
                 employer,
                 occupation,
                 transaction_date,
                 transaction_amount,
                 other_committee_id,
                 transaction_contribution_id,
                 file_num,
                 memo_code,
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

        # Parse transaction primary general indicator number.
        self.transaction_primary_general_indicator = transaction_primary_general_indicator
        # Check if its subscriptable.
        if transaction_primary_general_indicator and hasattr(transaction_primary_general_indicator, "__getitem__"):
            self.primary_general_or_general_election = transaction_primary_general_indicator[:1]
            self.election_year = transaction_primary_general_indicator[1:]
        else:
            self.primary_general_or_general_election = ''
            self.election_year = ''

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

        self.name = name
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.employer = employer
        self.occupation = occupation

        self.transaction_date = transaction_date
        self.transaction_amount = transaction_amount
        self.other_committee_id = other_committee_id
        
        self.transaction_contribution_id = transaction_contribution_id
        self.file_number = file_num

        # Memo code.
        self.memo_code = memo_code
        if memo_code == 'X':
            memo_text = """'X' indicates that the amount of the transaction is not incorporated 
                        into the total figure disclosed on the detailed summary page of the 
                        committee’s report. 'X' may also indicate that the amount was received as 
                        part of a joint fundraising transfer or other lump sum contribution 
                        required to be attributed to individual contributors. Memo items may be 
                        used to denote that a transaction was previously reported or in the case 
                        of an independent expenditure, that the amount represents activity that 
                        has occurred but has not yet been paid by the committee. When using the 
                        bulk data file these memo items should be included in your analysis."""
        self.memo_text = memo_text

        # SUB_ID on https://www.fec.gov/campaign-finance-data/any-transaction-one-committee-another-file-description/
        self.fec_record_number = fec_record_number 

    def printContribution(self):
        print(f"self.committee_id {self.committee_id}")
        # print(self.amendment_indicator)
        # print(self.report_type)
        # print(self.transaction_primary_general_indicator)
        # print(self.primary_general_or_general_election)
        # print(self.election_year)
        # print(self.image_number)
        # print(self.transaction_type)
        # print(self.entity_type)
        # print(self.name)
        # print(self.city)
        # print(self.state)
        # print(self.zip_code)
        # print(self.employer)
        # print(self.occupation)
        # print(self.transaction_date)
        # print(self.transaction_amount)
        print(f"self.other_committee_id {self.other_committee_id}")
        print(f"self.transaction_contribution_id {self.transaction_contribution_id}")
        # print(self.file_number)
        # print(self.memo_code)
        # print(self.memo_text)
        # print(self.fec_record_number)
        print()

    def __str__(self):
        return f"Other Transaction: {self.sub_id} - {self.transaction_type} ${self.transaction_amount} between {self.committee_id} and {self.other_id or 'N/A'} on {self.transaction_date}"