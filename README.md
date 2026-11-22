# astrobio

## Quickstart

Linux setup (Ubuntu/Debian commands below). Use Python 3.12 or newer and
run the project in a graphical desktop session so Chromium can open.

### 1. Install system tools and clone the project

```bash
sudo apt update
sudo apt install git curl ca-certificates tio

git clone https://github.com/mcuringa/astrobio.git
cd astrobio
```

Install Chromium for `invoke run-all`. On Ubuntu:

```bash
sudo snap install chromium
```

On Debian, use `sudo apt install chromium`. Keep running the remaining commands
from the project root.

### 2. Install Node.js and npm

Follow the [official Node.js Linux installation instructions](https://nodejs.org/en/download)
to install nvm, then install the current LTS release (npm is included):

```bash
nvm install --lts
nvm use --lts
node --version
npm --version
```

### 3. Create the Python environment with uv

Install [uv](https://docs.astral.sh/uv/getting-started/installation/):

On Ubuntu, install the [uv snap](https://snapcraft.io/astral-uv):

```bash
sudo snap install astral-uv --classic
```

For other distributions, use the uv installation instructions linked above.
Create `.venv` with Python 3.14 and install the host dependencies. The Node
server also uses `.venv/bin/python` to run Piper:

```bash
uv python install 3.14
uv venv --python 3.14 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 4. Install and update npm libraries

Install and update dependencies for both the React client and Node server:

```bash
invoke install-node
```

This runs `npm install` and `npm update` in both projects, updating libraries
within the version ranges in each `package.json`.

Updates can change the lockfiles; review and commit those changes when keeping
the updated versions.

### 5. Download the voice

```bash
invoke get-voices
```

This creates `svr/voices` if needed and downloads the `en_GB-alba-medium` model
and its configuration. Internet access is required for the download.

### 6. Run the app

From the project root with the virtual environment active:

```bash
invoke run-all
```

This builds both projects, starts the Node server, and opens Chromium at
<http://127.0.0.1:3000>. Port 3000 must be available. Press Ctrl+C in the
terminal to stop the server. In a new terminal, run `source .venv/bin/activate`
before using Invoke again.

### Optional: CircuitPython hardware

For the microcontroller, install CircuitPython on the board and connect it so
its `CIRCUITPY` drive is mounted. Review `config.toml`.

Install the board libraries:

```bash
invoke circup
```

`invoke circup` installs the board libraries from `micro/requirements.txt`.

To push a program to the board, run:

```bash
# Copy nfc.py as code.py so it runs when the board starts.
invoke push --code nfc.py
```

Use `tio` to connect to the board's serial console. Our boards do not auto-reload,
so after pushing code, press Ctrl+C to enter the REPL, then Ctrl+D to restart
the program (see the [CircuitPython REPL guide](https://learn.adafruit.com/welcome-to-circuitpython/the-repl)).

Connect to the board with:

```bash
tio /dev/ttyACM0
```

Replace `/dev/ttyACM0` with your board's serial device if needed; use
`ls /dev/ttyACM* /dev/ttyUSB*` to look for connected devices. The board should
also appear as a mounted drive named `CIRCUITPY`.
