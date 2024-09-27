# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     base_test.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import time
import pytest
from apollo_proxy.client import ApolloClient
from mixiu_pytest_helper.annotation import logger
from airtest_helper.core import DeviceProxy, DeviceApi
from mixiu_pytest_helper.repository import MiddlewareRepository
from mixiu_app_helper.api.page.popup.gift import UiDailyCheckInApi
from mixiu_pytest_helper.conftest import get_idle_device, get_phone_device_lock_key
from mixiu_pytest_helper.infrastructure import ApolloClientManager, RedisAuthClientManager, RedisLockClientManager, \
    RedisClientManager

__all__ = ['BeforeAndroidUiTest', 'BeforeIOSUiTest', 'BeforeAndroidApiTest', 'BeforeIOSApiTest']


class SetupClass(object):
    timestamp: int = None
    apollo: ApolloClient = None

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def init_setup(cls, request: pytest.FixtureRequest):
        logger.info("开始初始化自动化测试环境...")
        request.cls.timestamp = int(time.time() * 1000)
        request.cls.apollo = ApolloClientManager()


class UiDataSetupClass(SetupClass):
    test_data: dict = dict()
    config_namespace = "test-data-ui"

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def data_setup(cls, request: pytest.FixtureRequest, init_setup: pytest.Function):
        request.cls.test_data = MiddlewareRepository.get_test_datas(namespace=cls.config_namespace, apollo=cls.apollo)
        logger.info("step1: 获取apollo配置的UI测试【预期数据】成功")


class DeviceSetupClass(UiDataSetupClass):
    device: DeviceProxy = None

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def device_setup(cls, request: pytest.FixtureRequest, data_setup: pytest.Function):
        # 此处的 setup 只会在每个测试类开始时调用一次
        lock_client = RedisClientManager(redis=RedisLockClientManager(apollo=cls.apollo))
        request.cls.device = get_idle_device(redis_api=lock_client, apollo=cls.apollo)
        if request.cls.device is None:
            logger.error("step2: 绑定移动终端设备失败，当前没有空闲设备，或者网络连接不正常")
        else:
            logger.info("step2: 绑定移动终端成功---> {}".format(request.cls.device.device_id))
        yield
        if request.cls.device:
            lock_key = get_phone_device_lock_key(device_ip=request.cls.device.device_id)
            lock_client.set_redis_data(key=lock_key, value="idle", ex=86400)
        lock_client.redis.close()


class AppSetupClass(DeviceSetupClass):
    app_name: str = 'null'
    device_api: DeviceApi = None

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def app_setup(cls, device_setup: pytest.Function):
        cls.device_api = DeviceApi(device=cls.device)
        cls.app_name = cls.test_data.get('app_name')
        # logger.info("开始唤醒设备")
        # device_api.wake()  真机的可能处于息屏状态，因此需要唤醒，模拟机的话，可以忽略此步骤
        logger.info("step3: 开始启动APP---> {}".format(cls.app_name))
        cls.device_api.restart_app(app_name=cls.app_name)


class BeforeAndroidUiTest(AppSetupClass):

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def before_test_setup(cls, app_setup: pytest.Function):
        popui_api = UiDailyCheckInApi(device=cls.device)
        signup_button = popui_api.get_signup_button(loop=5, is_log_output=False)
        # 可能存在签到的弹窗
        if signup_button:
            logger.info("step4*: 检测到【每日签到】弹窗，关闭弹窗并退出直播室")
            popui_api.touch_signup_button()
            logger.info("step4.1*: 已签到")
            popui_api.touch_signup_submit_button()
            popui_api.touch_live_leave_enter()
            popui_api.touch_close_room_button()
            logger.info("step4.2*: 已退出直播间")
        else:
            logger.info("step4*: 没有检测到【每日签到】弹窗，签到步骤将跳过")


