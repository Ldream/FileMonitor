import functools
import logging
import os
import re
import threading
import time
from functools import partial

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def log(s):
    logging.debug('[Monitor] %s' % s)


class MyFileSystemEventHandler(FileSystemEventHandler):
    def __init__(self):
        super(MyFileSystemEventHandler, self).__init__()
        self.__event_quene__ = dict()
        self['created'] = dict()
        self['deleted'] = dict()
        self['modified'] = dict()
        self['moved'] = dict()
        self['start'] = dict()

    def __getitem__(self, item):
        return self.__event_quene__.get(item, {})

    def __setitem__(self, key, value):
        self.__event_quene__[key] = value

    @staticmethod
    def dic_filter(src_path, dic):
        return filter(lambda x: x.match(src_path) is not None, dic)

    @staticmethod
    def dic_run(filter_list, dic, src_path, des_path=None):
        find_list = map(lambda find: dic[find], filter_list)
        for func_list in find_list:
            for func in func_list:
                try:
                    if des_path is None:
                        t = threading.Thread(target=func, args=(src_path,))
                    else:
                        t = threading.Thread(target=func, args=(src_path, src_path))
                    t.start()
                    if func.__once__:
                        func_list.remove(func)
                except Exception as e:
                    log('ERROR:' + str(e))

    def on_created(self, event):
        log("created: %s" % event.src_path)
        if event.is_directory:
            return
        else:
            self.do_file(self['created'], event.src_path)

    def on_deleted(self, event):
        log("deleted: %s" % event.src_path)
        if event.is_directory:
            return
        else:
            self.do_file(self['deleted'], event.src_path)

    def on_modified(self, event):
        log("modified: %s" % event.src_path)
        if event.is_directory:
            return
        else:
            self.do_file(self['modified'], event.src_path)

    def on_moved(self, event):
        log("moved: %s to %s" % (event.src_path, event.dest_path))
        if event.is_directory:
            return
        else:
            self.do_file(self['moved'], event.src_path, event.dest_path)

    def on_start(self, src_path):
        self.do_file(self['start'], src_path)

    def do_file(self, dic, src_path, dest_path=None):
        find = self.dic_filter(src_path, dic)
        self.dic_run(find, dic, src_path, dest_path)

    def add_fn(self, re_path, method, fn):
        log(("add " + method + " func: %s") % re_path)
        temp_dict = self[method]
        fn.__app__ = self
        if temp_dict.get(re_path, None):
            temp_dict[re_path].append(fn)
        else:
            temp_dict[re_path] = [fn]

    def register_callback(self, fn):
        if callable(fn):
            re_path = getattr(fn, '__re_path__', None)
            method = getattr(fn, '__method__', None)
            if re_path and method:
                self.add_fn(re_path, method, fn)

    def start_scan(self, src_path):
        l = [src_path]
        while True:
            temp_path = l.pop()
            for scan in os.scandir(temp_path):
                if scan.is_file():
                    self.on_start(os.path.join(temp_path, scan.name))
                elif scan.is_dir():
                    l.append(os.path.join(temp_path, scan.name))
            if len(l) == 0:
                break


def create_engine():
    return MyFileSystemEventHandler()


def start_watch(app, monitor_path):
    observer = Observer()
    handler = app
    observer.schedule(handler, monitor_path, recursive=True)
    app.start_scan(monitor_path)
    observer.start()
    log('Watching directory %s...' % monitor_path)
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
        print("end")
    observer.join()


def add_routers(app, module_name):
    n = module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n + 1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            re_path = getattr(fn, '__re_path__', None)
            method = getattr(fn, '__method__', None)
            if re_path and method:
                app.add_fn(re_path, method, fn)


def base_event(re_path, method, once=False, escape=False, **kw):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        if escape:
            wrapper.__re_path__ = re.compile(re.escape(re_path))
        else:
            wrapper.__re_path__ = re.compile(re_path)
        wrapper.__method__ = method
        wrapper.__callback__ = []
        wrapper.__data__ = kw
        wrapper.__once__ = once
        wrapper.__app__ = "NoSet"
        return wrapper

    return decorator


created = partial(base_event, method="created")
deleted = partial(base_event, method="deleted")
modified = partial(base_event, method="modified")
start = partial(base_event, method="start")

# if __name__ == '__main__':
#     path = os.path.abspath('.')
#     start_watch(path, None)
