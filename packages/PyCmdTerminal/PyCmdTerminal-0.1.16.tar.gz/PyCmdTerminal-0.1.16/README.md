# py-terminal

## 介绍

py-terminal整合本地和远程的终端操作

# 安装

```bash
pip install PyCmdTerminal

```

## 使用

注意： 结束请使用close()方法保证打开的资源被释放以及保证正常结束当前进程，推荐使用上下文管理器(`with`)

```python
from py_terminal import LocalTerminal
from py_terminal import RemoteTerminal

with LocalTerminal() as terminal:
    terminal.get_os()

with RemoteTerminal(host="xx.xx.xx.xx", username="user") as r_terminal:
    r_terminal.get_os()

```

# 接口

## <a id="base-terminal">Class ` _Terminal`</a>

#### <a id="base-terminal-parm">参数</a>

- <h3>logger (可选)</h3>

  用于记录消息的记录器实例(默认为名为“RemoteTerminal”的记录器)。


- <h3>log_level (可选)</h3>

  日志记录级别(默认为`NOTSET`)。

#### <a id="base-terminal-method">方法</a>

- <h3>execute_command(command: `str`, timeout: `Optional[int]`, password: `Optional[str]`) -> `dict`</h3>

  执行命令，并返回有关执行的详细信息。 阻塞

  `command (必选)`：要执行的命令。
  `timeout (可选)`：命令执行的超时时间，以秒为单位(默认值为`None`)。
  `password (可选)`：用于身份验证的密码(默认为`None`)。


- <a id="base-asyncexecute-command"><h3>async_execute_command(command: `str`) -> `List[int]`</h3></a>

  执行命令而不等待它完成，并返回该命令的进程和子进程ID。 非阻塞

  `command (必选)`：要在远程服务器上执行的命令。


