#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from typing import Callable, Sequence, Union

import requests
from addict import Dict
from requests import Response


class ResponseCallable(object):
    """
    Response Callable
    """

    @staticmethod
    def text(response: Response = None, status_code: int = 200):
        if isinstance(response, Response):
            if response.status_code == status_code:
                return response.text
        return None

    @staticmethod
    def json(response: Response = None, status_code: int = 200):
        if isinstance(response, Response):
            if response.status_code == status_code:
                return response.json()
        return None

    @staticmethod
    def json_addict(response: Response = None, status_code: int = 200):
        return Dict(ResponseCallable.json(response=response, status_code=status_code))


def request(
        response_callable: Callable = None,
        method: str = None,
        url: str = None,
        **kwargs
):
    """
    request by requests.request()
    :param response_callable: return response_callable(response) if isinstance(response_callable, callable) else response
    :param method: requests.request(method,url, **kwargs)
    :param url: requests.request(method,url, **kwargs)
    :param args: requests.request(method,url, **kwargs)
    :param kwargs: requests.request(method,url,  **kwargs)
    :return:
    """
    response = requests.request(method=method, url=url, **kwargs)
    if isinstance(response_callable, Callable):
        return response_callable(response)
    return response
