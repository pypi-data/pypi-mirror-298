#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_brhk
=================================================
"""
from typing import Callable, Any

import requests
from addict import Dict
from guolei_py3_requests.library import ResponseCallable, request
from jsonschema.validators import validate, Draft202012Validator
from requests import Response


class ResponseCallable(ResponseCallable):
    """
    Response Callable Class
    """

    @staticmethod
    def json_addict__errcode_is_0(response: Response = None, status_code: int = 200):
        json_addict = ResponseCallable.json_addict(response=response, status_code=status_code)
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "errcode": {
                    "oneOf": [
                        {"type": "integer", "const": 0},
                        {"type": "string", "const": "0"},
                    ],
                },
            },
            "required": ["errcode"]
        }).is_valid(json_addict):
            return True
        return False


class UrlsSetting:
    NOTIFY = "/notify.php"


class Api(object):
    """
    博瑞皓科 Speaker Api Class
    @see https://www.yuque.com/lingdutuandui/ugcpag/umbzsd#yG8IS
    """

    def __init__(
            self,
            base_url: str = "https://speaker.17laimai.cn/",
            token: str = "",
            id: str = "",
            version: str = "1"
    ):
        """
        @see https://www.yuque.com/lingdutuandui/ugcpag/umbzsd
        :param base_url:
        :param token:
        :param id:
        :param version:
        """
        self._base_url = base_url
        self._token = token
        self._id = id
        self._version = version

    @property
    def base_url(self):
        """
        base url
        :return:
        """
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    def post(
            self,
            response_callable: Callable = ResponseCallable.json_addict__errcode_is_0,
            url: str = None,
            params: Any = None,
            data: Any = None,
            json: Any = None,
            headers: Any = None,
            **kwargs: Any
    ):
        return self.request(
            response_callable=response_callable,
            method="POST",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            **kwargs
        )

    def request(
            self,
            response_callable: Callable = ResponseCallable.json_addict__errcode_is_0,
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

    def notify(
            self,
            message: str = None,
    ):
        validate(instance=message, schema={"type": "string", "minLength": 1})
        data = Dict({})
        data.setdefault("token", self.token)
        data.setdefault("id", self.id)
        data.setdefault("version", self.version)
        data.setdefault("message", message)
        return self.post(
            response_callable=ResponseCallable.json_addict__errcode_is_0,
            url=UrlsSetting.NOTIFY,
            data=data.to_dict()
        )
