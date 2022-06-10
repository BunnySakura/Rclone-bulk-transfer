# Rclone批量操作

*鉴于似乎并未发现Rclone提供该功能，故实现此脚本。基于Rclone实现文件的**批量**操作：同步、复制、移动、删除等等。*

------------

## 使用方法
- **安装fire库**：
  ```bash
  pip install fire
  ```

- **获取帮助**：
  ```bash
  python quickRclone.py --help
  ```
  使用`--help`参数即可获取各类指令的帮助信息。

- **举例**：
  ```bash
  python quickRclone.py sync OneDrive:/目录 GoogleDrive:/目录 files.txt '"--ignore-errors --cache-chunk-size 20M --drive-server-side-across-configs "'
  ```
  单引号包裹的字符串为Rclone接收的参数，使用单引号避免被错误解析。一般无需设置此项参数，默认值即可。

- **如何获得待操作文件列表**：
  - 获取本地路径文件列表：
    ```bash
    python quickRclone.py ll <本地路径> files.txt
    ```

  - 获取远程路径文件列表：
    ```bash
    python quickRclone.py lr <远程路径> files.txt
    ```

  在输出的文件中仅保留待操作文件即可。

## 补充
- Rclone无法使用proxychains4。因为其由golang编写，而golang实现了自己的网络库，所以基于Linux网络库的代理无法使用。
  详见：[proxychains4 with Go lang](https://github.com/rofl0r/proxychains-ng/issues/199 "proxychains4 with Go lang")。
- 可以使用环境变量设置代理，详见：[Can I use rclone with an HTTP proxy?](https://rclone.org/faq/#can-i-use-rclone-with-an-http-proxy "Can I use rclone with an HTTP proxy?")

## 引用
- [Python之系统交互（subprocess）](https://www.cnblogs.com/yyds/p/7288916.html "Python之系统交互（subprocess）")
- [Python 命令行之旅](https://github.com/HelloGitHub-Team/Article/blob/master/contents/Python/cmdline/catalog.md "Python 命令行之旅")
