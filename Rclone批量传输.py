# Rclone批量传输
"""
subprocess使用参考：https://www.cnblogs.com/yyds/p/7288916.html
run()函数默认不会捕获命令执行结果的正常输出和错误输出，需要获取这些内容需要传递subprocess.PIPE，
    然后可以通过返回的CompletedProcess类实例的stdout和stderr属性或捕获相应的内容；
returncode： 子进程的退出状态码。通常情况下，退出状态码为0则表示进程成功运行了；
如果run()函数被调用时指定universal_newlines=True，则该属性值是一个字符串；
"""
import subprocess
import sys


def upload_files(argv: list):
    """使用Rclone批量上传文件。

    Args:
        argv: 命令行参数列表。

    Returns:
        None
    """
    with open(argv[3]) as files:
        files_list = files.readlines()  # 包含待传输文件的列表。

    failed_count = 0  # 失败文件计数。
    file_suffix_list = [
        ".exe", ".zip", ".rar", ".7z", ".tar", ".gz",
        ".mp3", "wav", ".mp4", ".mov", ".avi", ".mpeg",
        ".txt", ".doc", ".docx", ".xls", ".xlsx", ".pdf", ".ppt",
        ".htm", ".html", ".xml", ".csv",
        ".bmp", ".jpg", ".jpeg", ".png", ".gif", ".psd",
    ]  # 常见文件后缀列表。

    while files_list:
        file = files_list.pop()
        if file == '\n':  # 跳过空行。
            continue
        file = file.rstrip('\n')  # 删除行尾换行符。
        if any(file.lower().endswith(fsl) for fsl in file_suffix_list):
            # 如果结尾包含列表中任何文件后缀，则返回True。
            # 粗略判断是否为文件而不是文件夹（传输文件需指定目标文件夹，而不能直接指定目标文件）。
            cmd0 = "rclone copy -P " + \
                   argv[1] + '/"' + file + '" ' + \
                   argv[2] + '/' + ' '.join(argv[4:])
            cmd1 = "rclone check " + \
                   argv[1] + '/"' + file + '" ' + \
                   argv[2] + '/'
        else:
            cmd0 = "rclone copy -P " + \
                   argv[1] + '/"' + file + '" ' + \
                   argv[2] + '/"' + file + '" ' + ' '.join(argv[4:])
            cmd1 = "rclone check " + \
                   argv[1] + '/"' + file + '" ' + \
                   argv[2] + '/"' + file + '" '
        print(f"{argv[1]}/{file}\t开始传输!")
        subprocess.run(cmd0, shell=True)
        cmd_exec = subprocess.run(cmd1, shell=True, universal_newlines=True, stderr=subprocess.PIPE)  # 确认文件是否上传成功。
        if cmd_exec.returncode == 0:
            with open(argv[3], "w+") as files:  # 删除文件列表内已完成的文件，便于下次续传。
                files.writelines(files_list)
            print(f"{argv[1]}/{file}\t传输成功!")
        else:
            failed_count += 1
            with open("failed_files.txt", "a") as failed:  # 存储传输失败的文件以待重试。
                failed.write(f"{argv[1]}/{file}\n")
            with open("error_info.txt", "a") as error:  # 存储传输失败的报错信息。
                error.write(cmd_exec.stderr)
            print(f"{argv[1]}/{file}\t传输失败!")

    if failed_count:
        print(f"文件传输完毕，有{failed_count}个文件传输失败!!!")
    else:
        print("文件传输完毕，全部传输成功！！！")


if __name__ == "__main__":
    upload_files(sys.argv)
