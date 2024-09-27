# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     conftest.py
# Description:  全局初始化，动态上下文
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import sys
from airtest_helper.core import DeviceProxy
from apollo_proxy.client import ApolloClient
from mixiu_pytest_helper.annotation import logger
from mixiu_pytest_helper.repository import MiddlewareRepository
from mixiu_pytest_helper.infrastructure import RedisClientManager


def get_phone_device_lock_key(device_ip: str, port: int = None) -> str:
    string = "phone:{}".format(device_ip)
    if port and port > 0:
        string += ":{}".format(port)
    return string


def get_idle_device(redis_api: RedisClientManager, apollo: ApolloClient) -> DeviceProxy or None:
    devices = MiddlewareRepository.get_devices(apollo=apollo)
    for device_info in devices:
        port = device_info.get("port")
        device_ip = device_info.get("device")
        lock_key = get_phone_device_lock_key(device_ip=device_ip, port=port)
        lock_status = redis_api.get_redis_data(key=lock_key)
        if not lock_status or lock_status != "running":
            try:
                # 重置 sys.argv 为新的参数列表，避免与airtest包冲突，同时保留当前运行的文件名，作为sys.argv的第一个参数
                sys.argv = sys.argv[:1]
                device = DeviceProxy(**device_info)
                redis_api.set_redis_data(key=lock_key, value="running", ex=7200)
                return device
            except Exception as e:
                logger.error(e)
    return None


"""
@pytest.fixture(scope="session")
def apollo_context() -> ApolloClient:
    apollo_client = ApolloClientManager()
    yield apollo_client


@pytest.fixture(scope="session")
def cache_context(apollo_context: ApolloClient) -> RedisClientManager:
    redis_client = RedisCacheClientManager(apollo=apollo_context)
    redis_api = RedisClientManager(redis=redis_client)
    yield redis_api
    redis_api.redis.close()


@pytest.fixture(scope="session")
def lock_context(apollo_context: ApolloClient) -> RedisClientManager:
    redis_client = RedisLockClientManager(apollo=apollo_context)
    redis_api = RedisClientManager(redis=redis_client)
    yield redis_api
    redis_api.redis.close()


@pytest.fixture(scope="session")
def auth_context(apollo_context: ApolloClient) -> RedisClientManager:
    redis_client = RedisAuthClientManager(apollo=apollo_context)
    redis_api = RedisClientManager(redis=redis_client)
    yield redis_api
    redis_api.redis.close()


@pytest.fixture(scope="session")
def device_context(apollo_context: ApolloClient, lock_context: RedisClientManager) -> DeviceProxy:
    device = get_idle_device(redis_api=lock_context, apollo=apollo_context)
    yield device
    if device:
        lock_key = get_phone_device_lock_key(device_ip=device.device_id)
        lock_context.set_redis_data(key=lock_key, value="idle", ex=86400)
"""
