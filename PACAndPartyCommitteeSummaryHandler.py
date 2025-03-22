from FECDataModel.PACAndPartyCommitteeSummary import PACAndPartyCommitteeSummary
from Handler import Handler
from decimal import Decimal

from typing import List

class PACAndPartyCommitteeSummaryHandler(Handler):

    DATA_DIRECTORY = '/Users/steve/Documents/Dev/DEICheck.ai-LLM-RAG/FECData/manual/pac_and_party_committee_summary'
    TEST_DATA_DIRECTORY = DATA_DIRECTORY + '/2023-2024/'
    TEST_DATA_FILE_PATH = TEST_DATA_DIRECTORY + '/PACSummary-2023-2024.txt'
    
    def processFiles(self):
        self.processFileInFolder()

    def processFileInFolder(self):
        # process files within folder
        committees_list = self.parseTextFileWithSeperator(self.TEST_DATA_FILE_PATH, '|') 

        self.batchUploadPACAndCommitteeSummaryToGraphDB(committees_list)
        return
    
    def parseTextFileWithSeperator(self, text_file_path:str, seperator: str) -> list[PACAndPartyCommitteeSummary]:
        f = open(text_file_path, "r")
        print(f)

        text_file = f.read()
        file_rows = text_file.splitlines()
        print(len(file_rows))
    
        committees_so_far = 0
        total_committees = len(file_rows)
        committees_list = []
        i = 0
        for one_row in file_rows:
            if len(one_row) < 27:  # We expect 27 columns based on the spec
                    print(f"Warning: Row has insufficient columns ({len(one_row)}). Skipping row.")
                    continue
            
            columns = one_row.split(seperator)
            # print(columns)

            committee_id = columns[0]
            committee_name = columns[1] if len(columns[1].strip()) > 0 else None
            committee_type_code = columns[2] if len(columns[2].strip()) > 0 else None
            committee_designation_code = columns[3] if len(columns[3].strip()) > 0 else None
            committee_filing_freq_code = columns[4] if len(columns[4].strip()) > 0 else None
            total_receipts = columns[5]
            trans_from_aff = columns[6]
            indv_contrib = columns[7]
            other_pol_cmte_contrib = columns[8]
            cand_contrib = columns[9]
            cand_loans = columns[10]
            ttl_loans_received = columns[11]
            ttl_disb = columns[12]
            tranf_to_aff = columns[13]
            indv_refunds = columns[14]
            other_pol_cmte_refunds = columns[15]
            cand_loan_repay = columns[16]
            loan_repay = columns[17]
            coh_bop = columns[18]
            coh_cop = columns[19]
            debts_owed_by = columns[20]
            nonfed_trans_received = columns[21]
            contrib_to_other_cmte = columns[22]
            ind_exp = columns[23]
            pty_coord_exp = columns[24]
            nonfed_share_exp = columns[25]
            cvg_end_dt = columns[26]
            
            # Create the PACAndPartyCommitteeSummary object
            committee_data = PACAndPartyCommitteeSummary(
                committee_id, committee_name, committee_type_code, committee_designation_code, committee_filing_freq_code,
                total_receipts, trans_from_aff, indv_contrib, other_pol_cmte_contrib,
                cand_contrib, cand_loans, ttl_loans_received, ttl_disb,
                tranf_to_aff, indv_refunds, other_pol_cmte_refunds, cand_loan_repay,
                loan_repay, coh_bop, coh_cop, debts_owed_by, nonfed_trans_received,
                contrib_to_other_cmte, ind_exp, pty_coord_exp, nonfed_share_exp, cvg_end_dt
            )
            
            committees_list.append(committee_data)
            # committee_data.printSummary()

            committees_so_far += 1
            i += 1
            if committees_so_far % 100 == 0:
                print(f"From the text file processed {committees_so_far}/{total_committees} PAC/party committee records")
        
        if committees_so_far == total_committees:
                print(f"From the text file processed {committees_so_far}/{total_committees} PAC/party committee records")

        return committees_list
    
    def batchUploadPACAndCommitteeSummaryToGraphDB(self, pac_committee_summary_list: List[PACAndPartyCommitteeSummary], batch_size: int = 1000):
        # Use Neo4J graph DB python driver.
        print('  ' + str(self.neo4j_driver))
        total_pac_committee_summaries = len(pac_committee_summary_list)
        processed = 0
        with self.neo4j_driver.session() as session:
            # Process committees in batches
            for i in range(0, total_pac_committee_summaries, batch_size):
                batch = pac_committee_summary_list[i:i + batch_size]
                
                for pac_committee_summary in batch:
                    try:
                        # Create the Committee node
                        session.execute_write(self._create_PACOrComitteeSummary, pac_committee_summary)

                        processed += 1
                        if processed % 100 == 0:
                            print(f"Processed {processed}/{total_pac_committee_summaries} PACAndCommitteeSummaries")
                                    
                    except Exception as e:
                        print(f"Error processing committee {pac_committee_summary.committee_id}: {str(e)}")

        print(f"Completed uploading {processed}/{total_pac_committee_summaries} PACAndCommitteeSummaries")
        return

    def _create_PACOrComitteeSummary(self, tx, committee_data):
        """Create or merge a PAC or Party Committee node with summary data."""
        query = """
        MERGE (committee:PACAndPartyCommittee {id: $committee_id})
        SET committee.committee_id = $committee_id,
            committee.committee_name = $committee_name,
            committee.committee_type = $committee_type,
            committee.committee_designation = $committee_designation,
            committee.committee_filing_freq = $committee_filing_freq,
            committee.total_receipts = $total_receipts,
            committee.trans_from_affiliates = $trans_from_aff,
            committee.individual_contributions = $indv_contrib,
            committee.other_political_committee_contributions = $other_pol_cmte_contrib,
            committee.candidate_contributions = $cand_contrib,
            committee.candidate_loans = $cand_loans,
            committee.total_loans_received = $ttl_loans_received,
            committee.total_disbursements = $ttl_disb,
            committee.transfers_to_affiliates = $tranf_to_aff,
            committee.refunds_to_individuals = $indv_refunds,
            committee.refunds_to_other_political_committees = $other_pol_cmte_refunds,
            committee.candidate_loan_repayments = $cand_loan_repay,
            committee.loan_repayments = $loan_repay,
            committee.cash_beginning_of_period = $coh_bop,
            committee.cash_close_of_period = $coh_cop,
            committee.debts_owed_by = $debts_owed_by,
            committee.nonfederal_transactions_received = $nonfed_trans_received,
            committee.contributions_to_other_committees = $contrib_to_other_cmte,
            committee.independent_expenditures = $ind_exp,
            committee.party_coordinated_expenditures = $pty_coord_exp,
            committee.nonfederal_share_expenditures = $nonfed_share_exp,
            committee.coverage_end_date = $cvg_end_dt,
            committee.last_updated = datetime()
        RETURN committee
        """
        result = tx.run(query,
                    committee_id=committee_data.committee_id,
                    committee_name=committee_data.committee_name,
                    committee_type=committee_data.committee_type,
                    committee_designation=committee_data.committee_designation,
                    committee_filing_freq=committee_data.committee_filing_freq,
                    total_receipts=committee_data.total_receipts,
                    trans_from_aff=committee_data.trans_from_aff,
                    indv_contrib=committee_data.indv_contrib,
                    other_pol_cmte_contrib=committee_data.other_pol_cmte_contrib,
                    cand_contrib=committee_data.cand_contrib,
                    cand_loans=committee_data.cand_loans,
                    ttl_loans_received=committee_data.ttl_loans_received,
                    ttl_disb=committee_data.ttl_disb,
                    tranf_to_aff=committee_data.tranf_to_aff,
                    indv_refunds=committee_data.indv_refunds,
                    other_pol_cmte_refunds=committee_data.other_pol_cmte_refunds,
                    cand_loan_repay=committee_data.cand_loan_repay,
                    loan_repay=committee_data.loan_repay,
                    coh_bop=committee_data.coh_bop,
                    coh_cop=committee_data.coh_cop,
                    debts_owed_by=committee_data.debts_owed_by,
                    nonfed_trans_received=committee_data.nonfed_trans_received,
                    contrib_to_other_cmte=committee_data.contrib_to_other_cmte,
                    ind_exp=committee_data.ind_exp,
                    pty_coord_exp=committee_data.pty_coord_exp,
                    nonfed_share_exp=committee_data.nonfed_share_exp,
                    cvg_end_dt=committee_data.cvg_end_dt)
        return result.single()
    
    def __init__(self):
        super(PACAndPartyCommitteeSummaryHandler, self).__init__('pac_party_committee_summary')