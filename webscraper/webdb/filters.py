import webdb.interface as interface
import webdb.cache as cache


def get_requests_where_session_id(cursor, session_id):
    sql = ("SELECT "
           "REQUEST_ID "
           "FROM REQUESTS "
           "WHERE SESSION_ID = :session_id"
           ";")

    sqlparams = {
        'session_id': session_id
    }
    cursor.execute(sql, sqlparams)

    request_list = []
    for x in cursor.fetchall():
        request_id = x[0]
        request_list.append(
            interface.get_request_where_request_id(
                cursor,
                request_id
            )
        )

    return request_list


def get_requests_where_session_id_and_content_type(cursor, session_id, content_type):

    sql = ("SELECT REQUEST_ID FROM REQUESTS WHERE "
           "SESSION_ID = :session_id AND "
           "RESPONSE_ID IN ("
           "SELECT RESPONSE_ID FROM RESPONSES WHERE "
           "  CONTENT_TYPE_ID = :content_type_id"
           ") "
           ";")

    sqlparams = {
        'session_id': session_id,
        'content_type_id': cache.get_content_type_id_where_content_type(cursor, content_type)
    }

    cursor.execute(sql, sqlparams)

    return [ interface.get_request_where_request_id(cursor, x[0])
        for x in cursor.fetchall()]


def get_response_where_session_id_and_request(cursor, session_id, request):

    uri_id = cache.get_uri_id_where_uri(
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

    return interface.get_response_where_response_id(cursor, response_id)
