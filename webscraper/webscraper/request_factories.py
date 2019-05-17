import logging
import requests
import webdb
import sys
import bz2
from webtypes.request import Request
from webtypes.response import Response

__CURSOR__ = None
COMPRESSION_LEVEL = 9

# chrome 70.0.3538.77
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}


class RequestInternetFcn:
    def __init__(self):
        pass

    def __call__(self, request):

        response_raw = requests.get(
            request.get_url(),
            headers=HEADERS
        )

        response = Response.fromGMT(
            status_code=response_raw.status_code,
            date_gmt=response_raw.headers['Date'],
            content_type=response_raw.headers['Content-Type'],
            bz2Content=bz2.compress(response_raw.content, COMPRESSION_LEVEL)
        )

        return response


class RequestToInternet:
    def __init__(self):
        pass

    def get(self):
        return RequestInternetFcn()


class RequestDatabaseFcn:

    def __init__(self,  session_id):
        self.session_id = session_id

    def __call__(self, request):

        response, _ = webdb.filters.get_response_where_session_id_and_request(
            __CURSOR__,
            self.session_id,
            request
        )
        return response


class RequestToDatabase:
    def __init__(self, db_name, session_id):
        self.session_id = session_id
        self.db_name = db_name

    def get(self):
        # This is used for spawning multiple processes
        global __CURSOR__
        __CURSOR__ = webdb.db.open_db_readonly(self.db_name).cursor()

        return RequestDatabaseFcn(self.session_id)
