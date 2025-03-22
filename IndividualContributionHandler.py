from FECDataModel.IndividualContribution import IndividualContribution
from Handler import Handler
from datetime import datetime
from typing import List
#
#
#
#
#  NOT TESTED YEt
#
#
#
##
#
#
#
#  NOT TESTED YEt
#
#
#
##
#
#
#
#  NOT TESTED YEt
#
#
#
##
#
#
#
#  NOT TESTED YEt
#
#
#
#
class IndividualContributionHandler(Handler):

    # FILENAME = 'itcont_2024_20000101_20230330.txt'
    FILENAME = '/itcont_2024_20230331_20230527.txt'
    # FILENAME = '/itcont_2024_20230528_20230709.txt'
    # FILENAME = '/itcont_2024_20230710_20230811.txt'
    # FILENAME = '/itcont_2024_20230812_20230910.txt'
    # FILENAME = '/itcont_2024_20230911_20231007.txt'
    # FILENAME = '/itcont_2024_20231008_20231103.txt'
    # FILENAME = '/itcont_2024_20231104_20231130.txt'
    # FILENAME = '/itcont_2024_20231201_20231228.txt'
    # FILENAME = '/itcont_2024_20231229_20240215.txt'
    # FILENAME = '/itcont_2024_20240216_20240326.txt'
    # FILENAME = '/itcont_2024_20240327_20240428.txt'
    # FILENAME = '/itcont_2024_20240429_20240528.txt'
    # FILENAME = '/itcont_2024_20240529_20240619.txt'
    # FILENAME = '/itcont_2024_20240620_20240709.txt'
    # FILENAME = '/itcont_2024_20240710_20240722.txt'
    # FILENAME = '/itcont_2024_20240723_20240804.txt'
    # FILENAME = '/itcont_2024_20240805_20240817.txt'
    # FILENAME = '/itcont_2024_20240818_20240829.txt'
    # FILENAME = '/itcont_2024_20240830_20240909.txt'
    # FILENAME = '/itcont_2024_20240910_20240918.txt'
    # FILENAME = '/itcont_2024_20240919_20240928.txt'
    # FILENAME = '/itcont_2024_20240929_20241005.txt'
    # FILENAME = '/itcont_2024_20241006_20241013.txt'
    # FILENAME = '/itcont_2024_20241014_20241019.txt'
    # FILENAME = '/itcont_2024_20241020_20241025.txt'
    # FILENAME = '/itcont_2024_20241026_20241030.txt'
    # FILENAME = '/itcont_2024_20241031_20241104.txt'
    # FILENAME = '/itcont_2024_20241105_20241125.txt'
    # FILENAME = '/itcont_2024_20241126_20241227.txt'
    # FILENAME = '/itcont_2024_20241227_20290521.txt'

    DATA_DIRECTORY = '/Users/steve/Documents/Dev/Compass-AI-LLM-RAG/FECDataOriginalTextFiles/manual/individual_contributions'
    TEST_DATA_DIRECTORY = DATA_DIRECTORY + '/2023-2024/indiv24/by_date'

    TEST_DATA_FILE_PATH = TEST_DATA_DIRECTORY + '/' + FILENAME
    
    #
    #
    #
    # Modify to work with multiple files folders in one folder per period
    # 
    #
    #
    #
    #

    def processFiles(self):
        self.processFileInFolder()

    def processFileInFolder(self):
        # process files within folder
        contributions_list = self.parseTextFileWithSeperator(self.TEST_DATA_FILE_PATH, '|') 

        self.batchUploadContributionsToGraphDB(contributions_list)
        return
    
    def parseTextFileWithSeperator(self, text_file_path:str, seperator: str) -> list[IndividualContribution]:
        f = open(text_file_path, "r")
        print(f)

        text_file = f.read()
        file_rows = text_file.splitlines()
        print(len(file_rows))
        
    
        contributions_so_far = 0
        total_contributions = len(file_rows)
        contributions_list = []
        
        for one_row in file_rows:
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
            contributor_name = columns[7] if len(columns[7].strip()) > 0 else None
            city = columns[8] if len(columns[8].strip()) > 0 else None
            state = columns[9] if len(columns[9].strip()) > 0 else None
            zip_code = columns[10] if len(columns[10].strip()) > 0 else None
            employer = columns[11] if len(columns[11].strip()) > 0 else None
            occupation = columns[12] if len(columns[12].strip()) > 0 else None
            transaction_date = columns[13]
            transaction_amount = columns[14]
            other_id = columns[15] if len(columns[15].strip()) > 0 else None
            tran_id = columns[16] if len(columns[16].strip()) > 0 else None
            file_num = columns[17] if len(columns[17].strip()) > 0 else None
            memo_cd = columns[18] if len(columns[18].strip()) > 0 else None
            memo_text = columns[19] if len(columns[19].strip()) > 0 else None
            fec_record_number = columns[20]
            
            # Create the IndividualContribution object
            contribution = IndividualContribution(
                committee_id, amendment_indicator, report_type, transaction_pgi,
                image_num, transaction_type, entity_type, contributor_name,
                city, state, zip_code, employer, occupation,
                transaction_date, transaction_amount, other_id,
                tran_id, file_num, memo_cd, memo_text, fec_record_number
            )
            # print(contribution.printContribution())
            contributions_list.append(contribution)

            contributions_so_far += 1
            if contributions_so_far % 100 == 0:
                print(f"From the text file processed {contributions_so_far}/{total_contributions} individual contributions")
        
        if contributions_so_far == total_contributions:
            print(f"From the text file processed {contributions_so_far}/{total_contributions} individual contributions")

        return contributions_list
    
    def batchUploadContributionsToGraphDB(self, contributions: List[IndividualContribution], batch_size: int = 1000):
        # Use Neo4J graph DB python driver.
        print('  ' + str(self.neo4j_driver))
        total_contributions = len(contributions)
        processed = self.proccessed_counter
        with self.neo4j_driver.session() as session:
            # Process contributions in batches
            for i in range(0, total_contributions, batch_size):
                batch = contributions[i:i + batch_size]
                
                for contribution in batch:
                    try:
                        # Create the Individual and Committee nodes and the CONTRIBUTED_TO relationship
                        session.execute_write(self._create_contribution, contribution)

                        processed += 1
                        if processed % 5000 == 0:
                            print(f"Processed {processed}/{total_contributions} contributions")
                            self.writeCounterToFile(processed, total_contributions)
                                    
                    except Exception as e:
                        print(f"Error processing contribution {contribution.fec_record_number}: {str(e)}")

        if processed == total_contributions:
            print(f"Completed uploading {processed}/{total_contributions} committees")
            self.writeCounterToFile(processed, total_contributions)
        return

    def _create_contribution(self, tx, contribution):
        """
        Create or merge nodes for the Individual, Committee, and the CONTRIBUTED_TO relationship.
        """
        query = """
        // First, ensure the Committee node exists
        MERGE (committee:Committee {id: $committee_id})
        
        // Create or update the Individual node if entity_type is 'IND'
        WITH committee
        MERGE (individual:Individual {
            name: $contributor_name,
            city: $city
        })
        SET individual.employer = $employer,
            individual.occupation = $occupation,
            individual.last_updated = datetime()
            
        // Create the CONTRIBUTED_TO relationship
        WITH committee, individual
        CREATE (individual)-[contrib:CONTRIBUTED_TO {
            amendment_indicator: $amendment_indicator,
            report_type: $report_type,
            transaction_primary_general_indicator: $transaction_primary_general_indicator,
            image_number: $image_number,
            transaction_type: $transaction_type,
            entity_type: $entity_type,
            transaction_date: $transaction_date,
            transaction_amount: $transaction_amount,
            other_id: $other_id,
            transaction_id: $transaction_id,
            file_number: $file_number,
            memo_code: $memo_code,
            memo_text: $memo_text,
            fec_record_number: $fec_record_number,
            last_updated: datetime()
        }]->(committee)
        
        RETURN individual, contrib, committee
        """
        
        # Build parameters dictionary from contribution object
        params = {
            'committee_id': contribution.committee_id,
            'amendment_indicator': contribution.amendment_indicator,
            'report_type': contribution.report_type,
            'transaction_primary_general_indicator': contribution.transaction_primary_general_indicator,
            'image_number': contribution.image_number,
            'transaction_type': contribution.transaction_type,
            'entity_type': contribution.entity_type,
            'contributor_name': contribution.contributor_name,
            'city': contribution.city,
            'state': contribution.state,
            'zip_code': contribution.zip_code,
            'employer': contribution.employer,
            'occupation': contribution.occupation,
            'transaction_date': contribution.transaction_date,
            'transaction_amount': contribution.transaction_amount,
            'other_id': contribution.other_id,
            'transaction_id': contribution.transaction_id,
            'file_number': contribution.file_number,
            'memo_code': contribution.memo_code,
            'memo_text': contribution.memo_text,
            'fec_record_number': contribution.fec_record_number
        }
        
        result = tx.run(query, **params)
        return result.single()
    
    def __init__(self):
        super(IndividualContributionHandler, self).__init__('individual_contribution')