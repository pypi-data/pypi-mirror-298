import time

from py_terminal.RemoteTerminal import RemoteTerminal
from py_terminal.LocalTerminal import LocalTerminal

if __name__ == '__main__':
    def call(out, err):
        print("Calling1", [out], [err])


    def call2(out, err):
        print("Calling2", [out], [err])


    # with LocalTerminal() as lt:
    #     pid = lt.async_execute_command(r"/home/ubuntu2204/anaconda3/envs/aidi_fillback/bin/python /mnt/c/Users/BX3MDyy/WorkSpaces/Code/MY/python_terminal/test.py")
    #     lt.get_sync_process_output(pid, wait=False)
    #     while True:
    #         print(lt.get_async_process_status(pid))
    #         time.sleep(0.5)

    with RemoteTerminal('10.22.0.71',
                        username="user",
                        password="1234",
                        port=22
                        ) as ssh_client:
        pids = ssh_client.async_execute_command("python3 /home/user/test/test.py")
        print(pids)
        ssh_client.get_sync_process_output(pids, wait=False)
        while True:

            code = ssh_client.get_async_process_status(pids)
            print(code)
            if code == 0:
                break
            time.sleep(0.5)
