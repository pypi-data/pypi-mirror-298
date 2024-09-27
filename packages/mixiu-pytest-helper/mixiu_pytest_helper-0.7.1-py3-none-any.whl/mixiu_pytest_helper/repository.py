# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     repository.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import typing as t
from apollo_proxy.client import ApolloClient
from mixiu_pytest_helper.infrastructure import RedisClientManager


class MiddlewareRepository(object):

    @classmethod
    def get_devices(cls, apollo: ApolloClient, namespace: str = "application") -> list:
        return apollo.get_value(key="device_ids", namespace=namespace) or list()

    @classmethod
    def get_api_user_uuid(cls, apollo: ApolloClient, namespace: str = "test-data-api-common") -> int:
        return apollo.get_value(key="login_user_uuid", namespace=namespace) or None

    @classmethod
    def get_api_protocol(cls, apollo: ApolloClient, namespace: str = "test-data-api-common") -> str:
        return apollo.get_value(key="api_protocol", namespace=namespace) or None

    @classmethod
    def get_api_domain(cls, apollo: ApolloClient, namespace: str = "test-data-api-common") -> str:
        return apollo.get_value(key="api_domain", namespace=namespace) or None

    @classmethod
    def get_test_data(cls, key: str, namespace: str, apollo: ApolloClient) -> t.Any:
        return apollo.get_value(key=key, namespace=namespace)

    @classmethod
    def get_test_datas(cls, namespace: str, apollo: ApolloClient) -> dict:
        test_datas = apollo.get_all_values(namespace=namespace)
        return test_datas if isinstance(test_datas, dict) else dict()

    @classmethod
    def get_login_user_token(cls, uuid: int, redis: RedisClientManager) -> str:
        return redis.get_redis_data(key="POPO:USER:TOKEN:CACHE::{}".format(uuid))
