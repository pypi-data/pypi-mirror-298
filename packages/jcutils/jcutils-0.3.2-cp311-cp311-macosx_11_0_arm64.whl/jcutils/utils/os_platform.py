"""
@Time   : 2018/12/14
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import platform


def get_platform():
    """获取操作系统名称及版本号"""
    return platform.platform()


def get_system():
    """获取操作系统名称及版本号"""
    return platform.system()


if __name__ == "__main__":
    print(get_platform())
    print(get_system())
