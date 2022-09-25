import subprocess

error_code = {
    "未定义操作": -1,
    "文件操作成功": 0,
    "文件操作失败": 1,

    "文件列表获取成功": 255,
    "文件列表获取失败": 254
}

global_basic_list_files = []  # 指定路径的文件列表。


def get_global_value() -> list:
    global global_basic_list_files
    return global_basic_list_files


def basic_file_operations(option: str,
                          source_path: str,
                          destination_path: str,
                          files_list: str,
                          parameters: str,
                          failed_files: str,
                          error_info: str,
                          debug: bool) -> int:
    """基类。

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
        返回整型数据。
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
        isfile = any(file.lower().endswith(fsl) for fsl in file_suffix_list)  # 如果结尾包含列表中任何文件后缀，则返回True。

        # 根据操作生成对应命令。
        if option == "copy" or option == "move" or option == "sync":
            if isfile:
                # 粗略判断是否为文件而不是文件夹（操作文件需指定目标文件夹，而不能直接指定目标文件）。
                cmd.extend([source_path + file, destination_path] + parameters.split())
            else:
                cmd.extend([source_path + file, destination_path + file] + parameters.split())
        elif option == "del":
            # 删除文件无法使用purge。
            cmd[1] = "delete" if isfile else "purge"
            cmd.extend([source_path + file] + parameters.split())
        elif option == "check":
            cmd.extend([source_path + file, destination_path + file] + parameters.split())
        else:
            print("未定义操作！")
            return error_code.get("未定义操作")

        print(" ".join(cmd)) if debug else None
        cmd_echo = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)  # 执行命令，并以文本字符串形式捕获输出。
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
        return error_code.get("文件操作失败")
    else:
        print(f"文件{option_map[option]}完毕，全部{option_map[option]}成功。")
        return error_code.get("文件操作成功")


def basic_list_files(option: str,
                     specified_path: str,
                     debug: bool) -> int:
    """获取指定路径的文件列表。

    Args:
        option: 操作类型，ll、lr等。
        specified_path: 文件所在路径。
        debug: 调试模式。

    Returns:

    """
    # 替换文件路径分隔符为'/'，末尾添加'/'。
    specified_path.replace('\\', '/')
    if specified_path[-1] != '/':
        specified_path += '/'
    if option == "ll":
        cmd = ["ls", "-F", specified_path]
    elif option == "lr":
        cmd = ["rclone", "lsf", specified_path]
    else:
        print("未定义操作！")
        return error_code.get("未定义操作")

    print(" ".join(cmd)) if debug else None
    cmd_echo = subprocess.run(cmd, capture_output=True, text=True)  # 执行命令，并以文本字符串形式捕获输出。

    if cmd_echo.returncode == 0:
        file_list = cmd_echo.stdout
        global global_basic_list_files
        global_basic_list_files = file_list.split('\n')

        print(global_basic_list_files) if debug else None

        print(file_list)
        return error_code.get("文件列表获取成功")
    else:
        print(cmd_echo.stderr)
        return error_code.get("文件列表获取成失败")
