import logging
import os
import stat
import subprocess
import tempfile
import threading
import time

from typing import Iterator, Optional, Union, TextIO, Any, Generator, Dict, Callable, List, Tuple, BinaryIO

import asyncio
from paramiko.ssh_exception import SSHException


class Os:
    UNKNOWN = 'UNKNOWN'
    LINUX = 'LINUX'
    WINDOWS = 'WINDOWS'
    MACOS = 'MACOS'


class AsyncThread(threading.Thread):
    def __init__(self, target=None, name=None, args=(), kwargs=None, daemon=None):
        super().__init__(target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._target = target
        self._asyncio_tasks = {}
        self._stop_events = {}
        self._task_queue = []
        self._asyncio_task_stop = False
        self.t_run = False

    def run(self):
        self.t_run = True
        asyncio.run(self._main())
        self.t_run = False

    async def _start_task(self, pid: int, _callable: Callable[[bytes, bytes], None], stop_event: asyncio.Event):
        try:
            await self._target(pid, _callable, event=stop_event)
        except asyncio.CancelledError:
            pass

    async def _wait_for_tasks(self):
        await asyncio.gather(*self._asyncio_tasks.values(), return_exceptions=True)

    def add_task(self, pid: int, _callable: Callable[[bytes, bytes], None]) -> asyncio.Event:
        stop_event = asyncio.Event()
        self._task_queue.append((pid, _callable))
        self._stop_events[pid] = stop_event
        return stop_event

    def _stop_task(self, pid: int):
        if pid in self._stop_events:
            self._stop_events[pid].set()
        if pid in self._asyncio_tasks:
            task = self._asyncio_tasks[pid]
            task.cancel()

    async def _main(self):
        while not self._asyncio_task_stop:
            if self._task_queue:
                pid, _callable = self._task_queue.pop(0)
                stop_event = self._stop_events[pid]
                task = asyncio.create_task(self._start_task(pid, _callable, stop_event))
                self._asyncio_tasks[pid] = task
            await asyncio.sleep(0.5)
        await self._wait_for_tasks()

    def stop(self):
        self._asyncio_task_stop = True
        for pid in list(self._asyncio_tasks):
            self._stop_task(pid)


class Version:
    def __init__(self, version_str):
        self.version = list(map(int, version_str.split(".")))

    def __lt__(self, other):
        return self.version < other.version

    def __le__(self, other):
        return self.version <= other.version

    def __gt__(self, other):
        return self.version > other.version

    def __ge__(self, other):
        return self.version >= other.version

    def __eq__(self, other):
        return self.version == other.version

    def __repr__(self):
        return ".".join(map(str, self.version))


class LocalSftp:
    @staticmethod
    def stat(path):
        return os.stat(path)

    @staticmethod
    def lstat(path):
        return os.lstat(path)

    @staticmethod
    def close():
        pass

    @staticmethod
    def file(filename, mode="r"):
        return open(filename, mode=mode)

    @staticmethod
    def remove(path):
        os.remove(path)

    @staticmethod
    def listdir(path):
        return os.listdir(path)

    @staticmethod
    def rmdir(path):
        os.rmdir(path)

    @staticmethod
    def readlink(path):
        return os.readlink(path)

    @staticmethod
    def mkdir(path, mode=0o777, exist_ok=False):
        try:
            os.mkdir(path, mode=mode)
        except FileExistsError:
            if not exist_ok:
                raise

    @staticmethod
    def makedirs(path, mode=0o777, exist_ok=False):
        os.makedirs(path, mode=mode, exist_ok=exist_ok)


class Popen(subprocess.Popen):

    def __init__(self, *args, **kwargs):
        stdout = kwargs.get('stdout', None)
        if stdout:
            self.output = stdout
        stderr = kwargs.get('stderr', None)
        if stderr:
            self.error = stderr

        super().__init__(*args, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_t):
        super().__exit__(exc_type, exc_val, exc_t)
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        try:
            if hasattr(self.output, 'close'):
                self.output.close()
        except (Exception,):
            pass
        try:
            if hasattr(self.error, 'close'):
                self.error.close()
        except (Exception,):
            pass


class _Terminal:
    def __init__(self, logger=logging.getLogger('Terminal'), log_level=logging.WARNING):
        self.logger = logger
        if log_level:
            self.logger.setLevel(log_level)
        self._password = None
        self._async_log: Dict[int, Any] = {}
        self._async_t = AsyncThread(self._sync_process_std)
        self._open_file = set()
        self.system = None

    def execute_command(self, command: str, timeout: Optional[int] = None, password: Optional[str] = None) -> dict:
        result = {
            'stdout': '',
            'stderr': '',
            'exit_status': None
        }
        _, stdout, stderr = self._exec_command(command, timeout=timeout)
        if "password" in stderr.lower() or "interactive authentication required" in stderr.lower():
            if not password:
                password = self._password
            if password:
                command_with_sudo = f"echo {password} | sudo -S {command.replace('sudo', '')}"
                _, stdout, stderr = self._exec_command(command_with_sudo, timeout=timeout)

        result['stdout'] = stdout
        result['stderr'] = stderr
        result['exit_status'] = _.returncode

        return result

    def async_execute_command(self, command: str) -> List[int]:
        out_temp = tempfile.NamedTemporaryFile()
        err_temp = tempfile.NamedTemporaryFile()
        out_temp.write(command.encode('utf'))
        self._open_file.add(out_temp)
        self._open_file.add(err_temp)
        if command.startswith("python"):
            if command.startswith("python3"):
                command = command.replace("python3", "python3 -u")
            elif command.startswith("python"):
                command = command.replace("python", "python -u")
        process = Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=out_temp,
            stderr=err_temp,
            preexec_fn=os.setsid
        )

        sub_process = self.get_subprocess_pids(process.pid)
        sub_process.append(process.pid)
        for sub in sub_process:
            self._async_log[sub] = process
        return sub_process

    def get_sync_process_output(self, pid: int, callable_f: Callable[[bytes, bytes], None] = print, wait: bool = True) -> Union[Tuple[AsyncThread, asyncio.Event], None]:
        if wait:
            asyncio.run(self._sync_process_std(pid, callable_f))
            return
        if not self._async_t.t_run:
            self._async_t = AsyncThread(self._sync_process_std)
            self._async_t.start()
        task = self._async_t.add_task(pid, callable_f)
        return self._async_t, task

    def read(self, path: str, mode="r", decode="utf-8", chunk_size: int = -1, position: int = 0) -> Union[Iterator[Any], str, Generator[str, Any, Any]]:
        valid_modes = ['r', 'rb', 'r+', 'rb+']
        if mode not in valid_modes:
            raise IOError(f"Invalid mode: {mode}. Valid modes are {', '.join(valid_modes)}.")
        sftp = self.open_sftp()
        if not self.is_file(path, sftp):
            raise FileNotFoundError('%s is not a file.' % path)
        if not self.path_exists(path, sftp):
            self.logger.error('Path %s does not exist' % path)
            raise FileExistsError('Path not found: %s' % path)
        file_size = self.get_size(path, sftp)
        if chunk_size > -1 and file_size < position:
            return iter([])

        file_buf = sftp.file(path, mode)
        if chunk_size == -1:
            try:
                file_buf.seek(position)
                data = file_buf.read()
                file_buf.close()
                if 'b' not in mode and isinstance(data, bytes):
                    return data.decode(decode)
                return data
            except (SSHException, EOFError, IOError) as e:
                self.logger.error(f'Error while reading file: {path}, error: {str(e)}')
                raise IOError(f'Error while reading file: {path}') from e

        def iterator():
            nonlocal position
            remaining_data = b''
            while True:
                try:
                    file_buf.seek(position)
                    chunk = file_buf.read(chunk_size)
                    if not chunk:
                        file_buf.close()
                        break
                    position += len(chunk)
                    if 'b' not in mode and isinstance(chunk, bytes):
                        try:
                            chunk = remaining_data + chunk
                            yield chunk.decode(decode)
                            remaining_data = b''
                        except UnicodeDecodeError as ud_e:
                            remaining_data = chunk[ud_e.start:]
                            yield chunk[:ud_e.start].decode(decode)
                    else:
                        yield chunk
                except (SSHException, EOFError, IOError) as ioE:
                    file_buf.close()
                    self.logger.error('error while reading file: %s' % str(ioE))
                    raise IOError('error while reading file: %s' % path) from ioE
            try:
                file_buf.close()
            except (Exception,):
                pass

        return iterator()

    def write(self, path: str, data: Union[str, bytes], mode: str = 'w') -> None:
        if 'x' in mode and self.path_exists(path):
            self.logger.error(f'File already exists: {path}')
            raise FileExistsError(f'File already exists: {path}')

        valid_modes = ['w', 'wb', 'a', 'ab', 'x', 'xb']
        if mode not in valid_modes:
            raise IOError(f"Invalid mode: {mode}. Valid modes are {', '.join(valid_modes)}.")
        try:
            sftp = self.open_sftp()
            with sftp.file(path, mode) as file_buf:
                if isinstance(data, str) and 'b' not in mode:
                    file_buf.write(data)
                elif isinstance(data, bytes) and 'b' in mode:
                    file_buf.write(data)
                else:
                    raise TypeError(f"Data type does not match mode: {mode}. Use 'b' in mode for binary data.")
        except Exception as e:
            self.logger.error(f'Error writing to file: {path}, mode: {mode}, error: {str(e)}')
            raise IOError(f'Unable to write to file: {path}') from e

    def delete(self, path: str) -> bool:
        try:
            sftp = self.open_sftp()
            if not self.path_exists(path, sftp):
                self.logger.error(f'Path does not exist: {path}')
                raise FileNotFoundError(f"File or directory '{path}' does not exist.")
            if self.is_file(path, sftp):
                sftp.remove(path)
            elif self.is_dir(path, sftp):
                self._d_dir(path, sftp)
            else:
                self.logger.error(f'Path is neither a file nor a directory: {path}')
                raise FileNotFoundError(f"Path '{path}' is neither a file nor a directory.")
            return True
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Failed to delete file or directory: {e}")
            raise RuntimeError(f"Failed to delete '{path}'.") from e

    def move(self, source_path: str, dest_path: str) -> bool:

        if not self.path_exists(source_path):
            raise FileNotFoundError(f"File or directory '{source_path}' does not exist.")

        os_type = self.get_os()

        if os_type == Os.WINDOWS:
            command = f'move "{source_path}" "{dest_path}"'
        elif os_type == Os.LINUX or os_type == Os.MACOS:
            command = f'mv "{source_path}" "{dest_path}"'
        else:
            raise NotImplementedError(f"Unsupported operating system: {os_type}")

        result = self.execute_command(command)
        if result['exit_status'] == 0:
            return True
        elif result["stderr"]:
            raise Exception(f"Error occurred during move: {result['stderr']}")
        else:
            return False

    def copy(self, source_path: str, dest_path: str) -> bool:
        if not self.path_exists(source_path):
            raise FileNotFoundError(f"File or directory '{source_path}' does not exist.")
        if not self.path_exists(dest_path):
            raise FileNotFoundError(f"Destination directory '{dest_path}' does not exist.")
        if self.is_dir(source_path):
            dest_path = os.path.join(dest_path, os.path.basename(source_path))

        os_type = self.get_os()

        if os_type == Os.WINDOWS:
            command = f'xcopy "{source_path}" "{dest_path}" /E /I /Y'
        elif os_type == Os.LINUX or os_type == Os.MACOS:
            command = f'cp -r "{source_path}" "{dest_path}"'
        else:
            raise NotImplementedError(f"Unsupported operating system: {os_type}")

        result = self.execute_command(command)
        if result['exit_status'] == 0:
            return True
        elif result["stderr"]:
            raise Exception(f"Error occurred during copy: {result['stderr']}")
        else:
            return False

    def open_file(self, path: str, mode: str = 'r') -> Union[BinaryIO, TextIO]:
        valid_modes = ['r', 'w', 'x', 'a', 'b', 't', 'r+', 'w+', 'x+', 'a+', 'rb', 'wb', 'ab', 'rt', 'wt', 'xt', 'at']
        if mode not in valid_modes:
            raise IOError(f"Invalid mode: {mode}. Valid modes are {', '.join(valid_modes)}.")

        try:
            sftp = self.open_sftp()
            file_obj = sftp.file(path, mode=mode)
            self._open_file.add(file_obj)
            return file_obj
        except Exception as e:
            self.logger.error(f'Error opening file: {path}, mode: {mode}, error: {str(e)}')
            raise IOError(f'Unable to open file: {path}') from e

    def get_size(self, path: str, sftp=None) -> int:
        if sftp is None:
            sftp = self.open_sftp()
        if not self.path_exists(path, sftp):
            raise FileNotFoundError('Path not found: %s' % path)

        def _get_size(p):
            total_size = 0
            if self.is_link(p, sftp):
                if not self.path_exists(p, sftp):
                    resolved_path = sftp.readlink(p)
                    self.logger.warning('Broken symlink detected at %s -> %s' % (p, resolved_path))
                    return 0
            if not self.path_exists(p, sftp):
                self.logger.warning(f"Path does not exist")
                return 0
            if self.is_file(p, sftp):
                return sftp.stat(p).st_size
            elif self.is_dir(p, sftp):
                for dir_path, _, filenames in os.walk(p, topdown=True, followlinks=True):
                    for f in filenames:
                        fp = str(os.path.join(dir_path, f))
                        if self.is_link(fp, sftp) and not self.path_exists(fp, sftp):
                            resolved_path = sftp.readlink(fp)
                            self.logger.warning('Broken symlink detected at %s -> %s' % (fp, resolved_path))
                            continue
                        total_size += _get_size(fp)

            return total_size

        return _get_size(path)

    def list_dir(self, path: str, sftp=None) -> List[str]:
        if sftp is None:
            sftp = self.open_sftp()
        if not self.path_exists(path, sftp):
            raise FileNotFoundError('Path not found: %s' % path)
        return sftp.listdir(path)

    def mkdir(self, path: str, mode=0o777, exist_ok=False, sftp=None):
        if sftp is None:
            sftp = self.open_sftp()
        try:
            sftp.mkdir(path, mode, exist_ok)
            self.logger.info(f'Directory created: {path}')
        except Exception as e:
            self.logger.error(f'Error creating directory: {path}, error: {str(e)}')
            raise RuntimeError(f'Unable to create directory: {path}') from e

    def makedirs(self, path: str, mode=0o777, exist_ok=False, sftp=None):
        if sftp is None:
            sftp = self.open_sftp()
        try:
            sftp.makedirs(path, mode=mode, exist_ok=exist_ok)
        except Exception as e:
            self.logger.error(f'Error creating directory: {path}, error: {str(e)}')
            raise RuntimeError(f'Unable to create directory: {path}') from e

    def is_dir(self, path: str, sftp=None) -> bool:
        return stat.S_ISDIR(self._stat(path, sftp).st_mode)

    def is_file(self, path: str, sftp=None) -> bool:
        return stat.S_ISREG(self._stat(path, sftp).st_mode)

    def is_link(self, path: str, sftp=None) -> bool:
        return stat.S_ISLNK(self._lstat(path, sftp).st_mode)

    def path_exists(self, path: str, sftp=None) -> bool:
        try:
            return bool(self._stat(path, sftp))
        except FileNotFoundError:
            return False

    def pid_exists(self, pid: int) -> bool:
        os_type = self.get_os()
        if os_type == Os.LINUX or os_type == Os.MACOS:
            command = f"ps -p {pid}" if self.command_exists("ps") else f"test -d /proc/{pid}"
            _, result, _ = self._exec_command(command)
            return str(pid) in result
        elif os_type == Os.WINDOWS:
            command = f'tasklist /FI "PID eq {pid}"'
            _, result, _ = self._exec_command(command)
            return str(pid) in result
        else:
            return False

    def process_exists(self, identifier: Union[str, int]) -> bool:
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            pid = int(identifier)
            return self.pid_exists(pid)
        elif isinstance(identifier, str):
            return bool(self.get_pids_by_pname(identifier))
        else:
            return False

    def get_subprocess_pids(self, pid: int) -> List[int]:
        os_type = self.get_os()
        all_pids = []

        if os_type == Os.LINUX or os_type == Os.MACOS:
            command = f'ps --ppid {pid} -o pid --no-headers'
            _, result, _ = self._exec_command(command)
            child_pids = [int(pid) for pid in result.splitlines() if pid.strip()]
            all_pids.extend(child_pids)

            for child_pid in child_pids:
                all_pids.extend(self.get_subprocess_pids(child_pid))

        elif os_type == Os.WINDOWS:
            command = f'tasklist /FI "ParentProcessId eq {pid}"'
            _, result, _ = self._exec_command(command)
            lines = result.splitlines()
            child_pids = []
            for line in lines:
                if str(pid) in line:
                    child_pids.append(int(line.split()[1]))
            all_pids.extend(child_pids)

            for child_pid in child_pids:
                all_pids.extend(self.get_subprocess_pids(child_pid))

        return all_pids

    def get_pname_by_pid(self, pid: int) -> Optional[str]:
        os_type = self.get_os()
        if os_type == Os.LINUX or os_type == Os.MACOS:
            command = f'ps -p {pid} -o comm'
            _, result, _ = self._exec_command(command)
            return result.strip()
        elif os_type == Os.WINDOWS:
            command = f'tasklist /FI "PID eq {pid}"'
            _, result, _ = self._exec_command(command)
            lines = result.splitlines()
            for line in lines:
                if str(pid) in line:
                    return line.split()[0]
            return None
        else:
            return None

    def get_pids_by_pname(self, pname: str) -> List[int]:
        os_type = self.get_os()
        if os_type == Os.LINUX or os_type == Os.MACOS:
            command = f'pgrep -x {pname}' if self.command_exists('pgrep') else f"ps -e -o comm,pid | grep {pname} | grep -v grep | awk '{{print $2}}'"
            _, result, _ = self._exec_command(command)
            return [int(pid) for pid in result.splitlines() if pid.strip()]
        elif os_type == Os.WINDOWS:
            command = f'tasklist /FI "IMAGENAME eq {pname}"'
            _, result, _ = self._exec_command(command)
            lines = result.splitlines()
            pids = []
            for line in lines:
                if pname in line:
                    pid = int(line.split()[1])
                    pids.append(pid)
            return pids
        else:
            return []

    def kill(self, process_identifier: Optional[Union[int, str, List[Union[int, str]]]], force: bool = False, timeout: int = 5, kill_all: bool = False) -> bool:
        pid = None
        if isinstance(process_identifier, int):
            pid = process_identifier
        elif isinstance(process_identifier, List):
            for identifier in process_identifier:
                try:
                    self.kill(identifier, force=force, timeout=timeout, kill_all=kill_all)
                except Exception as e:
                    self.logger.error(f"Error killing process with PID {identifier}: {str(e)}")
            return True
        elif isinstance(process_identifier, str) and process_identifier.isdigit():
            pid = int(process_identifier)
        elif isinstance(process_identifier, str):
            pids = self.get_pids_by_pname(process_identifier)
            if pids is None:
                return True
            if len(pids) > 1:
                if kill_all:
                    for pid in pids:
                        try:
                            self._kill_by_pid(pid, force, timeout)
                        except Exception as e:
                            self.logger.error(f"Error killing process with PID {pid}: {str(e)}")
                    return True
                else:
                    self.logger.error(f"Multiple PIDs found for process name '{process_identifier}': {pids}.")
                    raise RuntimeError(f"Multiple processes found with name '{process_identifier}': {pids}")
            else:
                pid = pids[0]
        else:
            self.logger.error(f"Invalid process identifier. Must be either an integer PID or a string process name. INPUT 'process_identifier' : '{process_identifier}'")
            raise RuntimeError(f"Invalid process identifier. Must be either an integer PID or a string process name. INPUT 'process_identifier' : '{process_identifier}'")
        if pid is not None:
            return self._kill_by_pid(pid, force, timeout)

    def command_exists(self, cmd: str) -> bool:
        check_command = f"command -v {cmd} || which {cmd}"
        if self.get_os() == Os.WINDOWS:
            check_command = f"Powershell -Command Get-Command {cmd}"
        result = self.execute_command(check_command)
        return bool(result['exit_status'] == 0 and result['stdout'])

    def get_os(self) -> str:
        if self.system:
            return self.system
        _, result, _ = self._exec_command('ver')
        result = result.lower()
        if 'microsoft' in result or 'windows' in result:
            self.system = Os.WINDOWS
        _, result, _ = self._exec_command('uname')
        result = result.lower()
        if 'linux' in result:
            self.system = Os.LINUX
        _, result, _ = self._exec_command('sw_vers')
        result = result.lower()
        if 'productName' in result and 'productVersion' in result:
            self.system = Os.MACOS
        return self.system

    async def _sync_process_std(self, pid: int, _callable: Callable[[bytes, bytes], None] = print, *, event: asyncio.Event = None):
        if pid not in self._async_log:
            raise ValueError(f"No {pid} was found for asynchronous execution")
        process: Popen = self._async_log[pid]
        stdout = process.output
        stderr = process.error
        stdout_position = 0
        stderr_position = 0

        while True:
            if (event and event.is_set()) or process.poll() is not None:
                break

            stdout_data, stderr_data = b"", b""
            try:
                if stdout and not stdout.closed:
                    stdout.seek(stdout_position)
                    stdout_data = stdout.read()
                    if stdout_data:
                        stdout_position = stdout.tell()
                if stderr and not stderr.closed:
                    stderr.seek(stderr_position)
                    stderr_data = stderr.read()
                    if stderr_data:
                        stderr_position = stderr.tell()

            except (IOError, ValueError) as e:
                self.logger.error(f"Error reading {pid} process output: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error while reading {pid} process output: {e}")
                raise

            if stdout_data or stderr_data:
                _callable(stdout_data, stderr_data)

            await asyncio.sleep(0.001)

    @staticmethod
    def _exec_command(command, timeout=None):
        result = subprocess.run(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        return result, result.stdout, result.stderr

    def _kill_by_pid(self, pid: int, force: bool, timeout: int = 1) -> bool:
        time_step = 0.5
        if not self.pid_exists(pid):
            return True
        os_type = self.get_os()
        if os_type == Os.LINUX or os_type == Os.MACOS:
            sigterm_command = f"kill -15 {pid}"
            result = self.execute_command(sigterm_command)
            if result['exit_status'] == 0:
                while timeout > 0:
                    if not self.pid_exists(pid):
                        return True
                    timeout -= time_step
                    time.sleep(time_step)
                if force:
                    sigkill_command = f"kill -9 {pid}"
                    result = self.execute_command(sigkill_command)
                    if result['exit_status'] == 0:
                        return True
                    raise RuntimeError(f"Failed to send SIGTERM to process with PID {pid}   ERROR: {result['stderr']}")
                else:
                    TimeoutError(f"Kill program timeout {pid}")
            else:
                raise RuntimeError(f"Failed to send SIGTERM to process with PID {pid}   ERROR: {result['stderr']}")
        elif os_type == Os.WINDOWS:
            command = "taskkill /PID {pid} /F"
            result = self.execute_command(command.format(pid=pid))
            if result['exit_status'] == 0:
                return True
            else:
                raise RuntimeError(f"Failed to terminate process with PID {pid}   ERROR: {result['stderr']}")

    @staticmethod
    def open_sftp():
        return LocalSftp()

    def _stat(self, path: str, sftp=None):
        try:
            if sftp is None:
                sftp = self.open_sftp()
            return sftp.stat(path)
        except FileNotFoundError:
            raise FileNotFoundError(f'Path not found: {path}')
        except Exception as e:
            raise IOError(f'Error retrieving status for path: {path}, error: {str(e)}') from e

    def _lstat(self, path: str, sftp=None):
        try:
            if sftp is None:
                sftp = self.open_sftp()
            return sftp.lstat(path)
        except FileNotFoundError:
            self.logger.error(f'Path not found: {path}')
            raise FileNotFoundError(f'Path not found: {path}')
        except Exception as e:
            self.logger.error(f'Error retrieving status for path: {path}, error: {str(e)}')
            raise IOError(f'Error retrieving status for path: {path}, error: {str(e)}') from e

    def _d_dir(self, path, sftp=None):
        if sftp is None:
            sftp = self.open_sftp()
        for item in sftp.listdir(path):
            remote_item = os.path.join(path, item)
            if self.is_file(remote_item, sftp):
                sftp.remove(remote_item)
            elif self.is_dir(remote_item, sftp):
                self._d_dir(remote_item, sftp)
        sftp.rmdir(path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self._async_t.t_run:
            self._async_t.stop()
            self._async_t.join()
        while self._open_file:
            try:
                self._open_file.pop().close()
            except (Exception,):
                pass

    def __del__(self):
        self.close()
