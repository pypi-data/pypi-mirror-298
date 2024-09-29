from abstract_utilities import safe_json_loads,make_list,os,get_any_value
from .responseContentParser import get_updated_response_content,get_file_path,get_title
from abstract_database import ensure_db_manager,flatten_json,pd
from abstract_apis import get_async_response
from abstract_pandas import safe_excel_save
import asyncio,logging
from concurrent.futures import ThreadPoolExecutor
logging.basicConfig(
    level=logging.INFO,                     # Set the logging level (INFO, in this case)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.StreamHandler()             # Also log to the console (optional)
    ]
)
logger = logging.getLogger(__name__)
# Define the executor globally
executor = ThreadPoolExecutor()

from ..gpt_classes.nogui_selection.general_query import make_general_query
async def async_safe_excel_save(df, original_file_path, index=False, suffix=None, engine=None):
    """
    Asynchronous wrapper for safe_excel_save, running it in an executor.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor, safe_excel_save, df, original_file_path, index, suffix, engine
    )
async def save_to_excel_async(rows, file_path="output.xlsx"):
    """Save query results to an Excel file asynchronously."""
    excel_data = []
    if rows:
        for row in rows:
            # Ensure the row is a list before flattening
            row = list(row) if isinstance(row, tuple) else row
            # Flatten JSON and append to data
            excel_data.append(flatten_json(row, parent_key='', sep='_'))

        # Convert data to a pandas DataFrame
        df = pd.DataFrame(excel_data)

        # Use the asynchronous safe save function
        await async_safe_excel_save(df, file_path)
        logging.info(f"Excel file saved asynchronously to {file_path}.")
async def search_multiple_fields(query_result=None,db_mgr=None,env_path=None,dbType=None,dbName=None,conn_mgr=None):
    db_mgr = ensure_db_manager(db_mgr=db_mgr,env_path=env_path,dbType=dbType,dbName=dbName,conn_mgr=conn_mgr)
    return db_mgr.search_multiple_fields(**query_result)
async def async_get_xlsx_file_path_from_response_vars(data=None,file_path=None,db_mgr=None,env_path=None,dbType=None,dbName=None,conn_mgr=None):
    db_mgr = ensure_db_manager(db_mgr=db_mgr,env_path=env_path,dbType=dbType,dbName=dbName,conn_mgr=conn_mgr)
    response_content = get_updated_response_content(data=data,file_path=file_path)
    new_directory = os.path.join(os.path.dirname(get_file_path(response_content)), 'queries')
    os.makedirs(new_directory, exist_ok=True)
    new_file_path = os.path.join(new_directory, f"{get_title(response_content)}.xlsx")
    return new_file_path
async def async_get_raw_response_for_query(prompt,tableName,db_mgr=None,env_path=None,dbType=None,dbName=None,conn_mgr=None):
    db_mgr = ensure_db_manager(db_mgr=db_mgr,env_path=env_path,dbType=dbType,dbName=dbName,conn_mgr=conn_mgr)
    data = db_mgr.get_instruction_from_tableName(tableName)
    raw_response = await make_general_query(prompt=[prompt],data=str(data),instruction_bools={"database_query":True})
    if isinstance(raw_response,list):
        raw_response = safe_json_loads(raw_response[0])
    return raw_response
async def async_get_auto_db_query(prompt,tableName,db_mgr=None,env_path=None,dbType=None,dbName=None,conn_mgr=None):
    db_mgr = ensure_db_manager(db_mgr=db_mgr,env_path=env_path,dbType=dbType,dbName=dbName,conn_mgr=conn_mgr)
    raw_response = await async_get_raw_response_for_query(prompt,tableName,db_mgr=db_mgr)
    
    xlsx_file_path = await async_get_xlsx_file_path_from_response_vars(data=raw_response)
    response_content = get_updated_response_content(data=raw_response)
    query_result = make_list(get_any_value(response_content,'database_query'))[-1]
    query_response = await search_multiple_fields(query_result=query_result,db_mgr=None,env_path=None,dbType=None,dbName=None,conn_mgr=None)
    await save_to_excel_async(rows = query_response,file_path = xlsx_file_path)
    response_content["excelPath"]=xlsx_file_path
    return response_content
def get_auto_db_query(prompt,tableName,db_mgr=None,env_path=None,dbType=None,dbName=None,conn_mgr=None):
    return get_async_response(async_get_auto_db_query,prompt,tableName,db_mgr=db_mgr,env_path=env_path,dbType=dbType,dbName=dbName,conn_mgr=conn_mgr)