- <h3>get_sync_process_output(pid: `int`, _callable_f: `Callable[[bytes, bytes], None]`, wait: `bool`) -> `Union[Tuple[AsyncThread, asyncio.Event], None]`</h3>

  获取给定[异步执行](#base-asyncexecute-command)的进程的标准输出和标准错误。

  `pid (必选)`：进程的 PID，用于获取该进程的输出。

  `callable_f (可选）`：处理标准输出和标准错误的回调函数，默认使用 `print` 输出。

  `wait (可选）`：是否同步等待进程完成输出。如果为 True，则阻塞等待进程输出；如果为 False，异步执行进程的输出处理。默认为 True。


- <h3>read(path: `str`, mode:`str`, decode="utf-8", chunk_size: `int`, position: `int`) -> `Union[Iterator[Any], str, Generator[str, Any, Any]]`</h3>

  读取指定路径下的文件内容。
  该方法根据“块大小”和“模式”的值读取文件。如果' chunk_size '为-1，则读取整个文件。
  如果' chunk_size '大于-1，它将逐块读取文件内容，并返回一个迭代器以逐块读取。
  “模式”参数决定如何解释文件内容。

  `path (必选)`：要读取的文件的路径。

  `mode (可选)`：解释文件内容的模式。默认为“r”(文本模式)。使用“rb”表示二进制模式。

  `decode (可选)`：decode是用于解码文件的编码。

  `chunk_size (可选)`：要读取的每个块的大小。默认为-1，这意味着读取整个文件。如果大于-1，则按块读取。

  `position (可选)`：从文件中读取的起始位置。默认为0，这意味着从文件的开头开始。


- <h3>write(path: `str`, data: `Union[str, bytes]`, mode: `str`) -> `None`</h3>

  将数据写入指定路径的文件。

  `path (必选)`：要写入的文件的路径。

  `data (必选)`：要写入文件的数据。对于文本模式应为字符串，对于二进制模式应为字节。

  `mode (可选)`：打开文件的模式。默认为“w”(写模式)。使用“wb”表示二进制写入模式，“a”表示追加模式，依此类推。


- <h3>delete(path: `str`) -> `bool`</h3>

  删除指定路径的文件或目录。如果路径不存在，将引发“FileNotFoundError”。如果在删除过程中出现任何其他错误，将引发“RuntimeError”。

  `path (必选)`：要删除的文件或目录的路径。


- <h3>open_file(path: `str`, mode: `str`) -> `Union[BinaryIO, TextIO]`</h3>

  基于指定模式打开文件。返回文件对象

  `path (必选)`：要打开文件的路径。

  `sftp (可选)`：打开文件的模式。默认为“r”(文本模式)。 支持的模式包括“r”、“w”、“x”、“a”、“b”、“t”及其与“+”的组合。(默认为`r`)


- <h3>get_size(path: `str`, sftp) -> `int`</h3>

  获取路径的大小。如果是文件，返回文件大小； 如果是一个目录，递归计算目录中所有文件的总大小。

  `path (必选)`：文件或目录的路径。

  `sftp (可选)`：用于与服务器交互的SFTP客户端实例。


- <h3>is_dir(path: `str`, sftp) -> `bool`</h3>

  检查指定的路径是否是目录。

  `path (必选)`：要检查的文件或目录路径。

  `sftp (可选)`：用于与服务器交互的SFTP客户端实例。


- <h3>is_file(path: `str`, sftp) -> `bool`</h3>

  检查指定的路径是否是文件。

  `path (必选)`：要检查的文件或目录路径。

  `sftp (可选)`：用于与服务器交互的SFTP客户端实例。


- <h3>is_link(path: `str`, sftp) -> `bool`</h3>

  用于检查给定的路径是否是一个符号链接（symlink）

  `path (必选)`：要检查的文件或目录路径。

  `sftp (可选)`：用于与服务器交互的SFTP客户端实例。


- <h3>path_exists(path: `str`, sftp) -> `bool`</h3>

  检查指定的路径是否存在。

  `path (必选)`：要检查的文件或目录路径。

  `sftp (可选)`：用于与服务器交互的SFTP客户端实例。


- <h3>pid_exists(pid: `int`) -> `bool`</h3>

  检查指定的进程ID是否存在。

  `pid (必选)`：要检查的进程ID。


- <h3>process_exists(identifier: `Union[str, int]`) -> `bool`</h3>

  使用PID或进程名称检查是否正在运行。

  `identifier (必选)`：要检查的进程ID (PID)或进程名称。


- <h3>get_pname_by_pid(pid: `int`) -> `Optional[str]`</h3>

  检索与指定进程ID关联的进程名。

  `pid (必选)`：检索的进程ID。


- <h3>get_pids_by_pname(pname: `str`) -> `List[int]`</h3>

  检索与指定进程名称关联的所有进程id。

  `pname (必选)`：检索id的进程名称。


- <h3>kill(process_identifier: `Optional[Union[int, str, List[Union[int, str]]]]`, force: `bool`, timeout: `int`, kill_all: `bool`) -> `bool`</h3>

  通过PID或进程名称终止进程。

  `process_identifier (必选)`： 要终止的进程的PID或进程的名称或者集合。

  `force (可选)`： 如果是`True`，如果`SIGTERM`不起作用，升级到强制终止(`SIGKILL`) (默认值为`False`)。

  `timeout (可选)`： 发送SIGTERM后等待进程终止的时间(秒)(默认值为5), 超时会引发错误。

  `kill_all (可选)`： 如果为真，则终止所有与进程名匹配的进程。如果为False，则仅终止单个进程，并在发现多个PID时引发错误(默认值为False)。


- <h3>command_exists(cmd: `str`) -> `bool`</h3>

  判断给定的命令是否存在。

  `cmd (必选)`：表示要检查的命令名称（如 ls, python, git 等）。


- <h3>get_os() -> `str`</h3>

  获取机器的操作系统。


- <h3>close()</h3>

  关闭打开的资源，包括异步执行的输出线程、协程和打开的文件资源


- <h3>list_dir(self, path: `str`, sftp=None) -> `List[str]`</h3>

  返回指定目录下的所有文件和目录的名称列表。

  `path (必选)`：要列出内容的目录的路径。这个参数是可选的，默认为当前目录 (.)。


- <h3>mkdir(self, path: `str`, mode=0o777, exist_ok=False, sftp=None)</h3>

  创建单一目录

  `path (必选)`：要创建的目录的路径。可以是相对路径或绝对路径。

  `mode (可选)`：用于指定创建目录的权限，默认是 0o777。注意，该权限在某些平台上可能不起作用。

  `exist_ok (可选)`：如果设置为 True，当目标目录已经存在时不会抛出异常；如果为 False 且目录已经存在，会抛出 FileExistsError。


- <h3>makedirs(self, path: str, mode=0o777, exist_ok=False, sftp=None)</h3>

  递归创建多级目录

  `path (必选)`：要创建的目录的路径。可以是相对路径或绝对路径。

  `mode (可选)`：用于指定创建目录的权限，默认是 0o777。注意，该权限在某些平台上可能不起作用。

  `exist_ok (可选)`：如果设置为 True，当目标目录已经存在时不会抛出异常；如果为 False 且目录已经存在，会抛出 FileExistsError。


- <h3>get_subprocess_pids(pid: `int`) -> `List[int]`</h3>

  获取指定pid所有的子进程ID

  `pid (必选)`： 进程的ID。


- <h3>move(source_path: `str`, dest_path: `str`) -> `bool`</h3>

  移动文件或目录到指定的位置

  `source_path (必选)`：源路径
  `dest_path (必选)`：目标路径


- <h3>copy(source_path: `str`, dest_path: `str`) -> `bool`</h3>

  复制文件或目录到指定的位置

  `source_path (必选)`：源路径
  `dest_path (必选)`：目标路径

## Class `RemoteTerminal`

#### 介绍

继承[`paramiko.SSHClient](https://docs.paramiko.org/en/latest/api/client.html#paramiko.client.SSHClient)`和[`_Terminal(基类)`](#base-terminal)类，实现对远程设备的终端操作

#### 参数

继承[`_Terminal(基类)`](#base-terminal-parm)所有参数

- <h3>host (必选)</h3>

  SSH服务器的主机名或IP地址。


- <h3>username (必选)</h3>

  用于身份验证的用户名。


- <h3>password (可选)</h3>

  身份验证的密码(默认为空)。


- <h3>port (可选)</h3>

  SSH连接的端口号(默认为22)。


- <h3>try_retry_password (可选)</h3>

  失败时是否重试密码输入。


- <h3>try_retry_password_times (可选)</h3>

  密码输入的重试最大次数(默认值为3)。


- <h3>use_terminal_input_password (可选)</h3>

  是否允许终端输入密码(默认值为False)。


- <h3>terminal_password_show (可选)</h3>

  在终端中键入时是否显示密码(默认为False)。


- <h3>timeout (可选)</h3>

  连接远程的超时时间(秒)(默认值为10)。


- <h3>allow_agent: (可选)</h3>

  是否允许使用SSH代理(默认值为True)。


- <h3>look_for_keys (可选)</h3>

  是否搜索可发现的私钥文件(默认值为True)。


- <h3>key_filename (可选)</h3>

  私钥的文件名或文件名列表(默认为无)。


- <h3>host_key_policy (可选)</h3>

  自定义主机密钥策略(默认为“WarningPolicy”)。


- <h3>known_hosts_file (可选)</h3>

  用于主机密钥验证的已知主机文件的路径(默认为无)。

#### 方法

继承父类[`paramiko.SSHClient`](https://docs.paramiko.org/en/latest/api/client.html#paramiko.client.SSHClient)和[`_Terminal(基类)`](#base-terminal-method)所有方法

- <h3>check_connect() -> `bool`</h3>

  通过执行一个简单的命令来检查SSH连接是否处于活动状态。


- <h3>push(local_path: `str`, remote_path: `str`) -> `bool`</h3>

  将文件或目录从本地系统上传到远程服务器，包括元数据。

  `local_path (必选)`：本地文件或目录的路径。

  `remote_path (必选)`：文件或目录在远程服务器上的保存路径。


- <h3>pull(remote_path: str, local_path: str) -> `bool`</h3>

  将文件或目录从远程服务器下载到本地系统，包括元数据。

  `remote_path (必选)`：远程文件或目录的路径。

  `local_path (必选)`：本地保存文件或目录的路径。


- <h3>async_execute_command(command: `str`) -> `Optional[int]`</h3>

  在远程服务器上执行命令而不等待它完成， 并返回该命令的进程ID。[*重载基类方法*](#base-asyncexecute-command)；注意：不支持windows

  `command (必选)`：要在远程服务器上执行的命令。

- <h3>reboot(force: `bool`, wait_time: `int`, max_retries: `int`) -> `bool`</h3>

  重新启动远程服务器并等待连接。默认情况下，它会尝试使用“reboot”或“shutdown -r now”进行正常重启。

  `force (可选)`：如果为`True`，使用更强制的方法重新启动(如果可用)(默认值为`False`)。

  `wait_time (可选)`：重新启动后尝试重新连接前等待的时间(秒)(默认值为`10`)

  `max_retries (可选)`：重新启动后尝试重新连接的最大次数。(默认值为`10`)


- <h3>get_transport() -> `Transport`</h3>

  获取自定义SSH传输。


- <h3>reconnect(timeout: `str`=None) -> `bool`</h3>

  重新连接远程。

  `timeout`： 设置连接超时时间， 默认创建实例时的时长。

## Class `LocalTerminal`

#### 介绍

继承[`_Terminal(基类)`](#base-terminal)类，实现本地终端操作和基础操作

#### 参数

继承[`_Terminal(基类)`](#base-terminal-parm)所有参数

#### 方法

继承[`_Terminal(基类)`](#base-terminal-method)所有方法



