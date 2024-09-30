#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import functools
import os.path
import pathlib
import shutil
import time

from funnylog2 import logger
from nocmd import Cmd
from nocmd import RemoteCmd

from pylinuxauto.config import config


def exclude():
    exclude_files = [
        "report",
        "__pycache__",
        ".pytest_cache",
        ".vscode",
        ".idea",
        ".git",
    ]

    exclude_str = ""
    for i in exclude_files:
        exclude_str += f"--exclude='{i}' "

    return exclude_str


def server_rootdir(project_abspath: str = None):
    path = "." if project_abspath is None else project_abspath
    return pathlib.Path(path).absolute()


def client_rootdir(project_abspath: str,user: str):
    return project_abspath.replace(config.USERNAME, user)


def transfer_to_client(user, ip, password, project_abspath):
    rsync = 'rsync -av -e "ssh -o StrictHostKeyChecking=no"'
    Cmd.run(f"rm -rf ~/.ssh/known_hosts")
    remote_cmd = RemoteCmd(user, ip, password)
    remote_cmd.remote_run(f"mkdir -p {client_rootdir(project_abspath, user)}")
    for file in ["*", ".env"]:
        Cmd.expect_run(
            f"/bin/bash -c '{rsync} {exclude()} {server_rootdir(project_abspath)}/{file} {user}@{ip}:{client_rootdir(project_abspath, user)}/'",
            events={'password': f'{password}\n'},
        )
    stdout, return_code = remote_cmd.remote_run(
        "export PATH=$PATH:$HOME/.local/bin;"
        f"cd {client_rootdir(project_abspath, user)} && youqu3 envx",
        return_code=True
    )
    logger.info(f"环境安装{'成功' if return_code == 0 else '失败'} - < {user}@{ip} >")


def start_client_service(user, ip, password, service_name, project_abspath):
    service_name = f"{service_name}.service"
    remote_cmd = RemoteCmd(user, ip, password)

    stdout, return_code = remote_cmd.remote_run(f"ls /lib/systemd/system/{service_name}", return_code=True)
    if return_code != 0:
        remote_cmd.remote_sudo_run(
            f"cp {os.path.join(client_rootdir(project_abspath, user), service_name)} /lib/systemd/system/"
        )
        remote_cmd.remote_sudo_run(f"chmod 644 /lib/systemd/system/{service_name}")
        remote_cmd.remote_sudo_run(f"systemctl daemon-reload")
        remote_cmd.remote_sudo_run(f"systemctl restart {service_name}")
        time.sleep(1)


def restart_client_service(ip, password, user, filename):
    RemoteCmd(user, ip, password).remote_sudo_run(f"sudo systemctl restart {filename}.service")
    time.sleep(1)


def gen_service_file(user, project_abspath, tmp_service_file, tmp_server_py):
    if not os.path.exists(project_abspath):
        raise FileNotFoundError(project_abspath)

    if os.path.exists(tmp_service_file) and os.path.exists(tmp_server_py):
        return

    tpl_service_file = os.path.join(config.REMOTE_PATH, "tpl.service")
    tpl_server_py = os.path.join(config.REMOTE_PATH, "server.py")

    shutil.copyfile(tpl_server_py, tmp_server_py)

    with open(tpl_service_file, "r", encoding="utf-8") as sf:
        service = sf.read()
    with open(tmp_service_file, "w", encoding="utf-8") as sf:
        sf.write(
            service.format(
                user=user,
                client_rootdir=client_rootdir(project_abspath, user),
                start_service=f"pipenv run python server.py"
            )
        )
    time.sleep(1)


def guard_rpc(service_name="remote_pylinuxauto"):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("user") or args[0]
            ip = kwargs.get("ip") or args[1]
            if not user or not ip:
                raise ValueError("user and ip are required")
            password = kwargs.get("password")
            project_abspath = kwargs.get("project_abspath")
            if project_abspath:
                project_abspath = str(project_abspath)
            auto_restart = kwargs.get("auto_restart")
            stdout, return_code = RemoteCmd(user, ip, password).remote_sudo_run(
                f"systemctl status {service_name}.service",
                return_code=True,
            )
            tmp_service_file = os.path.join(project_abspath, f"{service_name}.service")
            tmp_server_py = os.path.join(project_abspath, "server.py")
            if return_code != 0 or "running" not in stdout:
                gen_service_file(user, project_abspath, tmp_service_file, tmp_server_py)
                transfer_to_client(user, ip, password, project_abspath)
                start_client_service(user, ip, password, service_name, project_abspath)
            else:
                if os.path.exists(tmp_service_file):
                    Cmd.run(f"rm -f {tmp_service_file}")
                if os.path.exists(tmp_server_py):
                    Cmd.run(f"rm -f {tmp_server_py}")
            if auto_restart:
                restart_client_service(ip, password, user, service_name)
            res = func(*args, **kwargs)
            return res

        return wrapper

    return deco
