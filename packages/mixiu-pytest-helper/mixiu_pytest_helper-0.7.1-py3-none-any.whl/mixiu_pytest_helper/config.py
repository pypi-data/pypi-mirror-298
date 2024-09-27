# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     config.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""

apollo_params_map = {
    "mixiu": {
        "app_id": "mixiu-app-autotest",
        "cluster": "dev",
        "namespace_name": "application",
        "secret": "29f1628c966444d58dce1e54792ac208",
        "domain": "http://139.199.225.100:30080",  # 通过命令行传递赋值
    },
    "catlive": {
        "app_id": "catshow-app-autotest",
        "cluster": "dev",
        "namespace_name": "application",
        "secret": "3d7e329197244feba35ff6844936ab1f",
        "domain": "http://139.199.225.100:30080",  # 通过命令行传递赋值
    }
}

pytest_config = r"""[pytest]
addopts = --strict-markers --tb=short -v -ra -q -s
markers =
    smoke: mark a test as a smoke test.
    regression: mark a test as a regression test.
    my: mark a test related to the 'My' section.
    messages: mark a test related to the 'Message' section.
    square: mark a test related to the 'Square' section.
    home: mark a test related to the 'Home' section.
    api: mark a test related to the 'API' section.
    case_level: 用于标记测试用例的级别
    case_desc: 用于标记测试用例的描述
    case_name: 用于标记测试用例的名称
    case_module: 用于标记测试用例所在的功能模块
    case_id: 用于标记测试用例的唯一ID
filterwarnings =
    error
    ignore::UserWarning
    ignore::DeprecationWarning
    ignore:function ham\(\) is deprecated:DeprecationWarning
    ignore:.*_SixMetaPathImporter.find_spec.*:ImportWarning
"""

coverage_config = """[run]
# 排除特定模块或代码
omit =
    */mixiu_pytest_helper/execute_all.py
    */__init__.py
    *if __name__ == "__main__":*
    *from mixiu_pytest_helper.run import run_tests*
    *run_tests()*

[report]
# 在报告中隐藏某些行或文件
exclude_lines =
    if __name__ == "__main__":
    from mixiu_pytest_helper.run import run_tests
    run_tests()
    pragma: no cover
    def __str__
"""

