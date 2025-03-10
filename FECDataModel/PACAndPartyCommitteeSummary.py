from FECDataModel.CodeMaps.CommitteeDesignationMap import committee_designation_code_map
from FECDataModel.CodeMaps.CommitteeTypeMap import committee_type_code_map
from FECDataModel.CodeMaps.FilingFrequencyMap import filing_frequency_map

class PACAndPartyCommitteeSummary:
    def __init__(self, 
                 committee_id, 
                 committee_name, 
                 committee_type_code, 
                 committee_designation_code, 
                 committee_filing_freq_code,
                 total_receipts,
                 trans_from_aff,
                 indv_contrib,
                 other_pol_cmte_contrib,
                 cand_contrib,
                 cand_loans,
                 ttl_loans_received,
                 ttl_disb,
                 tranf_to_aff,
                 indv_refunds,
                 other_pol_cmte_refunds,
                 cand_loan_repay,
                 loan_repay,
                 coh_bop,
                 coh_cop,
                 debts_owed_by,
                 nonfed_trans_received,
                 contrib_to_other_cmte,
                 ind_exp,
                 pty_coord_exp,
                 nonfed_share_exp,
                 cvg_end_dt):
        
        self.committee_id = committee_id
        self.committee_name = committee_name

        if committee_type_code in committee_type_code_map:
            committee_type = committee_type_code_map[committee_type_code]
        else:
            committee_type = committee_type_code
        self.committee_type = committee_type

        if committee_designation_code in committee_designation_code_map:
            committee_designation = committee_designation_code_map[committee_designation_code]
        else:
            committee_designation = committee_designation_code
        self.committee_designation = committee_designation

        if committee_filing_freq_code in filing_frequency_map:
            committee_filing_freq = filing_frequency_map[committee_filing_freq_code]
        else:
            committee_filing_freq = committee_filing_freq_code
        self.committee_filing_freq = committee_filing_freq

        self.total_receipts = total_receipts
        self.trans_from_aff = trans_from_aff
        self.indv_contrib = indv_contrib
        self.other_pol_cmte_contrib = other_pol_cmte_contrib
        self.cand_contrib = cand_contrib
        self.cand_loans = cand_loans
        self.ttl_loans_received = ttl_loans_received
        self.ttl_disb = ttl_disb
        self.tranf_to_aff = tranf_to_aff
        self.indv_refunds = indv_refunds
        self.other_pol_cmte_refunds = other_pol_cmte_refunds
        self.cand_loan_repay = cand_loan_repay
        self.loan_repay = loan_repay
        self.coh_bop = coh_bop
        self.coh_cop = coh_cop
        self.debts_owed_by = debts_owed_by
        self.nonfed_trans_received = nonfed_trans_received
        self.contrib_to_other_cmte = contrib_to_other_cmte
        self.ind_exp = ind_exp
        self.pty_coord_exp = pty_coord_exp
        self.nonfed_share_exp = nonfed_share_exp
        self.cvg_end_dt = cvg_end_dt
    
    def printSummary(self):
        print(self.committee_id)
        print(self.committee_name)
        print(self.committee_type)
        print(self.committee_designation )
        print(self.committee_filing_freq)
        print(self.total_receipts)
        print(self.trans_from_aff)
        print(self.indv_contrib)
        print(self.other_pol_cmte_contrib)
        print(self.cand_contrib)
        print(self.cand_loans)
        print(self.ttl_loans_received)
        print(self.ttl_disb)
        print(self.tranf_to_aff)
        print(self.indv_refunds)
        print(self.other_pol_cmte_refunds)
        print(self.cand_loan_repay)
        print(self.loan_repay)
        print(self.coh_bop)
        print(self.coh_cop)
        print(self.debts_owed_by)
        print(self.nonfed_trans_received)
        print(self.contrib_to_other_cmte )
        print(self.ind_exp)
        print(self.pty_coord_exp)
        print(self.nonfed_share_exp)
        print(self.cvg_end_dt)
        print()
        print()

    def __str__(self):
        return f"Committee: {self.committee_name} ({self.committee_id}) - Type: {self.committee_type}"