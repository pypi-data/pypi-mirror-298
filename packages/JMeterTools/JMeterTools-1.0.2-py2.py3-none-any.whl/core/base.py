"""
用于生成jmeter脚本
"""

__author__ = "zhangkx"
__version__ = "0.0.1"


import xml.etree.ElementTree as ET


class General:

    def add_int_prop(self, parent, name, value):
        int_prop = ET.SubElement(parent, 'intProp')
        int_prop.set('name', name)
        int_prop.text = str(value)

    def add_long_prop(self, parent, name, value):
        int_prop = ET.SubElement(parent, 'longProp')
        int_prop.set('name', name)
        int_prop.text = str(value)

    def add_str_prop(self, parent, name, value):
        str_prop = ET.SubElement(parent, 'stringProp')
        str_prop.set('name', name)
        str_prop.text = value

    def add_bool_prop(self, parent, name, value):
        bool_prop = ET.SubElement(parent, 'boolProp')
        bool_prop.set('name', name)
        bool_prop.text = str(value)

    def add_loop_controller(self, parent, loops):
        element_prop = ET.SubElement(parent, 'elementProp')
        element_prop.set('name', 'ThreadGroup.main_controller')
        element_prop.set('elementType', 'LoopController')
        element_prop.set('guiclass', 'LoopControlPanel')
        element_prop.set('testclass', 'LoopController')
        element_prop.set('testname', '循环控制器')
        self.add_int_prop(self, element_prop, 'LoopController.loops', loops)
        self.add_bool_prop(self, parent, '.LoopController.continue_forever', 'false')

    def indent(self, elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

