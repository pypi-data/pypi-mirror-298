from api_functions import solcatcher_api_call
from abstract_solana import get_pubkey,Pubkey,return_oldest_last_and_original_length_from_signature_array,get_sigkey
def async_getGenesisSignature(address,before=None,limit=None,commitment=None):
    before = before or None
    genesisSignature = None
    limit = limit or 1000
    commitment = commitment or "confirmed"
    while True:
        signatureArray = solcatcher_api_call('getSignaturesForAddress',address=address,before=before,limit=limit,commitment=commitment)
        signatureArrayInfo = return_oldest_last_and_original_length_from_signature_array(signatureArray)
        genesisSignature = signatureArrayInfo.get("oldestValid") or genesisSignature
        if before == signatureArrayInfo.get("oldest") or signatureArrayInfo.get("length") < limit:
            return genesisSignature
        before = signatureArrayInfo.get("oldest")
    return genesisSignature

async def getParsedTransaction(signature: Signature=None,
                                     txnData=None,
                                     programId=None,
                                     encoding: str = None,
                                     commitment: Optional[Commitment] = None,
                                     maxSupportedTransactionVersion: Optional[int] = None):
    if not txnData and not signature:
        return
    if txnData and not signature:
        signature = get_sig_from_txn_data(txnData)
    if signature and not txnData:
        txnData = await gettransaction(signature=signature,encoding=encoding,commitment=commitment,maxSupportedTransactionVersion=maxSupportedTransactionVersion)
    parsedTxnData = await search_Db(method.lower(), signature)
    if not parsedTxnData:
        parsedTxnData = await parse_pool_info_from_lp_transaction(txnData=safe_json_loads(txnData),programId=programId)
        await insert_Db(method.lower(), str(signature), (str(signature), json.dumps(parsedTxnData)))
    return parsedTxnData
