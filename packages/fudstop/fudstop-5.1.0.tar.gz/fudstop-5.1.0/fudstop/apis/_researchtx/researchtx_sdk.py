from imps import *

import os
from dotenv import load_dotenv
load_dotenv()
import requests
case_id = os.environ.get('divorce_case_id')


class ResearchTexasSDK:
    def __init__(self):
        pass


    async def get_filings(self,id:str=case_id, page_size:int=50, search_text:str='', headers:str=None):
        """Get case filings"""
        url = f"https://research.txcourts.gov/CourtRecordsSearch/case/{id}/filings"
        
        r = requests.post(url=url, data={"pageSize":page_size,"pageIndex":0,"sortNewestToOldest":False,"searchText":search_text,"isSearchAll":True,"eventType":0}, headers=headers)
        print(r)
        if r.status_code == 200:
            r = r.json()
            
            events = r.get('events')

            filingID = [i.get('filingID') for i in events]
            filingCode = [i.get('filingCode') for i in events]
            description = [i.get('description') for i in events]
            submitted = [i.get('submitted') for i in events]
            submitterFullName = [i.get('submitterFullName') for i in events]
            docketed = [i.get('docketed') for i in events]
            isHiddenFromPublic = [i.get('isHiddenFromPublic') for i in events]
            hasManualSecurityOverride = [i.get('hasManualSecurityOverride') for i in events]
            jurisdiction = [i.get('jurisdiction') for i in events]
            jurisdictionKey = [i.get('jurisdictionKey') for i in events]
            externalKey = [i.get('externalKey') for i in events]
            ofsFilingID = [i.get('ofsFilingID') for i in events]
            hasNoReportedDocuments = [i.get('hasNoReportedDocuments') for i in events]
            case = [i.get('case') for i in events]
            hasHiddenDocument = [i.get('hasHiddenDocument') for i in events]
            hasNoDocument = [i.get('hasNoDocument') for i in events]
            eventType = [i.get('eventType') for i in events]
            documentIndexNumber = [i.get('documentIndexNumber') for i in events]
            type = [i.get('type') for i in events]
            highlights = [i.get('highlights') for i in events]

            documents = [i.get('documents') for i in events]

            flat_docs = [item for sublist in documents for item in sublist]

            documentID = [i.get('documentID') for i in flat_docs]
            documentKey = [i.get('documentKey') for i in flat_docs]
            documentCategoryCode = [i.get('documentCategoryCode') for i in flat_docs]
            documentSecurityCode = [i.get('documentSecurityCode') for i in flat_docs]
            fileName = [i.get('fileName') for i in flat_docs]
            fileSize = [i.get('fileSize') for i in flat_docs]
            pageCount = [i.get('pageCount') for i in flat_docs]
            description = [i.get('description') for i in flat_docs]
            isSecured = [i.get('isSecured') for i in flat_docs]
            isHiddenFromPublic = [i.get('isHiddenFromPublic') for i in flat_docs]
            isSealed = [i.get('isSealed') for i in flat_docs]
            hasManualSecurityOverride = [i.get('hasManualSecurityOverride') for i in flat_docs]
            documentStatus = [i.get('documentStatus') for i in flat_docs]
            isDocumentOnDemand = [i.get('isDocumentOnDemand') for i in flat_docs]
            externalSource = [i.get('externalSource') for i in flat_docs]
            externalKey = [i.get('externalKey') for i in flat_docs]
            jurisdictionKey = [i.get('jurisdictionKey') for i in flat_docs]
            isOwned = [i.get('isOwned') for i in flat_docs]
            isFree = [i.get('isFree') for i in flat_docs]
            isPrivileged = [i.get('isPrivileged') for i in flat_docs]
            price = [i.get('price') for i in flat_docs]
            priceKey = [i.get('priceKey') for i in flat_docs]
            isInCart = [i.get('isInCart') for i in flat_docs]
            expires = [i.get('expires') for i in flat_docs]
            filingId = [i.get('filingId') for i in flat_docs]
            isRedactedVersionAvailable = [i.get('isRedactedVersionAvailable') for i in flat_docs]


            data_dict = {
                'filing_code': filingCode,
                'description': description,
                'submitted': submitted,
                'submitter_full_name': submitterFullName,
                'docketed': docketed,
                'jurisdiction': jurisdiction,
                'jurisdiction_key': jurisdictionKey,
                'external_key': externalKey,
                'ofs_filing_id': ofsFilingID,
                'event_type': eventType,
                'document_index_number': documentIndexNumber,
                'highlights': highlights,
                'document_id': documentID,
                'document_key': documentKey,
                'document_category_code': documentCategoryCode,
                'document_security_code': documentSecurityCode,
                'file_name': fileName,
                'file_size': fileSize,
                'page_count': pageCount,
                'document_status': documentStatus,
                'external_source': externalSource,
                'price': price,
                'price_key': priceKey,
                'is_in_cart': isInCart,
                'expires': expires,
                'filing_id': filingId,
                'is_redacted_version_available': isRedactedVersionAvailable
            }
                        # Find the maximum length
            max_length = max(len(lst) for lst in data_dict.values())

            # Ensure all lists are of the same length by padding shorter lists with None
            for key in data_dict:
                if len(data_dict[key]) < max_length:
                    data_dict[key].extend([None] * (max_length - len(data_dict[key])))
            df = pd.DataFrame(data_dict)

            df.to_csv('filings_divorce.csv')


            return df