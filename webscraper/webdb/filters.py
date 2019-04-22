import webdb.interface as interface
def get_content_type_list(cursor):
    sql = ("SELECT * FROM CONTENT_TYPE_CACHE ("
              "CONTENT_TYPE"
           ") VALUES (?);")
    
    cursor.execute(sql)
    content_types = [x[0] for x in cursor.fetchall() ]
    return content_types


def filter_response_ids_by_content_type(cursor, response_ids, content_type):

    sql = ("SELECT ID FROM REQUESTS WHERE"
           "CONTENT_TYPE_ID = :content_type_id")
    

def get_responses_of_session_and_content_type(cursor, session_id, content_type):
    
    request_list = interface.get_request_list_of_session_id(cursor, session_id)

    response_id_list = [x[1]['response_id'] for x in request_list]


