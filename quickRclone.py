"""使用Rclone批量操作文件。"""
import subprocess
import time

import fire


def base_function(option: str,
                  source_path: str,
                  destination_path: str,
                  files_list: str,
                  parameters: str,
                  failed_files: str,
                  error_info: str,
                  debug: bool) -> int:
    """封装类似操作的基本函数。

    Args:
        option: 操作类型，move、copy、sync等。
        source_path: 源文件路径。
        destination_path: 目标路径。
        files_list: 存放待操作文件列表的文本文件。
        parameters: Rclone参数。
        failed_files: 保存操作失败的源文件名的文本文件。
        error_info: 保存错误信息的文本文件。
        debug: 调试模式。

    Returns:
        操作失败的源文件数量。未定义操作返回-1。
    """
    failed_count = 0  # 失败文件计数。
    file_suffix_list = [  # 常见文件后缀列表。
        ".exe", ".jar", ".bat",
        ".zip", ".rar", ".7z", ".tar", ".gz",
        ".mp3", "wav", ".mp4", ".mov", ".avi", ".mpeg",
        ".txt", ".doc", ".docx", ".xls", ".xlsx", ".pdf", ".ppt",
        ".htm", ".html", ".xml", ".csv",
        ".bmp", ".jpg", ".jpeg", ".png", ".gif", ".psd",
    ]
    option_map = {  # 操作映射。
        "copy": "复制",
        "move": "移动",
        "sync": "同步",
        "check": "匹配",
        "del": "删除",
    }

    with open(files_list) as files:
        _files_list = files.readlines()  # 包含待操作文件的列表。

    # 替换文件路径分隔符为'/'，末尾添加'/'。
    source_path.replace('\\', '/')
    destination_path.replace('\\', '/')
    if source_path[-1] != '/':
        source_path += '/'
    if destination_path[-1] != '/':
        destination_path += '/'

    while _files_list:
        cmd = ["rclone", option, "-P"]
        file = _files_list.pop()
        if file == '\n':  # 跳过空行。
            continue
        file = file.rstrip('\n')  # 删除行尾换行符。

        # 根据操作生成对应命令。
        if option == "copy" or option == "move" or option == "sync":
            if any(file.lower().endswith(fsl) for fsl in file_suffix_list):
                # 如果结尾包含列表中任何文件后缀，则返回True。
                # 粗略判断是否为文件而不是文件夹（操作文件需指定目标文件夹，而不能直接指定目标文件）。
                cmd.extend(['"' + source_path + file + '"', '"' + destination_path + '"', parameters])
            else:
                cmd.extend(['"' + source_path + file + '"', '"' + destination_path + file + '"', parameters])
        elif option == "del":
            # 删除文件无法使用purge。
            if any(file.lower().endswith(fsl) for fsl in file_suffix_list):
                cmd[1] = "delete"
                cmd.extend(['"' + source_path + file + '"', parameters])
            else:
                cmd[1] = "purge"
                cmd.extend(['"' + source_path + file + '"', parameters])
        elif option == "check":
            time.sleep(600)
            cmd.extend(['"' + source_path + file + '"', '"' + destination_path + file + '"', parameters])
        else:
            print("未定义操作！")
            return -1

        cmd = " ".join(cmd)  # 使用subprocess执行命令时，推荐设”shell=True“，命令以字符串形式传参。
        if debug:
            print(cmd)
        cmd_echo = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, text=True)  # 执行命令，并以文本字符串形式捕获输出。
        if cmd_echo.returncode == 0:
            with open(files_list, "w+") as files:  # 删除文件列表内已完成的文件，便于下次续传。
                files.writelines(_files_list)
            print(f"{source_path}{file}\t{option_map[option]}成功！")
        else:
            failed_count += 1
            with open(failed_files, "a") as failed:  # 保存操作失败的源文件名以待重试。
                failed.write(f"{file}\n")
            with open(error_info, "a") as error:  # 保存错误信息。
                error.write(cmd_echo.stderr)
            print(f"{source_path}{file}\t{option_map[option]}失败！")

    if failed_count:
        print(f"文件{option_map[option]}完毕，有{failed_count}个文件{option_map[option]}失败。"
              f"{option_map[option]}失败的文件信息见{failed_files}，错误输出见{error_info}")
        return failed_count
    else:
        print(f"文件{option_map[option]}完毕，全部{option_map[option]}成功。")
        return failed_count


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
        无。
    """
    base_function("copy",
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
        无。
    """
    base_function("move",
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
    """将源文件移动到指定路径。

    Args:
        source_path: 源文件路径。
        destination_path: 目标路径。
        files_list: 存放待同步文件列表的文本文件。
        parameters: Rclone参数。
        failed_files: 保存同步失败的源文件名的文本文件。
        error_info: 保存错误信息的文本文件。
        debug: 调试模式。

    Returns:
        无。
    """
    base_function("sync",
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
        无。
    """
    base_function("check",
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
        无。
    """
    base_function("del",
                  source_path,
                  "None",
                  files_list,
                  parameters,
                  failed_files,
                  error_info,
                  debug)


def list_local_files(source_path: str,
                     output_file: str,
                     debug: bool = False):
    """获取本地指定路径的文件列表。

    Args:
        source_path: 文件所在路径。
        output_file: 保存输出数据的文件名。
        debug: 调试模式。

    Returns:
        无。
    """
    # 替换文件路径分隔符为'/'，末尾添加'/'。
    source_path.replace('\\', '/')
    if source_path[-1] != '/':
        source_path += '/'
    cmd = ["ls -F", source_path, ">>", output_file]
    cmd = " ".join(cmd)  # 使用subprocess执行命令时，推荐设”shell=True“，命令以字符串形式传参。
    if debug:
        print(cmd)
    cmd_echo = subprocess.run(cmd, shell=True, capture_output=True, text=True)  # 执行命令，并以文本字符串形式捕获输出。

    if cmd_echo.returncode == 0:
        print(cmd_echo.stdout)
        print("获取成功！")
    else:
        print(cmd_echo.stderr)


def list_remote_files(source_path: str,
                      output_file: str,
                      debug: bool = False):
    """获取远程指定路径的文件列表。

    Args:
        source_path: 文件所在路径。
        output_file: 保存输出数据的文件名。
        debug: 调试模式。

    Returns:
        无。
    """
    # 替换文件路径分隔符为'/'，末尾添加'/'。
    source_path.replace('\\', '/')
    if source_path[-1] != '/':
        source_path += '/'
    cmd = ["rclone", "lsf", source_path, ">>", output_file]
    cmd = " ".join(cmd)  # 使用subprocess执行命令时，推荐设”shell=True“，命令以字符串形式传参。
    if debug:
        print(cmd)
    cmd_echo = subprocess.run(cmd, shell=True, capture_output=True, text=True)  # 执行命令，并以文本字符串形式捕获输出。

    if cmd_echo.returncode == 0:
        print(cmd_echo.stdout)
        print("获取成功！")
    else:
        print(cmd_echo.stderr)


def compare_files(source_path: str,
                  destination_path: str,
                  debug: bool = False):
    """输出两支路径下文件目录的差异。

    Args:
        source_path: 存放作为标准的文件目录的文本文件。
        destination_path: 存放待对比文件目录的文本文件。
        debug: 调试模式。

    Returns:
        无。
    """
    with open(source_path) as directory:
        first_directory = directory.readlines()
    with open(destination_path) as directory:
        second_directory = directory.readlines()
    for i in second_directory:
        if i not in first_directory:
            print(i)


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
