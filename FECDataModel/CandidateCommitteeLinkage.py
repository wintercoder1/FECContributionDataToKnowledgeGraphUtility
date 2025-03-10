from FECDataModel.CodeMaps.CommitteeDesignationMap import committee_designation_code_map
from FECDataModel.CodeMaps.CommitteeTypeMap import committee_type_code_map

class CandidateCommitteeLinkage:

    def __init__(self, candidate_id, candidate_election_year, fec_election_year, committee_id, 
                 committee_type_code, committee_designation_code, linkage_id):
        
        self.candidate_id = candidate_id
        self.candidate_election_year = candidate_election_year
        self.fec_election_year = fec_election_year
        self.committee_id = committee_id

        # Committee type.
        if committee_type_code in committee_type_code_map:
            committee_type_text = committee_type_code_map[committee_type_code]
            self.committee_type = committee_type_text[0] + '    ' + committee_type_text[1]
        else:
            self.committee_type = committee_type_code

        # Committee designation.
        if committee_designation_code in  committee_designation_code_map:
            self.committee_designation =  committee_designation_code_map[committee_designation_code]
        else:
            self.committee_designation = committee_designation_code


        self.linkage_id = linkage_id