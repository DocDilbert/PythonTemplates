import logging
import bz2
import sqlite3

import webdb.interface 

from webdb.exceptions import (
    UriNotFound,
    ContentTypeNotFound,
    ResponseNotFound
)
module_logger = logging.getLogger('webdb.cache')

COMPRESSION_LEVEL = 9
BLOB_STR_LENGTH = 10


#############################################################
# URI CACHE
#############################################################
def get_uri(cursor, uri_id):
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


def get_id_of_uri(cursor, scheme, netloc, path, params, query, fragment):
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

    sql_params = {
        "scheme": scheme,
        "netloc": netloc,
        "path": path,
        "params": params,
        "query": query,
        "fragment": fragment
    }

    cursor.execute(sql, sql_params)
    x = cursor.fetchone()
    if x:
        return x[0]
    else:
        raise UriNotFound()


def create_or_get_uri_id(cursor, scheme, netloc, path, params, query, fragment):
    try:
        uid = get_id_of_uri(
            cursor,
            scheme,
            netloc,
            path,
            params,
            query,
            fragment
        )
        module_logger.debug("Found uri in URI_CACHE. Id is %i", uid)
        return uid

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
        uid = int(cursor.lastrowid)
        module_logger.debug("The uri is new. Inserting it. Id is %i", uid)
        return uid

#############################################################
# CONTENT_TYPE CACHE
#############################################################


def get_content_type_by_id(cursor, content_type_id):
    sql = ("SELECT "
           "CONTENT_TYPE "
           "FROM CONTENT_TYPE_CACHE "
           "WHERE CONTENT_TYPE_ID = :content_type_id;")

    params = {
        'content_type_id': content_type_id
    }

    cursor.execute(sql, params)
    x = cursor.fetchone()

    content_type = x[0]
    module_logger.debug(
        "Found content_type=\"%s\" with id %i in CONTENT_TYPE_CACHE.", content_type, content_type_id)

    return content_type


def get_content_type_id(cursor, content_type):
    sql = ("SELECT "
           "CONTENT_TYPE_ID "
           "FROM CONTENT_TYPE_CACHE "
           "WHERE CONTENT_TYPE = :content_type;")

    params = {
        'content_type': content_type
    }

    cursor.execute(sql, params)
    x = cursor.fetchone()
    if x:
        return x[0]
    else:
        raise ContentTypeNotFound()


def create_or_get_content_type_id(cursor, content_type):
    try:
        content_type_id = get_content_type_id(cursor, content_type)
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

def insert_content(cursor, content):
    sql = ("INSERT INTO CONTENT_CACHE ("
           "CONTENT"
           ") VALUES (?);")

    content_compressed = bz2.compress(content, COMPRESSION_LEVEL)

    module_logger.debug("Compression of content reduced the file size to %.3f %% of the original size.",
                        len(content_compressed)/len(content)*100.0)
    cursor.execute(sql, [
        sqlite3.Binary(content_compressed)
    ])

    cid = int(cursor.lastrowid)

    l = min(len(content), BLOB_STR_LENGTH)

    module_logger.debug(
        "sql: INSERT \"%s ...\" into CONTENT_CACHE. Id is %i.", str(content[0:l]), cid)

    return cid

def create_or_get_content_id(cursor, request, content):
    try:
        (newest_response, newest_response_metadata) = get_newest_response_of_request(
            cursor, request)

        if (content != newest_response.content):
            module_logger.debug("The received response content is new.")
            return insert_content(cursor, content)
        else:
            module_logger.debug(
                "The received response content was stored beforehand. Using this instead.")

            return newest_response_metadata['content_id']

    except ResponseNotFound:
        module_logger.debug(
            "This is the first time the request %s was perfomed.", request)

        return insert_content(cursor, content)


def get_content_by_id(cursor, content_id):
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
           "FROM CONTENT_CACHE WHERE CONTENT_ID = :rid;")

    param = {'rid': content_id}
    cursor.execute(sql, param)
    x = cursor.fetchone()

    content = bz2.decompress(x[0])

    l = min(len(content), BLOB_STR_LENGTH)

    module_logger.debug(
        "Got \"%s ...\" with id = %i from CONTENT_CACHE.", str(content[0:l]), content_id)

    return content


def get_newest_response_of_request(cursor, request):
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
        uri_id = get_id_of_uri(
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

    sql = ("SELECT MAX(RESPONSE_ID) FROM ("
                "SELECT RESPONSE_ID FROM REQUESTS "
                "WHERE "
                    "URI_ID = :uri_id" 
                ");")

    params = {
        'uri_id': uri_id
    }

    cursor.execute(sql, params)
    x =  cursor.fetchone()
    if not x:
        raise ResponseNotFound()

    response_id = x[0]

    return webdb.interface.get_response_by_id(cursor, response_id)