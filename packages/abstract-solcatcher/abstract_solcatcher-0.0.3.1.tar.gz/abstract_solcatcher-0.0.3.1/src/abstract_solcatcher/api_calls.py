from abstract_apis import asyncPostRequest
from abstract_solana import get_rpc_dict,abstract_solana_rate_limited_call,get_pubkey,Pubkey,return_oldest_last_and_original_length_from_signature_array,get_sigkey
from abstract_solana.abstract_rpcs.rate_limiter import RateLimiter
from .utils import getSolcatcherUrl,get_async_response
from .abstract_rate_limit import asyncMakeLimitedCall
async def async_solcatcher_api_call(endpoint, *args, **kwargs):
    return await asyncPostRequest(url=getSolcatcherUrl(),endpoint=endpoint,status_code=True,data={'args': args, **kwargs})
def solcatcher_api_call(endpoint,*args,**kwargs):        
    response = get_async_response(async_solcatcher_api_call,endpoint, *args, **kwargs)
    response,status_code = response[0],response[1]
    if status_code < 500:
        return response
    response = abstract_solana_rate_limited_call(endpoint,*args,**kwargs)
    return response
def solcatcherSolanaDbCall(method,*args,**kwargs):
    rpc_dict =  get_rpc_dict(method,*args,**kwargs)
    return solcatcher_api_call(endpoint='api/v1/rpc_call',**rpc_dict)


