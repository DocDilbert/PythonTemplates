import logging
import sqlite3

import webdb.interface 

from webdb.exceptions import (
    UriNotFound,
    ContentTypeNotFound,
    ResponseNotFound
)
module_logger = logging.getLogger('webdb.cache')

BLOB_STR_LENGTH = 10


#############################################################
# URI CACHE
#############################################################
def get_uri_where_uri_id(cursor, uri_id):
    sql = ("SELECT "
           "SCHEME,"
           "NETLOC,"
           "PATH,"
           "PARAMS,"
           "QUERY,"
           "FRAGMENT "
           "FROM URI_CACHE "
           "WHERE URI_ID = :uri_id;")

    sql_params = {
        'uri_id': uri_id
    }

    cursor.execute(sql, sql_params)
    x = cursor.fetchone()
    if x:
        return {
            'scheme': x[0],
            'netloc': x[1],
            'path': x[2],
            'params': x[3],
            'query': x[4],
            'fragment': x[5],
        }
    else:
        raise UriNotFound()


def get_uri_id_where_uri(cursor, scheme, netloc, path, params, query, fragment):
    sql = ("SELECT "
           "URI_ID "
           "FROM URI_CACHE "
           "WHERE "
           "SCHEME = :scheme AND "
           "NETLOC = :netloc AND "
           "PATH   = :path AND "
           "PARAMS = :params AND "
           "QUERY = :query AND "
           "FRAGMENT = :fragment"
           ";")

    sqlparams = {
        "scheme": scheme,
        "netloc": netloc,
        "path": path,
        "params": params,
        "query": query,
        "fragment": fragment
    }

    cursor.execute(sql, sqlparams)
    x = cursor.fetchone()
    if x:
        return x[0]
    else:
        raise UriNotFound()


def create_or_get_uri_id(cursor, scheme, netloc, path, params, query, fragment):
    try:
        uri_id = get_uri_id_where_uri(
            cursor,
            scheme,
            netloc,
            path,
            params,
            query,
            fragment
        )
        module_logger.debug("Found uri in URI_CACHE. Id is %i", uri_id)
        return uri_id

    except UriNotFound:
        sql = ("INSERT INTO URI_CACHE ("
               "SCHEME, "
               "NETLOC, "
               "PATH, "
               "PARAMS, "
               "QUERY, "
               "FRAGMENT "
               ") VALUES (?, ?, ?, ?, ?, ?);")

        cursor.execute(sql, [
            scheme,
            netloc,
            path,
            params,
            query,
            fragment
        ])
        uri_id = int(cursor.lastrowid)
        module_logger.debug("The uri is new. Inserting it. Id is %i", uri_id)
        return uri_id

#############################################################
# CONTENT_TYPE CACHE
#############################################################


def get_content_type_where_content_type_id(cursor, content_type_id):
    sql = ("SELECT "
           "CONTENT_TYPE "
           "FROM CONTENT_TYPE_CACHE "
           "WHERE CONTENT_TYPE_ID = :content_type_id;")

    sqlparams = {
        'content_type_id': content_type_id
    }

    cursor.execute(sql, sqlparams)
    x = cursor.fetchone()

    content_type = x[0]
    module_logger.debug(
        "Found content_type=\"%s\" with id %i in CONTENT_TYPE_CACHE.", content_type, content_type_id)

    return content_type


def get_content_type_id_where_content_type(cursor, content_type):
    sql = ("SELECT "
           "CONTENT_TYPE_ID "
           "FROM CONTENT_TYPE_CACHE "
           "WHERE CONTENT_TYPE = :content_type;")

    sqlparams = {
        'content_type': content_type
    }

    cursor.execute(sql, sqlparams)
    x = cursor.fetchone()
    if x:
        return x[0]
    else:
        raise ContentTypeNotFound()


