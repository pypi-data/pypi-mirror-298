import xml.etree.ElementTree as ET
from jmetertools.core.base import General


class __JMeterRespTimeGraphVisualizer:
    def __init__(self):
        self.__name = '响应时间图'
        # 显示日志内容  为true时勾选仅错误日志
        self.__error_logging = 'false'
        # 显示日志内容 为true时勾选仅成功日志，与错误日志只能选择一个
        self.__success_only_logging = ''
        # 数据写入文件的文件名称
        self.__filename = ''
        # 时间间隔，为空时默认10秒/10000ms
        self.__interval = ''
        # 取样器标签选择，默认为空，不勾选，勾选为true
        self.__seriesselection = ''
        # 取样器标签选择输入
        self.__seriesselection_match_label = ''
        # 取样器标签区分大小写, 默认为空，不勾选，勾选为true
        self.__seriesselectioncasesensitive = ''
        # 取样器正则表达式, 默认为空，勾选，不勾选为false
        self.__seriesselectionregexp = ''
        # 图标题
        self.__graphtitle = ''
        # 描边宽度， 默认为3.0f   0 1.0f   1 1.5f    2 2.0f    3 2.5f    5 3.5f 以此类推最终到6.5f对应的值为11
        self.__linestrockwidth = ''
        # 形状  默认空为原型    1 菱形    2 正方形    3 三角形    4 空
        self.__lineshapepoint = ''
        # 动态图形大小，默认为空，勾选状态
        self.__graphsizedynamic = ''
        # 非动态图标的宽和高，配合动态图形大小为false时使用
        self.__graphsizewidth = ''
        self.__graphsizeheight = ''
        # 时间格式 默认为空的时候是 HH:mm:ss
        self.__xaxistimeformat = ''
        # Y轴最大值
        self.__yaxisscalemaxvalue = ''
        # Y轴增量比例
        self.__yaxisscaleincrement = ''
        # Y轴显示号码分组，默认勾选为空，取消勾选为false
        self.__yaxisnumbergrouping = ''
        # 图例位置 默认为空，对应底部位置  1 右    2 左    3 顶部
        self.__legendplacement = ''
        # 图例字体 默认为空，对应无衬线体    1 衬线体
        self.__legendfont = ''
        # 图例字体尺寸 默认为空，对应尺寸为10  下标【0，1，2，3，4，5，6，7，8，9，10.11】对应尺寸为【8，9，10，11，12，14，16，18，20，24，28，32】
        self.__legendsize = ''
        # 图例字体样式 默认为空，对应样式普通， 1 粗体    2 斜体
        self.__legendstyle = ''
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

    def set_name(self, name):
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

    def get_interval(self):
        return self.__interval

    def set_interval(self, interval):
        self.__interval = interval

    def get_seriesselection(self):
        return self.__seriesselection

    def set_seriesselection(self, seriesselection):
        self.__seriesselection = seriesselection

    def get_seriesselection_match_label(self):
        return self.seriesselection_match_label

    def set_seriesselection_match_label(self, seriesselection_match_label):
        self.__seriesselection_match_label = seriesselection_match_label

    def get_seriesselectioncasesensitive(self):
        return self.__seriesselectioncasesensitive

    def set_seriesselectioncasesensitive(self, seriesselectioncasesensitive):
        self.__seriesselectioncasesensitive = seriesselectioncasesensitive

    def get_seriesselectionregexp(self):
        return self.__seriesselectionregexp

    def set_seriesselectionregexp(self, seriesselectionregexp):
        self.__seriesselectionregexp = seriesselectionregexp

    def get_graphtitle(self):
        return self.__graphtitle

    def set_graphtitle(self, graphtitle):
        self.__graphtitle = graphtitle

    def get_linestrockwidth(self):
        return self.__linestrockwidth

    def set_linestrockwidth(self, linestrockwidth):
        self.linestrockwidth = linestrockwidth

    def get_lineshapepoint(self):
        return self.__lineshapepoint

    def set_lineshapepoint(self, lineshapepoint):
        self.__lineshapepoint = lineshapepoint

    def get_graphsizedynamic(self):
        return self.__graphsizedynamic

    def set_graphsizedynamic(self, graphsizedynamic):
        self.__graphsizedynamic = graphsizedynamic

    def get_graphsizewidth(self):
        return self.__graphsizewidth

    def set_graphsizewidth(self, graphsizewidth):
        self.__graphsizewidth = graphsizewidth

    def get_graphsizeheight(self):
        return self.__graphsizeheight

    def set_graphsizeheight(self, graphsizeheight):
        self.graphsizeheight = graphsizeheight

    def get_xaxistimeformat(self):
        return self.__xaxistimeformat

    def set_xaxistimeformat(self, xaxistimeformat):
        self.__xaxistimeformat = xaxistimeformat

    def get_yaxisscalemaxvalue(self):
        return self.__yaxisscalemaxvalue

    def set_yaxisscalemaxvalue(self, yaxisscalemaxvalue):
        self.__yaxisscalemaxvalue = yaxisscalemaxvalue

    def get_yaxisnumbergrouping(self):
        return self.__yaxisnumbergrouping

    def set_yaxisnumbergrouping(self, yaxisnumbergrouping):
        self.__yaxisnumbergrouping = yaxisnumbergrouping

    def get_legendplacement(self):
        return self.__legendplacement

    def set_legendplacement(self, legendplacement):
        self.__legendplacement = legendplacement

    def get_legendfont(self):
        return self.__legendfont

    def set_legendfont(self, legendfont):
        self.__legendfont = legendfont

    def get_legendsize(self):
        return self.__legendsize

    def set_legendsize(self, legendsize):
        self.__legendsize = legendsize

    def get_legendstyle(self):
        return self.__legendstyle

    def set_legendstyle(self, legendstyle):
        self.__legendstyle = legendstyle

    def items(self):
        dicts = {
            'error_logging': self.__error_logging,
            'success_only_logging': self.__success_only_logging,
            'filename': self.__filename,
            'interval': self.__interval,
            'seriesselection': self.__seriesselection,
            'seriesselection_match_label': self.__seriesselection_match_label,
            'seriesselectioncasesensitive': self.__seriesselectioncasesensitive,
            'seriesselectionregexp': self.__seriesselectionregexp,
            'graphtitle': self.__graphtitle,
            'linestrockwidth': self.__linestrockwidth,
            'lineshapepoint': self.__lineshapepoint,
            'graphsizedynamic': self.__graphsizedynamic,
            'graphsizewidth': self.__graphsizewidth,
            'graphsizeheight': self.__graphsizeheight,
            'xaxistimeformat': self.__xaxistimeformat,
            'yaxisscalemaxvalue': self.__yaxisscalemaxvalue,
            'yaxisnumbergrouping': self.__yaxisnumbergrouping,
            'yaxisscaleincrement': self.__yaxisscaleincrement,
            'legendplacement': self.__legendplacement,
            'legendfont': self.__legendfont,
            'legendsize': self.__legendsize,
            'legendstyle': self.__legendstyle

        }
        return dicts

    def get(self, parent):
        prop_map = {
            'error_logging': General.add_bool_prop,
            'success_only_logging': General.add_bool_prop,
            'filename': General.add_str_prop,
            'interval': General.add_str_prop,
            'seriesselection': General.add_bool_prop,
            'seriesselection_match_label': General.add_str_prop,
            'seriesselectioncasesensitive': General.add_bool_prop,
            'seriesselectionregexp': General.add_bool_prop,
            'graphtitle': General.add_str_prop,
            'linestrockwidth': General.add_int_prop,
            'lineshapepoint': General.add_int_prop,
            'graphsizedynamic': General.add_bool_prop,
            'graphsizewidth': General.add_str_prop,
            'graphsizeheight': General.add_str_prop,
            'xaxistimeformat': General.add_str_prop,
            'yaxisscalemaxvalue': General.add_str_prop,
            'yaxisnumbergrouping': General.add_bool_prop,
            'yaxisscaleincrement': General.add_str_prop,
            'legendplacement': General.add_int_prop,
            'legendfont': General.add_int_prop,
            'legendsize': General.add_int_prop,
            'legendstyle': General.add_int_prop
        }

        keys_map = {
            'error_logging': 'ResultCollector.error_logging',
            'success_only_logging': 'ResultCollector.success_only_logging',
            'filename': 'filename',
            'interval': 'RespTimeGraph.interval',
            'seriesselection': 'RespTimeGraph.seriesselection',
            'seriesselection_match_label': 'RespTimeGraph.seriesselectionmatchlabel',
            'seriesselectioncasesensitive': 'RespTimeGraph.seriesselectioncasesensitive',
            'seriesselectionregexp': 'RespTimeGraph.seriesselectionregexp',
            'graphtitle': 'RespTimeGraph.graphtitle',
            'linestrockwidth': 'RespTimeGraph.linestrockwidth',
            'lineshapepoint': 'RespTimeGraph.lineshapepoint',
            'graphsizedynamic': 'RespTimeGraph.graphsizedynamic',
            'graphsizewidth': 'RespTimeGraph.graphsizewidth',
            'graphsizeheight': 'RespTimeGraph.graphsizeheight',
            'xaxistimeformat': 'RespTimeGraph.xaxistimeformat',
            'yaxisscalemaxvalue': 'RespTimeGraph.yaxisscalemaxvalue',
            'yaxisnumbergrouping': 'RespTimeGraph.yaxisnumbergrouping',
            'yaxisscaleincrement': 'RespTimeGraph.yaxisscaleincrement',
            'legendplacement': 'RespTimeGraph.legendplacement',
            'legendfont': 'RespTimeGraph.legendfont',
            'legendsize': 'RespTimeGraph.legendsize',
            'legendstyle': 'RespTimeGraph.legendstyle'
        }

        resp_time_graph_visualizer_prop = ET.SubElement(parent, 'ResultCollector')
        resp_time_graph_visualizer_prop.set('guiclass', 'RespTimeGraphVisualizer')
        resp_time_graph_visualizer_prop.set('testclass', 'ResultCollector')
        resp_time_graph_visualizer_prop.set('testname', self.__name)

        for key, value in self.items().items():
            if key in prop_map:
                # prop_map[key](self, resp_time_graph_visualizer_prop, keys_map[key], str(value))
                if value == '' or value == 'false':
                    pass
                else:
                    prop_map[key](self, resp_time_graph_visualizer_prop, keys_map[key], str(value))
        obj_prop = ET.SubElement(resp_time_graph_visualizer_prop, 'objProp')
        config_name_prop = ET.SubElement(obj_prop, 'name')
        config_name_prop.text = 'saveConfig'
        value_prop = ET.SubElement(obj_prop, 'value')
        value_prop.set('class', 'SampleSaveConfiguration')
        for key, value in self.__sample_save_config.items():
            props = ET.SubElement(value_prop, key)
            props.text = str(value)
        hashtree = ET.SubElement(parent, 'hashTree')
        return resp_time_graph_visualizer_prop
