import CandidateHandler
import CommitteeOrganizationHandler
import CandidateCommitteeLinkagesHandler
import HouseSenateCurrentCampaignsHandler
import PACAndPartyCommitteeSummaryHandler
import IndividualContributionHandler
import CommitteeToCandidateContributionHandler
import CommitteeToOtherCommitteeContributionHandler
import OperatingExpendituresHandler

def main():
    # Initialize uploader
    # uploader = CandidateHandler.CandidateHandler()
    # uploader = CommitteeOrganizationHandler.CommitteeOrganizationHandler()
    # uploader = CandidateCommitteeLinkagesHandler.CandidateCommitteeLinkagesHandler()
    # uploader = HouseSenateCurrentCampaignsHandler.HouseSenateCurrentCampaignsHandler()
    # uploader = PACAndPartyCommitteeSummaryHandler.PACAndPartyCommitteeSummaryHandler()
    uploader = IndividualContributionHandler.IndividualContributionHandler()
    # uploader = CommitteeToCandidateContributionHandler.CommitteeToCandidateContributionHandler()
    # uploader = CommitteeToOtherCommitteeContributionHandler.CommitteeToOtherCommitteeContributionHandler()
    # uploader = OperatingExpendituresHandler.OperatingExpendituresHandler()

    uploader.processFiles()

if __name__ == "__main__":
    main()