# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     collector.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/03
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import json
import importlib
import subprocess
from pandas import set_option, DataFrame
from mixiu_pytest_helper.log import logger
from mixiu_pytest_helper.dir import get_project_path, delete_file, init_dir

"""
display.max_rows:     设置要显示的最大行数
display.max_columns:  设置要显示的最大列数
display.width:        设置显示的宽度，以字符数为单位
display.precision:    设置浮点数的精度
display.max_colwidth: 设置要显示的列的最大宽度，以字符数为单位
"""

# 设置要显示的最大行数和列数
set_option('display.width', 65535)
set_option('display.max_rows', 5000)
set_option('display.max_columns', 1024)
set_option('display.max_colwidth', 1000)
# 设置打印格式，使列头和行内容对齐
set_option('display.unicode.east_asian_width', True)


def collect_marks(collect_dir: str, print_enable: bool = False) -> list:
    if collect_dir is None:
        collect_dir = get_project_path()
    init_dir(project_path=collect_dir)
    collect_marks = list()
    collect_marks_file = 'collect_marks.json'
    # 使用 subprocess 运行 pytest
    result = subprocess.run(
        ['pytest', '--disable-warnings', '--collect-only', '--verbose', '--json-report',
         '--json-report-file={}'.format(collect_marks_file),
         collect_dir],
        capture_output=True,
        text=True
    )

    # 检查 pytest 是否成功执行
    if result.returncode != 0:
        logger.error(result.stderr)
        return collect_marks

    # 解析 pytest 输出的 JSON 报告
    with open(collect_marks_file, 'r') as f:
        report = json.load(f)

    delete_file(file_path=collect_marks_file)

    for x in report.get("collectors"):
        for y in x.get("result"):
            if y.get("type") == "Function":
                node_id = y.get('nodeid')
                marks = get_decorators(nodeid=node_id)
                if marks:
                    node_id_slice = node_id.split("::")
                    module_name = node_id_slice[0][:-3].replace('/', '.')
                    # module_name = importlib.import_module(module_path.replace('/', '.'))
                    class_name = node_id_slice[1] if len(node_id_slice) == 3 else None
                    function_name = node_id_slice[-1]
                    marks.update(module_name=module_name, class_name=class_name, function_name=function_name)
                    collect_marks.append(marks)
    if print_enable is True and collect_marks:
        df = DataFrame.from_records(collect_marks)
        df = df[['case_id', 'case_level', 'case_module', 'case_name', 'case_desc']]
        # 打印DataFrame
        # print(df.to_string(justify='left', index=False))
        print(df.to_markdown(index=True, tablefmt="grid"))
    return collect_marks


def get_decorators(nodeid: str) -> dict:
    """获取函数的所有装饰器"""
    marks = dict()
    # 分解字符串
    parts = nodeid.split('::')
    # 导入模块
    module = importlib.import_module(parts[0][:-3].replace('/', '.'))
    if len(parts) == 3:
        # 获取类
        cls = getattr(module, parts[1], None)
        func = getattr(cls, parts[2], None) if cls is not None else None
    else:
        # cls = None
        func = getattr(module, parts[1], None)
    if func is not None and callable(func):
        if hasattr(func, 'pytestmark'):
            # 获取当前函数的pytestmark属性（如果有）
            pytestmark = getattr(func, 'pytestmark') or list()
            for mark in pytestmark:
                if getattr(mark, 'name', '').startswith("case"):
                    args = getattr(mark, 'args')
                    marks[getattr(mark, 'name')] = args[0] if args and isinstance(args, tuple) else None
    return marks
