from FECDataModel.CandidateCommitteeLinkage import CandidateCommitteeLinkage
from Handler import Handler

from typing import List

class CandidateCommitteeLinkagesHandler(Handler):
    DATA_DIRECTORY = '/Users/steve/Documents/Dev/DEICheck.ai-LLM-RAG/FECData/manual/candidate_committee_linkage'
    TEST_DATA_DIRECTORY = DATA_DIRECTORY + '/2023-2024/'
    # TEST_DATA_FILE_PATH = TEST_DATA_DIRECTORY + '/weball24-2.txt'
    TEST_DATA_FILE_PATH = TEST_DATA_DIRECTORY + '/candidate-committee-linkage-2023-2024.txt'
    
    def processFiles(self):
        self.processFileInFolder()

    def processFileInFolder(self):
        # process files within folder
        candidate_committee_linkages_list = self.parseTextFileWithSeperator(self.TEST_DATA_FILE_PATH, '|') 

        self.batchUploadCandidateCommitteeLinkagesToGraphDB(candidate_committee_linkages_list)

        return
    
    def parseTextFileWithSeperator(self, text_file_path:str, seperator: str) -> list[CandidateCommitteeLinkage]:
        f = open(text_file_path, "r")
        print(f)

        text_file = f.read()
        # print(text_file.read())
        file_rows = text_file.splitlines()
        # print(file_rows)
        print(len(file_rows))

        candidate_committee_linkages_so_far = 0
        total_candidate_committee_linkages = len(file_rows)
        candidate_committee_linkage_list = []
        for one_row in file_rows:
            # print(one_row)
            columns = one_row.split(seperator)
            print(columns)
            print()

            candidate_id = columns[0]
            candidate_election_year = columns[1]
            fec_election_year = columns[2]
            committee_id = columns[3]
            committee_type_code = columns[4]
            committee_designation_code = columns[5]
            linkage_id = columns[6] 
              
            # c == Candidate()
            candidate_committee_linkage = CandidateCommitteeLinkage(
                candidate_id ,
                candidate_election_year,
                fec_election_year,
                committee_id ,
                committee_type_code,
                committee_designation_code,
                linkage_id,
            )
            candidate_committee_linkage_list.append(candidate_committee_linkage)
            print(candidate_committee_linkage)

            candidate_committee_linkages_so_far += 1
            if candidate_committee_linkages_so_far % 100 == 0:
                print(f"From the text file processed {candidate_committee_linkages_so_far}/{total_candidate_committee_linkages} candidate_committee_linkages")

        return candidate_committee_linkage_list
    
    
    def batchUploadCandidateCommitteeLinkagesToGraphDB(self, candidate_committee_linkages: List[CandidateCommitteeLinkage], batch_size: int = 1000):
        # Use Neo4J graph DB python driver.
        print('  ' +str(self.neo4j_driver) )
        total_linkages = len(candidate_committee_linkages)
        processed = 0
        with self.neo4j_driver.session() as session:
            # Process contributions in batches
            for i in range(0, total_linkages, batch_size):
                batch = candidate_committee_linkages[i:i + batch_size]
                
                for linkage in batch:
                    try:
    
                        # Create the Candidate Committee Linkage relationship
                        session.execute_write(self._create_candidate_committee_linkage, linkage)

                        processed += 1
                        if processed % 100 == 0:
                            print(f"Processed {processed}/{total_linkages} linkages")
                            # logging.info(f"Processed {processed}/{total_contributions} contributions")
                                    
                    except Exception as e:
                        print(f"Error processing candidate committee linkage {linkage.linkage_id}: {str(e)}")
        
        if processed == total_linkages:
            print(f"Completed uploading {processed}/{total_linkages} linkages")
        return
    
    def _create_candidate_committee_linkage(self, tx, linkage: CandidateCommitteeLinkage):
        """Create a Contribution relationship between Individual and Organization."""
        query = """
        MATCH (cand:CANDIDATE {id: $candidate_id})
        MATCH (com:COMMITEE {id: $committee_id})
        CREATE (cand)-[linkage:Candidate_Committee_Linkage{
            linkage_id: $linkage_id,
            candidate_id: $candidate_id,
            candidate_election_year: $candidate_election_year,
            fec_election_year: $fec_election_year,
            committee_id: $committee_id,
            committee_type: $committee_type,
            committee_designation: $committee_designation
        }]->(com)
        RETURN linkage
        """
        # CREATE (i)-[c:CONTRIBUTED_TO {
        #     id: $transaction_id,
        #     amount: $amount,
        #     memo: $memo
        # }]->(o)
        # RETURN c
        result = tx.run(query,
                        linkage_id = linkage.linkage_id,
                        candidate_id = linkage.candidate_id,
                        committee_id = linkage.committee_id,
                        candidate_election_year = linkage.candidate_election_year,
                        fec_election_year = linkage.fec_election_year,
                        committee_type = linkage.committee_type,
                        committee_designation = linkage.committee_designation)
        return result.single()
    
    def __init__(self):
        super(CandidateCommitteeLinkagesHandler, self).__init__('candidate_committee_linkage')