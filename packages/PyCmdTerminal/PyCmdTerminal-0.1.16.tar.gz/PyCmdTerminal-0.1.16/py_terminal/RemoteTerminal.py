import asyncio
import os
import time
from multiprocessing import AuthenticationError

import paramiko
from paramiko import SSHClient, WarningPolicy, SFTPClient
from paramiko.auth_handler import AuthHandler as ParamsHandler
from paramiko.ssh_exception import BadAuthenticationType, AuthenticationException, SSHException
from paramiko.common import cMSG_SERVICE_REQUEST
from paramiko.message import Message
from paramiko.transport import Transport as _Transport
from typing import Optional, Union, List, Callable, Mapping, Tuple
import threading
import getpass
import logging
from ._base import _Terminal, Version, Os
from .exception import SSHCommandExecutionError


class AuthHandler(ParamsHandler):
    """
    Custom authentication handler to handle SSH authentication requests.
    """

    def request_auth(self):
        """
        Send an authentication request message to the SSH server.
        """
        m = Message()
        m.add_byte(cMSG_SERVICE_REQUEST)
        m.add_string("terminal-userauth")
        self.transport.send_message(m)


class Transport(_Transport):
    """
    Custom Transport class to override send_message and handle custom authentication handlers.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_message(self, data):
        """
        Send a message through the SSH transport.

        Args:
            data: The message data to send.
        """
        self.packetizer.send_message(data)

    def get_auth_handler(self) -> AuthHandler:
        """
        Get the current authentication handler.

        Returns:
            AuthHandler: The authentication handler.
        """
        return self.auth_handler

    def set_auth_handler(self, handler: AuthHandler):
        """
        Set the authentication handler.

        Args:
            handler (AuthHandler): The authentication handler to set.
        """
        self.auth_handler = handler


class RemoteTerminal(SSHClient, _Terminal):
    """
    A wrapper class for SSHClient from the Paramiko library to simplify SSH connections.

    Attributes:
        host (Optional[str]): The hostname or IP address of the SSH server.
        username (Optional[str]): The username to use for authentication.
        port (int): The port number for the SSH connection (default is 22).
        use_terminal_input_password (bool): Whether to allow terminal input for passwords.
        terminal_password_show (bool): Whether to show the password while typing in the terminal.
        timeout (int): The timeout for the SSH connection in seconds.
        allow_agent (bool): Whether to allow the use of SSH agents.
        look_for_keys (bool): Whether to search for discoverable private key files.
        key_filename (Optional[Union[str, List[str]]]): The filename, or list of filenames, of the private key(s).
        host_key_policy (Optional[Type[HostKeyPolicy]]): Custom host key policy (default is `WarningPolicy`).
        known_hosts_file (Optional[str]): Path to known hosts file for host key validation.
    """

    def __init__(self,
                 host: Optional[str],
                 username: Optional[str],
                 password: Union[str, None] = None,
                 port: int = 22,
                 try_retry_password: bool = False,
                 try_retry_password_times: int = 3,
                 use_terminal_input_password: bool = False,
                 terminal_password_show: bool = False,
                 timeout: int = 10,
                 allow_agent: bool = True,
                 look_for_keys: bool = True,
                 key_filename: Optional[Union[str, List[str]]] = None,
                 host_key_policy: Optional = WarningPolicy(),
                 known_hosts_file: Optional[str] = None,
                 logger=logging.getLogger('RemoteTerminal'),
                 log_level=None):
        _Terminal.__init__(self, logger=logger, log_level=log_level)
        self._transport: Optional[Transport] = None
        SSHClient.__init__(self)

        self.host: Optional[str] = host
        self.username: Optional[str] = username
        self.port: int = port
        self.use_terminal_input_password: bool = use_terminal_input_password
        self.terminal_password_show: bool = terminal_password_show
        self.timeout: int = timeout
        self.allow_agent: bool = allow_agent
        self.look_for_keys: bool = look_for_keys
        self.key_filename: Optional[Union[str, List[str]]] = key_filename
        self.host_key_policy = host_key_policy
        self.known_hosts_file = known_hosts_file
        self.state = False

        self._password: Union[str, None] = password
        self._try_retry_password: bool = try_retry_password
        self._try_retry_password_times: int = try_retry_password_times
        self._handler: Optional[AuthHandler] = None

        self.set_missing_host_key_policy(self.host_key_policy)
        if self.known_hosts_file:
            self.load_system_host_keys(self.known_hosts_file)
        self._connect()

    def check_connect(self) -> bool:
        try:
            transport = self.get_transport()
            if transport is not None and transport.is_active():
                _, stdout, _ = self._exec_command("echo test", timeout=0.5)
                if "test" in stdout:
                    return True
            return False
        except (EOFError, SSHException) as e:
            self.logger.error(f"Network check failed: {e}")
        return False

    def reconnect(self, timeout: int = 100) -> bool:
        try:
            for _ in range(10):
                if self.check_connect():
                    time.sleep(0.5)
                    timeout -= 0.5
                else:
                    self.state = False
            if not self.state:
                self._reconnection(timeout)
                self.state = self.check_connect()
        except Exception:
            raise
        return self.state

    def push(self, local_path: str, remote_path: str) -> bool:
        sftp = None
        success = False
        try:
            sftp = self.open_sftp()

            if self.path_exists(remote_path, sftp):
                if self.is_dir(remote_path, sftp):
                    remote_path = os.path.join(remote_path, os.path.basename(local_path))
            else:
                parent_dir = os.path.dirname(remote_path)
                if not self.path_exists(parent_dir, sftp):
                    raise FileNotFoundError(f"Parent directory '{parent_dir}' does not exist.")

            if os.path.isfile(local_path):
                sftp.put(local_path, remote_path)
                self._set_remote_file_metadata(sftp, local_path, remote_path)
            elif os.path.isdir(local_path):
                self._push_directory(sftp, local_path, remote_path)
            else:
                raise FileNotFoundError(f"Local path '{local_path}' is neither a file nor a directory.")

            self.logger.info(f"File or directory {local_path} uploaded to {remote_path}.")
            success = True

        except FileNotFoundError as fnf_error:
            self.logger.error(f"File or directory not found: {fnf_error}")
            raise FileNotFoundError(f"Failed to upload '{local_path}' to '{remote_path}'.") from fnf_error
        except PermissionError as perm_error:
            self.logger.error(f"Permission error: {perm_error}")
            raise PermissionError(f"Failed to upload '{local_path}' to '{remote_path}'.") from perm_error
        except IOError as io_error:
            self.logger.error(f"I/O error occurred: {io_error}")
            raise IOError(f"Failed to upload '{local_path}' to '{remote_path}'.") from io_error
        except Exception as e:
            self.logger.error(f"Failed to upload file or directory: {e}")
            raise RuntimeError(f"Failed to upload '{local_path}' to '{remote_path}'.") from e
        finally:
            if sftp:
                try:
                    sftp.close()
                except Exception as close_error:
                    self.logger.error(f"Failed to close SFTP connection: {close_error}")

        return success

    def pull(self, remote_path: str, local_path: str) -> bool:
        sftp = None
        success = False
        try:
            if os.path.exists(local_path):
                if os.path.isdir(local_path):
                    local_path = os.path.join(local_path, os.path.basename(remote_path))
            else:
                parent_dir = os.path.dirname(local_path)
                if not os.path.exists(parent_dir):
                    raise FileNotFoundError(f"Parent directory '{parent_dir}' does not exist.")

            sftp = self.open_sftp()

            if self.is_file(remote_path, sftp):
                sftp.get(remote_path, local_path)
                self._set_local_file_metadata(sftp, remote_path, local_path)
            elif self.is_dir(remote_path, sftp):
                self._pull_directory(sftp, remote_path, local_path)
            else:
                raise FileNotFoundError(f"Remote path '{remote_path}' is neither a file nor a directory.")
            self.logger.info(f"File or directory '{remote_path}' downloaded to '{local_path}'.")
            success = True

        except FileNotFoundError as fnf_error:
            self.logger.error(f"File or directory not found: {fnf_error}")
            raise FileNotFoundError(f"Failed to download '{remote_path}' to '{local_path}'.") from fnf_error
        except PermissionError as perm_error:
            self.logger.error(f"Permission error: {perm_error}")
            raise PermissionError(f"Failed to download '{remote_path}' to '{local_path}'.") from perm_error
        except IOError as io_error:
            self.logger.error(f"I/O error occurred: {io_error}")
            raise IOError(f"Failed to download '{remote_path}' to '{local_path}'.") from io_error
        except Exception as e:
            self.logger.error(f"Failed to download file or directory: {e}")
            raise RuntimeError(f"Failed to download '{remote_path}' to '{local_path}'.") from e
        finally:
            if sftp:
                try:
                    sftp.close()
                except Exception as close_error:
                    self.logger.error(f"Failed to close SFTP connection: {close_error}")
        return success

    def async_execute_command(self, command: str) -> Tuple[int, ...]:
        if self.get_os() == Os.WINDOWS:
            raise RuntimeError(f"Windows does not support asynchronous execution")

        if command.startswith("python"):
            if command.startswith("python3"):
                command = command.replace("python3", "python3 -u")
            elif command.startswith("python2"):
                command = command.replace("python2", "python2 -u")
            elif command.startswith("python"):
                command = command.replace("python", "python -u")
        stdbuf = ""
        if self.command_exists("stdbuf"):
            stdbuf = "stdbuf -o0 -e0 "
        elif self.command_exists("unbuffer"):
            stdbuf = "unbuffer "
        sh = ''
        if self.command_exists('bash'):
            sh = "bash -c "
        elif self.command_exists('sh'):
            sh = "sh -c "
        ns = time.time_ns()
        out_tmp = f"/tmp/SSHCLIECT_out_{ns}_XXXXXX"
        err_tmp = f"/tmp/SSHCLIECT_err_{ns}_XXXXXX"
        status_tmp = f"/tmp/SSHCLIECT_status_{ns}_XXXXXX"
        full_command = f"setsid {stdbuf}{sh}'{command} 1> {out_tmp} 2> {err_tmp} && echo $? > {status_tmp} || echo $? > {status_tmp}  & echo $!' && echo $!"
        try:
            _, stdout, stderr = self._exec_command(full_command, get_pty=True)
            pid = stdout.strip()

            if stderr:
                self.logger.warning(f"Command error output: {stderr}")

            if pid.isdigit():
                self.logger.info(f"Command '{command}' started in background with PID {pid}.")
                sub_process = self.get_subprocess_pids(int(pid))
                sub_process.insert(0, int(pid))
                for i in sub_process:
                    self._async_process[int(i)] = {"out": out_tmp, "err": err_tmp, "status": status_tmp}
                sub_process = tuple(sorted(sub_process))
                self._async_process[sub_process] = {"out": out_tmp, "err": err_tmp, "status": status_tmp}
                return sub_process
            else:
                self.logger.warning(f"Failed to retrieve PID for command '{command}'.")
                return tuple()

        except paramiko.SSHException as ssh_error:
            self.logger.error(f"SSH error while executing command '{command}': {ssh_error}")
            raise SSHCommandExecutionError(f"SSH error: {ssh_error}") from ssh_error

        except Exception as e:
            self.logger.error(f"Unexpected error while executing command '{command}': {e}")
            raise SSHCommandExecutionError(f"Unexpected error: {e}") from e

    def get_async_process_status(self, pid: Union[int, Tuple[int, ...]]) -> Union[int, None]:
        if pid not in self._async_process:
            raise ValueError(f"No such async process: {pid}")
        status_tmp = self._async_process[pid]['status']
        if not self.path_exists(status_tmp):
            return None
        status_data = self.read(status_tmp)
        status_code = status_data.strip().strip("\n")
        if not status_code:
            return None
        return int(status_code)

    def reboot(self, force: bool = False, wait_time: int = 10, max_retries: int = 10) -> bool:
        if wait_time < 10:
            wait_time = 10
        try:
            has_reboot = self.command_exists("reboot")
            has_shutdown = self.command_exists("shutdown")

            if has_reboot:
                reboot_command = "reboot"
            elif has_shutdown:
                reboot_command = "shutdown -r now"
            else:
                error_message = "Neither 'reboot' nor 'shutdown' is available on the remote system."
                self.logger.error(error_message)
                raise RuntimeError(error_message)

            if force:
                self.logger.warning("Force option enabled. Attempting a forceful reboot...")
                reboot_command = "reboot -f" if has_reboot else "shutdown -rf now"
            sleep_time = 5
            result = self.execute_command(reboot_command)
            time.sleep(sleep_time)
            self._async_process.clear()
            if not self.check_connect():
                self.state = False
                retry_count = 0
                _wait_time = wait_time - sleep_time
                while retry_count < max_retries:
                    try:
                        self.logger.info(f"Attempting to reconnect... (Attempt {retry_count + 1}/{max_retries})")
                        self._reconnection(_wait_time)
                        if self.check_connect():
                            self.logger.info("Reconnected to the server after reboot.")
                            return True
                    except Exception as reconnect_error:
                        self.logger.error(f"Reconnection attempt {retry_count + 1} failed: {reconnect_error}")
                    retry_count += 1
                    _wait_time = wait_time
                self.logger.error("Failed to reconnect to the server after reboot.")
                return False
            else:
                error_message = f"Failed to execute reboot command: {reboot_command}, {result['stderr']}"
                self.logger.error(error_message)
                raise RuntimeError(error_message)
        except RuntimeError as runtime_error:
            self.logger.error(f"Runtime error during reboot process: {runtime_error}")
            raise RuntimeError(f"Error during reboot: {runtime_error}") from runtime_error
        except Exception as e:
            self.logger.error(f"Unexpected error while attempting to reboot: {e}")
            raise RuntimeError(f"Unexpected error during reboot: {e}") from e

    def mkdir(self, path: str, mode=0o777, exist_ok=False, sftp=None):
        if sftp is None:
            sftp = self.open_sftp()
        if self.path_exists(path, sftp):
            if exist_ok:
                return
            self.logger.error(f'Path already exists: {path}')
            raise FileExistsError(f'Path already exists: {path}')
        try:
            sftp.mkdir(path, mode)
            self.logger.info(f'Directory created: {path}')
        except Exception as e:
            self.logger.error(f"Unexpected error while creating directory '{path}': {e}")
            raise RuntimeError(f"Unexpected error while creating directory: {e}") from e

    def makedirs(self, path: str, mode=0o777, exist_ok=False, sftp=None):
        if sftp is None:
            sftp = self.open_sftp()

        def mk(name):
            head, tail = os.path.split(name)
            if not tail:
                head, tail = os.path.split(head)
            if head and tail and not self.path_exists(head, sftp):
                try:
                    mk(head)
                except FileExistsError:
                    pass
                cdir = os.curdir
                if isinstance(tail, bytes):
                    cdir = bytes(os.curdir, 'ASCII')
                if tail == cdir:
                    return
            try:
                sftp.mkdir(name, mode)
            except IOError:
                if not exist_ok or not self.is_dir(name):
                    raise

        return mk(path)

    def get_transport(self) -> Transport:
        return self._transport

    def _exec_command(self, command: str, bufsize: int = -1, timeout: Union[float, None] = None, get_pty: Optional[bool] = False, environment: Union[Mapping[str, str], None] = None):
        stdin, stdout, stderr = self.exec_command(command, bufsize=bufsize, timeout=timeout, get_pty=get_pty, environment=environment)
        setattr(stdin, 'returncode', stdout.channel.recv_exit_status())
        if not stdin.channel.closed:
            stdin.write('\n')
            stdin.flush()
        return stdin, stdout.read().decode(), stderr.read().decode()

    def _clear_tmp_file(self):
        result = self.execute_command("rm -rf /tmp/SSHCLIECT_*_XXXXXX")
        self.logger.debug(f"Result of clearing temporary SSH key file: {result}")

    def _create_ssh_server(self):
        if self.check_connect():
            return
        try:
            if Version(paramiko.__version__) < Version("2.12.0"):
                setattr(paramiko.transport.Transport, "send_message", Transport.send_message)
                setattr(paramiko.transport.Transport, "get_auth_handler", Transport.get_auth_handler)
                setattr(paramiko.transport.Transport, "set_auth_handler", Transport.set_auth_handler)
                self.connect(hostname=self.host,
                             port=self.port,
                             username=self.username,
                             password=self._password,
                             timeout=self.timeout,
                             allow_agent=self.allow_agent,
                             look_for_keys=self.look_for_keys,
                             key_filename=self.key_filename,
                             )
            else:
                self.connect(hostname=self.host,
                             port=self.port,
                             username=self.username,
                             password=self._password,
                             timeout=self.timeout,
                             allow_agent=self.allow_agent,
                             look_for_keys=self.look_for_keys,
                             key_filename=self.key_filename,
                             transport_factory=Transport
                             )
            self._transport = self.get_transport()
            self._transport.set_keepalive(30)
            self._handler = AuthHandler(self._transport)
            self._transport.set_auth_handler(self._handler)
        except AuthenticationException as e:
            self.logger.error(f"Failed to create SSH server connection: {e}")
            raise ConnectionError(f"Failed to create SSH server connection: {e}")

    def _connect(self):
        self.state = False
        if not self.host or not self.username:
            self.logger.error("Host or username is not provided.")
            raise ValueError("Host or username is not provided.")

        self._create_ssh_server()

        if self.check_connect():
            self.logger.info("Connection successful.")
            self.state = True
            self._clear_tmp_file()
            return

        if not self._password and not self.state:
            thread_event = threading.Event()
            self._handler.auth_none(self.username, thread_event)
            try:
                self._handler.wait_for_response(thread_event)
            except BadAuthenticationType as e:
                self.logger.warning(f"Password is empty, skipping authentication. {e}")
            if self.check_connect():
                self.logger.info("Connection successful after none authentication.")
                self.state = True
                self._clear_tmp_file()
                return

        self.logger.info("Initial connection failed, retrying password authentication.")
        if self._try_retry_password and not self.state:
            for i in range(self._try_retry_password_times):
                self._password = self._get_password()
                thread_event = threading.Event()
                self._handler.auth_password(self.username, self._password, thread_event)
                try:
                    self._handler.wait_for_response(thread_event)
                    if self.check_connect():
                        self.logger.info("Connection successful after password retry.")
                        self.state = True
                        self._clear_tmp_file()
                        return
                except AuthenticationException as e:
                    self.logger.error(f"Authentication failed on attempt {i + 1}/{self._try_retry_password_times}: {e}")
                    continue
            raise AuthenticationError("Authentication failed after multiple attempts.")

    def _get_password(self, password_show: bool = False) -> str:
        if self.use_terminal_input_password:
            password_prompt_field = f"Enter password for {self.username}@{self.host}: "
            return getpass.getpass(prompt=password_prompt_field, stream=None) if not password_show else getpass.getpass(prompt=password_prompt_field)
        return self._password

    def _push_directory(self, sftp: SFTPClient, local_path: str, remote_path: str) -> None:
        try:
            sftp.mkdir(remote_path)
        except IOError:
            self.logger.warning(f"Directory {remote_path} already exists on remote server.")
        except Exception as e:
            self.logger.error(f"Failed to create directory {remote_path} on remote server: {e}")
            raise OSError(f"Failed to create directory {remote_path} on remote server: {e}")

        for item in os.listdir(local_path):
            local_item = os.path.join(local_path, item)
            remote_item = os.path.join(remote_path, item)
            if os.path.isfile(local_item):
                try:
                    sftp.put(local_item, remote_item)
                    self._set_remote_file_metadata(sftp, local_item, remote_item)
                except Exception as e:
                    self.logger.error(f"Failed to upload file {local_item}: {e}")
                    raise OSError(f"Failed to upload file {local_item}: {e}") from e
            elif os.path.isdir(local_item):
                self._push_directory(sftp, local_item, remote_item)

    def _pull_directory(self, sftp: SFTPClient, remote_path: str, local_path: str) -> None:
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        for item in sftp.listdir(remote_path):
            remote_item = os.path.join(remote_path, item)
            local_item = os.path.join(local_path, item)
            if self.is_file(remote_item, sftp):
                try:
                    sftp.get(remote_item, local_item)
                    self._set_local_file_metadata(sftp, remote_item, local_item)
                except Exception as e:
                    self.logger.error(f"Failed to download file {remote_item}: {e}")
                    raise OSError(f"Failed to download file {remote_item}: {e}")
            elif self.is_dir(remote_item, sftp):
                self._pull_directory(sftp, remote_item, local_item)

    def _set_remote_file_metadata(self, sftp: SFTPClient, local_path: str, remote_path: str) -> None:
        try:
            local_stat = os.stat(local_path)
            sftp.utime(remote_path, (local_stat.st_atime, local_stat.st_mtime))
            sftp.chmod(remote_path, local_stat.st_mode)
        except Exception as e:
            self.logger.error(f"Failed to set metadata for remote file {remote_path}: {e}")

    def _set_local_file_metadata(self, sftp: SFTPClient, remote_path: str, local_path: str) -> None:
        try:
            remote_stat = sftp.stat(remote_path)
            os.utime(local_path, (remote_stat.st_atime, remote_stat.st_mtime))
            os.chmod(local_path, remote_stat.st_mode)
        except Exception as e:
            self.logger.error(f"Failed to set metadata for local file {local_path}: {e}")

    async def _sync_process_std(self, pid: Union[int, Tuple[int, ...]], _callable: Callable[[bytes, bytes], None] = print, *, event: asyncio.Event = None):
        if pid not in self._async_process:
            raise ValueError(f"No {pid} was found for asynchronous execution")

        func = lambda: self.process_exists(pid) if isinstance(pid, int) else any(self.process_exists(p) for p in pid)

        try:
            out_log = self._async_process[pid]["out"]
            err_log = self._async_process[pid]["err"]
            out_last_position = 0
            err_last_position = 0

            while True:
                if event and event.is_set():
                    break
                out_content, err_content = b"", b""
                sftp = self.open_sftp()
                try:
                    if self.path_exists(out_log, sftp):
                        with sftp.file(out_log, 'r') as out_f:
                            out_f.seek(out_last_position)
                            out_content = out_f.read()
                            out_last_position = out_f.tell()
                    if self.path_exists(err_log, sftp):

                        with sftp.file(err_log, 'r') as err_f:
                            err_f.seek(err_last_position)
                            err_content = err_f.read()
                            err_last_position = err_f.tell()

                        if out_content or err_content:
                            _callable(out_content, err_content)
                    if not func():
                        break
                except (Exception,) as e:
                    self.logger.error(f"Error reading {pid} process output: {e}")
                    raise f"Error reading {pid} process output" from e
                finally:
                    sftp.close()
                await asyncio.sleep(0.01)

        except paramiko.SSHException as ssh_error:
            self.logger.error(f"SSH error while monitoring command output: {ssh_error}")
            raise SSHCommandExecutionError(f"SSH error: {ssh_error}") from ssh_error

        except ValueError as value_error:
            self.logger.error(f"Value error while processing PID {pid}: {value_error}")
            raise SSHCommandExecutionError(f"Value error: {value_error}") from value_error

        except Exception as e:
            self.logger.error(f"Unexpected error while monitoring command output: {e}")
            raise SSHCommandExecutionError(f"Unexpected error: {e}") from e

    def _reconnection(self, time_out: int):
        while time_out > 0:
            t = time.time()
            try:
                self._create_ssh_server()
                if self.check_connect():
                    return
            except (Exception,) as e:
                time_out -= (time.time() - t)
                if time_out < 0:
                    time_out = 0
                self.logger.warning(f"Crate service fali: {e}, Retrying. ({time_out:.2f})")
            time.sleep(0.5)
            time_out -= 0.5
        raise TimeoutError(f"Reconnection timeout")

    def close(self):
        try:
            self._clear_tmp_file()
            _Terminal.close(self)
            SSHClient.close(self)
        except (Exception,):
            pass

    def open_sftp(self) -> SFTPClient:
        try:
            return SSHClient.open_sftp(self)
        except paramiko.SSHException:
            self.logger.warning("Reconnection . . .")
            self.reconnect()
        return SSHClient.open_sftp(self)
