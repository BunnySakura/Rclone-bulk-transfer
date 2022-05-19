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

## 引用
[Python之系统交互（subprocess）](https://www.cnblogs.com/yyds/p/7288916.html "Python之系统交互（subprocess）")
