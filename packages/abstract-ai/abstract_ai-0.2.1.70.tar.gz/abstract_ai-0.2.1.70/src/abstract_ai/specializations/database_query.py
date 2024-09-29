from abstract_utilities import safe_json_loads,make_list
from .responseContentParser import get_updated_response_content,get_file_path,get_title
from abstract_database import ensure_db_manager
from ..general_query import make_general_query
def get_xlsx_file_path_from_response_vars(data=None,file_path=None,db_mgr=None,env_path=None,dbType=None,dbName=None,conn_mgr=None):
    db_mgr = ensure_db_manager(db_mgr=db_mgr,env_path=env_path,dbName=dbName,dbType=dbType,conn_mgr=conn_mgr)
    response_content = get_updated_response_content(data=data,file_path=file_path)
    new_directory = os.path.join(os.path.dirname(get_file_path(response_content)), 'queries')
    os.makedirs(new_directory, exist_ok=True)
    new_file_path = os.path.join(new_directory, f"{get_title(response_content)}.xlsx")
    return new_file_path
def get_raw_response_for_query(prompt,tableName,db_mgr=None,env_path=None,dbType=None,dbName=None,conn_mgr=None):
    db_mgr = ensure_db_manager(db_mgr=db_mgr,env_path=env_path,dbName=dbName,dbType=dbType,conn_mgr=conn_mgr)
    data = db_mgr.get_instruction_from_tableName(tableName)
    raw_response = make_general_query(prompt=[prompt],data=str(data),instruction_bools={"database_query":True})
    if isinstance(raw_response,list):
        raw_response = safe_json_loads(raw_response[0])
    return raw_response
def get_auto_db_query(prompt,tableName,db_mgr=None,env_path=None,dbType=None,dbName=None,conn_mgr=None):
    db_mgr = ensure_db_manager(db_mgr=db_mgr,env_path=env_path,dbName=dbName,dbType=dbType,conn_mgr=conn_mgr)
    raw_response = get_raw_response_for_query(prompt,tableName,db_mgr=db_mgr)
    xlsx_file_path = get_xlsx_file_path_from_response_vars(data=raw_response)
    response_content = get_updated_response_content(data=raw_response)
    query_result = make_list(get_any_value(response_content,'database_query'))[-1]
    return db_mgr.get_query_save_to_excel(query_result, file_path=xlsx_file_path)
