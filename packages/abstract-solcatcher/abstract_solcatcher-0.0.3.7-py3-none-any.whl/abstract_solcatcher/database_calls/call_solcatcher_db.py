import asyncio,json
from abstract_solana import get_rpc_dict
from abstract_apis import postRpcRequest,asyncPostRpcRequest,asyncPostRequest,get_async_response,postRequest
async def getSolcatcherPost(endpoint, *args, **kwargs):
    # Ensure that the arguments are fully resolved and not coroutines
    resolved_args = [await arg if asyncio.iscoroutine(arg) else arg for arg in args]
    
    # Check for coroutines in kwargs and resolve them without reusing
    resolved_kwargs = {}
    for k, v in kwargs.items():
        if asyncio.iscoroutine(v):
            resolved_kwargs[k] = await v
        else:
            resolved_kwargs[k] = v
    
    # Now pass resolved data into the request
    return await asyncPostRequest(
        url="https://solcatcher.io",
        endpoint=endpoint,
        data={"args": resolved_args, **resolved_kwargs}
    )
def get_rate_limit(*args,**kwargs):
    return get_async_response(getSolcatcherPost,'get_rate_limit_url',*args,**kwargs)
def insert_db(*args,**kwargs):
    return get_async_response(getSolcatcherPost,'insert_into_db',*args,**kwargs)
def fetch_from_db(*args,**kwargs):
    return get_async_response(getSolcatcherPost,'fetch_from_db',*args,**kwargs)
def get_templates(method=None):
    return postRequest('https://solcatcher.io/get_solcatcher_templates',data={"args":[method]})
def call_solcatcher_api(*args,**kwargs):
    return get_async_response(getSolcatcherPost,'/api/v1/rpc_call',*args,**kwargs)
def solcatcherApi(method,*args,**kwargs):
    return get_async_response(getSolcatcherPost,method,*args,**kwargs)
def call_solcatcher_db_api(method,*args,**kwargs):
    insertTable = get_templates(method=method)
    freshCall = insertTable.get('freshCall')
    tableName=insertTable.get('tableName')
    if insertTable.get('rpcCall'):
        rpc_dict = get_rpc_dict(method,*args,**kwargs)
        searchValue=rpc_dict.get('params')[0]
        if not freshCall:
            insertValue  = fetch_from_db(tableName=tableName,searchValue=searchValue)
            if insertValue:
                return insertValue
        url = get_rate_limit(method)
        insertValue = postRpcRequest(url=url.get('url'),**rpc_dict)
        url = get_rate_limit(method,insertValue)
        insert_db(tableName=tableName,searchValue=searchValue,insertValue=insertValue)
        return insertValue
    else:
        searchValue=args[0]
        if not freshCall:
            insertValue  = fetch_from_db(tableName=tableName,searchValue=searchValue)
            if insertValue:
                return insertValue
        insertValue = postRequest(url=f'https://solcatcher.io/{method}',data=json.dumps({"args":args,**kwargs}))
        url = get_rate_limit(method,insertValue)
        insert_db(tableName=tableName,searchValue=searchValue,insertValue=insertValue)
        return insertValue    
    return response
