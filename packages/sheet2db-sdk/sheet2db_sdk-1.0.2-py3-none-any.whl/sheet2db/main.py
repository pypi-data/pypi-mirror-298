import base64
from urllib.parse import urlencode, urljoin
import requests


class Sheet2DBOptions:
    def __init__(self, mode, apiKey=None, spreadsheetId=None, connectionId=None, version="v1",
                 basicAuth=None, jwtAuth=None, fetchFn=None):
        self.mode = mode
        self.apiKey = apiKey
        self.spreadsheetId = spreadsheetId
        self.connectionId = connectionId
        self.basicAuth = basicAuth
        self.jwtAuth = jwtAuth
        self.version = "v1"
        self.fetchFn = fetchFn or requests.request


class ReadOptions:
    def __init__(self, limit=None, offset=None, sheet=None, format=None, cast_numbers=None,columns=None, value_render=None):
        self.limit = limit
        self.offset = offset
        self.sheet = sheet
        self.format = format
        self.cast_numbers = cast_numbers
        self.columns = columns
        self.value_render = value_render


class GetKeysOptions:
    def __init__(self, sheet=None):
        self.sheet = sheet


class GetCountOptions:
    def __init__(self, sheet=None):
        self.sheet = sheet


class GetRangeOptions:
    def __init__(self, range):
        self.range = range


class SearchOptions:
    def __init__(self, query, sheet=None, or_=False, limit=None, offset=None, cast_numbers=None,columns=None):
        self.query = query
        self.sheet = sheet
        self.or_ = or_
        if limit is not None:
            self.query = f"{self.query}&__limit={limit}"
        if offset is not None:
            self.query = f"{self.query}&__offset={offset}"
        if columns is not None:
            if not isinstance(columns, str):
                columns = ",".join(columns)
            self.query = f"{self.query}&__columns={columns}"
        if cast_numbers is not None:
            if not isinstance(cast_numbers, str):
                cast_numbers = ",".join(cast_numbers)
            self.query = f"{self.query}&__cast_numbers={cast_numbers}"


class InsertOptions:
    def __init__(self, data, sheet=None):
        self.data = data
        self.sheet = sheet


class UpdateRowOptions:
    def __init__(self, row, data, sheet=None):
        self.row = row
        self.data = data
        self.sheet = sheet


class UpdateWithQueryOptions:
    def __init__(self, query, data, sheet=None):
        self.query = query
        self.data = data
        self.sheet = sheet


class BatchUpdateOptions:
    def __init__(self, batches, sheet=None):
        self.batches = batches
        self.sheet = sheet


class DeleteRowOptions:
    def __init__(self, row, sheet=None):
        self.row = row
        self.sheet = sheet


class DeleteWithQueryOptions:
    def __init__(self, query, sheet=None):
        self.query = query
        self.sheet = sheet


class ClearSheetOptions:
    def __init__(self, sheet):
        self.sheet = sheet


class CreateSheetOptions:
    def __init__(self, title=None):
        self.title = title


class DeleteSheetOptions:
    def __init__(self, sheet):
        self.sheet = sheet


class Sheet2DB:
    def __init__(self, options: Sheet2DBOptions):
        self.api_endpoint = "https://api.sheet2db.com"
        self.options = options
        self.fetchFn = options.fetchFn

    def _fetch(self, path, method="GET", query_params=None, body=None):
        endpoint = f"{self.api_endpoint}/{self.options.version}"
        headers = {"Content-Type": "application/json"}

        if self.options.mode == "connectionId":
            endpoint = f"{endpoint}/{self.options.connectionId}{path}"
            if self.options.basicAuth:
                auth = base64.b64encode(f"{self.options.basicAuth['username']}:{self.options.basicAuth['password']}".encode()).decode()
                headers["Authorization"] = f"Basic {auth}"
            elif self.options.jwtAuth:
                headers["Authorization"] = f"Bearer {self.options.jwtAuth['bearerToken']}"
        else:
            endpoint = f"{endpoint}/{self.options.apiKey}{path}"
            query_params = query_params or {}
            query_params["__id"] = self.options.spreadsheetId

        if query_params:
            endpoint = f"{endpoint}?{urlencode(query_params)}"

        response = self.fetchFn(method, endpoint, headers=headers, json=body)
        response.raise_for_status()
        return response.json()

    def read_content(self, options:ReadOptions=None):
        if(options and options.cast_numbers and not isinstance(options.cast_numbers, str)):
            options.cast_numbers = ','.join(options.cast_numbers)
        if(options and options.columns and not isinstance(options.columns, str)):
            options.columns = ','.join(options.columns)
        query = vars(options) if options else {}
        return self._fetch("", "GET", query)

    def keys(self, options=None):
        query = vars(options) if options else {}
        return self._fetch("/keys", "GET", query)

    def count(self, options=None):
        query = vars(options) if options else {}
        return self._fetch("/count", "GET", query)

    def title(self):
        return self._fetch("/title", "GET")

    def range(self, options: GetRangeOptions):
        return self._fetch(f"/range/{options.range}", "GET")

    def search(self, options: SearchOptions):
        path = "/search_or" if options.or_ else "/search"
        if options.sheet:
            path = f"{path}/{options.sheet}?{options.query}"
        else:
            path = f"{path}?{options.query}"
        return self._fetch(path, "GET", {})

    def insert(self, options: InsertOptions):
        query = {k: v for k, v in vars(options).items() if k != "data"}
        return self._fetch("", "POST", query, options.data)

    def update_row(self, options: UpdateRowOptions):
        query = {k: v for k, v in vars(options).items() if k != "data"}
        return self._fetch(f"/row/{options.row}", "PATCH", query, options.data)

    def update_with_query(self, options: UpdateWithQueryOptions):
        path = f"/{options.sheet}" if options.sheet else ""
        path = f"{path}?{options.query}"
        return self._fetch(path, "PATCH", {}, options.data)

    def batch_update(self, options: BatchUpdateOptions):
        path = f"/batch/{options.sheet}" if options.sheet else "/batch"
        return self._fetch(path, "PATCH", None, options.batches)

    def delete_row(self, options: DeleteRowOptions):
        query = vars(options)
        return self._fetch(f"/row/{options.row}", "DELETE", query)

    def delete_with_query(self, options: DeleteWithQueryOptions):
        path = f"/{options.sheet}" if options.sheet else ""
        path = f"{path}?{options.query}"
        return self._fetch(path, "DELETE", {})

    def clear(self, options: ClearSheetOptions):
        return self._fetch(f"/clear/{options.sheet}", "DELETE")

    def create_sheet(self, options: CreateSheetOptions):
        query = vars(options)
        return self._fetch("/sheet", "POST", query)

    def delete_sheet(self, options: DeleteSheetOptions):
        return self._fetch(f"/sheet/{options.sheet}", "DELETE")

def __version__():
    return "0.0.1"