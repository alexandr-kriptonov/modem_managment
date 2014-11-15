# -*- coding: utf-8 -*-

from yaml import load, dump
from os import access, F_OK, W_OK, R_OK
import logging
from yaml import YAMLError

try:
    from yaml import CLoader as Loader, CSafeDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# _logger printging.getLogger('spam_application').addHandler(logging.NullHandler())


class YamlObject(object):

    def __init__(self, work_with_file=None):
        super(YamlObject, self).__init__()
        self.filename = work_with_file

    def deserialize(self, _data=None):
        result = None
        if(self.filename is not None):
            if not access(self.filename, F_OK):
                print("no find file: %s!" % self.filename)
                result = None
            else:
                if access(self.filename, R_OK):
                    with open(self.filename, "r") as _file:
                        try:
                            result = load(_file, Loader=Loader)
                        except YAMLError, _error:
                            if hasattr(_error, 'problem_mark'):
                                mark = _error.problem_mark
                                print("Error position: (%s:%s)" % (mark.line+1, mark.column+1))
                            else:
                                print("Error yaml load: %s" % (str(_error)))
                else:
                    print("no access reading file: %s" % self.filename)
                    result = None
        else:
            if(_data is not None):
                try:
                    result = load(_data, Loader=Loader)
                except YAMLError, _error:
                    if hasattr(_error, 'problem_mark'):
                        mark = _error.problem_mark
                        print("Error position: (%s:%s)" % (mark.line+1, mark.column+1))
                    else:
                        print("Error yaml load: %s" % (str(_error)))
            else:
                print("not find deserialize data!")
                result = None
        return result

    def serialize(self, _data=None):
        result = None
        if(self.filename is not None):
            if not access(self.filename, F_OK):
                print("no find file: %s, created new file!" % self.filename)
                with open(self.filename, "w+"):
                    pass
            if access(self.filename, W_OK):
                with open(self.filename, "w") as _file:
                    if(_data is None):
                        print("not find data!")
                        result = None
                    else:
                        result = dump(_data, Dumper=Dumper, allow_unicode=True, canonical=True)
                        _file.write(result)
            else:
                print("no access writing to file: %s" % self.filename)
                result = None
        else:
            if(_data is not None):
                result = dump(_data, Dumper=Dumper, allow_unicode=True, canonical=True)
            else:
                print("not find serialize data!")
                result = None
        return result


class YamlOrder(object):

    def __init__(self, serialized_order=None):
        super(YamlOrder, self).__init__()
        self.serialized_order = serialized_order

    def getOrderObj(self):
        import traceback
        from datetime import datetime
        if(self.serialized_order == ""):
            return {}
        yaml_obj = YamlObject()
        try:
            order_obj = yaml_obj.deserialize(_data=self.serialized_order)
        except Exception:
            _title_msg = 'error for order: {0}'.format(order_obj.get('order_no', False))
            _msg = traceback.format_exc()
            self._log.append({
                'title': "Deserialize order error: {0}".format(self.customer),
                'msg': '\n'.join([_title_msg, _msg]),
                'type': 'deserialize error',
                'create_date': "{:'%Y-%m-%d %H:%M:%S}".format(datetime.now())
            })
            order_obj = {}
        return order_obj
