from invoke import task
from pathlib import Path
import subprocess

VOICES = """
en_GB-alba-medium.onnx
es_AR-daniela-high.onnx
it_IT-paola-medium.onnx
""".split()


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

@task
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

@task(name="circup-libs")
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
