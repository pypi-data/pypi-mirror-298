"""
用于生成jmeter脚本
"""

__author__ = "zhangkx"
__version__ = "0.0.1"

import os
import xml.etree.ElementTree as ET
import subprocess
from jmetertools.core.__JMeterHeaderManager import __JMeterHeaderManager
from jmetertools.core.__JMeterArguments import __JMeterArguments
from jmetertools.core.__JMeterRespTimeGraphVisualizer import __JMeterRespTimeGraphVisualizer
from jmetertools.core.__JMeterSummaryReport import __JMeterSummaryReport
from jmetertools.core.__JMeterStatVisualizer import __JMeterStatVisualizer
from jmetertools.core.__JMeterHttpSampler import __JMeterHttpSampler
from jmetertools.core.__JMeterTestPlan import __JMeterTestPlan
from jmetertools.core.__JMeterThreadGroup import __JMeterThreadGroup
from jmetertools.core.__JMeterResponseAssert import __JMeterResponseAssert
from jmetertools.core.__JMeterViewResultsFullVisualizer import __JMeterViewResultsFullVisualizer
from jmetertools.core.yaml_tool import read_yaml


def get():
    jmeter_test_plan = ET.Element('jmeterTestPlan')
    jmeter_test_plan.set('version', '1.2')
    jmeter_test_plan.set('properties', '5.0')
    jmeter_test_plan.set('jmeter', '5.6.3')
    return jmeter_test_plan


def run_jmeter_test(jmx_file, result_file, result_dir):
    print('开始测试')
    # 构建JMeter命令行命令
    # 注意：根据你的JMeter安装路径和需要，命令可能有所不同
    # 这里的例子假设JMeter的bin目录已添加到PATH中
    conf_path = os.path.dirname(__file__)
    config = os.path.join(conf_path + '/config.yaml')
    jmeter_home = read_yaml(config)['jmeter_home']
    command = [
        jmeter_home + 'jmeter',
        '-n',  # 非GUI模式
        '-t', jmx_file,  # 指定JMX文件
        '-l', result_file,  # 指定结果文件
        '-e',  # 生成报告
        '-o', result_dir  # 报告输出目录
    ]

    # 运行JMeter命令
    process = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 打印输出（可选）
    print("JMeter输出:")
    print(process.stdout)

    if process.stderr:
        print("JMeter错误:")
        print(process.stderr)


class JMeterHeaderManager(__JMeterHeaderManager):
    pass


class JMeterArguments(__JMeterArguments):
    pass


class JMeterRespTimeGraphVisualizer(__JMeterRespTimeGraphVisualizer):
    pass


class JMeterSummaryReport(__JMeterSummaryReport):
    pass


class JMeterStatVisualizer(__JMeterStatVisualizer):
    pass


class JMeterHttpSampler(__JMeterHttpSampler):
    pass


class JMeterTestPlan(__JMeterTestPlan):
    pass


class JMeterThreadGroup(__JMeterThreadGroup):
    pass


class JMeterResponseAssert(__JMeterResponseAssert):
    pass


class JMeterViewResultsFullVisualizer(__JMeterViewResultsFullVisualizer):
    pass