logging_config = r"""development:
  version: 1
  disable_existing_loggers: false
  formatters:
    standard:
      format: '%(asctime)s - [PID-%(process)d] - [Thread-%(thread)d] - [%(levelname)s] - %(message)s - <%(funcName)s> - [Line-%(lineno)d] - %(filename)s'
      class: logging.Formatter
    console:
      format: '%(asctime)s - [%(levelname)s] - %(message)s - <%(funcName)s> - [Line-%(lineno)d] - %(filename)s'
      class: logging.Formatter
    json:
      class: distributed_logging.JSONFormatter
  handlers:
    stream:
      level: INFO
      stream: ~~sys_module sys.stdout
      formatter: console
      class: logging.StreamHandler
    test.log:
      level: DEBUG
      formatter: standard
      class: distributed_logging.ConcurrentRotatingFileHandler  # 日志类，当前类支持多进程模式的日志记录
      filename: ~~abspath ./log/test.log    # 日志文件路径，请使用相对路径
      max_bytes: 20971520    #  以20M为单位按此大小分切文件
      mode: a           # 日志文件写入模式
      debug: false  # 向此class添加额外的调试语句（用于开发）
      delay: ~   # 已弃用，请忽略
      use_gzip: false  # 启用后，自动以gzip格式打包分切的日志文件
      owner: ~  # 默认为None， 日志文件的元素序列（用户所有者、组所有者）(仅限Unix)
      chmod: ~  # 默认为None， 日志文件的权限(仅限Unix)
      umask: ~   # 默认为None， 创建日志文件时要临时进行的umask设置，这是chmod的替代方法。它主要用于Unix系统，但是也可以在Windows上使用。Windows安全模型更为复杂这与更改访问控制条目不同。
      newline: ~  #  默认为None， 在Windows上使用CRLF，在Unix上使用LF。设置为""的无翻译，在这种情况下，"terminator"参数决定行的结尾。
      terminator: "\n"  #  设置为\r\n并加上换行符=，以强制Windows样式不考虑操作系统平台的newline。
      backup_count: 9   # 删除日志文件前要保留的分切文件数
      encoding: utf-8  # 日志文件的文本编码
      unicode_error_policy: ignore  #  应为'ignore'、'replace'、'strict'之一确定将消息写入流编码所在的日志时发生的情况不支持。默认设置为忽略，即删除不可用的字符。
    test.json:
      level: DEBUG
      formatter: json
      class: distributed_logging.ConcurrentRotatingFileHandler  # 日志类，当前类支持多进程模式的日志记录
      filename: ~~abspath ./log/test.json    # 日志文件路径，请使用相对路径
      max_bytes: 52428800    #  以50M为单位按此大小分切文件
      mode: a           # 日志文件写入模式
      debug: false  # 向此class添加额外的调试语句（用于开发）
      delay: ~   # 已弃用，请忽略
      use_gzip: false  # 启用后，自动以gzip格式打包分切的日志文件
      owner: ~  # 默认为None， 日志文件的元素序列（用户所有者、组所有者）(仅限Unix)
      chmod: ~  # 默认为None， 日志文件的权限(仅限Unix)
      umask: ~   # 默认为None， 创建日志文件时要临时进行的umask设置，这是chmod的替代方法。它主要用于Unix系统，但是也可以在Windows上使用。Windows安全模型更为复杂这与更改访问控制条目不同。
      newline: ~  #  默认为None， 在Windows上使用CRLF，在Unix上使用LF。设置为""的无翻译，在这种情况下，"terminator"参数决定行的结尾。
      terminator: "\n"  #  设置为\r\n并加上换行符=，以强制Windows样式不考虑操作系统平台的newline。
      backup_count: 9   # 删除日志文件前要保留的分切文件数
      encoding: utf-8  # 日志文件的文本编码
      unicode_error_policy: ignore  #  应为'ignore'、'replace'、'strict'之一确定将消息写入流编码所在的日志时发生的情况不支持。默认设置为忽略，即删除不可用的字符。
    airtest.log:
      level: DEBUG
      formatter: standard
      class: distributed_logging.ConcurrentRotatingFileHandler  # 日志类，当前类支持多进程模式的日志记录
      filename: ~~abspath ./log/airtest.log    # 日志文件路径，请使用相对路径
      max_bytes: 20971520    #  以20M为单位按此大小分切文件
      mode: a           # 日志文件写入模式
      debug: false  # 向此class添加额外的调试语句（用于开发）
      delay: ~   # 已弃用，请忽略
      use_gzip: false  # 启用后，自动以gzip格式打包分切的日志文件
      owner: ~  # 默认为None， 日志文件的元素序列（用户所有者、组所有者）(仅限Unix)
      chmod: ~  # 默认为None， 日志文件的权限(仅限Unix)
      umask: ~   # 默认为None， 创建日志文件时要临时进行的umask设置，这是chmod的替代方法。它主要用于Unix系统，但是也可以在Windows上使用。Windows安全模型更为复杂这与更改访问控制条目不同。
      newline: ~  #  默认为None， 在Windows上使用CRLF，在Unix上使用LF。设置为""的无翻译，在这种情况下，"terminator"参数决定行的结尾。
      terminator: "\n"  #  设置为\r\n并加上换行符=，以强制Windows样式不考虑操作系统平台的newline。
      backup_count: 9   # 删除日志文件前要保留的分切文件数
      encoding: utf-8  # 日志文件的文本编码
      unicode_error_policy: ignore  #  应为'ignore'、'replace'、'strict'之一确定将消息写入流编码所在的日志时发生的情况不支持。默认设置为忽略，即删除不可用的字符。
    airtest.json:
      level: DEBUG
      formatter: json
      class: distributed_logging.ConcurrentRotatingFileHandler  # 日志类，当前类支持多进程模式的日志记录
      filename: ~~abspath ./log/airtest.json    # 日志文件路径，请使用相对路径
      max_bytes: 52428800    #  以50M为单位按此大小分切文件
      mode: a           # 日志文件写入模式
      debug: false  # 向此class添加额外的调试语句（用于开发）
      delay: ~   # 已弃用，请忽略
      use_gzip: false  # 启用后，自动以gzip格式打包分切的日志文件
      owner: ~  # 默认为None， 日志文件的元素序列（用户所有者、组所有者）(仅限Unix)
      chmod: ~  # 默认为None， 日志文件的权限(仅限Unix)
      umask: ~   # 默认为None， 创建日志文件时要临时进行的umask设置，这是chmod的替代方法。它主要用于Unix系统，但是也可以在Windows上使用。Windows安全模型更为复杂这与更改访问控制条目不同。
      newline: ~  #  默认为None， 在Windows上使用CRLF，在Unix上使用LF。设置为""的无翻译，在这种情况下，"terminator"参数决定行的结尾。
      terminator: "\n"  #  设置为\r\n并加上换行符=，以强制Windows样式不考虑操作系统平台的newline。
      backup_count: 9   # 删除日志文件前要保留的分切文件数
      encoding: utf-8  # 日志文件的文本编码
      unicode_error_policy: ignore  #  应为'ignore'、'replace'、'strict'之一确定将消息写入流编码所在的日志时发生的情况不支持。默认设置为忽略，即删除不可用的字符。
  loggers:
    root:
      handlers:
        - stream
        - test.log
        - test.json
      level: DEBUG
      propagate: false
    airtest:
      handlers:
        - stream
        - airtest.log
        - airtest.json
      level: DEBUG
      propagate: false
    pytest:
      handlers:
        - stream
        - test.log
        - test.json
      level: DEBUG
      propagate: false
    urllib3:
      handlers:
        - stream
        - test.log
        - test.json
      level: DEBUG
      propagate: false
    requests:
      handlers:
        - stream
        - test.log
        - test.json
      level: DEBUG
      propagate: false
"""
