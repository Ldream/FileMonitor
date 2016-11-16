import logging
import os

from FileMonitor import start_watch, create_engine, add_routers

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    # filename='/tmp/test.log',
    # filemode='w')
    app = create_engine()
    add_routers(app, "handler")
    watch_path = os.path.join(os.path.abspath('.'), 'monitor')
    start_watch(app, watch_path)
