import webdb.interface as interface
import webdb.cache as cache


def filter_response_ids_by_content_type(cursor, response_ids, content_type):

    content_type_id = cache.get_content_type_id(cursor, content_type)

    sql = ("SELECT ID FROM RESPONSES WHERE "
           "CONTENT_TYPE_ID = :content_type_id AND "
           "ID IN("+",".join(str(x) for x in response_ids)+")"
           "")

    params = {
        'content_type_id' : content_type_id
    }
    
    cursor.execute(sql, params)

    return [x[0] for x in cursor.fetchall() ]

def get_requests_of_session_id(cursor, session_id):
    sql = ("SELECT "
           "ID "
           "FROM REQUESTS "
           "WHERE SESSION_ID = :session_id"
           ";")

    sqlparams = {
        'session_id' : session_id
    }
    cursor.execute(sql, sqlparams)

    request_list = []
    for x in cursor.fetchall():
        request_id = x[0]
        request, (session_id, response_id) = interface.get_request_by_id(cursor, request_id)
        request_list.append(
            (request, 
                {
                    'session_id' : session_id, 
                    'request_id' : request_id, 
                    'response_id' : response_id
                }
            )
        )
    
    return request_list



def get_requests_of_session_id_and_content_type(cursor, session_id, content_type):
    
    request_list = get_requests_of_session_id(cursor, session_id)

    filtered_response_id_list = filter_response_ids_by_content_type(
        cursor, 
        (x[1]['response_id'] for x in request_list), 
        content_type
    )

    filtered_response_id_set = set(filtered_response_id_list)

    return [x for x in request_list if x[1]['response_id'] in filtered_response_id_set]

def get_response_of_session_id_and_request(cursor, session_id, request):

    uri_id = cache.get_id_of_uri(
        cursor,
        request.scheme,
        request.netloc,
        request.path,
        request.params,
        request.query,
        request.fragment
    )

    sql = ("SELECT RESPONSE_ID FROM REQUESTS "
           "WHERE "
           "URI_ID =:uri_id AND "
           "SESSION_ID =:session_id;")

    params = {
        'uri_id': uri_id,
        'session_id': session_id
    }

    cursor.execute(sql, params)
    x = cursor.fetchone()
    response_id = x[0]

    return interface.get_response_by_id(cursor, response_id)



