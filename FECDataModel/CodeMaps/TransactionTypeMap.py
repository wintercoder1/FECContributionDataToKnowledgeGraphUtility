transaction_type_map = {
    '10'   : 'Contribution to Independent Expenditure-Only Committees (Super PACs), Political Committees with non-contribution accounts (Hybrid PACs) and nonfederal party "soft money" accounts (1991-2002) from a person (individual, partnership, limited liability company, corporation, labor organization, or any other organization or group of persons)',
    '10J'  : '''Memo - Recipient committee's percentage of nonfederal receipt from a person (individual, partnership, limited liability company, corporation, labor organization, or any other organization or group of persons)''',
    '11	'  : 'Native American Tribe contribution',
    '11J'  : '''Memo - Recipient committee's percentage of contribution from Native American Tribe given to joint fundraising committee''',
    '12'   : 'Nonfederal other receipt - Levin Account (Line 2)',
    '13'   : 'Inaugural donation accepted',
    '15'   : 'Contribution to political committees (other than Super PACs and Hybrid PACs) from an individual, partnership or limited liability company',
    '15C'  : 'Contribution from candidate',
    '15E'  : 'Earmarked contributions to political committees (other than Super PACs and Hybrid PACs) from an individual, partnership or limited liability company',
    '15F'  : 'Loans forgiven by candidate',
    '15I'  : '''Earmarked contribution from an individual, partnership or limited liability company received by intermediary committee and passed on in the form of contributor's check (intermediary in)''',
    '15J'  : '''Memo - Recipient committee's percentage of contribution from an individual, partnership or limited liability company given to joint fundraising committee''',
    '15K'  : 'Contribution received from registered filer disclosed on authorized committee report',
    '15T'  : '''Earmarked contribution from an individual, partnership or limited liability company received by intermediary committee and entered into intermediary's treasury (intermediary treasury in)''',
    '15Z'  : 'In-kind contribution received from registered filer',
    '16C'  : 'Loan received from the candidate',
    '16F'  : 'Loan received from bank',
    '16G'  : 'Loan from individual',
    '16H'  : 'Loan from registered filers',
    '16J'  : 'Loan repayment from individual',
    '6K'   : 'Loan repayment from from registered filer',
    '16L'  : 'Loan repayment received from unregistered entity',
    '16R'  : 'Loan received from registered filers',
    '16U'  : 'Loan received from unregistered entity',
    '17R'  : 'Contribution refund received from registered entity',
    '17U'  : 'Refund/Rebate/Return received from unregistered entity',
    '17Y'  : 'Refund/Rebate/Return from individual or corporation',
    '17Z'  : 'Refund/Rebate/Return from candidate or committee',
    '18G'  : 'Transfer in from affiliated committee',
    '18H'  : 'Honorarium received',
    '18J'  : '''Memo - Recipient committee's percentage of contribution from a registered committee given to joint fundraising committee''',
    '18K'  : 'Contribution received from registered filer',
    '18L'  : 'Bundled contribution',
    '18U'  : 'Contribution received from unregistered committee',
    '19'   : 'Electioneering communication donation received',
    '20'   : 'Nonfederal disbursement - nonfederal party "soft money" accounts (1991-2002)',
    '20A'  : 'Nonfederal disbursement - Levin Account (Line 4A) Voter Registration',
    '20B'  : 'Nonfederal Disbursement - Levin Account (Line 4B) Voter Identification',
    '20C'  : 'Loan repayment made to candidate',
    '20D'  : 'Nonfederal disbursement - Levin Account (Line 4D) Generic Campaign',
    '20F'  : 'Loan repayment made to banks',
    '20G'  : 'Loan repayment made to individual',
    '20R'  : 'Loan repayment made to registered filer',
    '20V'  : 'Nonfederal disbursement - Levin Account (Line 4C) Get Out The Vote',
    '20Y'  : 'Nonfederal refund',
    '21Y'  : 'Native American Tribe refund',
    '22G'  : 'Loan to individual',
    '22H'  : 'Loan to candidate or committee',
    '22J'  : 'Loan repayment to individual',
    '22K'  : 'Loan repayment to candidate or committee',
    '22L'  : 'Loan repayment to bank',
    '22R'  : 'Contribution refund to unregistered entity',
    '22U'  : 'Loan repaid to unregistered entity',
    '22X'  : 'Loan made to unregistered entity',
    '22Y'  : 'Contribution refund to an individual, partnership or limited liability company',
    '22Z'  : 'Contribution refund to candidate or committee',
    '23Y'  : 'Inaugural donation refund',
    '24A'  : 'Independent expenditure opposing election of candidate',
    '24C'  : 'Coordinated party expenditure',
    '24E'  : 'Independent expenditure advocating election of candidate',
    '24F'  : 'Communication cost for candidate (only for Form 7 filer)',
    '24G'  : 'Transfer out to affiliated committee',
    '24H'  : 'Honorarium to candidate',
    '24I'  : '''Earmarked contributor's check passed on by intermediary committee to intended recipient (intermediary out)''',
    '24K'  : 'Contribution made to nonaffiliated committee',
    '24N'  : 'Communication cost against candidate (only for Form 7 filer)',
    '24P'  : 'Contribution made to possible federal candidate including in-kind contributions',
    '24R'  : 'Election recount disbursement',
    '24T'  : '''Earmarked contribution passed to intended recipient from intermediary's treasury (treasury out)''',
    '24U'  : 'Contribution made to unregistered entity',
    '24Z'  : 'In-kind contribution made to registered filer',
    '28L'  : 'Refund of bundled contribution',
    '29'   : 'Electioneering Communication disbursement or obligation',
    '30'   : 'Convention Account receipt from an individual, partnership or limited liability company',
    '30E'  : 'Convention Account - Earmarked receipt',
    '30F'  : '''Convention Account - Memo - Recipient committee's percentage of contributions from a registered committee given to joint fundraising committee''',
    '30G'  : 'Convention Account - transfer in from affiliated committee',
    '30J'  : '''Convention Account - Memo - Recipient committee's percentage of contributions from an individual, partnership or limited liability company given to joint fundraising committee''',
    '30K'  : 'Convention Account receipt from registered filer',
    '30T'  : 'Convention Account receipt from Native American Tribe',
    '31'   : 'Headquarters Account receipt from an individual, partnership or limited liability company',
    '31E'  : 'Headquarters Account - Earmarked receipt',
    '31F'  : '''Headquarters Account - Memo - Recipient committee's percentage of contributions from a registered committee given to joint fundraising committee''',
    '31G'  : 'Headquarters Account - transfer in from affiliated committee',
    '31J'  : '''Headquarters Account - Memo - Recipient committee's percentage of contributions from an individual, partnership or limited liability company given to joint fundraising committee''',
    '31K'  : 'Headquarters Account receipt from registered filer',
    '31T'  : 'Headquarters Account receipt from Native American Tribe',
    '32'   : 'Recount Account receipt from an individual, partnership or limited liability company',
    '32E'  : 'Recount Account - Earmarked receipt',
    '32F'  : '''Recount Account - Memo - Recipient committee's percentage of contributions from a registered committee given to joint fundraising committee''',
    '32G'  : 'Recount Account - transfer in from affiliated committee',
    '32J'  : '''Recount Account - Memo - Recipient committee's percentage of contributions from an individual, partnership or limited liability company given to joint fundraising committee''',
    '32K'  : 'Recount Account receipt from registered filer',
    '32T'  : 'Recount Account receipt from Native American Tribe',
    '40'   : 'Convention Account disbursement',
    '40Y'  : 'Convention Account refund to an individual, partnership or limited liability company',
    '40T'  : 'Convention Account refund to Native American Tribe',
    '40Z'  : 'Convention Account refund to registered filer',
    '41'   : 'Headquarters Account disbursement',
    '41Y'  : 'Headquarters Account refund to an individual, partnership or limited liability company',
    '41T'  : 'Headquarters Account refund to Native American Tribe',
    '41Z'  : 'Headquarters Account refund to registered filer',
    '42'   : 'Recount Account disbursement',
    '42Y'  : 'Recount Account refund to an individual, partnership or limited liability company',
    '42T'  : 'Recount Account refund to Native American Tribe',
    '42Z'  : 'Recount Account refund to registered filer'
}