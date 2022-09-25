"""使用Rclone批量操作文件。"""
from basic_function import *

import fire


def copy_files(source_path: str,
               destination_path: str,
               files_list: str,
               parameters: str = "--ignore-errors --cache-chunk-size 20M --drive-server-side-across-configs",
               failed_files: str = "failed_files.txt",
               error_info: str = "error_info.txt",
               debug: bool = False):
    """将源文件复制到指定路径。

    Args:
        source_path: 源文件路径。
        destination_path: 目标路径。
        files_list: 存放待复制文件列表的文本文件。
        parameters: Rclone参数。
        failed_files: 保存复制失败的源文件名的文本文件。
        error_info: 保存错误信息的文本文件。
        debug: 调试模式。

    Returns:

    """
    basic_file_operations("copy",
                          source_path,
                          destination_path,
                          files_list,
                          parameters,
                          failed_files,
                          error_info,
                          debug)


def move_files(source_path: str,
               destination_path: str,
               files_list: str,
               parameters: str = "--ignore-errors --cache-chunk-size 20M --drive-server-side-across-configs",
               failed_files: str = "failed_files.txt",
               error_info: str = "error_info.txt",
               debug: bool = False):
    """将源文件移动到指定路径。

    Args:
        source_path: 源文件路径。
        destination_path: 目标路径。
        files_list: 存放待移动文件列表的文本文件。
        parameters: Rclone参数。
        failed_files: 保存移动失败的源文件名的文本文件。
        error_info: 保存错误信息的文本文件。
        debug: 调试模式。

    Returns:

    """
    basic_file_operations("move",
                          source_path,
                          destination_path,
                          files_list,
                          parameters,
                          failed_files,
                          error_info,
                          debug)


def sync_files(source_path: str,
               destination_path: str,
               files_list: str,
               parameters: str = "--ignore-errors --cache-chunk-size 20M --drive-server-side-across-configs",
               failed_files: str = "failed_files.txt",
               error_info: str = "error_info.txt",
               debug: bool = False):
    """将源文件同步到指定路径。

    Args:
        source_path: 源文件路径。
        destination_path: 目标路径。
        files_list: 存放待同步文件列表的文本文件。
        parameters: Rclone参数。
        failed_files: 保存同步失败的源文件名的文本文件。
        error_info: 保存错误信息的文本文件。
        debug: 调试模式。

    Returns:

    """
    basic_file_operations("sync",
                          source_path,
                          destination_path,
                          files_list,
                          parameters,
                          failed_files,
                          error_info,
                          debug)


def check_files(source_path: str,
                destination_path: str,
                files_list: str,
                parameters: str = "",
                failed_files: str = "failed_files.txt",
                error_info: str = "error_info.txt",
                debug: bool = False):
    """检查源文件和目标文件是否匹配。

    Args:
        source_path: 源文件路径。
        destination_path: 目标路径。
        files_list: 存放待匹配文件列表的文本文件。
        parameters: Rclone参数。
        failed_files: 保存匹配失败的源文件名的文本文件。
        error_info: 保存错误信息的文本文件。
        debug: 调试模式。

    Returns:

    """
    basic_file_operations("check",
                          source_path,
                          destination_path,
                          files_list,
                          parameters,
                          failed_files,
                          error_info,
                          debug)


def delete_files(source_path: str,
                 files_list: str,
                 parameters: str = "",
                 failed_files: str = "failed_files.txt",
                 error_info: str = "error_info.txt",
                 debug: bool = False):
    """删除指定文件。

    Args:
        source_path: 待删除文件的路径。
        files_list: 存放待删除文件列表的文本文件。
        parameters: Rclone参数。
        failed_files: 保存删除失败的源文件名的文本文件。
        error_info: 保存错误信息的文本文件。
        debug: 调试模式。

    Returns:

    """
    basic_file_operations("del",
                          source_path,
                          "None",
                          files_list,
                          parameters,
                          failed_files,
                          error_info,
                          debug)


def list_local_files(specified_path: str,
                     debug: bool = False):
    """获取本地指定路径的文件列表。

    Args:
        specified_path: 指定路径。
        debug: 调试模式。

    Returns:

    """
    basic_list_files("ll", specified_path, debug)


def list_remote_files(specified_path: str,
                      debug: bool = False):
    """获取网盘指定路径的文件列表。

    Args:
        specified_path: 指定路径。
        debug: 调试模式。

    Returns:

    """
    basic_list_files("lr", specified_path, debug)


def compare_files(source_path: str,
                  destination_path: str,
                  debug: bool = False):
    """对比两条路径下的文件目录差异。

    Args:
        source_path: 作为对比标准的文件路径。
        destination_path: 待对比的文件路径。
        debug: 调试模式。

    Returns:

    """
    print(f"路径1：\"{source_path}\"")
    if ":" in source_path:
        list_remote_files(source_path, True) if debug else list_remote_files(source_path)
        first_directory = get_global_value()
    else:
        list_local_files(source_path, True) if debug else list_local_files(source_path)
        first_directory = get_global_value()

    print(f"路径2：\"{destination_path}\"")
    if ":" in destination_path:
        list_remote_files(destination_path, True) if debug else list_remote_files(destination_path)
        second_directory = get_global_value()
    else:
        list_local_files(destination_path, True) if debug else list_local_files(destination_path)
        second_directory = get_global_value()

    for i in second_directory:
        if i not in first_directory:
            print(f"差异点：{i}")


if __name__ == "__main__":
    fire.Fire({
        "copy": copy_files,
        "del": delete_files,
        "move": move_files,
        "sync": sync_files,
        "check": check_files,
        "ll": list_local_files,
        "lr": list_remote_files,
        "compare": compare_files,
    })
