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

    