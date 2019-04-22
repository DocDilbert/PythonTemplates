import logging
import bz2
import sqlite3

from webdb.exceptions import (
    UriNotFound,
    ContentTypeNotFound
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
           "WHERE id = :uri_id;")

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
           "ID "
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


def get_content_type(cursor, content_type_id):
    sql = ("SELECT "
           "CONTENT_TYPE "
           "FROM CONTENT_TYPE_CACHE "
           "WHERE id = :content_type_id;")

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
           "ID "
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


def get_content(cursor, content_id):
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
           "FROM CONTENT_CACHE WHERE id = :rid;")

    param = {'rid': content_id}
    cursor.execute(sql, param)
    x = cursor.fetchone()

    content = bz2.decompress(x[0])

    l = min(len(content), BLOB_STR_LENGTH)

    module_logger.debug(
        "Got \"%s ...\" with id = %i from CONTENT_CACHE.", str(content[0:l]), content_id)

    return content
