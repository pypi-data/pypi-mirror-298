#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_qywx
=================================================
"""
from typing import Callable, Any

from guolei_py3_requests.library import ResponseCallable, request
from jsonschema import validate, Draft202012Validator
import requests
from addict import Dict
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
            return json_addict.get("media_id", True)
        return False


class UrlsSetting:
    """
    Urls Settings
    """
    CGI_BIN__WEBHOOK__SEND = "/cgi-bin/webhook/send"
    CGI_BIN__WEBHOOK__UPLOAD_MEDIA = "/cgi-bin/webhook/upload_media"


class Api(object):
    """
    企业微信 群机器人 Webhook Api Class
    @see https://developer.work.weixin.qq.com/document/path/91770
    """

    def __init__(
            self,
            base_url: str = "https://qyapi.weixin.qq.com/",
            key: str = "",
            mentioned_list: list = [],
            mentioned_mobile_list: list = []
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770
        :param base_url: base url
        :param key: key
        :param mentioned_list:
        :param mentioned_mobile_list:
        """
        self._base_url = base_url
        self._key = key
        self._mentioned_list = mentioned_list
        self._mentioned_mobile_list = mentioned_mobile_list

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def mentioned_list(self):
        return self._mentioned_list

    @mentioned_list.setter
    def mentioned_list(self, mentioned_list):
        self._mentioned_list = mentioned_list

    @property
    def mentioned_mobile_list(self):
        return self._mentioned_mobile_list

    @mentioned_mobile_list.setter
    def mentioned_mobile_list(self, mentioned_mobile_list):
        self._mentioned_mobile_list = mentioned_mobile_list

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
        params = Dict(params) if isinstance(params, dict) else Dict()
        params.setdefault("key", self.key)
        return self.request(
            response_callable=response_callable,
            method="POST",
            url=url,
            params=params.to_dict(),
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

    def send_text(self, content: str = None, mentioned_list: list[str] = [], mentioned_mobile_list: list[str] = []):
        return self.post(
            url=UrlsSetting.CGI_BIN__WEBHOOK__SEND,
            json={
                "msgtype": "text",
                "text": {
                    "content": f"{content}",
                    "mentioned_list": mentioned_list,
                    "mentioned_mobile_list": mentioned_mobile_list,
                }
            }
        )

    def send_markdown(self, content: str = None):
        return self.post(
            url=UrlsSetting.CGI_BIN__WEBHOOK__SEND,
            json={
                "msgtype": "markdown",
                "markdown": {
                    "content": ""
                }
            }
        )

    def send_file(self, media_id: str = None):
        return self.post(
            url=UrlsSetting.CGI_BIN__WEBHOOK__SEND,
            json={
                "msgtype": "file",
                "file": {
                    "media_id": f"{media_id}"
                }
            }
        )

    def send_voice(self, media_id: str = None):
        return self.post(
            url=UrlsSetting.CGI_BIN__WEBHOOK__SEND,
            json={
                "msgtype": "voice",
                "voice": {
                    "media_id": f"{media_id}"
                }
            }
        )

    def upload_media(self, types: str = "file", files: Any = None):
        params = Dict()
        params.setdefault("type", types)
        return self.post(
            url=UrlsSetting.CGI_BIN__WEBHOOK__UPLOAD_MEDIA,
            params=params.to_dict(),
            files=files
        )
