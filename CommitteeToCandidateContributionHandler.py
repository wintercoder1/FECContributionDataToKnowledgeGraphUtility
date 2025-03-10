from FECDataModel.CommitteeToCandidateContribution import CommitteeToCandidateContribution
from Handler import Handler
from datetime import datetime
from typing import List

class CommitteeToCandidateContributionHandler(Handler):

    DATA_DIRECTORY = '/Users/steve/Documents/Dev/DEICheck.ai-LLM-RAG/FECData/manual/contributions_from_committees_to_candidates'
    TEST_DATA_DIRECTORY = DATA_DIRECTORY + '/2023-2024'
    TEST_DATA_FILE_PATH = TEST_DATA_DIRECTORY + '/contributions-from-committees-to-candidates-2023-2024.txt'
    
    def processFiles(self):
        self.processFileInFolder()

    def processFileInFolder(self):
        # process files within folder
        contributions_list = self.parseTextFileWithSeperator(self.TEST_DATA_FILE_PATH, '|') 

        self.batchUploadContributionsToGraphDB(contributions_list)
        return
    
    def parseTextFileWithSeperator(self, text_file_path:str, seperator: str) -> list[CommitteeToCandidateContribution]:
        f = open(text_file_path, "r")
        print(f)

        text_file = f.read()
        file_rows = text_file.splitlines()
        print(len(file_rows))
 
        # Helper function to parse date string to date object
        def parse_date(date_str):
            if date_str and date_str.strip():
                try:
                    return datetime.strptime(date_str, '%m%d%Y').date()
                except:
                    return None
            return None
    
        contributions_so_far = 0
        total_contributions = len(file_rows)
        contributions_list = []

        for one_row in file_rows:

            if len(one_row) < 22:  # We expect 22 columns based on the spec
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
            transaction_date = parse_date(columns[13])
            transaction_amount = columns[14]
            other_id = columns[15] if len(columns[15].strip()) > 0 else None
            candidate_id = columns[16] if len(columns[16].strip()) > 0 else None
            tran_id = columns[17] if len(columns[17].strip()) > 0 else None
            file_num = columns[18] if len(columns[18].strip()) > 0 else None
            memo_cd = columns[19] if len(columns[19].strip()) > 0 else None
            memo_text = columns[20] if len(columns[20].strip()) > 0 else None
            sub_id = columns[21]
            
            # Create the CommitteeToCandidateContribution object
            contribution = CommitteeToCandidateContribution(
                committee_id, amendment_indicator, report_type, transaction_pgi,
                image_num, transaction_type, entity_type, contributor_name,
                city, state, zip_code, employer, occupation,
                transaction_date, transaction_amount, other_id, candidate_id,
                tran_id, file_num, memo_cd, memo_text, sub_id
            )
            
            contributions_list.append(contribution)
            # contribution.printContribution()

            contributions_so_far += 1
            if contributions_so_far % 100 == 0:
                print(f"From the text file processed {contributions_so_far}/{total_contributions} committee-to-candidate contributions")
        
        if contributions_so_far >= total_contributions:
            print(f"From the text file processed {contributions_so_far}/{total_contributions} committee-to-candidate contributions")

        return contributions_list
    
    def batchUploadContributionsToGraphDB(self, contributions: List[CommitteeToCandidateContribution], batch_size: int = 1000):
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
                        # Create the Committee, Candidate nodes and the CONTRIBUTED_TO relationship
                        session.execute_write(self._create_contribution, contribution)

                        processed += 1
                        if processed % 100 == 0:
                            print(f"Processed {processed}/{total_contributions} contributions")
                            self.writeCounterToFile(processed, total_contributions)
                                    
                    except Exception as e:
                        print(f"Error processing contribution {contribution.committee_id} to {contribution.candidate_id} fec record: {contribution.fec_record_number}: {str(e)}")

        if processed >= total_contributions:
            print(f"Completed uploading {processed}/{total_contributions} committees")
            self.writeCounterToFile(processed, total_contributions)
        return

    def _create_contribution(self, tx, contribution):
        """
        Create or merge nodes for the Committee, Candidate, and the CONTRIBUTED_TO relationship.
        """
        query = """
        // First, ensure the Donor Committee node exists
        MERGE (donor_committee:Committee {id: $committee_id})
        SET donor_committee.name = $contributor_name,
            donor_committee.city = $city,
            donor_committee.state = $state,
            donor_committee.zip_code = $zip_code,
            donor_committee.last_updated = datetime()
        
        // Next, ensure the Candidate node exists
        WITH donor_committee
        MERGE (candidate:Candidate {id: $candidate_id})
        
        // Then ensure the Recipient Committee node exists (if other_id is provided) Now called other_candidate_or_committee_id
        WITH donor_committee, candidate
        OPTIONAL MATCH (recipient_committee:Committee {id: $other_candidate_or_committee_id})
        
        // Create the CONTRIBUTED_TO relationship
        WITH donor_committee, candidate, recipient_committee
        FOREACH (committee IN CASE WHEN recipient_committee IS NOT NULL THEN [recipient_committee] ELSE [] END |
            CREATE (donor_committee)-[contrib_to_committee:CONTRIBUTED_TO {
                amendment_indicator: $amendment_indicator,
                report_type: $report_type,
                transaction_primary_general_indicator: $transaction_primary_general_indicator,
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
            }]->(committee)
        )
        
        WITH donor_committee, candidate
        CREATE (donor_committee)-[contrib_to_candidate:CONTRIBUTED_TO_CANDIDATE {
            amendment_indicator: $amendment_indicator,
            report_type: $report_type,
            transaction_primary_general_indicator: $transaction_primary_general_indicator,
            image_number: $image_number,
            transaction_type: $transaction_type,
            entity_type: $entity_type,
            transaction_date: $transaction_date,
            transaction_amount: $transaction_amount,
            recipient_committee_id: $other_candidate_or_committee_id,
            transaction_contribution_id: $transaction_contribution_id,
            file_number: $file_number,
            memo_code: $memo_code,
            memo_text: $memo_text,
            fec_record_number: $fec_record_number,
            last_updated: datetime()
        }]->(candidate)
        
        RETURN donor_committee, contrib_to_candidate, candidate
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
            'other_candidate_or_committee_id': contribution.other_candidate_or_committee_id,
            'candidate_id': contribution.candidate_id,
            'transaction_contribution_id': contribution.transaction_contribution_id,
            'file_number': contribution.file_number,
            'memo_code': contribution.memo_code,
            'memo_text': contribution.memo_text,
            'fec_record_number': contribution.fec_record_number
        }
        
        result = tx.run(query, **params)
        return result.single()
    
    def __init__(self):
        super(CommitteeToCandidateContributionHandler, self).__init__('committee_to_candidate_contributions')