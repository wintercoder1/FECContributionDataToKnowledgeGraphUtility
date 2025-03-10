from FECDataModel.CodeMaps.AmendmentIndicatorMap import amendment_indicator_map
from FECDataModel.CodeMaps.EntityTypeMap import entity_type_map
from FECDataModel.CodeMaps.ReportTypeMap import report_type_map
from FECDataModel.CodeMaps.TransactionTypeMap import transaction_type_map

from datetime import date

class CommitteeToCandidateContribution:
    def __init__(self, 
                 committee_id,
                 amendment_indicator_code,
                 report_type_code,
                 transaction_primary_general_indicator,
                 image_number,
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
                 other_other_candidate_or_committee_id,
                 candidate_id,
                 transaction_contribution_id,
                 file_number,
                 memo_code,
                 memo_text,
                 fec_record_number):
        
        self.committee_id = committee_id

        # Amendment indicator.
        if amendment_indicator_code in amendment_indicator_map:
            amendment_indicator = amendment_indicator_map[amendment_indicator_code ]
        else:
            amendment_indicator = amendment_indicator_code

        self.amendment_indicator = amendment_indicator

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

        # Parse image number or not? its not imprtant tbh.
        self.image_number = image_number

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

        # For other_id
        # For contributions from individuals this column is null. 
        # For contributions from candidates or other committees this 
        # column will contain the recipient's FEC ID.
        self.other_candidate_or_committee_id = other_other_candidate_or_committee_id

        self.candidate_id = candidate_id
        self.transaction_contribution_id = transaction_contribution_id
        self.file_number = file_number

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

        # SUB_ID https://www.fec.gov/campaign-finance-data/contributions-committees-candidates-file-description/
        self.fec_record_number = fec_record_number 

    def printContribution(self):
        print(self.committee_id)
        print(self.amendment_indicator)
        print(self.report_type)
        print(self.transaction_primary_general_indicator)
        print(self.primary_general_or_general_election)
        print(self.election_year)
        print(self.image_number)
        print(self.transaction_type )
        print(self.entity_type )
        print(self.contributor_name)
        print(self.city)
        print(self.state)
        print(self.zip_code)
        print(self.employer)
        print(self.occupation)
        print(self.transaction_date)
        print(self.transaction_amount)
        # for other_id
        # For contributions from individuals this column is null. 
        # For contributions from candidates or other committees this 
        # column will contain the recipient's FEC ID.
        print(self.other_candidate_or_committee_id)
        print(self.candidate_id)
        print(self.transaction_contribution_id)
        print(self.file_number)
        print(self.memo_code)
        print(self.memo_text)
        print(self.fec_record_number)
        print()
        print()

    def __str__(self):
        return f"Committee-to-Candidate Contribution: {self.sub_id} - {self.contributor_name} ({self.committee_id}) contributed ${self.transaction_amount} to candidate {self.candidate_id} on {self.transaction_date}"