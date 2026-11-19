import wifi
import config
import adafruit_requests
import socketpool
import time
import ssl


def scan_networks():
    print("Scanning for networks...")
    for network in wifi.radio.start_scanning_networks():
        if network.ssid == config.wifi.ssid:
            print(
                network.ssid,
                "RSSI:", network.rssi,
                "channel:", network.channel
            )

    wifi.radio.stop_scanning_networks()


def connect_wifi(timeout=30):

    if not wifi.radio.connected:
        print("Connecting to Wi-Fi...")
        print("SSID:", config.wifi.ssid)
        print("Password:", config.wifi.password is not None and len(
            config.wifi.password) > 0)
        try:
            wifi.radio.connect(
                config.wifi.ssid,
                config.wifi.password,
                timeout=timeout,
            )
        except Exception as e:
            print("Failed to connect to Wi-Fi:", e)
            raise e
        print("Connected!")
        print("IP address:", wifi.radio.ipv4_address)


session = None


def get_requests():
    connect_wifi()
    global session
    if session is None:
        pool = socketpool.SocketPool(wifi.radio)
        session = adafruit_requests.Session(pool, ssl.create_default_context())
    return session


def debounce(f, delay):
    last_call = 0

    def wrapper(*args, **kwargs):
        nonlocal last_call
        now = time.monotonic()
        if now - last_call >= delay:
            last_call = now
            return f(*args, **kwargs)
    return wrapper


def throttle(delay):
    def decorator(f):
        last_call = 0

        def wrapper(*args, **kwargs):
            nonlocal last_call
            now = time.monotonic()

            if now - last_call >= delay:
                last_call = now
                return f(*args, **kwargs)

        return wrapper

    return decorator
