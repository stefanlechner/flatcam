from importlib.machinery import SourceFileLoader
import os
from abc import ABCMeta, abstractmethod
from datetime import datetime
import math

#module-root dictionary of postprocessors
import FlatCAMApp

postprocessors = {}


class ABCPostProcRegister(ABCMeta):
    #handles postprocessors registration on instantation
    def __new__(cls, clsname, bases, attrs):
        newclass = super(ABCPostProcRegister, cls).__new__(cls, clsname, bases, attrs)
        if object not in bases:
            if newclass.__name__ in postprocessors:
                FlatCAMApp.App.log.warning('Postprocessor %s has been overriden'%(newclass.__name__))
            postprocessors[newclass.__name__] = newclass()  # here is your register function
        return newclass

class FlatCAMPostProc(object, metaclass=ABCPostProcRegister):
    @abstractmethod
    def start_code(self, p):
        pass

    @abstractmethod
    def lift_code(self, p):
        pass

    @abstractmethod
    def down_code(self, p):
        pass

    @abstractmethod
    def toolchange_code(self, p):
        pass

    @abstractmethod
    def up_to_zero_code(self, p):
        pass

    @abstractmethod
    def rapid_code(self, p):
        pass

    @abstractmethod
    def linear_code(self, p):
        pass

    @abstractmethod
    def end_code(self, p):
        pass

    @abstractmethod
    def feedrate_code(self, p):
        pass

    @abstractmethod
    def spindle_code(self,p):
        pass

    @abstractmethod
    def spindle_stop_code(self,p):
        pass

def load_postprocessors(app):
    postprocessors_path_search = [os.path.join(app.data_path,'postprocessors','*.py'),
                                  os.path.join('postprocessors', '*.py')]
    import glob
    for path_search in postprocessors_path_search:
        for file in glob.glob(path_search):
            try:
                SourceFileLoader('FlatCAMPostProcessor', file).load_module()
            except Exception as e:
                app.log.error(str(e))
    return postprocessors
