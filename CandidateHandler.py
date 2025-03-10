from FECDataModel.Candidate import Candidate
from Handler import Handler

from typing import List
# from neo4j import GraphDatabase

class CandidateHandler(Handler):
    
    DATA_DIRECTORY = '/Users/steve/Documents/Dev/DEICheck.ai-LLM-RAG/FECData/manual/candidates'
    TEST_DATA_DIRECTORY = DATA_DIRECTORY + '/2023-2024/'
    # TEST_DATA_FILE_PATH = TEST_DATA_DIRECTORY + '/weball24-2.txt'
    TEST_DATA_FILE_PATH = TEST_DATA_DIRECTORY + '/candidate-master-2023-2024.txt'
    
    def processFiles(self):
        self.processFileInFolder()

    def processFileInFolder(self):
        # process files within folder
        candidate_list = self.parseTextFileWithSeperator(self.TEST_DATA_FILE_PATH, '|') 

        self.batchUploadCandidatesToGraphDB(candidate_list)
        return
    
    def parseTextFileWithSeperator(self, text_file_path:str, seperator: str) -> list[Candidate]:
        f = open(text_file_path, "r")
        print(f)

        text_file = f.read()
        # print(text_file.read())
        file_rows = text_file.splitlines()
        # print(file_rows)
        print(len(file_rows))

        candidates_so_far = 0
        total_candidates = len(file_rows)
        candidate_list = []
        for one_row in file_rows:
            # print(one_row)
            columns = one_row.split(seperator)
            print(columns)
            print()

            candidate_id = columns[0]
            name = columns[1]
            party_affiliation_code = columns[2]
            year_of_election = columns[3]
            candidate_state = columns[4]
            candidate_office = columns[5]
            candidate_district = columns[6]
            incumbent_challenger_status_code = columns[7]
            candidate_status_code = columns[8]
            principal_campaign_committee = columns[9]
            
            # c == Candidate()
            candidate = Candidate(
                candidate_id ,
                name,
                party_affiliation_code,
                year_of_election,
                candidate_state,
                candidate_office ,
                candidate_district ,
                incumbent_challenger_status_code,
                candidate_status_code,
                principal_campaign_committee,
            )
            candidate_list.append(candidate)
            print(candidate)

            candidates_so_far += 1
            if candidates_so_far % 100 == 0:
                print(f"From the text file processed {candidates_so_far}/{total_candidates} candidates")

        return candidate_list
    
    # def parseTextFileWithSeperatorAllCandidatesVersion(self, text_file_path:str, seperator: str) -> list[Candidate]:
    #     f = open(text_file_path, "r")
    #     print(f)

    #     text_file = f.read()
    #     # print(text_file.read())
    #     file_rows = text_file.splitlines()
    #     # print(file_rows)
    #     print(len(file_rows))

    #     candidates_so_far = 0
    #     total_candidates = len(file_rows)
    #     candidate_list = []
    #     for one_row in file_rows:
    #         # print(one_row)
    #         columns = one_row.split(seperator)
    #         print(columns)
    #         print()
    #         election_year = '2023-2024'
    #     #     # print(type(columns))
    #     #     print(len(columns))

    #         candidate_id = columns[0]
    #         name = columns[1]
    #         incumbent_challenger_status_code = columns[2]
    #         party_affiliation_code = columns[3]
    #         party_affiliation_code = columns[4]
    #         total_recipts = columns[5]
    #         total_disburstments = columns[7]
    #         transfers_to_authorized_committees = columns[8]
    #         beginning_cash = columns[9]
    #         ending_cash = columns[10]
    #         contributions_from_candidate = columns[11] # Contributions from candidate
    #         loans_from_candidate = columns[12] # Loans from candidate	13	Y	Number(14,2)		250000.00
    #         other_loans = columns[13] # Other loans
    #         loan_repayments = columns[14] # Candidate loan repayments
    #         other_loan_repayments = columns[15] # Other loan repayments
    #         debts_owed_by = columns[16]
    #         total_individual_contributions = columns[17]
    #         office_state = columns[18]
    #         office_district = columns[19]
    #         special_election_status = columns[20]
    #         primary_election_status = columns[21]
    #         runoff_election_status = columns[22]
    #         general_election_status = columns[23]
    #         general_election_percentage = columns[24]
    #         contrib_from_other_political_committees = columns[25]
    #         contrib_from_party_committees = columns[26] 
    #         coverage_end_date = columns[27] 
    #         refunds_to_individuals = columns[28] 
    #         committee_refunds = columns[29]
            
    #         # c == Candidate()
    #         candidate = Candidate(
    #             candidate_id ,
    #             name,
    #             party_affiliation_code,
    #             election_year,
    #             office_state,
    #             office_code,
    #             office_district,
    #             incumbent_challenger_status_code,
    #             candidate_status_code,
    #             principal_campaign_committee,
    #             last_updated 
    #         )
    #         candidate_list.append(candidate)

    #         candidates_so_far += 1
    #         if candidates_so_far % 100 == 0:
    #             print(f"From the text file processed {candidates_so_far}/{total_candidates} candidates")

    #     return candidate_list
    

    def batchUploadCandidatesToGraphDB(self, candidates: List[Candidate], batch_size: int = 1000):
        # Use Neo4J graph DB python driver.
        total_candidates = len(candidates)
        # Pick up where peresitent storage left off.
        processed_so_far = self.proccessed_counter

        with self.neo4j_driver.session() as session:
            # Process contributions in batches
            for i in range(processed_so_far, total_candidates, batch_size):
                batch = candidates[i:i + batch_size]
                
                for one_candidate in batch:
                    try:
                        # Create candidate node.
                        session.execute_write(self._create_candidate_node, one_candidate)                   
 
                        processed_so_far += 1
                        if processed_so_far % 100 == 0:
                            self.writeCounterToFile(processed_so_far, total_candidates)
                                    
                    except Exception as e:
                        print(f"Error processing contribution {one_candidate.id}: {str(e)}")
                        # logging.error(f"Error processing contribution {contribution.id}: {str(e)}")
                # continue

        if processed_so_far == total_candidates:
            print(f"Completed uploading {processed_so_far}/{total_candidates} candidatess")
            self.writeCounterToFile(processed_so_far, total_candidates)
        return
   
    def _create_candidate_node(self, tx, candidate: Candidate):
        """Create or merge a Candidate node."""
        query = """
        MERGE (c:Candidate {id: $id})
        SET c.id = $id,
            c.name = $name,
            c.first_name = $first_name,
            c.last_name = $last_name,
            c.political_party_affliiation = $political_party_affliiation,
            c.election_year = $election_year,
            c.office_state = $office_state,
            c.office_district = $office_district, 
            c.candidate_office = $candidate_office,
            c.incumbent_challenger_status = $incumbent_challenger_status, 
            c.candidate_status = $candidate_status,
            c.principal_campaign_committee = $principal_campaign_committee,
            c.last_updated = datetime()
        RETURN c
        """
        
        print('candidate id:')
        print(candidate.id)
        print('candidate name:')
        print(candidate.name)
        # print('candidate first name:')
        # print(candidate.first_name)
        # print('candidate last name:')
        # print(candidate.last_name)
        # print('candidate political_party_affliiation:')
        # print(candidate.political_party_affliiation)
        # print('candidate election_year')
        # print(candidate.election_year)
        # print('candidate office_state')
        # print(candidate.office_state)
        # print('candidate office_district')
        # print(candidate.office_district)

        # print('candidate candidate_office')
        # print(candidate.candidate_office)
        # print('candidate office_district')
        # print(candidate.office_district)
        # print('candidate incumbent_challenger_status')
        # print(candidate.incumbent_challenger_status)
        # print('candidate candidate_status')
        # print(candidate.candidate_status)
        # print('candidate principal_campaign_committee')
        # print(candidate.principal_campaign_committee)
        # print('candidate last_updated')
        # print(candidate.last_updated)
        print()
        # c.political_party_affliiation = $political_party_affliiation,
        #     c.election_year = $election_year,
        
        # office_state,
        #     c.candidate_office = $candidate_office,
        

        # c.office_district = $office_district, 
        #     c.incumbent_challenger_status = $incumbent_challenger_status, 
        
        # c.candidate_status = $candidate_status,
        #     c.principal_campaign_committee = $principal_campaign_committee,
        #     c.last_updated = datetime()
        result = tx.run(query,
                       id=candidate.id,
                       name=candidate.name,
                       first_name=candidate.first_name,
                       last_name=candidate.last_name,
                       political_party_affliiation=candidate.political_party_affliiation,
                       election_year=candidate.election_year,
                       office_state=candidate.office_state,
                       office_district=candidate.office_district,
                       candidate_office=candidate.candidate_office,
                       office_districtr=candidate.office_district,
                       incumbent_challenger_status=candidate.incumbent_challenger_status,
                       candidate_status=candidate.principal_campaign_committee,
                       principal_campaign_committee=candidate.principal_campaign_committee)
        return result.single()
    
    

    # def initNeo4J(self):
    #     NEO4J_CONNECTION_STR = 'bolt://localhost:7687'
    #     NEO4J_URI = 'neo4j://localhost'
    #     AUTH = ("Admin", "Password")
    #     with GraphDatabase.driver(NEO4J_URI, auth=AUTH) as driver:
    #         driver.verify_connectivity()
    #         return driver
    #     # If driver can not init or connect to DB throw exception.
    #     raise Exception("Could not connect to Neo4J.")
    
    def __init__(self):
        super(CandidateHandler, self).__init__('candidates')
        # try:
        #     with open('Counters/candidates_uploaded_counter.txt', 'r') as f:
        #         val = f.read()
        #         if val == '':
        #             self.proccessed_counter = 0
        #         else:
        #             self.proccessed_counter = int(val)
                
        #     print(f"Counter value {self.proccessed_counter} loaded from counter.pickle")
        # except FileNotFoundError:
        #     print("counter.pickle not found. Initializing counter to 0.")
        #     self.proccessed_counter = 0
        #     # pickle.dump(self.proccessed_counter, f)
        #     f.write(self.proccessed_counter)

        # self.neo4j_driver = self.initNeo4J()

# def main():
#     # Initialize uploader
#     uploader = FECDataUploaderIndividualContributions()
#     #  
#     uploader.processFiles()


# if __name__ == "__main__":
#     main()