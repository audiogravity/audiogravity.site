"""Tests for dev.sh — the landing's local server and its start, stop, restart and status.

`./dev.sh restart` used to start a second server on the port the first one held — the script
took no command, and answered with Python's "Address already in use". Each test runs the real
script on a free port of its own, never the 8081 a developer may be looking at.

Run with ``python3 -m pytest scripts/test_dev_server.py``. Not in a workflow: it checks a tool
of the developer's box, not the published site.
"""

import os
import shutil
import socket
import subprocess
import urllib.request
from pathlib import Path

import pytest

DEV_SH = Path(__file__).resolve().parent.parent / "dev.sh"

pytestmark = pytest.mark.skipif(
    not (shutil.which("ss") and shutil.which("setsid")), reason="dev.sh finds its server with ss and starts it with setsid"
)


def free_port() -> int:
    """A port nothing listens on."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def port():
    """A free port for the test, and whatever dev.sh left on it stopped afterwards."""
    chosen = free_port()
    yield chosen
    dev(chosen, "stop")


def dev(port: int, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Run dev.sh with the given command on the given port."""
    env = {**os.environ, "PORT": str(port), "AG_DEV_HOST": "localhost"}
    return subprocess.run(["bash", str(DEV_SH), *args], env=env, cwd=cwd, capture_output=True, text=True, timeout=30)


def page(port: int, path: str = "/") -> int:
    """The status the server answers a page with."""
    with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=5) as answer:
        return answer.status


def listening(port: int) -> bool:
    """Whether anything accepts a connection on the port."""
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def test_start_serves_the_landing_in_the_background(port):
    started = dev(port, "start")
    assert started.returncode == 0, started.stderr
    assert "Started: http://localhost:" in started.stdout
    assert page(port) == 200
    assert page(port, "/docs/manual/03-first-run.html") == 200
    assert dev(port, "status").stdout.startswith("Running:")


def test_start_twice_keeps_the_one_server():
    port = free_port()
    try:
        dev(port, "start")
        again = dev(port, "start")
        assert again.returncode == 0
        assert again.stdout.startswith("Already running:")
        # The script run without a command — the foreground server — says so too, where Python
        # printed a traceback.
        foreground = dev(port)
        assert foreground.returncode == 0
        assert "Already running" in foreground.stdout
        assert "Traceback" not in foreground.stderr
    finally:
        dev(port, "stop")


def test_restart_replaces_the_server(port):
    dev(port, "start")
    before = dev(port, "status").stdout
    restarted = dev(port, "restart")
    assert restarted.returncode == 0, restarted.stderr
    assert "Stopped" in restarted.stdout and "Started:" in restarted.stdout
    assert page(port) == 200
    assert dev(port, "status").stdout != before  # another PID


def test_stop_frees_the_port(port):
    dev(port, "start")
    stopped = dev(port, "stop")
    assert stopped.stdout.strip() == "Stopped"
    assert not listening(port)
    assert dev(port, "status").returncode == 3
    assert dev(port, "stop").stdout.strip() == "Not running"


def test_a_server_started_in_the_foreground_is_stopped_too(port):
    # The way the server was always started — no PID file to find it by.
    foreground = subprocess.Popen(
        ["bash", str(DEV_SH)], env={**os.environ, "PORT": str(port)},
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(50):
            if listening(port):
                break
            subprocess.run(["sleep", "0.1"])
        assert dev(port, "status").stdout.startswith("Running:")
        assert dev(port, "stop").stdout.strip() == "Stopped"
        assert foreground.wait(timeout=5) is not None
    finally:
        foreground.kill()


def test_another_program_on_the_port_is_left_alone(port, tmp_path):
    other = subprocess.Popen(
        ["python3", "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=tmp_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(50):
            if listening(port):
                break
            subprocess.run(["sleep", "0.1"])
        assert "held by another program" in dev(port, "stop").stdout
        assert other.poll() is None
        refused = dev(port, "start")
        assert refused.returncode == 1
        assert "held by another program" in refused.stderr
        assert dev(port, "status").returncode == 1
    finally:
        other.kill()
        other.wait()


def test_runs_from_another_directory(port):
    # os.chdir() was given the script's path as the command line wrote it, relative to a
    # directory the script had already left: called as site/dev.sh, it served nothing.
    env = {**os.environ, "PORT": str(port), "AG_DEV_HOST": "localhost"}
    started = subprocess.run(["bash", f"{DEV_SH.parent.name}/dev.sh", "start"], env=env,
                             cwd=DEV_SH.parent.parent, capture_output=True, text=True, timeout=30)
    assert started.returncode == 0, started.stderr
    assert page(port) == 200


def test_an_unknown_command_is_refused(port):
    unknown = dev(port, "relaunch")
    assert unknown.returncode == 1
    assert "Unknown command: relaunch" in unknown.stderr
    assert not listening(port)
