import xml.etree.ElementTree as ET
from jmetertools.core.base import General


class __JMeterArguments:
    def __init__(self):
        self.__name = '用户定义的变量'
        self.__comments = ''
        self.__arguments = {}

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_comments(self):
        return self.__comments

    def set_comments(self, comments):
        self.__comments = comments

    def get_arguments(self):
        return self.__arguments

    def set_arguments(self, arguments):
        self.__arguments = arguments

    def get(self, parent):
        arguments_prop = ET.SubElement(parent, 'Arguments')
        arguments_prop.set('guiclass', 'ArgumentsPanel')
        arguments_prop.set('testclass', 'Arguments')
        arguments_prop.set('testname', self.__name)
        arguments_prop.set('enabled', 'true')
        if self.__comments != '':
            comments_prop = General.add_str_prop(self, arguments_prop, 'TestPlan.comments', self.__comments)
        collection_prop = ET.SubElement(arguments_prop, 'collectionProp')
        collection_prop.set('name', 'Arguments.arguments')
        if self.__arguments:
            for key, value in self.__arguments.items():
                element_prop = ET.SubElement(collection_prop, 'elementProp')
                element_prop.set('name', key)
                element_prop.set('elementType', 'Argument')
                arguments_value_prop = General.add_str_prop(self, element_prop, 'Argument.name', key)
                arguments_value_prop = General.add_str_prop(self, element_prop, 'Argument.value', value)
                arguments_value_prop = General.add_str_prop(self, element_prop, 'Argument.desc', '')
                arguments_value_prop = General.add_str_prop(self, element_prop, 'Argument.metadata', '=')
        hashtree = ET.SubElement(parent, 'hashTree')
        return arguments_prop
