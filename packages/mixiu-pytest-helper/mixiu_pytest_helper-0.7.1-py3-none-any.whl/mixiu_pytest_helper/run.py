# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     run.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import os
import sys
import shutil
import pytest
import platform
import subprocess
import pytest_cov
import logging.config
from airtest_helper.dir import join_path
from mixiu_pytest_helper.dir import init_dir, is_dir
from allure_pytest.utils import ALLURE_DESCRIPTION_MARK
from distributed_logging.parse_yaml import ProjectConfig
from pytest_html.__version import version as html_version
from pytest_metadata.__version import version as metadata_version


def run_tests(project_path: str = None, report_type: str = ALLURE_DESCRIPTION_MARK, app_name: str = 'mixiu',
              auto_report: bool = False):
    os.environ['APP_NAME'] = app_name
    pytest_args = list()
    pytest_plugins = list()
    run_scripts = sys.argv[0]
    if project_path is None:
        test_path = run_scripts
        project_path = os.path.dirname(os.path.abspath(run_scripts))
    else:
        test_path = project_path
    init_dir(project_path=project_path)
    config = ProjectConfig(project_home=project_path).get_object()
    logging_plus = getattr(config, "logging")
    logging.config.dictConfig(logging_plus)
    allure_dir = join_path([project_path, "allure-results"])
    if (report_type == ALLURE_DESCRIPTION_MARK and pytest_cov.__version__ >= '5.0.0' and
            html_version >= '4.1.1' and metadata_version >= '3.1.1'):
        pytest_plugins.extend(['allure_pytest', 'pytest_cov', 'pytest_html', 'pytest_metadata'])
        pytest_args.extend(
            ['--alluredir={}'.format(allure_dir), '--cov', '--cov-report=html', '--cov-config=.coveragerc']
        )
    pytest_args.append(test_path)
    pytest.main(args=pytest_args, plugins=pytest_plugins)
    if auto_report is True and is_dir(file_path=str(allure_dir)) is True:
        allure_bin = join_path(
            [os.getenv('ALLURE_HOME'), 'bin', 'allure.bat' if platform.system() == 'Windows' else 'allure']
        )
        allure_report = join_path([project_path, 'allure-report'])
        if is_dir(file_path=str(allure_report)) is True:
            shutil.rmtree(path=allure_report)
        # 使用 subprocess 生成报告
        generate_command = [allure_bin, 'generate', allure_dir, '-o', allure_report]
        open_command = [allure_bin, 'open', allure_report]
        try:
            subprocess.run(generate_command, check=True, capture_output=True, text=True)
            print("开始运行报表服务......")
            print("注意：若要终止，请按Ctrl + C 终止")
            subprocess.run(open_command, check=True, capture_output=True, text=True)
        except Exception as e:
            print(e)
            print("报表服务终止.")
