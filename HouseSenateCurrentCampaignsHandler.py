from FECDataModel.HouseSenateCurrentCampaigns import HouseSenateCurrentCampaigns
from Handler import Handler

from typing import List

class HouseSenateCurrentCampaignsHandler(Handler):

    DATA_DIRECTORY = '/Users/steve/Documents/Dev/DEICheck.ai-LLM-RAG/FECData/manual/house_senate_current_campaigns'
    TEST_DATA_DIRECTORY = DATA_DIRECTORY + '/2023-2024/'
    # TEST_DATA_FILE_PATH = TEST_DATA_DIRECTORY + '/weball24-2.txt'
    TEST_DATA_FILE_PATH = TEST_DATA_DIRECTORY + '/house-senate-current-campaigns-2023-2024.txt'
    
    def processFiles(self):
        self.processFileInFolder()

    def processFileInFolder(self):
        # process files within folder
        campaigns_list = self.parseTextFileWithSeperator(self.TEST_DATA_FILE_PATH, '|') 

        self.batchUploadCampaignsToGraphDB(campaigns_list)

        return
    
    def parseTextFileWithSeperator(self, text_file_path:str, seperator: str) -> list[HouseSenateCurrentCampaigns]:
        f = open(text_file_path, "r")
        print(f)

        text_file = f.read()
        # print(text_file.read())
        file_rows = text_file.splitlines()
        # print(file_rows)
        print(len(file_rows))
    
        campaigns_so_far = 0
        total_campaigns = len(file_rows)
        campaigns_list = []
        i = 0
        for one_row in file_rows:
            # if i > 8:
            #     break

            if len(one_row) < 28:  # We expect 30 columns based on the spec
                    print(f"Warning: Row has insufficient columns ({len(one_row)}). Skipping row.")
                    continue
            
            # print(one_row)
            columns = one_row.split(seperator)
            # print(columns)

            candidate_id = columns[0]
            name = columns[1] if len(columns[1].strip()) > 0 else None
            incumbent_challenger_status = columns[2] if len(columns[2].strip()) > 0 else None
            party_code = columns[3] if len(columns[3].strip()) > 0 else None
            party_affiliation = columns[4] if len(columns[4].strip()) > 0 else None
            ttl_receipts = columns[5]
            trans_from_auth = columns[6]
            ttl_disb = columns[7]
            trans_to_auth = columns[8]
            coh_bop = columns[9]
            coh_cop =  columns[10]
            cand_contrib = columns[11]
            cand_loans = columns[12]
            other_loans = columns[13]
            cand_loan_repay = columns[14]
            other_loan_repay = columns[15]
            debts_owed_by = columns[16]
            ttl_indiv_contrib = columns[17]
            cand_office_st = columns[18] if len(columns[18].strip()) > 0 else None
            cand_office_district = columns[19] if len(columns[19].strip()) > 0 else None
            spec_election = columns[20] if len(columns[20].strip()) > 0 else None
            prim_election = columns[21] if len(columns[21].strip()) > 0 else None
            run_election = columns[22] if len(columns[22].strip()) > 0 else None
            gen_election = columns[23] if len(columns[23].strip()) > 0 else None
                
            # Handle gen_election_percent specially as it's a percentage
            gen_election_percent = None
            if columns[24] and columns[24].strip():
                try:
                    gen_election_percent = columns[24]
                except:
                    gen_election_percent = None
            
            other_pol_cmte_contrib = columns[25]
            pol_pty_contrib = columns[26]
            cvg_end_dt =  columns[27] # cvg_end_dt = parse_date(row[27]) if we want datetime and not string date.
            indiv_refunds = columns[28]
            cmte_refunds = columns[29]
            
            # Create the CampaignFinanceData object
            campaign_data = HouseSenateCurrentCampaigns(
                candidate_id, name, incumbent_challenger_status, party_code, party_affiliation,
                ttl_receipts, trans_from_auth, ttl_disb, trans_to_auth,
                coh_bop, coh_cop, cand_contrib, cand_loans, other_loans,
                cand_loan_repay, other_loan_repay, debts_owed_by, ttl_indiv_contrib,
                cand_office_st, cand_office_district, spec_election, prim_election,
                run_election, gen_election, gen_election_percent, other_pol_cmte_contrib,
                pol_pty_contrib, cvg_end_dt, indiv_refunds, cmte_refunds
            )
            
            campaigns_list.append(campaign_data)

            campaigns_so_far += 1
            i += 1
            if campaigns_so_far % 100 == 0:
                print(f"From the text file processed {campaigns_so_far}/{total_campaigns} campaign finance records")
        
        if campaigns_so_far == total_campaigns:
                print(f"From the text file processed {campaigns_so_far}/{total_campaigns} campaign finance records")

        return campaigns_list
    
    def batchUploadCampaignsToGraphDB(self, campaigns: List[HouseSenateCurrentCampaigns], batch_size: int = 1000):
        # Use Neo4J graph DB python driver.
        print('  ' +str(self.neo4j_driver) )
        total_campaigns = len(campaigns)
        processed = 0
        with self.neo4j_driver.session() as session:
            # Process contributions in batches
            for i in range(0, total_campaigns, batch_size):
                batch = campaigns[i:i + batch_size]
                
                for campaign in batch:
                    try:
                        
                        # Create the Contribution relationship
                        session.execute_write(self._create_campaign, campaign)

                        processed += 1
                        if processed % 100 == 0:
                            print(f"Processed {processed}/{total_campaigns} campaigns")
                            # logging.info(f"Processed {processed}/{total_contributions} contributions")
                                    
                    except Exception as e:
                        print(f"Error processing campaign {campaign.candidate_id}: {str(e)}")
                        # logging.error(f"Error processing contribution {contribution.id}: {str(e)}")
                # continue

        print(f"Completed uploading {processed}/{total_campaigns} campaigns")
        return

    def _create_campaign(self, tx, candidate_finance_data):
        """Create or merge a Candidate node with campaign finance data."""
        query = """
        MERGE (campaign:HouseSenateCurrentCampaign {id: $id})
        SET campaign.candidate_id = $candidate_id,
            campaign.name = $name,
            campaign.incumbent_challenger_status = $incumbent_challenger_status,
            campaign.party_code = $party_code,
            campaign.party_affiliation = $party_affiliation,
            campaign.total_receipts = $total_receipts,
            campaign.transfers_from_auth = $trans_from_auth,
            campaign.total_disbursements = $total_disbursements,
            campaign.transfers_to_auth = $trans_to_auth,
            campaign.cash_on_hand_begining = $cash_on_hand_begining,
            campaign.cash_on_hand_end = $cash_on_hand_end,
            campaign.candidate_contributions = $cand_contrib,
            campaign.candidate_loans = $cand_loans,
            campaign.other_loans = $other_loans,
            campaign.candidate_loan_repayments = $cand_loan_repay,
            campaign.other_loan_repayments = $other_loan_repay,
            campaign.debts_owed_by = $debts_owed_by,
            campaign.total_individual_contributions = $ttl_indiv_contrib,
            campaign.state = $cand_office_st,
            campaign.district = $cand_office_district,
            campaign.special_election_status = $spec_election,
            campaign.primary_election_status = $prim_election,
            campaign.runoff_election_status = $run_election,
            campaign.general_election_status = $gen_election,
            campaign.general_election_percent = $gen_election_percent,
            campaign.committee_contributions = $other_pol_cmte_contrib,
            campaign.party_contributions = $pol_pty_contrib,
            campaign.coverage_end_date = $cvg_end_dt,
            campaign.individual_refunds = $indiv_refunds,
            campaign.committee_refunds = $cmte_refunds,
            campaign.last_updated = datetime()
        RETURN campaign
        """
        result = tx.run(query,
                    id=candidate_finance_data.candidate_id,
                    candidate_id=candidate_finance_data.candidate_id,
                    name=candidate_finance_data.name,
                    incumbent_challenger_status=candidate_finance_data.incumbent_challenger_status,
                    party_code=candidate_finance_data.party_code,
                    party_affiliation=candidate_finance_data.party_affiliation,
                    total_receipts=candidate_finance_data.total_receipts,
                    trans_from_auth=candidate_finance_data.trans_from_auth,
                    total_disbursements=candidate_finance_data.total_disbursements,
                    trans_to_auth=candidate_finance_data.trans_to_auth,
                    cash_on_hand_begining=candidate_finance_data.cash_on_hand_begining,
                    cash_on_hand_end=candidate_finance_data.cash_on_hand_end,
                    cand_contrib=candidate_finance_data.cand_contrib,
                    cand_loans=candidate_finance_data.cand_loans,
                    other_loans=candidate_finance_data.other_loans,
                    cand_loan_repay=candidate_finance_data.cand_loan_repay,
                    other_loan_repay=candidate_finance_data.other_loan_repay,
                    debts_owed_by=candidate_finance_data.debts_owed_by,
                    ttl_indiv_contrib=candidate_finance_data.ttl_indiv_contrib,
                    cand_office_st=candidate_finance_data.cand_office_st,
                    cand_office_district=candidate_finance_data.cand_office_district,
                    spec_election=candidate_finance_data.spec_election,
                    prim_election=candidate_finance_data.prim_election,
                    run_election=candidate_finance_data.run_election,
                    gen_election=candidate_finance_data.gen_election,
                    gen_election_percent=candidate_finance_data.gen_election_percent,
                    other_pol_cmte_contrib=candidate_finance_data.other_pol_cmte_contrib,
                    pol_pty_contrib=candidate_finance_data.pol_pty_contrib,
                    cvg_end_dt=candidate_finance_data.cvg_end_dt,
                    indiv_refunds=candidate_finance_data.indiv_refunds,
                    cmte_refunds=candidate_finance_data.cmte_refunds)
        return result.single()
    
     
    def __init__(self):
        super(HouseSenateCurrentCampaignsHandler, self).__init__('house_senate_current_campaigns')