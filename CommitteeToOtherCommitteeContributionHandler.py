from FECDataModel.CommitteeToOtherCommitteeContribution import CommitteeToOtherCommitteeContribution
from Handler import Handler
from typing import List


class CommitteeToOtherCommitteeContributionHandler(Handler):

    DATA_DIRECTORY = '/Users/steve/Documents/Dev/DEICheck.ai-LLM-RAG/FECData/manual/committee_to_other_committee_transactions'
    TEST_DATA_DIRECTORY = DATA_DIRECTORY + '/2023-2024/'
    TEST_DATA_FILE_PATH = TEST_DATA_DIRECTORY + '/committee-to-other-committee-transactions.txt'
    
    def processFiles(self):
        self.processFileInFolder()

    def processFileInFolder(self):
        # process files within folder
        transactions_list = self.batchParseTextFileWithSeperator(self.TEST_DATA_FILE_PATH, '|') 

        # self.batchUploadTransactionsToGraphDB(transactions_list)
        return
    
    def batchParseTextFileWithSeperator(self, text_file_path:str, seperator: str) -> list[CommitteeToOtherCommitteeContribution]:
        f = open(text_file_path, "r")
        print(f)

        text_file = f.read()
        file_rows = text_file.splitlines()
        print(len(file_rows))
    
        transactions_so_far = self.proccessed_counter
        total_transactions = len(file_rows)
        transactions_list = []
        
        for i in range(transactions_so_far, len(file_rows)):
            one_row = file_rows[i]
            if len(one_row) < 21:  # We expect 21 columns based on the spec
                print(f"Warning: Row has insufficient columns. Skipping row.")
                continue
            
            columns = one_row.split(seperator)
            # print(columns)

            committee_id = columns[0]
            amendment_indicator = columns[1] if len(columns[1].strip()) > 0 else None
            report_type = columns[2] if len(columns[2].strip()) > 0 else None
            transaction_pgi = columns[3] if len(columns[3].strip()) > 0 else None
            image_num = columns[4] if len(columns[4].strip()) > 0 else None
            transaction_type = columns[5] if len(columns[5].strip()) > 0 else None
            entity_type = columns[6] if len(columns[6].strip()) > 0 else None
            name = columns[7] if len(columns[7].strip()) > 0 else None
            city = columns[8] if len(columns[8].strip()) > 0 else None
            state = columns[9] if len(columns[9].strip()) > 0 else None
            zip_code = columns[10] if len(columns[10].strip()) > 0 else None
            employer = columns[11] if len(columns[11].strip()) > 0 else None
            occupation = columns[12] if len(columns[12].strip()) > 0 else None
            transaction_date =  columns[13]
            transaction_amount = columns[14]
            other_id = columns[15] if len(columns[15].strip()) > 0 else None
            tran_id = columns[16] if len(columns[16].strip()) > 0 else None
            file_num = columns[17] if len(columns[17].strip()) > 0 else None
            memo_cd = columns[18] if len(columns[18].strip()) > 0 else None
            memo_text = columns[19] if len(columns[19].strip()) > 0 else None
            sub_id = columns[20]
            
            # Create the OtherCommitteeTransaction object
            transaction = CommitteeToOtherCommitteeContribution(
                committee_id, amendment_indicator, report_type, transaction_pgi,
                image_num, transaction_type, entity_type, name,
                city, state, zip_code, employer, occupation,
                transaction_date, transaction_amount, other_id,
                tran_id, file_num, memo_cd, memo_text, sub_id
            )
            # transaction.printContribution()

            transactions_list.append(transaction)

            transactions_so_far += 1
            if transactions_so_far % 1000 == 0:
                            # print(f"____ Now batch uploading. ____")
                            self.batchUploadTransactionsToGraphDB(transactions_list)
                            self.writeCounterToFile(transactions_so_far, total_transactions)
                            transactions_list = []
                            # print(f"Processed {transactions_so_far}/{total_transactions} transactions")

        # if transactions_so_far == total_transactions:
        #     print(f"From the text file processed {transactions_so_far}/{total_transactions} other committee transactions")
        if transactions_so_far == total_transactions:
            print(f"Completed uploading {transactions_so_far}/{total_transactions} committees")
            self.writeCounterToFile(transactions_so_far, total_transactions)

        return transactions_list
    

    def batchUploadTransactionsToGraphDB(self, transactions: List[CommitteeToOtherCommitteeContribution], batch_size: int = 1000):
        if not transactions:
             print("____ Nothing to upload!! ____")
        # Use Neo4J graph DB python driver.
        print('  ' + str(self.neo4j_driver))
        total_transactions = len(transactions)
        # processed = self.proccessed_counter

        with self.neo4j_driver.session() as session:
            # Process transactions in batches
            for i in range(0, total_transactions, batch_size):
                batch = transactions[i:i + batch_size]
                
                for transaction in batch:
                    try:
                        # Create the transaction in Neo4j
                        session.execute_write(self._create_transaction, transaction)

                        # processed += 1
                        # if processed % 100 == 0:
                        #     print(f"Processed {processed}/{total_transactions} transactions")
                        #     self.writeCounterToFile(processed, total_transactions)
                                    
                    except Exception as e:
                        print(f"Error processing transaction {transaction.fec_record_number} committee {transaction.committee_id} to other committee {transaction.other_committee_id}: {str(e)}")


        # if processed == total_transactions:
        #     print(f"Completed uploading {processed}/{total_transactions} committees")
        #     self.writeCounterToFile(processed, total_transactions)
        return

    
    def _create_transaction(self, tx, contribution):
        """
        Create or merge nodes for donor and recipient committees, and create a CONTRIBUTED_TO 
        relationship between them with all transaction details as properties.
        """

        # Get donor committee
        # The reciptient committee id is basically not in these records for some reason
        # Create committee to other committee contribution relationship

        query = """
        // First, ensure the donor Committee node exists
        MERGE (donor:Committee {id: $committee_id})
        ON CREATE SET 
            donor.name = $name,
            donor.city = $city,
            donor.state = $state,
            donor.zip_code = $zip_code,
            donor.last_updated = datetime()
        
        // Next, ensure the recipient Committee node exists (if other_committee_id is provided)
        //WITH donor
        //MERGE (recipient:Committee {id: $other_committee_id})
        
        // Create the CONTRIBUTED_TO relationship
        WITH donor //, recipient
        CREATE (donor)-[contrib:CONTRIBUTED_TO {
            committee_id: $committee_id,
            other_committee_id: $other_committee_id,
            amendment_indicator: $amendment_indicator,
            report_type: $report_type,
            transaction_primary_general_indicator: $transaction_primary_general_indicator,
            primary_general_indicator: $primary_general_or_general_election,
            election_year: $election_year,
            image_number: $image_number,
            transaction_type: $transaction_type,
            entity_type: $entity_type,
            transaction_date: $transaction_date,
            transaction_amount: $transaction_amount,
            transaction_contribution_id: $transaction_contribution_id,
            file_number: $file_number,
            memo_code: $memo_code,
            memo_text: $memo_text,
            fec_record_number: $fec_record_number,
            last_updated: datetime()
        }]->(recipient)
        
        RETURN donor, contrib //, recipient
        """

        # query = """
        # // First, ensure the primary Committee node exists
        # MERGE (committee:Committee {id: $committee_id})
        
        # // Then create entity node based on entity_type
        # WITH committee
        # CALL {
        #     WITH committee
        #     // IND - Individual
        #     WITH committee
        #     FOREACH (dummy IN CASE WHEN $entity_type = 'IND' THEN [1] ELSE [] END |
        #         MERGE (entity:Individual {name: $name, city: $city, state: $state, zipcode: $zip_code})
        #         SET entity.employer = $employer, entity.occupation = $occupation, entity.last_updated = datetime()
        #         WITH committee, entity
        #         CREATE (entity)-[txn:%s {
        #             transaction_type: $transaction_type,
        #             amendment_indicator: $amendment_indicator,
        #             report_type: $report_type,
        #             transaction_primary_general_indicator: $transaction_primary_general_indicator,
        #             image_number: $image_number,
        #             transaction_date: $transaction_date,
        #             transaction_amount: $transaction_amount,
        #             tran_id: $tran_id,
        #             file_num: $file_num,
        #             memo_cd: $memo_cd,
        #             memo_text: $memo_text,
        #             sub_id: $sub_id,
        #             last_updated: datetime()
        #         }]->(committee)
        #     )
            
        #     // COM, PAC, PTY, CCM - Other Committee types
        #     UNION
        #     WITH committee
        #     FOREACH (dummy IN CASE WHEN $entity_type IN ['COM', 'PAC', 'PTY', 'CCM'] AND $other_id IS NOT NULL THEN [1] ELSE [] END |
        #         MERGE (entity:Committee {id: $other_id})
        #         SET entity.name = $name, entity.city = $city, entity.state = $state, 
        #             entity.zip_code = $zip_code, entity.last_updated = datetime()
        #         WITH committee, entity
        #         CREATE (entity)-[txn:%s {
        #             transaction_type: $transaction_type,
        #             amendment_indicator: $amendment_indicator,
        #             report_type: $report_type,
        #             transaction_primary_general_indicator: $transaction_primary_general_indicator,
        #             image_number: $image_number,
        #             transaction_date: $transaction_date,
        #             transaction_amount: $transaction_amount,
        #             tran_id: $tran_id,
        #             file_num: $file_num,
        #             memo_cd: $memo_cd,
        #             memo_text: $memo_text,
        #             sub_id: $sub_id,
        #             last_updated: datetime()
        #         }]->(committee)
        #     )
            
        #     // ORG - Organization
        #     UNION
        #     WITH committee
        #     FOREACH (dummy IN CASE WHEN $entity_type = 'ORG' THEN [1] ELSE [] END |
        #         MERGE (entity:Organization {name: $name, city: $city, state: $state, zipcode: $zip_code})
        #         SET entity.last_updated = datetime()
        #         WITH committee, entity
        #         CREATE (entity)-[txn:%s {
        #             transaction_type: $transaction_type,
        #             amendment_indicator: $amendment_indicator,
        #             report_type: $report_type,
        #             transaction_primary_general_indicator: $transaction_primary_general_indicator,
        #             primary_general_or_general_election: $primary_general_or_general_election,
        #             election_year: $election_year,
        #             image_number: $image_number,
        #             transaction_date: $transaction_date,
        #             transaction_amount: $transaction_amount,
        #             tran_id: $tran_id,
        #             file_num: $file_num,
        #             memo_cd: $memo_cd,
        #             memo_text: $memo_text,
        #             sub_id: $sub_id,
        #             last_updated: datetime()
        #         }]->(committee)
        #     )
            
        #     // CAN - Candidate
        #     UNION
        #     WITH committee
        #     FOREACH (dummy IN CASE WHEN $entity_type = 'CAN' THEN [1] ELSE [] END |
        #         MERGE (entity:Candidate {name: $name})
        #         SET entity.city = $city, entity.state = $state, entity.zipcode = $zip_code,
        #             entity.last_updated = datetime()
        #         WITH committee, entity
        #         CREATE (entity)-[txn:%s {
        #             transaction_type: $transaction_type,
        #             amendment_indicator: $amendment_indicator,
        #             report_type: $report_type,
        #             transaction_primary_general_indicator: $transaction_primary_general_indicator,
        #             image_number: $image_number,
        #             transaction_date: $transaction_date,
        #             transaction_amount: $transaction_amount,
        #             other_committee_id: $other_committee_id,
        #             transaction_contribution_id: $transaction_contribution_id,
        #             file_number: $file_number,
        #             memo_code: $memo_cdoe,
        #             memo_text: $memo_text,
        #             fec_record_number: $fec_record_number,
        #             last_updated: datetime()
        #         }]->(committee)
        #     )
        # }
        
        # RETURN count(*) as count
        # """ % (relationship_type, relationship_type, relationship_type, relationship_type)
        
        # # Build parameters dictionary from transaction object
        # params = {
        #     'committee_id': transaction.committee_id,
        #     'amendment_indicator': transaction.amendment_indicator,
        #     'report_type': transaction.report_type,
        #     'transaction_primary_general_indicator': transaction.transaction_primary_general_indicator,
        #     'image_number': transaction.image_number,
        #     'primary_general_or_general_election': transaction.primary_general_or_general_election,
        #     'election_year': transaction.election_year,
        #     'transaction_type': transaction.transaction_type,
        #     'entity_type': transaction.entity_type,
        #     'name': transaction.name,
        #     'city': transaction.city,
        #     'state': transaction.state,
        #     'zip_code': transaction.zip_code,
        #     'employer': transaction.employer,
        #     'occupation': transaction.occupation,
        #     'transaction_date': transaction.transaction_date,
        #     'transaction_amount': transaction.transaction_amount,
        #     'other_committee_id': transaction.other_committee_id,
        #     'transaction_contribution_id': transaction.transaction_contribution_id,
        #     'file_number': transaction.file_number,
        #     'memo_code': transaction.memo_code,
        #     'memo_text': transaction.memo_text,
        #     'fec_record_number': transaction.fec_record_number
        # }
        params = {
            'committee_id': contribution.committee_id,
            'name': contribution.name,
            'city': contribution.city,
            'state': contribution.state,
            'zip_code': contribution.zip_code,
            'amendment_indicator': contribution.amendment_indicator,
            'report_type': contribution.report_type,
            'transaction_primary_general_indicator': contribution.transaction_primary_general_indicator,
            'primary_general_or_general_election': contribution.primary_general_or_general_election,
            'election_year': contribution.election_year,
            'image_number': contribution.image_number,
            'transaction_type': contribution.transaction_type,
            'entity_type': contribution.entity_type,
            'transaction_date': contribution.transaction_date,
            'transaction_amount': contribution.transaction_amount,
            'other_committee_id': contribution.other_committee_id,
            'transaction_contribution_id': contribution.transaction_contribution_id,
            'file_number': contribution.file_number,
            'memo_code': contribution.memo_code,
            'memo_text': contribution.memo_text,
            'fec_record_number': contribution.fec_record_number
        }

        result = tx.run(query, **params)
        return result.single()
    
    # def _determine_relationship_type(self, transaction_type):
        # """
        # Determine the appropriate relationship type based on the transaction type.
        # This helps categorize different types of transactions in the graph.
        # """
        # # Map transaction type codes to meaningful relationship types
        # # These are example mappings - should be updated based on actual FEC transaction type meanings
        # if transaction_type in ['10J', '11J', '15J', '15Z', '18J', '19J']:
        #     return 'CONTRIBUTED_TO'
        # elif transaction_type in ['13', '16C', '16F', '16G', '16R', '17R']:
        #     return 'TRANSFERRED_TO'
        # elif transaction_type in ['20', '20C', '20F', '20G', '20R']:
        #     return 'LOAN_TO'
        # elif transaction_type in ['22H', '22Z', '23Y']:
        #     return 'EXPENSE_PAID_TO'
        # elif transaction_type in ['24A', '24C', '24E', '24F', '24G', '24H', '24K', '24N', '24P', '24R', '24U', '24Z']:
        #     return 'INDEPENDENT_EXPENDITURE_FOR'
        # elif transaction_type.startswith('30') or transaction_type.startswith('31') or transaction_type.startswith('32'):
        #     return 'COORDINATED_EXPENDITURE_FOR'
        # elif transaction_type.startswith('40') or transaction_type.startswith('41') or transaction_type.startswith('42'):
        #     return 'COMMUNICATION_COST_FOR'
        # else:
            # return 'TRANSACTION_WITH'  # Default fallback relationship
    
    def __init__(self):
        super(CommitteeToOtherCommitteeContributionHandler, self).__init__('committee_to_other_committee_transactions')