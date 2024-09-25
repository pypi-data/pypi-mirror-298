import xml.etree.ElementTree as ET
from jmetertools.core.base import General


class __JMeterThreadGroup:
    def __init__(self):
        self.__test_plan_name = '测试计划'
        self.__thread_group_name = '线程组'
        # 线程数
        self.__num_threads = 1
        # 注释
        self.__thread_comments = ''
        # 间隔时间
        self.__ramp_time = 1
        self.__same_user_on_next_iteration = 'true'
        # 取样器错误后执行动作  continue 继续   startnextloop 启动下一个进程循环    stopthread 停止线程    stoptest 停止测试    stoptestnow 立即停止测试
        self.__on_sample_error = 'continue'
        # 循环次数
        self.__loops = 1
        # 调度器持续时间 /秒
        self.__duration = ''
        # 调度器启动延迟 /秒
        self.__delay = ''
        # 延迟创建线程知道需要
        self.__delayedStart = 'false'
        # 调度器
        self.__scheduler = 'false'
        # 永远循环
        self.__continue_forever = 'false'

    def get_test_plan_name(self):
        return self.__test_plan_name

    def set_test_paln_name(self, test_plan_name):
        self.__test_plan_name = test_plan_name

    def get_thread_group_name(self):
        return self.__thread_group_name

    def set_thread_group_name(self, thread_group_name):
        self.__thread_group_name = thread_group_name

    def get_num_threads(self):
        return self.__num_threads

    def set_num_threads(self, num_threads):
        self.__num_threads = num_threads

    def get_thread_comments(self):
        return self.__thread_comments

    def set_thread_comments(self, thread_comments):
        self.__thread_comments = thread_comments

    def get_ramp_time(self):
        return self.__ramp_time

    def set_ramp_time(self, ramp_time):
        self.__ramp_time = ramp_time

    def get_same_user_on_next_iteration(self):
        return self.__same_user_on_next_iteration

    def set_same_user_on_next_iteration(self, same_user_on_next_iteration):
        self.__same_user_on_next_iteration = same_user_on_next_iteration

    def get_on_sample_error(self):
        return self.__on_sample_error

    def set_on_sample_error(self, on_sample_error):
        self.__on_sample_error = on_sample_error

    def get_loops(self):
        return self.__loops

    def set_loops(self, loops):
        self.__loops = loops

    def get_duration(self):
        return self.__duration

    def set_duration(self, duration):
        self.__duration = duration

    def get_delay(self):
        return self.__delay

    def set_delay(self, delay):
        self.__delay = delay

    def get_delayedStart(self):
        return self.__delayedStart

    def set_delayedStart(self, delayedStart):
        self.__delayedStart = delayedStart

    def get_scheduler(self):
        return self.__scheduler

    def set_scheduler(self, scheduler):
        self.__scheduler = scheduler

    def items(self):
        dicts = {
            'comments': self.__thread_comments,
            'num_threads':self.__num_threads,
            'ramp_time': self.__ramp_time,
            'same_user_on_next_iteration': self.__same_user_on_next_iteration,
            'on_sample_error': self.__on_sample_error,
            'duration': self.__duration,
            'delay': self.__delay,
            'delayedStart': self.__delayedStart,
            'scheduler': self.__scheduler,
            'continue_forever': self.__continue_forever,
            'loops': self.__loops
        }
        return dicts

    def add_loop_controller(self, parent, loops):
        element_prop = ET.SubElement(parent, 'elementProp')
        element_prop.set('name', 'ThreadGroup.main_controller')
        element_prop.set('elementType', 'LoopController')
        element_prop.set('guiclass', 'LoopControlPanel')
        element_prop.set('testclass', 'LoopController')
        element_prop.set('testname', '循环控制器')
        General.add_str_prop(self, element_prop, 'LoopController.loops', str(loops))
        General.add_bool_prop(self, element_prop, 'LoopController.continue_forever', self.__continue_forever)

    def get(self, parent):
        thread_group = ET.SubElement(parent,'ThreadGroup')
        thread_group.set('guiclass', 'ThreadGroupGui')
        thread_group.set('testclass', 'ThreadGroup')
        thread_group.set('testname', self.__thread_group_name)

        prop_map = {
            'comments': General.add_str_prop,
            'num_threads': General.add_int_prop,
            'ramp_time': General.add_int_prop,
            'same_user_on_next_iteration': General.add_bool_prop,
            'on_sample_error': General.add_str_prop,
            'duration': General.add_long_prop,
            'delay': General.add_long_prop,
            'delayedStart': General.add_bool_prop,
            'scheduler': General.add_bool_prop
        }

        keys_map = {
            'comments': 'TestPlan.comments',
            'num_threads': 'ThreadGroup.num_threads',
            'ramp_time': 'ThreadGroup.ramp_time',
            'same_user_on_next_iteration': 'ThreadGroup.same_user_on_next_iteration',
            'on_sample_error': 'ThreadGroup.on_sample_error',
            'duration': 'ThreadGroup.duration',
            'delay': 'ThreadGroup.delay',
            'delayedStart': 'ThreadGroup.delayedStart',
            'scheduler': 'ThreadGroup.scheduler'
        }

        for key, value in self.items().items():
            if key == 'loops':
                self.add_loop_controller(thread_group, value)
            elif key in prop_map:
                if value == '' or value == 'false':
                    pass
                else:
                    prop_map[key](self, thread_group, keys_map[key], value)
        return thread_group

