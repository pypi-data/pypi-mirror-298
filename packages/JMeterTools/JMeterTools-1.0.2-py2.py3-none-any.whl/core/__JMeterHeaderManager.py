import xml.etree.ElementTree as ET
from jmetertools.core.base import General


class __JMeterHeaderManager:
    def __init__(self):
        self.__name = 'HTTP信息头管理器'
        self.__comments = ''
        self.__headers = {}

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_comments(self):
        return self.__comments

    def set_comments(self, comments):
        self.__comments = comments

    def get_headers(self):
        return self.__headers

    def set_headers(self, headers):
        self.__headers = headers

    def get(self, parent):
        header_manager_prop = ET.SubElement(parent, 'HeaderManager')
        header_manager_prop.set('guiclass', 'HeaderPanel')
        header_manager_prop.set('testclass', 'HeaderManager')
        header_manager_prop.set('testname', self.__name)
        if self.__comments != '':
            comments_prop = General.add_str_prop(self, header_manager_prop, 'TestPlan.comments', self.__comments)
        collection_prop = ET.SubElement(header_manager_prop, 'collectionProp')
        collection_prop.set('name', 'HeaderManager.headers')
        if self.__headers:
            for key, value in self.__headers.items():
                element_prop = ET.SubElement(collection_prop, 'elementProp')
                element_prop.set('name', '')
                element_prop.set('elementType', 'Header')
                header_value_prop = General.add_str_prop(self, element_prop, 'Header.name', key)
                header_value_prop = General.add_str_prop(self, element_prop, 'Header.value', value)
        hashtree = ET.SubElement(parent, 'hashTree')
        return header_manager_prop
