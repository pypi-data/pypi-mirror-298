import mimetypes
import xml.etree.ElementTree as ET
from jmetertools.core.base import General


class __JMeterHttpSampler:
    def __init__(self):
        # 名称
        self.__http_sampler_name = 'http请求'
        # 注释
        self.__comments = ''
        # 服务器名称或IP
        self.__domain = ''
        # 端口
        self.__port = ''
        # 协议
        self.__protocol = ''
        # 内容编码
        self.__contentEncoding = ''
        # 路径
        self.__path = ''
        # 请求方法
        self.__method = 'GET'
        # 跟随重定向
        self.__follow_redirects = 'true'
        # 使用KeepAlive
        self.__use_keepalive = 'true'
        # 自动重定向
        self.__auto_redirects = 'false'
        # 对POST使用multipart/form-data
        self.__DO_MULTIPART_POST = 'false'
        # 与浏览器兼容的头
        self.__BROWSER_COMPATIBLE_MULTIPART = 'false'
        # 消息体数据
        self.__postBodyRaw = {}
        # 参数
        self.__params = {}
        # 文件
        self.__files = {}

    def get_http_sampler_name(self):
        return self.__http_sampler_name

    def set_http_sampler_name(self, http_sampler_name):
        self.__http_sampler_name = http_sampler_name

    def get_comments(self):
        return self.__comments

    def set_comments(self, comments):
        self.__comments = comments

    def get_domain(self):
        return self.__domain

    def set_domain(self, domain):
        self.__domain = domain

    def get_port(self):
        return self.__port

    def set_port(self, port):
        self.__port = port

    def get_protocol(self):
        return self.__protocol

    def set_protocol(self, protocol):
        self.__protocol = protocol

    def get_contentEncoding(self):
        return self.__contentEncoding

    def set_contentEncoding(self, contentEncoding):
        self.__contentEncoding = contentEncoding

    def get_path(self):
        return self.__path

    def set_path(self, path):
        self.__path = path

    def get_method(self):
        return self.__method

    def set_method(self, method):
        self.__method = method

    def get_follow_redirects(self):
        return self.__follow_redirects

    def set_follow_redirects(self, follow_redirects):
        self.__follow_redirects = follow_redirects

    def get_use_keepalive(self):
        return self.__use_keepalive

    def set_use_keepalive(self, use_keepalive):
        self.__use_keepalive = use_keepalive

    def get_auto_redirects(self):
        return self.__auto_redirects

    def set_auto_redirects(self, auto_redirects):
        self.__auto_redirects = auto_redirects

    def get_DO_MULTIPART_POST(self):
        return self.__DO_MULTIPART_POST

    def set_DO_MULTIPART_POST(self, DO_MULTIPART_POST):
        self.__DO_MULTIPART_POST = DO_MULTIPART_POST

    def get_BROWSER_COMPATIBLE_MULTIPART(self):
        return self.__BROWSER_COMPATIBLE_MULTIPART

    def set_BROWSER_COMPATIBLE_MULTIPART(self, BROWSER_COMPATIBLE_MULTIPART):
        self.__BROWSER_COMPATIBLE_MULTIPART = BROWSER_COMPATIBLE_MULTIPART

    def get_postBodyRaw(self):
        return self.__postBodyRaw

    def set_postBodyRaw(self, postBodyRaw):
        self.__postBodyRaw = postBodyRaw

    def get_params(self):
        return self.__params

    def set_params(self, params):
        self.__params = params

    def get_files(self):
        return self.__files

    def set_files(self, files):
        self.__files = files

    def items(self) -> dict:
        dicts = {
            'comments': self.__comments,
            'domain': self.__domain,
            'port': self.__port,
            'protocol': self.__protocol,
            'contentEncoding': self.__contentEncoding,
            'path': self.__path,
            'follow_redirects': self.__follow_redirects,
            'method': self.__method,
            'use_keepalive': self.__use_keepalive,
            'auto_redirects': self.__auto_redirects,
            'DO_MULTIPART_POST': self.__DO_MULTIPART_POST,
            'BROWSER_COMPATIBLE_MULTIPART': self.__BROWSER_COMPATIBLE_MULTIPART,
            'postBodyRaw': self.__postBodyRaw,
            'params': self.__params,
            'files': self.__files
        }
        return dicts

    def add_arguments(self, parent, value):
        bool_prop = ET.SubElement(parent, 'boolProp')
        bool_prop.set('name', 'HTTPSampler.postBodyRaw')
        bool_prop.text = 'true'
        element_prop = ET.SubElement(parent, 'elementProp')
        element_prop.set('name', 'HTTPsampler.Arguments')
        element_prop.set('elementType', 'Arguments')
        collection_prop = ET.SubElement(element_prop, 'collectionProp')
        collection_prop.set('name', 'Arguments.arguments')
        body_prop = ET.SubElement(collection_prop, 'elementProp')
        body_prop.set('name', '')
        body_prop.set('elementType', 'HTTPArgument')
        encode_prop = ET.SubElement(body_prop, 'boolProp')
        encode_prop.set('name', 'HTTPArgument.always_encode')
        encode_prop.text = 'false'
        bodys = ET.SubElement(body_prop, 'stringProp')
        bodys.set('name', 'Argument.value')
        bodys.text = str(value).replace('\'', '\"')
        metadata_prop = ET.SubElement(body_prop, 'stringProp')
        metadata_prop.set('name', 'Argument.metadata')
        metadata_prop.text = '='

    def add_params(self, parent, values):
        bool_prop = ET.SubElement(parent, 'boolProp')
        bool_prop.set('name', 'HTTPSampler.postBodyRaw')
        bool_prop.text = 'false'
        element_prop = ET.SubElement(parent, 'elementProp')
        element_prop.set('name', 'HTTPsampler.Arguments')
        element_prop.set('elementType', 'Arguments')
        collection_prop = ET.SubElement(element_prop, 'collectionProp')
        collection_prop.set('name', 'Arguments.arguments')
        for key, value in values.items():
            body_prop = ET.SubElement(collection_prop, 'elementProp')
            body_prop.set('name', key)
            body_prop.set('elementType', 'HTTPArgument')
            General.add_bool_prop(self, body_prop, 'HTTPArgument.always_encode', 'false')
            General.add_str_prop(self, body_prop, 'Argument.value', str(value))
            General.add_str_prop(self, body_prop, 'Argument.metadata', '=')
            General.add_bool_prop(self, body_prop, 'HTTPArgument.use_equals', 'true')
            General.add_str_prop(self, body_prop, 'Argument.name', key)

    def add_files(self, parent, values):
        bool_prop = ET.SubElement(parent, 'boolProp')
        bool_prop.set('name', 'HTTPSampler.postBodyRaw')
        if self.__postBodyRaw:
            bool_prop.text = 'true'
        else:
            bool_prop.text = 'false'
        element_prop = ET.SubElement(parent, 'elementProp')
        element_prop.set('name', 'HTTPsampler.Files')
        element_prop.set('elementType', 'HTTPFileArgs')
        collection_prop = ET.SubElement(element_prop, 'collectionProp')
        collection_prop.set('name', 'HTTPFileArgs.files')
        for key, value in values.items():
            body_prop = ET.SubElement(collection_prop, 'elementProp')
            body_prop.set('name', str(value))
            body_prop.set('elementType', 'HTTPFileArg')
            General.add_str_prop(self, body_prop, 'File.path', str(value))
            General.add_str_prop(self, body_prop, 'File.paramname', key)
            mime_type, encoding = mimetypes.guess_type(str(value))
            General.add_str_prop(self, body_prop, 'File.mimetype', mime_type)

    def get(self, parent):
        # hash_tree = ET.SubElement(parent, 'hashTree')
        http_sampler = ET.SubElement(parent, 'HTTPSamplerProxy')
        http_sampler.set('guiclass', 'HttpTestSampleGui')
        http_sampler.set('testclass', 'HTTPSamplerProxy')
        http_sampler.set('testname', self.__http_sampler_name)

        prop_map = {
            'comments': General.add_str_prop,
            'domain': General.add_str_prop,
            'port': General.add_str_prop,
            'protocol': General.add_str_prop,
            'contentEncoding': General.add_str_prop,
            'path': General.add_str_prop,
            'follow_redirects': General.add_bool_prop,
            'method': General.add_str_prop,
            'use_keepalive': General.add_bool_prop,
            'auto_redirects': General.add_bool_prop,
            'DO_MULTIPART_POST': General.add_bool_prop,
            'BROWSER_COMPATIBLE_MULTIPART': General.add_bool_prop,
        }

        keys_map = {
            'comments': 'TestPlan.comments',
            'domain': 'HTTPSampler.domain',
            'port': 'HTTPSampler.port',
            'protocol': 'HTTPSampler.protocol',
            'contentEncoding': 'HTTPSampler.contentEncoding',
            'path': 'HTTPSampler.path',
            'follow_redirects': 'HTTPSampler.follow_redirects',
            'method': 'HTTPSampler.method',
            'use_keepalive': 'HTTPSampler.use_keepalive',
            'auto_redirects': 'HTTPSampler.auto_redirects',
            'DO_MULTIPART_POST': 'HTTPSampler.DO_MULTIPART_POST',
            'BROWSER_COMPATIBLE_MULTIPART': 'HTTPSampler.BROWSER_COMPATIBLE_MULTIPART',
        }

        for key, value in self.items().items():
            if self.__postBodyRaw and key == 'postBodyRaw':
                self.add_arguments(http_sampler, value)
            elif self.__params and key == 'params':
                self.add_params(http_sampler, value)
            elif self.__files and key == 'files':
                self.add_files(http_sampler, value)
            elif key in prop_map:
                if value == 'false' or value == '':
                    pass
                else:
                    prop_map[key](self, http_sampler, keys_map[key], value)

        hashtree = ET.SubElement(parent, 'hashTree')
        return http_sampler
