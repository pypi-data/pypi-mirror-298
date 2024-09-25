import xml.etree.ElementTree as ET
from jmetertools.core.base import General
from jmetertools.core.HashCode import GetHashCode


class __JMeterResponseAssert:
    def __init__(self):
        # 断言名称
        self.__assert_name = '响应断言'
        # 注释
        self.__comments = ''
        # 自定义失败消息
        self.__custom_message = ''
        # 测试字段    Assertion.response_data 响应文本    Assertion.response_code 响应代码    Assertion.response_message 响应信息
        # Assertion.request_headers 请求头    Assertion.sample_label url样本    Assertion.response_data_as_document 文档(文本)
        # Assertion.request_data 请求数据
        self.__test_field = 'Assertion.response_data'
        self.__assume_success = 'false'
        # 模式匹配规则   1 匹配    2 包含    5 不匹配    6 不包含    8 相等    12 不相等    16 子字符串    20 不是子字符串    33 或者匹配    34 或者包含
        # 37 或者不匹配    38 或者不包含    40 或者相等    44 或者不相等    48 或者是子字符串    52 或者不是子字符串
        self.__test_type = ''
        # 适用方式  all 主样本和分支样本    children 分支样本    variable 使用jmeter变量名称    默认为空仅主样本
        self.__scope = ''
        # 变量名称
        self.__scope_variable = ''
        self.__assert_text = []

    def get_assert_name(self):
        return self.__assert_name

    def set_assert_name(self, name):
        self.__assert_name = name

    def get_comments(self):
        return self.__comments

    def set_comments(self, comments):
        self.__comments = comments

    def get_custom_message(self):
        return self.__custom_message

    def set_custom_message(self, custom_message):
        self.__custom_message = custom_message

    def get_test_field(self):
        return self.__test_field

    def set_test_field(self, test_field):
        self.__test_field = test_field

    def get_assume_type(self):
        return self.__assume_success

    def set_assume_type(self, assume_type):
        self.__assume_success = assume_type

    def get_test_type(self):
        return self.__test_type

    def set_test_type(self, test_type):
        self.__test_type = test_type

    def get_scope(self):
        return self.__scope

    def set_scope(self, scope):
        self.__scope = scope

    def get_scope_variable(self):
        return self.__scope_variable

    def get_scope_variable(self, scope_variable):
        self.__scope_variable = scope_variable

    def get_assert_text(self):
        return self.__assert_text

    def set_assert_text(self, assert_text):
        self.__assert_text = assert_text

    def items(self):
        dicts = {
            'comments': self.__comments,
            'custom_message': self.__custom_message,
            'test_field': self.__test_field,
            'assume_success': self.__assume_success,
            'test_type': self.__test_type,
            'scope': self.__scope,
            'scope_variable': self.__scope_variable,
        }
        return dicts

    def get(self, parent):
        prop_map = {
            'comments': General.add_str_prop,
            'custom_message': General.add_str_prop,
            'test_field': General.add_str_prop,
            'assume_success': General.add_bool_prop,
            'test_type': General.add_int_prop,
            'scope': General.add_str_prop,
            'scope_variable': General.add_str_prop
        }

        keys_map = {
            'comments': 'TestPlan.comments',
            'custom_message': 'Assertion.custom_message',
            'test_field': 'Assertion.test_field',
            'assume_success': 'Assertion.assume_success',
            'test_type': 'Assertion.test_type',
            'scope': 'Assertion.scope',
            'scope_variable': 'Scope.variable'
        }

        assert_prop = ET.SubElement(parent, 'ResponseAssertion')
        assert_prop.set('guiclass', 'AssertionGui')
        assert_prop.set('testclass', 'ResponseAssertion')
        assert_prop.set('testname', self.__assert_name)

        if self.__assert_text:
            collection_prop = ET.SubElement(assert_prop, 'collectionProp')
            collection_prop.set('name', 'Asserion.test_strings')
            for text in self.__assert_text:
                General.add_str_prop(self, collection_prop, str(GetHashCode.getHashCode(text)), text)

        for key, value in self.items().items():
            if key in prop_map:
                if value == '' or value == 'false':
                    pass
                else:
                    prop_map[key](self, assert_prop, keys_map[key], str(value))
        hashtree = ET.SubElement(parent, 'hashTree')
        return assert_prop
