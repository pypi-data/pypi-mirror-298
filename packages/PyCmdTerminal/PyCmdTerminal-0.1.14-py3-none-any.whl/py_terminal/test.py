import time

from py_terminal import LocalTerminal
from py_terminal.RemoteTerminal import RemoteTerminal

if __name__ == '__main__':
    def call(out, err):
        print("Calling1", out, err.decode())


    def call2(out, err):
        print("Calling2", [out], [err])


    with LocalTerminal() as l:
        print(l.get_subprocess_pids(29000))
    #     p = l.async_execute_command("python3 /mnt/c/Users/BX3MDyy/WorkSpaces/Code/MY/python_terminal/test.py")
    #     print(p)
    #     l.get_sync_process_output(p[0], call, wait=False)
    #     time.sleep(10)
    #
    #     l.kill(p)
    #     print("==================")
    # print("______________")

    # with RemoteTerminal('10.22.0.44',
    #                     username="temp",
    #                     password="Aa53142!",
    #                     port=22
    #                     ) as ssh_client:
    #     pass
        # print(ssh_client.write(r"/home/user/Test/cp_pack.hh", "dadaad".encode('utf-8'), mode="wb"))
        # print(ssh_client.list_dir("/home/temp"))
        # print(ssh_client.makedirs("/home/user/test/dong", exist_ok=True))
        # for  i in ssh_client.read(r"/home/user/Test/cp_pack.sh", mode="r", chunk_size=1):
        #     print(i)
        # 推送文件
        # print(ssh_client.push(f"/mnt/c/Users/BX3MDyy/WorkSpaces/Code/new_filback/t2.py", "/home/user"))
        # 推送目录
        # print(ssh_client.push(f"/mnt/c/Users/BX3MDyy/WorkSpaces/Code/new_filback/test", "/home/user"))
        # 拉文件
        # ssh_client.pull("/home/user/docker.sh", "./")
        # 删除
        # print(ssh_client.delete("/home/user/test"))
        # 杀死进程
        # print(ssh_client.kill('my_custom_proce'))
        # 杀死找到的所有PID
        # print(ssh_client.kill("my_custom_proce", kill_all=True))
        # 读取文件
        # print(ssh_client.read(r"/home/user/t2.py"))
        # 异步执行命令
        # p = ssh_client.async_execute_command("/user_data/temp/BolePack-2.1_linux_2024-0426/bolepack.sh -fillback /user_data/temp/auto_package/auto_package-develop/project/fillback/pc2/config/fill_back.json")
        # print(p)
        # ssh_client.get_sync_process_output(p[0], call, wait=False)
        # time.sleep(15)
        #
        # ssh_client.kill(p)

        # print(ssh_client.read("/user_data/temp/auto_package/auto_package-develop/project/fillback/pc2/config/fill_back.json"))
#         data = """{}"""
        # print(ssh_client.write("/user_data/temp/auto_package/auto_package-develop/project/fillback/pc2/config/fill_back.json", data=data, mode="w"))
        # print(ssh_client.get_subprocess_pids(p))
        # 通过PID获取异步执行命令的输出
        # t1 = ssh_client.get_sync_process_output(p, call)
        # t2 = ssh_client.get_sync_process_output(p, call2, wait=False)
        # time.sleep(2)
        # t1.stop()
        # t2.stop()
        # print(ssh_client.kill(p))

        # for i in ssh_client.read(r"/home/user/t3.py", chunk_size=20):
        #     print(i)
        # ssh_client.open_sftp()
        # print(ssh_client.delete(r"/home/user/t2.py"))

        # print(ssh_client.execute_command("sudo ls /home/user"))
        # print(ssh_client.get_os())
        # print(ssh_client.pid_exists(1017986))
        # print(ssh_client.get_pname_by_pid(1017986))
        # print(ssh_client.get_pids_by_pname('kworker/18:0-mm_percpu_wq'))
        # print(ssh_client.command_exists("ls"))
