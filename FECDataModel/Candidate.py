from FECDataModel.CodeMaps.PoliticalPartyMap import political_party_code_map
from FECDataModel.CodeMaps.IncumbentChallengerStatusMap import incumbent_challenger_status_map

class Candidate:

    def __init__(self, candidate_id, name, party_affiliation_code, election_year, office_state, office_code, 
                 office_district, incumbent_challenger_status_code, candidate_status_code, principal_campaign_committee, last_updated = ''):
        self.id = candidate_id
        self.name = name

        split_name = name.split(', ')
        if len(split_name) >= 2:
            self.first_name = split_name[1]
            self.last_name = split_name[0]
        else:
            self.first_name = self.name
            self.last_name = ''
        
        
        if party_affiliation_code in political_party_code_map:
            political_party_name = political_party_code_map[party_affiliation_code]
        elif party_affiliation_code == 'C':
            political_party_name = 'Conservative'
        elif party_affiliation_code == 'D':
            political_party_name = 'Democrat'
        else:
            political_party_name = party_affiliation_code
        # print(party_affiliation_code)
        # print(political_party_code_map)
        # print(political_party_name )
        # print()

        self.political_party_affliiation = political_party_name
 
        self.election_year = election_year

        self.office_state = office_state
        office_name = ''
        if office_code in self.office_map:
            office = self.office_map[office_code]
        else:
            office = office_code
        # print(office_code)
        # print(self.office_map)
        # print(office_name )
        # print()
        self.candidate_office = office 
        self.office_district = office_district

        # print(incumbent_challenger_status_code)
        # print(self.incumbent_challenger_status_map)
        if incumbent_challenger_status_code in incumbent_challenger_status_map:
            incumbent_status = incumbent_challenger_status_map[incumbent_challenger_status_code]
        else:
            incumbent_status = str(incumbent_challenger_status_code)
        # print(incumbent_status)
        # print()
        
        self.incumbent_challenger_status = incumbent_status

        # print(candidate_status_code)
        # print(self.candidate_status_map)
        if candidate_status_code in self.candidate_status_map:
            candidate_status = self.candidate_status_map[candidate_status_code]
        else:
            candidate_status =  candidate_status_code
        # print(candidate_status)
        # print()
        
        self.candidate_status = candidate_status

        # The ID assigned by the Federal Election Commission to the candidate's principal campaign committee for a given election cycle
        self.principal_campaign_committee= principal_campaign_committee

        self.last_updated = ''

    office_map = {
        'H' : 'House',
        'P' : 'President',
        'S' : 'Senate'
    }

    candidate_status_map = {
        'C' : 'Statutory candidate',
        'F' : 'Statutory candidate for future election',
        'N' : 'Not yet a statutory candidate',
        'P' : 'Statutory candidate in prior cycle'
    }