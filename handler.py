from FileMonitor import created, start


@created(r'py', once=True)
def pys(src_path):
    pass
    # print(pys.__re_path__)
    print(pys.__method__)
    # print("test:", src_path)


@start(r'.*py', once=True, )
def sl(src_path):
    print("sl:", src_path)

    @created(src_path, once=True, escape=True)
    def fk(src_path):
        print("fk:", src_path)

    sl.__app__.register_callback(fk)