class BeforeIOSUiTest(AppSetupClass):

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def before_test_setup(cls, app_setup: pytest.Function):
        popui_api = UiDailyCheckInApi(device=cls.device)
        signup_button = popui_api.get_signup_button()
        # 可能存在签到的弹窗
        if signup_button:
            logger.info("step4*: 检测到【每日签到】弹窗，关闭弹窗并退出直播室")
            popui_api.touch_signup_button()
            logger.info("step4.1*: 已签到")
            popui_api.touch_signup_submit_button()
            popui_api.touch_live_leave_enter()
            popui_api.touch_close_room_button()
            logger.info("step4.2*: 已退出直播间")


class ApiSetupClass(SetupClass):
    domain: str = None
    protocol: str = None
    api_uuid: int = None
    api_token: str = None

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def domain_setup(cls, request: pytest.FixtureRequest, init_setup: pytest.Function):
        request.cls.domain = MiddlewareRepository.get_api_domain(apollo=cls.apollo)
        request.cls.protocol = MiddlewareRepository.get_api_protocol(apollo=cls.apollo)
        logger.info("step1: 获取待测试环境: <{}>".format(request.cls.domain))
        request.cls.api_uuid = MiddlewareRepository.get_api_user_uuid(apollo=cls.apollo)
        auth_client = RedisClientManager(redis=RedisAuthClientManager(apollo=cls.apollo))
        api_token = MiddlewareRepository.get_login_user_token(uuid=request.cls.api_uuid, redis=auth_client)
        request.cls.api_token = api_token.replace('"', '') if api_token else api_token
        logger.info("step2: 获取待测试用户uuid: <{}>，token: <{}>".format(request.cls.api_uuid, request.cls.api_token))
        yield
        auth_client.redis.close()


class AndroidApiCommonSetupClass(ApiSetupClass):
    test_data_common: dict = dict()
    common_namespace = "test-data-api-android-common"

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def common_data_setup(cls, request: pytest.FixtureRequest, domain_setup: pytest.Function):
        request.cls.test_data_common = MiddlewareRepository.get_test_datas(
            namespace=cls.common_namespace, apollo=cls.apollo
        )
        logger.info("step3: 获取apollo配置的Android API common参数完成")


class IOSApiCommonSetupClass(ApiSetupClass):
    test_data_common: dict = dict()
    common_namespace = "test-data-api-ios-common"

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def common_data_setup(cls, request: pytest.FixtureRequest, domain_setup: pytest.Function):
        request.cls.test_data_common = MiddlewareRepository.get_test_datas(
            namespace=cls.common_namespace, apollo=cls.apollo
        )
        logger.info("step3: 获取apollo配置的iOS API common参数完成")


class AndroidApiDataSetupClass(AndroidApiCommonSetupClass):
    test_data: dict = dict()
    api_namespace = "test-data-api-android"

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def http_api_setup(cls, request: pytest.FixtureRequest, common_data_setup: pytest.Function):
        request.cls.test_data = MiddlewareRepository.get_test_datas(
            namespace=cls.api_namespace, apollo=cls.apollo
        )
        logger.info("step4: 获取apollo配置的Android API请求参数完成")


class IOSApiDataSetupClass(AndroidApiCommonSetupClass):
    test_data: dict = dict()
    api_namespace = "test-data-api-ios"

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def http_api_setup(cls, request: pytest.FixtureRequest, common_data_setup: pytest.Function):
        request.cls.test_data = MiddlewareRepository.get_test_datas(
            namespace=cls.api_namespace, apollo=cls.apollo
        )
        logger.info("step4: 获取apollo配置的iOS API请求参数完成")


class BeforeAndroidApiTest(AndroidApiDataSetupClass):

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def before_test_setup(cls, request: pytest.FixtureRequest, http_api_setup: pytest.Function):
        pass


class BeforeIOSApiTest(AndroidApiDataSetupClass):

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def before_test_setup(cls, request: pytest.FixtureRequest, http_api_setup: pytest.Function):
        pass