def create_or_get_content_type_id(cursor, content_type):
    try:
        content_type_id = get_content_type_id_where_content_type(cursor, content_type)
        module_logger.debug(
            "Found content_type=\"%s\" with id %i in CONTENT_TYPE_CACHE.", content_type, content_type_id)
    except ContentTypeNotFound:
        sql = ("INSERT INTO CONTENT_TYPE_CACHE ("
               "CONTENT_TYPE"
               ") VALUES (?);")
        cursor.execute(sql, [
            content_type
        ])
        content_type_id = int(cursor.lastrowid)
        module_logger.debug(
            "The content_type=%s is new. Inserting it n CONTENT_TYPE_CACHE. Id is %i", content_type, content_type_id)

    return content_type_id


#############################################################
# CONTENT CACHE
#############################################################

def get_bz2content_where_content_id(cursor, content_id):
    """ Extrahiert das unter der content_id in der Tabelle CONTENT_CACHE 
    abgelegten Blob.

    Arguments:
        cursor -- Datenbank Cursor
        content_id -- Die id des gewünschten Blobs.

    Returns:
        Ein befülltes Blob Objekt.
    """

    sql = ("SELECT "
           "CONTENT "
           "FROM CONTENT_CACHE WHERE CONTENT_ID = :content_id;")

    sqlparams = {'content_id': content_id}
    
    cursor.execute(sql, sqlparams)
    x = cursor.fetchone()

    bz2Content = x[0]

    l = min(len(bz2Content), BLOB_STR_LENGTH)

    module_logger.debug(
        "Got \"%s ...\" with id = %i from CONTENT_CACHE.", str(bz2Content[0:l]), content_id)

    return bz2Content

def insert_bz2content(cursor, bz2Content):
    sql = ("INSERT INTO CONTENT_CACHE ("
           "CONTENT"
           ") VALUES (?);")



    cursor.execute(sql, [
        sqlite3.Binary(bz2Content)
    ])

    content_id = int(cursor.lastrowid)

    l = min(len(bz2Content), BLOB_STR_LENGTH)

    module_logger.debug(
        "sql: INSERT \"%s ...\" into CONTENT_CACHE. Id is %i.", str(bz2Content[0:l]), content_id)

    return content_id

def create_or_get_bz2content_id(cursor, request, bz2Content):
    try:
        (newest_response, newest_response_metadata) = get_newest_response_where_request(
            cursor, request)

        if (bz2Content != newest_response.bz2Content):
            module_logger.debug("The received response content is new.")
            return insert_bz2content(cursor, bz2Content)
        else:
            module_logger.debug(
                "The received response content was stored beforehand. Using this instead.")

            return newest_response_metadata['content_id']

    except ResponseNotFound:
        module_logger.debug(
            "This is the first time the request %s was perfomed.", request)

        return insert_bz2content(cursor, bz2Content)


def get_newest_response_where_request(cursor, request):
    """ Extrahiert die letzte unter dem gegeben request gespeicherte response.

    Arguments:
        cursor -- Datenbank Cursor
        request -- Der request unter dem die response gesucht werden soll.

    Returns:
        Es wird ein tuple zurückgegeben. Das erste Element ist die
        gefundene response das zweite die content_id der gefundenen
        response. 

    Raises:
        ResponseNotFound - If no last response for request was found.
    """

    try:
        uri_id = get_uri_id_where_uri(
            cursor,
            request.scheme,
            request.netloc,
            request.path,
            request.params,
            request.query,
            request.fragment
        )
    except UriNotFound:
        raise ResponseNotFound()

    sql = ( "SELECT MAX(RESPONSE_ID) FROM ("
                "SELECT RESPONSE_ID FROM REQUESTS "
                "WHERE "
                    "URI_ID = :uri_id" 
            ");")

    sqlparams = {
        'uri_id': uri_id
    }

    cursor.execute(sql, sqlparams)
    x =  cursor.fetchone()
    if not x:
        raise ResponseNotFound()

    response_id = x[0]

    return webdb.interface.get_response_where_response_id(cursor, response_id)
