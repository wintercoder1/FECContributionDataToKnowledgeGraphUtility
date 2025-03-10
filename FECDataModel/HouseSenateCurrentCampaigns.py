from FECDataModel.CodeMaps.IncumbentChallengerStatusMap import incumbent_challenger_status_map
from FECDataModel.CodeMaps.PoliticalPartyMap import political_party_code_map

class HouseSenateCurrentCampaigns:

    def __init__(self, candidate_id, name, incumbent_challenger_status_code, party_cd, party_affiliation_code,
                ttl_receipts, trans_from_auth, ttl_disb, trans_to_auth,
                coh_bop, coh_cop, cand_contrib, cand_loans, other_loans,
                cand_loan_repay, other_loan_repay, debts_owed_by, ttl_indiv_contrib,
                cand_office_st, cand_office_district, spec_election, prim_election,
                run_election, gen_election, gen_election_percent, other_pol_cmte_contrib,
                pol_pty_contrib, cvg_end_dt, indiv_refunds, cmte_refunds):
        
        self.candidate_id = candidate_id
        self.name = name

        # Incumbent challenger status.
        if incumbent_challenger_status_code in incumbent_challenger_status_map:
            incumbent_status = incumbent_challenger_status_map[incumbent_challenger_status_code]
        else:
            incumbent_status = str(incumbent_challenger_status_code)
        self.incumbent_challenger_status = incumbent_status

        self.party_code = party_cd 

        if party_affiliation_code in political_party_code_map:
            party_affiliation = political_party_code_map[party_affiliation_code]
        else: 
            party_affiliation = party_affiliation_code
        self.party_affiliation = party_affiliation

        self.total_receipts = ttl_receipts
        self.trans_from_auth = trans_from_auth
        self.total_disbursements = ttl_disb 
        self.trans_to_auth = trans_to_auth
        self.cash_on_hand_begining = coh_bop
        self.cash_on_hand_end = coh_cop 
        self.cand_contrib = cand_contrib
        self.cand_loans = cand_loans
        self.other_loans = other_loans
        self.cand_loan_repay = cand_loan_repay
        self.other_loan_repay = other_loan_repay
        self.debts_owed_by = debts_owed_by
        self.ttl_indiv_contrib = ttl_indiv_contrib
        self.cand_office_st = cand_office_st
        self.cand_office_district = cand_office_district
        self.spec_election = spec_election
        self.prim_election = prim_election
        self.run_election = run_election 
        self.gen_election = gen_election
        self.gen_election_percent = gen_election_percent
        self.other_pol_cmte_contrib = other_pol_cmte_contrib
        self.pol_pty_contrib = pol_pty_contrib
        self.cvg_end_dt = cvg_end_dt
        self.indiv_refunds = indiv_refunds
        self.cmte_refunds = cmte_refunds

    def printCampaign(self):
        print(self.candidate_id)
        print(self.name)
        print(self.incumbent_challenger_status)
        print(self.party_cd)
        print(self.party_affiliation)
        print(self.total_receipts)
        print(self.trans_from_auth)
        print(self.ttl_disb)
        print(self.trans_to_auth)
        print(self.coh_bop)
        print(self.coh_cop)
        print(self.cand_contrib)
        print(self.cand_loans)
        print(self.other_loans)
        print(self.cand_loan_repay)
        print(self.other_loan_repay)
        print(self.debts_owed_by)
        print(self.ttl_indiv_contrib)
        print(self.cand_office_st)
        print(self.cand_office_district)
        print(self.spec_election)
        print(self.prim_election)
        print(self.run_election)
        print(self.gen_election)
        print(self.gen_election_percent)
        print(self.other_pol_cmte_contrib)
        print(self.pol_pty_contrib)
        print(self.cvg_end_dt)
        print(self.indiv_refunds)
        print(self.cmte_refunds)
        print()
        print()