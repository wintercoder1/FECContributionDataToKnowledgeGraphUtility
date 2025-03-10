from neo4j import GraphDatabase

class  Handler:
    def __init__(self, type: str):
        self.type = type
        try:
            with open(f'Counters/{type}_uploaded_counter.txt', 'r') as f:
                val = f.read()
                if val == '':
                    self.proccessed_counter = 0
                else:
                    self.proccessed_counter = int(val)     
            print(f"Counter value {self.proccessed_counter} loaded from local file.")
        except FileNotFoundError:
            print("File not found." ) # Initializing counter to 0.")
            # self.proccessed_counter = 0
            # f.write(self.proccessed_counter)
        self.neo4j_driver = self.initNeo4J()

    # def processFileInFolder(self):
    #     # process files within folder
    #     object_to_upload_list = self.parseTextFileWithSeperator(self.TEST_DATA_FILE_PATH, '|') 

    #     self.batchUploadToGraphDB(object_to_upload_list)

    #     return
     
    # def batchUploadToGraphDB(self, object_to_upload_list: List[Any], batch_size: int = 1000): #, lambda_f: lambda int):
    #     # Use Neo4J graph DB python driver.
    #     print('  ' +str(self.neo4j_driver) )
    #     total_linkages = len(object_to_upload_list)
    #     processed = 0
    #     with self.neo4j_driver.session() as session:
    #         # Process contributions in batches
    #         for i in range(0, total_linkages, batch_size):
    #             batch = object_to_upload_list[i:i + batch_size]
                
    #             for linkage in batch:
    #                 try:
    
    #                     # Create the Candidate Committee Linkage relationship
    #                     # session.execute_write(self._create_candidate_committee_linkage, linkage)
    #                     #
    #                     #
    #                     # replace with lambda.
    #                     #
    #                     #
    #                     processed += 1
    #                     if processed % 100 == 0:
    #                         print(f"Processed {processed}/{total_linkages} linkages")
    #                         # logging.info(f"Processed {processed}/{total_contributions} contributions")
                                    
    #                 except Exception as e:
    #                     print(f"Error processing candidate committee linkage {linkage.linkage_id}: {str(e)}")
        
    #     if processed == total_linkages:
    #         print(f"Completed uploading {processed}/{total_linkages} linkages")
    #     return

    def initNeo4J(self):
        NEO4J_CONNECTION_STR = 'bolt://localhost:7687'
        NEO4J_URI = 'neo4j://localhost'
        AUTH = ("Admin", "Password")
        with GraphDatabase.driver(NEO4J_URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            return driver
        # If driver can not init or connect to DB throw exception.
        raise Exception("Could not connect to Neo4J.")
    
    def writeCounterToFile(self, processed_so_far: int, total_candidates: int):
        print(f"\n\n!!        Uploaded {processed_so_far}/{total_candidates} {self.type} to Neo4j   !!\n\n\n")
        # logging.info(f"Processed {processed}/{total_candidates} candidates")
        self.proccessed_counter = processed_so_far
        with open(f'Counters/{self.type}_uploaded_counter.txt', 'w') as f:
            # pickle.dump(self.proccessed_counter, f)
            f.write(str(self.proccessed_counter))

    