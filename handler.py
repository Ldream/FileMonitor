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
