# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     context.py
# Description:  静态上下文
# Author:       mfkifhss2023
# CreateDate:   2024/08/13
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from middleware_helper.redis import get_redis_connection
from mixiu_pytest_helper.infrastructure import ApolloClientManager, RedisClientManager

apollo = ApolloClientManager()

auth_client = RedisClientManager(redis=get_redis_connection(**apollo.get_value("redis.auth")))
lock_client = RedisClientManager(redis=get_redis_connection(**apollo.get_value("redis.lock")))
cache_client = RedisClientManager(redis=get_redis_connection(**apollo.get_value("redis.cache")))
