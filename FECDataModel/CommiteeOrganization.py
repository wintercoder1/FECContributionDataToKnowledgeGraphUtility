from FECDataModel.CodeMaps.CommitteeDesignationMap import committee_designation_code_map
from FECDataModel.CodeMaps.CommitteeTypeMap import committee_type_code_map
from FECDataModel.CodeMaps.PoliticalPartyMap import political_party_code_map

class CommitteeOrganization:
    
    def __init__(self, committee_id, committee_name, treasurer_name, address, committee_designation_code, 
                 committee_type_code, party_affiliation_code, filing_frequency_code='', 
                 interest_group_category_code='', connected_organization_name='', candidate_id=''):
        
        self.id = committee_id
        self.name = committee_name
        self.treasurer_name = treasurer_name
        self.address = address

        # Committee designation.
        if committee_designation_code in committee_designation_code_map:
            self.committee_designation = committee_designation_code_map[committee_designation_code]
        else:
            self.committee_designation = committee_designation_code


        # Committee type.
        if committee_type_code in committee_type_code_map:
            committee_type_text = committee_type_code_map[committee_type_code]
            self.committee_type = committee_type_text[0] + '    ' + committee_type_text[1]
        else:
            self.committee_type = committee_type_code
        
        # Political party affiliation.
        if party_affiliation_code in political_party_code_map:
            political_party_name = political_party_code_map[party_affiliation_code]
        elif party_affiliation_code == 'C':
            political_party_name = 'Conservative'
        elif party_affiliation_code == 'D':
            political_party_name = 'Democrat'
        else:
            political_party_name = party_affiliation_code
        self.committee_political_party_affliiation = political_party_name

        # Filing frequency.
        if filing_frequency_code in self.filing_frequency_map:
            filing_frequency = self.filing_frequency_map[filing_frequency_code]
        else:
            filing_frequency = self.filing_frequency_map[filing_frequency_code]
        
        self.filing_frequency = filing_frequency

        # Interest group.
        if interest_group_category_code in self.interest_group_category_map:
            interest_group_category = self.interest_group_category_map[interest_group_category_code]
            self.interest_group_category = interest_group_category
        else:
            self.interest_group_category = interest_group_category_code

        self.connected_organization_name = connected_organization_name
        self.candidate_id = candidate_id
    
    def printCommittee(self):
        print(self.id)
        print(self.name)
        print(self.treasurer_name)
        print(self.address)
        print(self.committee_designation)
        print(self.committee_type)
        print(self.committee_political_party_affliiation)
        print(self.filing_frequency)
        print(self.interest_group_category)
        print(self.connected_organization_name)
        print(self.candidate_id)
        print()

    # committee_designation_code_map = {
    #     'A' :  'Authorized by a candidate',
    #     'B' :  'Lobbyist/Registrant PAC',
    #     'D' :  'Leadership PAC',
    #     'J' :  'Joint fundraiser',
    #     'P' :  'Principal campaign committee of a candidate',
    #     'U' :  'Unauthorized'
    # }

    # committee_type_code_map = {
    #     'C' :	['Communication cost',	'Organizations like corporations or unions may prepare communications for their employees or members that advocate the election of specific candidates and they must disclose them under certain circumstances. These are usually paid with direct corporate or union funds rather than from PACs.'], 
    #     'D' :	['Delegate committee',	'Delegate committees are organized for the purpose of influencing the selection of delegates to Presidential nominating conventions. The term includes a group of delegates, a group of individuals seeking to become delegates, and a group of individuals supporting delegates.'],
    #     'E' :	['Electioneering communication',	'Groups (other than PACs) making electioneering communications'],
    #     'H' :	['House',	'	Campaign committees for candidates for the U.S. House of Representatives'],
    #     'I' :	['Independent expenditor (person or group)',	'	Individuals or groups (other than PACs) making independent expenditures over $250 in a year must disclose those expenditures'],
    #     'N' :	['PAC - nonqualified',	'	PACs that have not yet been in existence for six months and received contributions from 50 people and made contributions to five federal candidates. These committees have lower limits for their contributions to candidates.'],
    #     'O' :	['Independent expenditure-only (Super PACs)',	'	Political Committee that has filed a statement consistent with AO 2010-09 or AO 2010-11.'],
    #     'P' :	['Presidential',	'	Campaign committee for candidate for U.S. President'],
    #     'Q' :	['PAC - qualified	',	'PACs that have been in existence for six months and received contributions from 50 people and made contributions to five federal candidates'],
    #     'S' :	['Senate',	'	Campaign committee for candidate for Senate'],
    #     'U' :	['Single-candidate independent expenditure',	''],
    #     'V' :	['	Hybrid PAC (with Non-Contribution Account) - Nonqualified',	'	Political committees with non-contribution accounts'],
    #     'W' :	['	Hybrid PAC (with Non-Contribution Account) - Qualified',	'	Political committees with non-contribution accounts'],
    #     'X' :	['	Party - nonqualified',	'	Party committees that have not yet been in existence for six months and received contributions from 50 people, unless they are affiliated with another party committee that has met these requirements.'],
    #     'Y' :	['	Party - qualified',	'	Party committees that have existed for at least six months and received contributions from 50 people or are affiliated with another party committee that meets these requirements.'],
    #     'Z' :	['	National party nonfederal account',	''] 
    # }

    interest_group_category_map = {
        'C' : 'Corporation',
        'L' : 'Labor organization',
        'M' : 'Membership organization',
        'T' : 'Trade association',
        'V' : 'Cooperative',
        'W' : 'Corporation without capital stock'
    }


    




    