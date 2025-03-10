#
#
#
#
#  NOT TESTED YEt
#
#
#
#
#
#
#
#
#  NOT TESTED YEt
#
#
#
#
#
#
#
#
#  NOT TESTED YEt
#
#
#
#
#
#
#
#
#  NOT TESTED YEt
#
#
#
#
#
#
#

from FECDataModel.OperatingExpenditures import OperatingExpenditures
from Handler import Handler
from decimal import Decimal
from datetime import datetime
from typing import List

class OperatingExpendituresHandler(Handler):

    DATA_DIRECTORY = '/Users/steve/Documents/Dev/DEICheck.ai-LLM-RAG/FECData/manual/operating_expenditures'
    TEST_DATA_DIRECTORY = DATA_DIRECTORY + '/2023-2024/'
    TEST_DATA_FILE_PATH = TEST_DATA_DIRECTORY + '/operating-expenditures-2023-2024.txt'
    
    def processFiles(self):
        self.processFileInFolder()

    def processFileInFolder(self):
        # process files within folder
        expenditures_list = self.parseTextFileWithSeperator(self.TEST_DATA_FILE_PATH, '|') 

        self.batchUploadExpendituresToGraphDB(expenditures_list)
        return
    
    def parseTextFileWithSeperator(self, text_file_path:str, seperator: str) -> list[OperatingExpenditures]:
        f = open(text_file_path, "r")
        print(f)

        text_file = f.read()
        file_rows = text_file.splitlines()
        print(len(file_rows))
    
        expenditures_so_far = 0
        total_expenditures = len(file_rows)
        expenditures_list = []
        
        

        for one_row in file_rows:
            if len(one_row) < 25:  # We expect 25 columns based on the spec
                print(f"Warning: Row has insufficient columns. Skipping row.")
                continue

            columns = one_row.split(seperator)
            # print(columns)

            committee_id = columns[0]
            amendment_indicator = columns[1] if len(columns[1].strip()) > 0 else None
            
            # Handle report_year - ensure it's an integer
            report_year = None
            if columns[2] and columns[2].strip():
                try:
                    report_year = int(columns[2])
                except:
                    report_year = None
                    
            report_type = columns[3] if len(columns[3].strip()) > 0 else None
            image_num = columns[4] if len(columns[4].strip()) > 0 else None
            line_num = columns[5] if len(columns[5].strip()) > 0 else None
            form_type = columns[6] if len(columns[6].strip()) > 0 else None
            schedule_type = columns[7] if len(columns[7].strip()) > 0 else None
            payee_name = columns[8] if len(columns[8].strip()) > 0 else None
            city = columns[9] if len(columns[9].strip()) > 0 else None
            state = columns[10] if len(columns[10].strip()) > 0 else None
            zip_code = columns[11] if len(columns[11].strip()) > 0 else None
            transaction_date = columns[12]
            transaction_amount = columns[13]
            transaction_pgi = columns[14] if len(columns[14].strip()) > 0 else None
            purpose = columns[15] if len(columns[15].strip()) > 0 else None
            category = columns[16] if len(columns[16].strip()) > 0 else None
            category_desc = columns[17] if len(columns[17].strip()) > 0 else None
            memo_cd = columns[18] if len(columns[18].strip()) > 0 else None
            memo_text = columns[19] if len(columns[19].strip()) > 0 else None
            entity_type = columns[20] if len(columns[20].strip()) > 0 else None
            sub_id = columns[21]
            file_num = columns[22] if len(columns[22].strip()) > 0 else None
            tran_id = columns[23] if len(columns[23].strip()) > 0 else None
            back_ref_tran_id = columns[24] if len(columns[24].strip()) > 0 else None
            
            # Create the OperatingExpenditures object
            expenditure = OperatingExpenditures(
                committee_id, amendment_indicator, report_year, report_type,
                image_num, line_num, form_type, schedule_type, payee_name,
                city, state, zip_code, transaction_date, transaction_amount,
                transaction_pgi, purpose, category, category_desc, memo_cd,
                memo_text, entity_type, sub_id, file_num, tran_id, back_ref_tran_id
            )
            # expenditure.printOperatingExpendature()
            # print(expenditure)
            expenditures_list.append(expenditure)

            expenditures_so_far += 1
            if expenditures_so_far % 100 == 0:
                print(f"From the text file processed {expenditures_so_far}/{total_expenditures} operating expenditures")
        
        if expenditures_so_far == total_expenditures:
            print(f"From the text file processed {expenditures_so_far}/{total_expenditures} operating expenditures")

        return expenditures_list
    
    def batchUploadExpendituresToGraphDB(self, expenditures: List[OperatingExpenditures], batch_size: int = 1000):
        # Use Neo4J graph DB python driver.
        print('  ' + str(self.neo4j_driver))
        total_expenditures = len(expenditures)
        processed = self.proccessed_counter
        with self.neo4j_driver.session() as session:
            # Process expenditures in batches
            for i in range(0, total_expenditures, batch_size):
                batch = expenditures[i:i + batch_size]
                
                for expenditure in batch:
                    try:
                        # Create the Committee and Payee nodes and the PAID relationship
                        session.execute_write(self._create_expenditure, expenditure)

                        processed += 1
                        if processed % 100 == 0:
                            print(f"Processed {processed}/{total_expenditures} expenditures")
                            self.writeCounterToFile(processed, total_expenditures)
                                    
                    except Exception as e:
                        print(f"Error processing expenditure {expenditure.fec_record_number}: {str(e)}")

        if processed == total_expenditures:
            print(f"Completed uploading {processed}/{total_expenditures} committees")
            self.writeCounterToFile(processed, total_expenditures)
        return

    def _create_expenditure(self, tx, expenditure):
        """
        Create or merge nodes for the Committee and Payee, and the PAID relationship.
        Also handle related transactions through back_ref_tran_id.
        """
        query = """
        // First, ensure the Committee node exists
        // First, ensure the Committee node exists
        MERGE (committee:Committee {id: $committee_id})
        
        // Then create payee entity based on entity_type
        WITH committee
        CALL {
            WITH committee
            // Create the appropriate payee node based on entity_type
            FOREACH (dummy IN CASE WHEN $entity_type = 'IND' THEN [1] ELSE [] END |
                MERGE (payee:Individual {name: $payee_name})
                SET payee.city = $city, 
                    payee.state = $state, 
                    payee.zipcode = $zip_code,
                    payee.last_updated = datetime()
                CREATE (committee)-[exp:PAID {
                    amendment_indicator: $amendment_indicator,
                    report_year: $report_year,
                    report_type: $report_type,
                    image_number: $image_number,
                    line_number: $line_number,
                    form_type: $form_type,
                    schedule_type: $schedule_type,
                    transaction_date: $transaction_date,
                    transaction_amount: $transaction_amount,
                    transaction_primary_general_indicator: $transaction_primary_general_indicator,
                    purpose: $purpose,
                    category: $category,
                    disbursement_category_description: $disbursement_category_description,
                    memo_code: $memo_code,
                    memo_text: $memo_text,
                    fec_record_number: $fec_record_number,
                    file_number: $file_number,
                    transaction_id: $transaction_id,
                    back_reference_transaction_id: $back_reference_transaction_id,
                    is_subitemization: CASE WHEN $back_reference_transaction_id IS NOT NULL THEN true ELSE false END,
                    last_updated: datetime()
                }]->(payee)
            )
    
            // COM, PAC, PTY, CCM - Committee types
            UNION
            WITH committee
            FOREACH (dummy IN CASE WHEN $entity_type IN ['COM', 'PAC', 'PTY', 'CCM'] THEN [1] ELSE [] END |
                MERGE (payee:Committee {name: $payee_name})
                SET payee.city = $city, 
                    payee.state = $state, 
                    payee.zipcode = $zip_code,
                    payee.last_updated = datetime()
                CREATE (committee)-[exp:PAID {
                    amendment_indicator: $amendment_indicator,
                    report_year: $report_year,
                    report_type: $report_type,
                    image_number: $image_number,
                    line_number: $line_number,
                    form_type: $form_type,
                    schedule_type: $schedule_type,
                    transaction_date: $transaction_date,
                    transaction_amount: $transaction_amount,
                    transaction_primary_general_indicator: $transaction_primary_general_indicator,
                    purpose: $purpose,
                    category: $category,
                    disbursement_category_description: $disbursement_category_description,
                    memo_code: $memo_code,
                    memo_text: $memo_text,
                    fec_record_number: $fec_record_number,
                    file_number: $file_number,
                    transaction_id: $transaction_id,
                    back_reference_transaction_id: $back_reference_transaction_id,
                    is_subitemization: CASE WHEN $back_reference_transaction_id IS NOT NULL THEN true ELSE false END,
                    last_updated: datetime()
                }]->(payee)
            )
    
            // ORG - Organization
            UNION
            WITH committee
            FOREACH (dummy IN CASE WHEN $entity_type = 'ORG' OR $entity_type IS NULL THEN [1] ELSE [] END |
                MERGE (payee:Organization {name: $payee_name})
                SET payee.city = $city, 
                    payee.state = $state, 
                    payee.zipcode = $zip_code,
                    payee.last_updated = datetime()
                CREATE (committee)-[exp:PAID {
                    amendment_indicator: $amendment_indicator,
                    report_year: $report_year,
                    report_type: $report_type,
                    image_number: $image_number,
                    line_number: $line_number,
                    form_type: $form_type,
                    schedule_type: $schedule_type,
                    transaction_date: $transaction_date,
                    transaction_amount: $transaction_amount,
                    transaction_primary_general_indicator: $transaction_primary_general_indicator,
                    purpose: $purpose,
                    category: $category,
                    disbursement_category_description: $disbursement_category_description,
                    memo_code: $memo_code,
                    memo_text: $memo_text,
                    fec_record_number: $fec_record_number,
                    file_number: $file_number,
                    transaction_id: $transaction_id,
                    back_reference_transaction_id: $back_reference_transaction_id,
                    is_subitemization: CASE WHEN $back_reference_transaction_id IS NOT NULL THEN true ELSE false END,
                    last_updated: datetime()
                }]->(payee)
            )
    
            // CAN - Candidate
            UNION
            WITH committee
            FOREACH (dummy IN CASE WHEN $entity_type = 'CAN' THEN [1] ELSE [] END |
                MERGE (payee:Candidate {name: $payee_name})
                SET payee.city = $city, 
                    payee.state = $state, 
                    payee.zipcode = $zip_code,
                    payee.last_updated = datetime()
                CREATE (committee)-[exp:PAID {
                    amendment_indicator: $amendment_indicator,
                    report_year: $report_year,
                    report_type: $report_type,
                    image_number: $image_number,
                    line_number: $line_number,
                    form_type: $form_type,
                    schedule_type: $schedule_type,
                    transaction_date: $transaction_date,
                    transaction_amount: $transaction_amount,
                    transaction_primary_general_indicator: $transaction_primary_general_indicator,
                    purpose: $purpose,
                    category: $category,
                    disbursement_category_description: $disbursement_category_description,
                    memo_code: $memo_code,
                    memo_text: $memo_text,
                    fec_record_number: $fec_record_number,
                    file_number: $file_number,
                    transaction_id: $transaction_id,
                    back_reference_transaction_id: $back_reference_transaction_id,
                    is_subitemization: CASE WHEN $back_reference_transaction_id IS NOT NULL THEN true ELSE false END,
                    last_updated: datetime()
                }]->(payee)
            )
        }

        // Handle parent-child relationships for subitemizations
        // Instead of using FOREACH with MATCH inside, we'll use a separate CALL block
        WITH committee
        CALL {
            WITH committee
            MATCH (committee)-[parent_exp:PAID]->(parent_payee)
            WHERE committee.id = $committee_id 
            AND $back_reference_transaction_id IS NOT NULL 
            AND parent_exp.transaction_id = $back_reference_transaction_id
            SET parent_exp.has_subitemizations = true
            RETURN count(*) as subitem_count
        }
        RETURN count(*) as count
        """
        
        # Build parameters dictionary from expenditure object
        params = {
            'committee_id': expenditure.committee_id,
            'amendment_indicator': expenditure.amendment_indicator,
            'report_year': expenditure.report_year,
            'report_type': expenditure.report_type,
            'image_number': expenditure.image_number,
            'line_number': expenditure.line_number,
            'form_type': expenditure.form_type,
            'schedule_type': expenditure.schedule_type,
            'payee_name': expenditure.payee_name,
            'city': expenditure.city,
            'state': expenditure.state,
            'zip_code': expenditure.zip_code,
            'transaction_date': expenditure.transaction_date,
            'transaction_amount': expenditure.transaction_amount,
            'transaction_primary_general_indicator': expenditure.transaction_primary_general_indicator,
            'purpose': expenditure.purpose,
            'category': expenditure.category,
            'disbursement_category_description': expenditure.disbursement_category_description,
            'memo_code': expenditure.memo_code,
            'memo_text': expenditure.memo_text,
            'entity_type': expenditure.entity_type,
            'fec_record_number': expenditure.fec_record_number,
            'file_number': expenditure.file_number,
            'transaction_id': expenditure.transaction_id,
            'back_reference_transaction_id': expenditure.back_reference_transaction_id
        }
        
        result = tx.run(query, **params)
        return result.single()
    
    def __init__(self):
        super(OperatingExpendituresHandler, self).__init__('operating_expenditures')