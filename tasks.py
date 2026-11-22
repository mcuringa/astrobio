from invoke import task
from pathlib import Path
import subprocess
import sys
import shutil
import tomllib
import os
import time
from urllib.error import URLError
from urllib.request import urlopen
from invoke.exceptions import Exit

VOICES = """
en_GB-alba-medium.onnx
es_AR-daniela-high.onnx
it_IT-paola-medium.onnx
""".split()


@task
def install_node(c):
    """Install and update npm dependencies for the client and server."""
    root = Path(__file__).resolve().parent
    for project in ("client", "svr"):
        for command in ("install", "update"):
            subprocess.run(["npm", command], cwd=root / project, check=True)


@task
def get_voices(c):
    """Download the en_GB-alba-medium Piper voice into svr/voices."""
    output = Path(__file__).resolve().parent / "svr" / "voices"
    output.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            sys.executable, "-m", "piper.download_voices",
            "--download-dir", str(output), "en_GB-alba-medium",
        ],
        check=True,
    )


@task
def run_all(c):
    """Build the app, start the server, and open it in Chromium."""
    root = Path(__file__).resolve().parent
    chromium = shutil.which("chromium") or shutil.which("chromium-browser")
    if chromium is None:
        raise Exit("Chromium was not found on PATH.", code=1)

    for project in ("client", "svr"):
        subprocess.run(["npm", "run", "build"], cwd=root / project, check=True)

    url = "http://127.0.0.1:3000"
    server = subprocess.Popen(["node", "dist/index.js"], cwd=root / "svr")
    try:
        deadline = time.monotonic() + 30
        while True:
            if server.poll() is not None:
                raise Exit("Node server exited during startup.", code=1)
            try:
                with urlopen(f"{url}/api/health", timeout=1) as response:
                    if response.status == 200:
                        break
            except (URLError, TimeoutError):
                pass
            if time.monotonic() >= deadline:
                raise Exit("Timed out waiting for the Node server.", code=1)
            time.sleep(0.2)

        subprocess.Popen([chromium, url])
        print(f"App running at {url}. Press Ctrl+C to stop.", flush=True)
        server.wait()
        if server.returncode:
            raise Exit(f"Node server exited with code {server.returncode}.", code=1)
    except KeyboardInterrupt:
        pass
    finally:
        if server.poll() is None:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait()


def get_config() -> dict:
    """Get the configuration from the config.toml file."""
    config_path = Path("./config.toml")
    if not config_path.exists():
        raise FileNotFoundError(f"Could not find config.toml at {config_path}")
    with config_path.open("rb") as f:
        config = tomllib.load(f)
    return config

@task
def test_voices(c):
    """Generate Piper voice samples."""
    output = Path("svr/voices/samples")
    output.mkdir(parents=True, exist_ok=True)

    for voice in VOICES:
        name = voice.split("-", 1)[1].rsplit("-", 1)[0].replace("_", " ")

        cmd = f"""python -m piper -m svr/voices/{voice} --"Hi, I'm {name}. Oxygen levels critical." """
        print(cmd)
        c.run(cmd)
        subprocess.run(cmd)

def find_circuitpy() -> Path:
    """Find the mount point for the CIRCUITPY volume."""
    candidates = []

    config = get_config()
    config_path = config.get("CIRCUITPY")
    if config_path:
        candidates.append(Path(config_path))

    # get linux paths
    user = os.environ.get("USER")
    if user:
        candidates.extend(
            [
                Path("/media") / user / "CIRCUITPY",
                Path("/run/media") / user / "CIRCUITPY",
            ]
        )
    # add macOS path
    candidates.append(Path("/Volumes/CIRCUITPY"))

    # add default Windows path
    candidates.append(Path("C:/CIRCUITPY"))

    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            print(f"CIRCUITPY mounted at {candidate}")
            return candidate

    searched = ", ".join(str(candidate) for candidate in candidates)
    print(f"Could not find CIRCUITPY volume. Searched: {searched}")
    return None

@task(name="circup")
def circ_libs(c):
    """Install CircuitPython libraries from requirements-circuitpython.txt."""

    libs = []
    with open("micro/requirements.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                libs.append(line)

    circup = shutil.which("circup")
    circuitpy_path = find_circuitpy()

    print(f"Installing CircuitPython libraries to {circuitpy_path}...")
    print(f"Libraries to install: {'\n\t'.join(libs)}")
    subprocess.run(
        [circup, "--path", str(circuitpy_path), "install", *libs],
        check=True,
    )


@task
def config_micro(c):
    """Generate config.py from config.toml for circuitpython programs."""
    def emit(data, indent=0):
        lines = []
        pad = " " * indent

        # Values first
        for key, value in data.items():
            if not isinstance(value, dict):
                lines.append(f"{pad}{key} = {value!r}")

        # Sections become namespace classes
        for key, value in data.items():
            if isinstance(value, dict):
                if lines:
                    lines.append("")
                lines.append(f"{pad}class {key}:")
                body = emit(value, indent + 4)
                lines.extend(body or [f"{pad}    pass"])

        return lines

    py_file = Path("./micro/config.py")
    config = get_config()

    output = [
        "# Generated from config.toml -- do not edit.",
        "",
        *emit(config),
        "",
    ]

    py_file.write_text("\n".join(output))


@task
def push(c, code="code.py"):
    """Copy config.toml into remote and all remote python files into CIRCUITPY."""
    print("Pushing config.toml and micro/*.py files to CIRCUITPY...")
    circuitpy_path = find_circuitpy()

    # update config to config.py
    config_micro(c)

    # copy all .py files from micro to CIRCUITPY
    for py_file in Path("micro").glob("*.py"):
        print(f"Copying {py_file} to {circuitpy_path / py_file.name}")
        shutil.copy2(py_file, circuitpy_path / py_file.name)
    # copy code to code.py
    shutil.copy2(Path("micro") / code, circuitpy_path / "code.py")

    print("Pushed micro/*.py files to CIRCUITPY.")
