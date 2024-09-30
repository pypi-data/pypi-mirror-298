from files3.f3utils import *
import lz4.frame as lzf
import pickletools
import pickle
import sys
import os
import io

# 目标文件不是F3Inst文件的错误
class NotF3InstError(Exception): ...

# 目标文件丢失源代码文件路径的错误
class LostSourceCodeError(Exception): ...

class _F3Unpickler(pickle._Unpickler):
    @memoize
    def find_class(self, __module_name: str, __global_name: str):
        """
        Find the class by the module name and the global name
        :param __module_name: like __main__
        :param __global_name: like MyClass
        :return:
        """
        # Try to get the target file path
        try:
            if self.rlinkpath:
                tar_file = self.rlinkpath
            elif len(self.metastack) > 1:
                tar_file = self.metastack[1][0]
            else:
                tar_file = self.stack[0]
            tar_file = os.path.abspath(tar_file)
        except:
            raise NotF3InstError(f"Can not get scp. # Meta = {self.metastack}, Stack = {self.stack}")

        # Get the directory of the target file
        tar_dir = os.path.dirname(tar_file)

        # If the module name is '__main__', do the following
        if __module_name == '__main__':
            # Check if the target file exists
            if not os.path.exists(tar_file):
                raise LostSourceCodeError(f"Can not find target source code file (not exist). # target file = {tar_file}")

            # Get the base name of the target file and remove the extension
            tar_name = os.path.basename(tar_file)
            tar_name, _ = os.path.splitext(tar_name)

            # Check if it's an init file
            if tar_name == "__init__":
                tar_name = os.path.basename(tar_dir)
                tar_dir = os.path.dirname(tar_dir)
                if not tar_name:
                    raise ValueError("Source code file:__init__.py file at a disk root.")

            # Set the module name to the base name of the target file
            __module_name = tar_name

        # Add the target directory to the system path
        sys.path.append(tar_dir)

        # Find and return the class
        kclass = super(_F3Unpickler, self).find_class(__module_name, __global_name)

        # Remove the target directory from the system path
        sys.path.pop(-1)

        return kclass

    def load(self, relink_path:str=None):
        self.rlinkpath = relink_path
        scp_obj = super(_F3Unpickler, self).load()  # [scp, obj]

        try:
            scp, obj = scp_obj
        except:
            raise NotF3InstError("Can not parse scp|obj from raw. Please make sure it's created by files3 >= 0.6")

        return obj

def f3dumps(obj, relink_path:str=None):
    """
    save as [scp, obj]
    * mean if any custom class in obj. we can get it's creater code path before find_class.
    * so it help code to find the real class code.

    :param obj:
    :param scp: Source Code Path(Auto Get)
    :return:
    """
    if relink_path is not None:
        scp = relink_path
    else:
        scp = get_top_target_file_path()
    s = pickle.dumps([scp, obj])
    s = pickletools.optimize(s)
    return lzf.compress(s)

def f3loads(s, *, fix_imports=True, encoding="ASCII", errors="strict",
           buffers=None, relink_path=None):
    """

    :param s:
    :param fix_imports:
    :param encoding:
    :param errors:
    :param buffers:
    :param relink_path: relink path
    :return:
    """
    try:
        s = lzf.decompress(s)
    except:
        raise ValueError("Can not decompress bytes data. Please make sure it's created by files3 >= 0.6")
    if isinstance(s, str):
        raise TypeError("Can't load pickle from unicode string")
    file = io.BytesIO(s)
    return _F3Unpickler(file, fix_imports=fix_imports, buffers=buffers,
                      encoding=encoding, errors=errors).load(relink_path)
