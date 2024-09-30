import pickle

from files3.f3utils import *
from files3.f3info import *
from files3.f3bool import *
from files3.f3io import *

class F3Core(metaclass=Singleton):
    def has(self, info: F3Info, key: str) -> F3Bool:
        """
        Has a pyfile file exists. Returns True successfully, or False if the target file doesnot exists

        :param info:     F3Info inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        """
        _path = info(key)
        if os.path.exists(_path): return F3True
        return F3False

    def set(self, info:F3Info, key: str, pyobject: object, error:bool=False, _sys_relink=None) -> F3Bool:
        """
        Set a new pyfile file. Returns True successfully

        :param info:     F3Info inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        :param pyobject: python对象   python object
        :param error:    bool Whether raise General Exception.
        """
        _path = info(key)
        try:
            s = f3dumps(pyobject, relink_path=_sys_relink)
            open(_path, "wb").write(s)
            return F3True
        except Exception as err:
            if isinstance(err, CannotSaveError) or error: raise err
            if isinstance(err, TypeError) and str(err).find("pickle 'module'") != -1:
                raise err
            if isinstance(err, AttributeError) and str(err).startswith("pickle local") != -1:
                raise err
            if isinstance(err, pickle.PickleError):
                raise err
            return F3False

    def delete(self, info:F3Info, key: str) -> F3Bool:
        """
        Delete pyfile file. Returns True if the target file is successful or does not exist. Returns False if the target file exists and cannot be deleted

        :param info:     F3Info inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        """
        _path = info(key)
        if not os.path.exists(_path): return F3True
        try:
            os.remove(_path)
            return F3True
        except:
            return F3False

    def get(self, info:F3Info, key: str, error:bool=False, _sys_relink=None) -> object:
        """
        增删改查之'查'。成功返回读取到的pyobject，如果目标文件不存在，则返回F3False
        Find data files. The read pyobject is returned successfully. If the target file does not exist, false is returned

        :param info:     F3Info inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        :param error:    bool Whether raise General Exception.
        """
        _path = info(key)
        if not os.path.exists(_path): return F3False
        try:
            s = open(_path, 'rb').read()
            return f3loads(s, relink_path=_sys_relink)
        except Exception as err:
            if isinstance(err, ModuleNotFoundError) or error: raise err
            if isinstance(err, pickle.PickleError):
                raise err
            return F3False
    
    def list(self, info:F3Info) -> list:
        """
        列举目标文件夹下所有目标类型的文件的key。返回一个列表结果
        List all info of keys (In the target folder The key of a file of type). Returns a list result
        """
        names = []
        for fnametype in os.listdir(info.path):
            if os.path.isfile(os.path.join(info.path, fnametype)):
                fname, type = os.path.splitext(fnametype)
                if type.lower() == info.type:
                    names.append(fname)

        # When yield reach return, will cause StopIteration to stop iter.
        # In general case, return the list
        return names

    def iter(self, info:F3Info):
        for fnametype in os.listdir(info.path):
            if os.path.isfile(os.path.join(info.path, fnametype)):
                fname, type = os.path.splitext(fnametype)
                if type.lower() == info.type:
                    yield fname

