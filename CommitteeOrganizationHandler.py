from FECDataModel.CommiteeOrganization import CommitteeOrganization
from Handler import Handler

from typing import List
# from neo4j import GraphDatabase

class CommitteeOrganizationHandler(Handler):
    DATA_DIRECTORY = '/Users/steve/Documents/Dev/DEICheck.ai-LLM-RAG/FECData/manual/committees'
    TEST_DATA_DIRECTORY = DATA_DIRECTORY + '/2023-2024/'
    # TEST_DATA_FILE_PATH = TEST_DATA_DIRECTORY + '/weball24-2.txt'
    TEST_DATA_FILE_PATH = TEST_DATA_DIRECTORY + '/committee-master-2023-2024.txt'
    

    def processFiles(self):
        self.processFileInFolder()

    def processFileInFolder(self):
        # process files within folder
        committee_list = self.parseTextFileWithSeperator(self.TEST_DATA_FILE_PATH, '|') 

        self.batchUploadCommitteesToGraphDB(committee_list)

        return

    # def parseTextFileWithSeperator(self, text_file_path:str, seperator: str) -> list[CommiteeOrganization]:
    #     return []
    def parseTextFileWithSeperator(self, text_file_path:str, seperator: str) -> list[CommitteeOrganization]:
        f = open(text_file_path, "r")
        print(f)

        text_file = f.read()
        # print(text_file.read())
        file_rows = text_file.splitlines()
        # print(file_rows)
        print(len(file_rows))

        committees_so_far = 0
        total_committees = len(file_rows)
        committees_list = []
        for one_row in file_rows:
            # print(one_row)
            columns = one_row.split(seperator)
            # print(columns)

            committee_id = columns[0]
            name = columns[1]
            treasurer_name = columns[2]

            street_one = columns[3]
            street_two = columns[4]
            city = columns[5]
            state = columns[6]
            zip_code = columns[7]
            address = f'{street_one}, {street_two} {city}, {state} {zip_code}'

            committee_designation = columns[8]
            committee_type = columns[9]
            committee_party = columns[10]

            filing_frequency = columns[11]
            interest_group_category = columns[12]
            connected_organizations_name = columns[14]
            candidates_id = columns[14]
            
            committee = CommitteeOrganization(
                committee_id,
                name,
                treasurer_name,
                address,
                committee_designation,
                committee_type,
                committee_party,
                filing_frequency,
                interest_group_category,
                connected_organizations_name,
                candidates_id
            )
            committees_list.append(committee)
            # committee.printCommittee()

            committees_so_far += 1
            if committees_so_far % 100 == 0:
                print(f"From the text file processed {committees_so_far}/{total_committees} committees")
        
        if committees_so_far == total_committees:
                print(f"From the text file processed {committees_so_far}/{total_committees} committees")

        return committees_list
    
    def batchUploadCommitteesToGraphDB(self, committees: List[CommitteeOrganization], batch_size: int = 1000):
        # Use Neo4J graph DB python driver.
        total_committees = len(committees)
        # Pick up where peresitent storage left off.
        processed_so_far = self.proccessed_counter

        with self.neo4j_driver.session() as session:
            # Process contributions in batches
            for i in range(processed_so_far, total_committees, batch_size):
                batch = committees[i:i + batch_size]
                
                for one_committee in batch:
                    try:
                        # Create committee node.
                        session.execute_write(self._create_committee_node, one_committee)                   
 
                        processed_so_far += 1
                        if processed_so_far % 100 == 0:
                            self.writeCounterToFile(processed_so_far, total_committees)
                                    
                    except Exception as e:
                        print(f"Error processing contribution {one_committee.id}: {str(e)}")
                        # logging.error(f"Error processing contribution {contribution.id}: {str(e)}")
                # continue

        if processed_so_far == total_committees:
            print(f"Completed uploading {processed_so_far}/{total_committees} committees")
            self.writeCounterToFile(processed_so_far, total_committees)
        return
    
    def _create_committee_node(self, tx, committee: CommitteeOrganization):
        """Create or merge an Individual node."""
        query = """
        MERGE (co:Committee {id: $id})
        SET co.id = $id,
            co.name = $name,
            co.treasurer_name = $treasurer_name,
            co.address = $address,
            co.committee_designation = $committee_designation,
            co.committee_type = $committee_type,
            co.committee_political_party_affliiation = $committee_political_party_affliiation,
            co.filing_frequency  = $filing_frequency,
            co.interest_group_category = $interest_group_category, 
            co.connected_organization_name = $connected_organization_name, 
            co.candidate_id = $candidate_id,
            co.last_updated = datetime()
        RETURN co
        """
        result = tx.run(query,
                       id=committee.id,
                       name=committee.name,
                       treasurer_name = committee.treasurer_name,
                       address = committee.address,
                       committee_designation = committee.committee_designation,
                       committee_type = committee.committee_type,
                       committee_political_party_affliiation=committee.committee_political_party_affliiation,
                       filing_frequency=committee.filing_frequency,
                       interest_group_category=committee.interest_group_category,
                       connected_organization_name=committee.connected_organization_name,
                       candidate_id=committee.candidate_id)
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
    
    # def __init__(self):
    #     try:
    #         with open('Counters/committees_uploaded_counter.txt', 'r') as f:
    #             val = f.read()
    #             if val == '':
    #                 self.proccessed_counter = 0
    #             else:
    #                 self.proccessed_counter = int(val)     
    #         print(f"Counter value {self.proccessed_counter} loaded from counter.pickle")
    #     except FileNotFoundError:
    #         print("counter.pickle not found. Initializing counter to 0.")
    #         self.proccessed_counter = 0
    #         # pickle.dump(self.proccessed_counter, f)
    #         f.write(self.proccessed_counter)
    #     self.neo4j_driver = self.initNeo4J()

    def __init__(self):
        super(CommitteeOrganizationHandler, self).__init__('committees')