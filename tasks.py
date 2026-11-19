from invoke import task
from pathlib import Path
import subprocess
import shutil
import tomllib
import os

VOICES = """
en_GB-alba-medium.onnx
es_AR-daniela-high.onnx
it_IT-paola-medium.onnx
""".split()


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
