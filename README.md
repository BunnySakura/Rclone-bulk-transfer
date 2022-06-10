# Rclone批量传输

*鉴于似乎并未发现Rclone提供该功能，故实现此脚本。
用于**有选择性**地将某一路径下的子文件或文件夹批量复制（copy）到指定路径，并检查（check）确认*

------------

## 使用方法

```
python3 Rclone批量传输.py <待传输文件所在目录> <目标目录> <待传输文件列表的文本文件> <传输参数>
```
- **举例**：
  ```python
  python3 Rclone批量传输.py OneDrive:/目录 GoogleDrive:/目录 files.txt --ignore-errors --cache-chunk-size 20M --drive-server-side-across-configs
  ```

- **待传输文件列表的文本文件如何获得**
  ```bash
  ls <目录> > files.txt
  ```
  
  ```bash
  rclone lsd <远程目录> | cut -b 44-99 > files.txt
  ```  
  在输出的文件中仅保留待传输文件夹或文件即可

------------

## 补充
- Rclone无法使用proxychains4。因为其由golang编写，而golang实现了自己的网络库，所以基于Linux网络库的代理无法使用。
  详见：[proxychains4 with Go lang](https://github.com/rofl0r/proxychains-ng/issues/199 "proxychains4 with Go lang")。
- 可以使用环境变量设置代理，详见：[Can I use rclone with an HTTP proxy?](https://rclone.org/faq/#can-i-use-rclone-with-an-http-proxy "Can I use rclone with an HTTP proxy?")

## 引用
[Python之系统交互（subprocess）](https://www.cnblogs.com/yyds/p/7288916.html "Python之系统交互（subprocess）")
