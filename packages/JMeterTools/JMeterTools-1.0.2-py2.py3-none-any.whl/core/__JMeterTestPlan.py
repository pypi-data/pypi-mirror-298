import xml.etree.ElementTree as ET


class __JMeterTestPlan:
    def __init__(self):
        self.__test_plan_name = '测试计划'
        # 函数测试模式
        self.__functional_mode = 'false'
        # 独立运行没给线程组
        self.__serialize_threadgroups = 'false'
        # 主线程结束后运行tearDown
        self.__tearDown_on_shutdown = 'false'
        # 用户设置定义的变量
        self.__user_defined_variables = {}

    def get_test_plan_name(self):
        return self.__test_plan_name

    def set_test_plan_name(self, test_plan_name):
        self.__test_plan_name = test_plan_name

    def get_functional_mode(self):
        return self.__functional_mode

    def set_funtional_mode(self, funtional_mode):
        self.__functional_mode = funtional_mode

    def get_serialize_threadgroups(self):
        return self.__serialize_threadgroups

    def set_serialize_threadgroups(self, serialize_threadgroups):
        self.__serialize_threadgroups = serialize_threadgroups

    def get_teardown_on_shutdown(self):
        return self.__tearDown_on_shutdown

    def set_teardown_on_shutdown(self, teardown_on_shutdown):
        self.__tearDown_on_shutdown = teardown_on_shutdown

    def get_user_defined_variables(self):
        return self.__user_defined_variables

    def set_user_defined_variables(self, user_defined_variables):
        self.__user_defined_variables = user_defined_variables

    def get(self, parent):
        test_plan = ET.SubElement(parent, 'TestPlan')
        test_plan.set('guiclass', 'TestPlanGui')
        test_plan.set('testclass', 'TestPlan')
        test_plan.set('testname', self.__test_plan_name)
        elemet_prop = ET.SubElement(test_plan, 'elementProp')
        elemet_prop.set('name', 'TestPlan.user_defined_variables')
        elemet_prop.set('elementType', 'Arguments')
        elemet_prop.set('guiclass', 'ArgumentsPanel')
        elemet_prop.set('testclass', 'Arguments')
        elemet_prop.set('testname', '用户定义的变量')
        collection_prop = ET.SubElement(elemet_prop, 'collectionProp')
        collection_prop.set('name', 'Arguments.arguments')
        if self.__user_defined_variables:
            for key, value in self.__user_defined_variables.items():
                variables_elem = ET.SubElement(collection_prop, 'elementProp')
                variables_elem.set('name', key)
                variables_elem.set('elementType', 'Argument')
                str_prop1 = ET.SubElement(variables_elem, 'stringProp')
                str_prop1.set('name', 'Argument.name')
                str_prop1.text = str(key)
                str_prop2 = ET.SubElement(variables_elem, 'stringProp')
                str_prop2.set('name', 'Argument.value')
                str_prop2.text = str(value)
                str_prop3 = ET.SubElement(variables_elem, 'stringProp')
                str_prop3.set('name', 'Argument.metadata')
                str_prop3.text = '='

        # functional_mode_prop = ET.SubElement(test_plan, 'boolProp')
        # functional_mode_prop.set('name', 'TestPlan.functional_mode')
        # functional_mode_prop.text = self.__functional_mode
        # serialize_threadgroups_prop = ET.SubElement(test_plan, 'boolProp')
        # serialize_threadgroups_prop.set('name', 'TestPlan.serialize_threadgroups')
        # serialize_threadgroups_prop.text = self.__serialize_threadgroups
        # tearDown_on_shutdown_prop = ET.SubElement(test_plan, 'boolProp')
        # tearDown_on_shutdown_prop.set('name', 'TestPlan.tearDown_on_shutdown')
        # tearDown_on_shutdown_prop.text = self.__tearDown_on_shutdown

        return test_plan

