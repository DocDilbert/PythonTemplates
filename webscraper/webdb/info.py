

def compute_content_size(cursor):
    sql = ("SELECT sum(length(CONTENT)) FROM CONTENT_CACHE;")
    cursor.execute(sql)
    x = cursor.fetchone()
    content_size = x[0]
    return content_size


def info(cursor):
    sql = ("SELECT count(*) FROM SESSIONS;")
    cursor.execute(sql)
    x = cursor.fetchone()
    session_count = x[0]

    sql = ("SELECT count(*) FROM REQUESTS;")
    cursor.execute(sql)
    x = cursor.fetchone()
    request_count = x[0]

    sql = ("SELECT count(*) FROM RESPONSES;")
    cursor.execute(sql)
    x = cursor.fetchone()
    response_count = x[0]

    return {
        'session': session_count,
        'request': request_count,
        'response': response_count
    }


def info_cache(cursor):

    sql = ("SELECT count(*) FROM REQUESTS;")
    cursor.execute(sql)
    x = cursor.fetchone()
    request_count = x[0]

    sql = ("SELECT count(*) FROM CONTENT_TYPE_CACHE;")
    cursor.execute(sql)
    x = cursor.fetchone()
    content_type_count = x[0]

    sql = ("SELECT count(*) FROM URI_CACHE;")
    cursor.execute(sql)
    x = cursor.fetchone()
    uri_count = x[0]

    sql = ("SELECT count(*) FROM CONTENT_CACHE;")
    cursor.execute(sql)
    x = cursor.fetchone()
    content_count = x[0]

    return {
        'content_type': (content_type_count, 1-content_type_count/request_count),
        'uri': (uri_count, 1-uri_count/request_count),
        'content': (content_count, 1-content_count/request_count),
    }
