import xml.etree.ElementTree as ET
from jmetertools.core.base import General


class __JMeterSummaryReport:
    def __init__(self):
        self.__name = '汇总报告'
        # 显示日志内容  为true时勾选仅错误日志
        self.__error_logging = 'false'
        # 显示日志内容 为true时勾选仅成功日志，与错误日志只能选择一个
        self.__success_only_logging = ''
        # 数据写入文件的文件名称
        self.__filename = ''
        # 示例保存配置
        self.__sample_save_config = {
            'time': 'true',
            'latency': 'true',
            'timestamp': 'true',
            'success': 'true',
            'label': 'true',
            'code': 'true',
            'message': 'true',
            'threadName': 'true',
            'dataType': 'true',
            'encoding': 'false',
            'assertions': 'true',
            'subresults': 'true',
            'responseData': 'false',
            'samplerData': 'false',
            'xml': 'false',
            'fieldNames': 'true',
            'responseHeaders': 'false',
            'requestHeaders': 'false',
            'responseDataOnError': 'false',
            'saveAssertionResultsFailureMessage': 'true',
            'assertionsResultsToSave': '0',
            'bytes': 'true',
            'sentBytes': 'true',
            'url': 'true',
            'threadCounts': 'true',
            'idleTime': 'true',
            'connectTime': 'true'
        }

    def get_name(self):
        return self.__name

    def set__name(self, name):
        self.__name = name

    def get_error_logging(self):
        return self.__error_logging

    def set_error_logging(self, error_logging):
        self.__error_logging = error_logging

    def get_success_only_logging(self):
        return self.__success_only_logging

    def set_success_only_logging(self, success_only_logging):
        self.__success_only_logging = success_only_logging

    def get_filename(self):
        return self.__filename

    def set_filename(self, filename):
        self.__filename = filename

    def get_sample_save_config(self):
        return self.__sample_save_config

    def set_sample_save_config(self, sample_save_config: dict):
        self.__sample_save_config = sample_save_config

    def set_config(self, config: dict):
        for key, value in config.items():
            self.__sample_save_config[key] = value

    def items(self):
        dicts = {
            'error_logging': self.__error_logging,
            'success_only_logging': self.__success_only_logging,
            'filename': self.__filename
        }
        return dicts

    def get(self, parent):
        prop_map = {
            'error_logging': General.add_bool_prop,
            'success_only_logging': General.add_bool_prop,
            'filename': General.add_str_prop
        }

        keys_map = {
            'error_logging': 'ResultCollector.error_logging',
            'success_only_logging': 'ResultCollector.success_only_logging',
            'filename': 'filename'
        }

        summary_report_prop = ET.SubElement(parent, 'ResultCollector')
        summary_report_prop.set('guiclass', 'SummaryReport')
        summary_report_prop.set('testclass', 'ResultCollector')
        summary_report_prop.set('testname', self.__name)

        for key, value in self.items().items():
            if key in prop_map:
                prop_map[key](self, summary_report_prop, keys_map[key], str(value))
                # if value == '' or value == 'false':
                #     pass
                # else:
                #     prop_map[key](self, result_collector_prop, keys_map[key], str(value))
        obj_prop = ET.SubElement(summary_report_prop, 'objProp')
        config_name_prop = ET.SubElement(obj_prop, 'name')
        config_name_prop.text = 'saveConfig'
        value_prop = ET.SubElement(obj_prop, 'value')
        value_prop.set('class', 'SampleSaveConfiguration')
        for key, value in self.__sample_save_config.items():
            props = ET.SubElement(value_prop, key)
            props.text = str(value)
        hashtree = ET.SubElement(parent, 'hashTree')
        return summary_report_prop
