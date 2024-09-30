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
from datetime import timedelta
from typing import Union, Callable, Any

import diskcache
import redis
from addict import Dict
from guolei_py3_requests.library import ResponseCallable, request
from jsonschema import validate
from jsonschema.validators import Draft202012Validator
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
            return json_addict
        return Dict()


class UrlsSetting:
    CGI_BIN__GETTOKEN = "/cgi-bin/gettoken"
    CGI_BIN__GET_API_DOMAIN_IP = "/cgi-bin/get_api_domain_ip"
    CGI_BIN__MESSAGE__SEND = "/cgi-bin/message/send"
    CGI_BIN__MEDIA__UPLOAD = "/cgi-bin/media/upload"
    CGI_BIN__MEDIA__GET = "/cgi-bin/media/get"
    CGI_BIN__MEDIA__UPLOADIMG = "/cgi-bin/media/uploadimg"


class Api(object):
    """
    @see https://developer.work.weixin.qq.com/document/path/90664
    """

    def __init__(
            self,
            base_url: str = "https://qyapi.weixin.qq.com/",
            corpid: str = "",
            corpsecret: str = "",
            agentid: Union[int, str] = "",
            cache_instance: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = None,
    ):
        self._base_url = base_url
        self._corpid = corpid
        self._corpsecret = corpsecret
        self._agentid = agentid
        self._cache_instance = cache_instance
        self._access_token = ""

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url

    @property
    def corpid(self):
        return self._corpid

    @corpid.setter
    def corpid(self, corpid):
        self._corpid = corpid

    @property
    def corpsecret(self):
        return self._corpsecret

    @corpsecret.setter
    def corpsecret(self, corpsecret):
        self._corpsecret = corpsecret

    @property
    def agentid(self):
        return self._agentid

    @agentid.setter
    def agentid(self, agentid):
        self._agentid = agentid

    @property
    def cache_instance(self):
        return self._cache_instance

    @cache_instance.setter
    def cache_instance(self, cache_instance):
        self._cache_instance = cache_instance

    def access_token(
            self,
            expire: Union[float | int | timedelta] = timedelta(seconds=7100).total_seconds(),
            access_token_callable: Callable = None
    ):
        """
        access token
        :param expire: 过期时间
        :param custom_callable: 自定义回调 custom_callable(self) if isinstance(custom_callable, Callable)
        :return: custom_callable(self) if isinstance(custom_callable, Callable) else self
        """
        if isinstance(access_token_callable, Callable):
            return access_token_callable(self)
        validate(instance=self.base_url, schema={"type": "string", "minLength": 1, "pattern": "^http"})
        # 缓存key
        cache_key = f"guolei_py3_qywx_server_access_token__{self.corpid}_{self.agentid}"
        # 使用缓存
        if isinstance(self.cache_instance, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
            if isinstance(self.cache_instance, diskcache.Cache):
                self._access_token = self.cache_instance.get(cache_key)
            if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
                self._access_token = self.cache_instance.get(cache_key)
        # 用户是否登录
        result = self.get(
            response_callable=ResponseCallable.json_addict__errcode_is_0,
            url=f"{UrlsSetting.CGI_BIN__GET_API_DOMAIN_IP}",
            verify=False,
            timeout=(60, 60)
        )
        if result.keys():
            return self
        result = self.get(
            response_callable=ResponseCallable.json_addict__errcode_is_0,
            url=f"{UrlsSetting.CGI_BIN__GETTOKEN}",
            params={
                "corpid": self.corpid,
                "corpsecret": self.corpsecret,
            },
            verify=False,
            timeout=(60, 60)
        )
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "access_token": {"type": "string", "minLength": 1},
            },
            "required": ["access_token"]
        }).is_valid(result):
            self._access_token = result.access_token
            # 缓存处理
            if isinstance(self.cache_instance, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
                if isinstance(self.cache_instance, diskcache.Cache):
                    self.cache_instance.set(
                        key=cache_key,
                        value=self._access_token,
                        expire=expire
                    )
                if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
                    self.cache_instance.setex(
                        name=cache_key,
                        value=self._access_token,
                        time=expire
                    )
        return self

    def get(
            self,
            response_callable: Callable = ResponseCallable.json_addict__errcode_is_0,
            url: str = None,
            params: Any = None,
            headers: Any = None,
            **kwargs: Any
    ):
        return self.request(
            response_callable=response_callable,
            method="GET",
            url=url,
            params=params,
            headers=headers,
            **kwargs
        )

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
        params = Dict(params) if isinstance(params, dict) else Dict()
        params.setdefault("access_token", self._access_token)
        return request(
            response_callable=response_callable,
            method=method,
            url=url,
            params=params,
            headers=headers,
            **kwargs
        )
