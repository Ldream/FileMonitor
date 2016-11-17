#FileMonitor
![py3][py3] [English Version][english_version]

FileMonitor是一个开放的文件监控接口，目的是让开发者提高开发效率。
提供方便的接口来对发送的文件变动进行处理


## Simple uses

通过如下代码，可以初步通过Python创建对应的引擎，注册函数和注册监控路径
main.py
```python
from FileMonitor import start_watch, create_engine, add_routers
import os
app = create_engine()
add_routers(app, "handler")
watch_path = os.path.join(os.path.abspath('.'), 'monitor')
start_watch(app, watch_path)
```
handler.py
```python
import subprocess
import sys

from FileMonitor import created, start, deleted


@created(r'py', once=True)
def pys(src_path):
    pass
    # print(pys.__re_path__)
    print(pys.__method__)
    # print("test:", src_path)


@start(r'.*py', once=True, )
def sl(src_path):
    print("sl:", src_path)
    command = ['python3', src_path]
    print('Start process %s...' % ' '.join(command))
    process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

    @deleted(src_path, once=True, escape=True, process=process)
    def fk(src_path):
        print('Kill process [%s]...' % fk.__data__['process'].pid)
        fk.__data__['process'].kill()
        fk.__data__['process'].wait()
        print('Process ended with code %s.' % fk.__data__['process'].returncode)
        process = None
        print("fk:", src_path)

    sl.__app__.register_callback(fk)
```


## Comments

如果有什么问题或者建议都可以在这个[Issue][issue#1]和我讨论

[py2]: https://img.shields.io/badge/python-2.7-ff69b4.svg "python2"
[py3]: https://img.shields.io/badge/python-3.5-red.svg "python3"
[english_version]: https://github.com/littlecodersh/danmu/blob/master/README_EN.md
[document]: http://danmu.readthedocs.io/zh_CN/latest/
[screenshot]: http://7xrip4.com1.z0.glb.clouddn.com/danmu/demo.png?imageView/2/w/400/ "screenshot"
[issue#1]: https://github.com/Ldream/FileMonitor/issues/1
[gitter_picture]: https://badges.gitter.im/littlecodersh/danmu.svg "gitter"
[gitter]: https://gitter.im/littlecodersh/danmu?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge