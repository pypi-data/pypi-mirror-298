#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
51welink SMS Class Library
-------------------------------------------------
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_51welink
=================================================
"""
import hashlib
import random
import string
from datetime import datetime
from typing import Callable, Iterable

from addict import Dict
from guolei_py3_requests import RequestsResponseCallable, requests_request
from requests import Response


class RequestsResponseCallable(RequestsResponseCallable):
    @staticmethod
    def status_code_200_json_addict_result_succ(response: Response = None):
        print(response.json())
        json_addict = RequestsResponseCallable.status_code_200_json_addict(response=response)
        return json_addict.Result == "succ"


class Api(object):
    """
    短信 Api Class
    """

    def __init__(
            self,
            base_url: str = "https://api.51welink.com/",
            account_id: str = "",
            password: str = "",
            product_id: int = 0,
            smms_encrypt_key: str = "SMmsEncryptKey",
    ):
        """

        :param base_url: base url
        :param account_id: 提交账户
        :param password: 密码
        :param product_id: 产品编码，供应商提供
        :param smms_encrypt_key:加密key
        """
        self._base_url = base_url
        self._account_id = account_id
        self._password = password
        self._product_id = product_id
        self._smms_encrypt_key = smms_encrypt_key

    @property
    def base_url(self) -> str:
        """
        base url
        :return:
        """
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def account_id(self) -> str:
        """
        提交账户
        :return:
        """
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @property
    def password(self) -> str:
        """
        密码
        :return:
        """
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def product_id(self) -> int:
        """
        产品编码，供应商提供
        :return:
        """
        return self._product_id

    @product_id.setter
    def product_id(self, value):
        self._product_id = value

    @property
    def smms_encrypt_key(self) -> str:
        """
        加盟key
        :return:
        """
        return self._smms_encrypt_key

    @smms_encrypt_key.setter
    def smms_encrypt_key(self, value):
        self._smms_encrypt_key = value

    def timestamp(self):
        return int(datetime.now().timestamp())

    def random_digits(self, length=10):
        return int("".join(random.sample(string.digits, length)))

    def password_md5(self):
        return hashlib.md5(f"{self.password}{self.smms_encrypt_key}".encode('utf-8')).hexdigest().upper()

    def signature(self, data: dict = {}):
        data = Dict(data)
        temp = f"AccountId={data.AccountId}&PhoneNos={data.PhoneNos}&Password={self.password_md5()}&Random={data.Random}&Timestamp={data.Timestamp}"
        return hashlib.sha256(temp.encode("utf-8")).hexdigest()

    def send_sms(
            self,
            phone_no: str = "",
            content: str = "",
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_result_succ,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ) -> bool:
        """
        用于提交发送短信的常规方法
        :param phone_no: 手机号
        :param content: 短信内容
        :param requests_response_callable:RequestsResponseCallable.status_code_200_json_addict_result_succ
        :param requests_request_args: guolei_py3_requests.requests_request(requests_response_callable,requests_request_args, requests_request_kwargs)
        :param requests_request_kwargs:guolei_py3_requests.requests_request(requests_response_callable,requests_request_args, requests_request_kwargs)
        :return: True=发送成功 False=发送失败
        """
        if not isinstance(phone_no, str):
            raise TypeError("phone_no must be str")
        if not len(phone_no):
            raise ValueError("phone_no must be str and not empty")
        if not isinstance(content, str):
            raise TypeError("content must be str")
        if not len(content):
            raise ValueError("content must be str and not empty")
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict({
            "url": f"{self.base_url}/EncryptionSubmit/SendSms.ashx",
            "method": "POST",
            "json": Dict({
                "AccountId": self.account_id,
                "AccessKey": "",
                "Timestamp": self.timestamp(),
                "Random": self.random_digits(),
                "ProductId": self.product_id,
                "PhoneNos": phone_no,
                "Content": content,
            }),
            **requests_request_kwargs,
        })
        requests_request_kwargs.json.AccessKey = self.signature(data=requests_request_kwargs.json)
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )
