import webdb.interface as interface
import webdb.cache as cache
def get_content_type_list(cursor):
    sql = ("SELECT * FROM CONTENT_TYPE_CACHE ("
              "CONTENT_TYPE"
           ") VALUES (?);")
    
    cursor.execute(sql)
    content_types = [x[0] for x in cursor.fetchall() ]
    return content_types


def filter_response_ids_by_content_type(cursor, response_ids, content_type):

    content_type_id = cache.get_content_type_id(cursor, content_type)

    response_ids_str = ",".join(str(x) for x in response_ids)

    sql = ("SELECT ID FROM RESPONSES WHERE "
           "CONTENT_TYPE_ID = :content_type_id AND "
           "ID IN("+response_ids_str+")"
           "")

    params = {
        'content_type_id' : content_type_id
    }
    
    cursor.execute(sql, params)

    return [x[0] for x in cursor.fetchall() ]

def get_responses_of_session_id_and_content_type(cursor, session_id, content_type):
    
    request_list = interface.get_request_list_of_session_id(cursor, session_id)

    response_id_list = [x[1]['response_id'] for x in request_list]

    print(response_id_list,"\n")
    filtered_response_id_list = filter_response_ids_by_content_type(
        cursor, 
        response_id_list, 
        content_type
    )

    print(filtered_response_id_list)
    return [interface.get_response_by_id(cursor, x) for x in filtered_response_id_list]




