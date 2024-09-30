#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_tiehu
=================================================
"""
import hashlib
from datetime import datetime
from typing import Callable, Any
import json
from addict import Dict
from guolei_py3_requests.library import ResponseCallable, request
from jsonschema.validators import Draft202012Validator
from requests import Response


class ResponseCallable(ResponseCallable):
    """
    Response Callable Class
    """

    @staticmethod
    def json_addict__status_is_1___Data(response: Response = None, status_code: int = 200):
        json_addict = ResponseCallable.json_addict(response=response, status_code=status_code)
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "errcode": {
                    "status": [
                        {"type": "integer", "const": 1},
                        {"type": "string", "const": "1"},
                    ],
                    "Data": {"type": "string", "minLength": 1}
                },
            },
            "required": ["status", "Data"]
        }).is_valid(json_addict):
            return json.loads(json_addict.get("Data", ""))
        return Dict({})


class UrlsSetting:
    CXZN__INTERFACE__QUERYPKLOT = "/cxzn/interface/queryPklot"
    CXZN__INTERFACE__GETPARKCARTYPE = "/cxzn/interface/getParkCarType"
    CXZN__INTERFACE__GETPARKCARMODEL = "/cxzn/interface/getParkCarModel"
    CXZN__INTERFACE__PAYMONTHLY = "/cxzn/interface/payMonthly"
    CXZN__INTERFACE__ADDVISIT = "/cxzn/interface/addVisit"
    CXZN__INTERFACE__LOCKCAR = "/cxzn/interface/lockCar"
    CXZN__INTERFACE__GETPARKINFO = "/cxzn/interface/getParkinfo"
    CXZN__INTERFACE__ADDPARKBLACK = "/cxzn/interface/addParkBlack"
    CXZN__INTERFACE__DELPARKBLACKLIST = "/cxzn/interface/delParkBlacklist"
    CXZN__INTERFACE__GETPARKGATE = "/cxzn/interface/getParkGate"
    CXZN__INTERFACE__OPENGATE = "/cxzn/interface/openGate"
    CXZN__INTERFACE__SAVEMONTHLYRENT = "/cxzn/interface/saveMonthlyRent"
    CXZN__INTERFACE__DELMONTHLYRENT = "/cxzn/interface/delMonthlyRent"
    CXZN__INTERFACE__GETMONTHLYRENT = "/cxzn/interface/getMonthlyRent"
    CXZN__INTERFACE__GETMONTHLYRENTLIST = "/cxzn/interface/getMonthlyRentList"
    CXZN__INTERFACE__DELMONTHLYRENTLIST = "/cxzn/interface/delMonthlyRentList"
    CXZN__INTERFACE__GETPARKDEVICESTATE = "/cxzn/interface/getParkDeviceState"
    CXZN__INTERFACE__UPATEPLATEINFO = "/cxzn/interface/upatePlateInfo"
    CXZN__INTERFACE__GETPARKBLACKLIST = "/cxzn/interface/getParkBlackList"
    CXZN__INTERFACE__DELETEVISITT = "/cxzn/interface/deleteVisit"


class Api(object):
    def __init__(
            self,
            base_url: str = "",
            parking_id: str = "",
            app_key: str = ""
    ):
        self._base_url = base_url
        self._parking_id = parking_id
        self._app_key = app_key

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def parking_id(self):
        return self._parking_id

    @parking_id.setter
    def parking_id(self, value):
        self._parking_id = value

    @property
    def app_key(self):
        return self._app_key

    @app_key.setter
    def app_key(self, value):
        self._app_key = value

    def signature(
            self,
            data: dict = {},
    ):
        signature_temp = ""
        data = Dict(data) if isinstance(data, Dict) else Dict()
        if data.keys():
            data_sorted = sorted(data.keys())
            if isinstance(data_sorted, list):
                signature_temp = "&".join([
                    f"{i}={data[i]}"
                    for i in
                    data_sorted if
                    i != "appKey"
                ]) + f"{hashlib.md5(self.app_key.encode('utf-8')).hexdigest().upper()}"
        return hashlib.md5(signature_temp.encode('utf-8')).hexdigest().upper()

    def post(
            self,
            response_callable: Callable = ResponseCallable.json_addict__status_is_1___Data,
            url: str = None,
            params: Any = None,
            data: Any = None,
            json: Any = None,
            headers: Any = None,
            **kwargs: Any
    ):
        json = Dict(params) if isinstance(json, dict) else Dict()
        json.setdefault("parkingId", self.parking_id)
        json.setdefault("timestamp", int(datetime.now().timestamp()))
        json.setdefault("sign", self.signature(json))
        return self.request(
            response_callable=response_callable,
            method="POST",
            url=url,
            params=params,
            data=data,
            json=json.to_dict(),
            headers=headers,
            **kwargs
        )

    def request(
            self,
            response_callable: Callable = ResponseCallable.json_addict__status_is_1___Data,
            method: str = "GET",
            url: str = None,
            params: Any = None,
            headers: Any = None,
            **kwargs
    ):
        if not Draft202012Validator({"type": "string", "minLength": 1, "pattern": "^http"}).is_valid(url):
            url = f"/{url}" if not url.startswith("/") else url
            url = f"{self.base_url}{url}"
        return request(
            response_callable=response_callable,
            method=method,
            url=url,
            params=params,
            headers=headers,
            **kwargs
        )
