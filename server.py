"""
Remote Pad server
------------------
Runs on your PC. Listens for WebSocket messages from the phone web app
(index.html) and translates them into real mouse/keyboard actions.

Install:
    pip install websockets pyautogui

Run:
    python server.py
    (starts on ws://0.0.0.0:5000/ws)

On the phone, open index.html in the browser, tap the gear icon, and set
the address to ws://<this-PC's-LAN-IP>:5000/ws, e.g. ws://192.168.1.10:5000/ws
Find your PC's LAN IP with `ipconfig` (Windows) or `ifconfig`/`ip addr` (Mac/Linux).

Notes:
- pyautogui.FAILSAFE is disabled below so the cursor can move to screen
  corners without raising an exception. Move the mouse away from a corner
  if you ever need to stop the script from the keyboard (Ctrl+C in the
  terminal always works).
- On Linux with Wayland, pyautogui/pynput cannot control the mouse/keyboard
  for security reasons. Use an X11 session, or switch this script to a
  Wayland-compatible tool (e.g. ydotool).
"""

import asyncio
import json
import logging

import pyautogui
import websockets

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0  # don't add pyautogui's default delay after every call

HOST = "0.0.0.0"
PORT = 5000

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("remote-pad")

# Carries leftover fractional pixels between move events so small,
# fast deltas don't get rounded away to nothing.
_move_accum = {"x": 0.0, "y": 0.0}

# Map the key names sent by the browser to pyautogui key names.
KEY_MAP = {
    "Escape": "esc",
    "Enter": "enter",
    "Backspace": "backspace",
    "ArrowLeft": "left",
    "ArrowRight": "right",
    "ArrowUp": "up",
    "ArrowDown": "down",
    "Control": "ctrl",
    "Alt": "alt",
    "Shift": "shift",
    " ": "space",
}


def resolve_key(key: str) -> str:
    return KEY_MAP.get(key, key)


async def handle_message(raw: str):
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError:
        log.warning("Bad message: %s", raw)
        return

    mtype = msg.get("type")

    if mtype == "move":
        dx, dy = msg.get("dx", 0), msg.get("dy", 0)
        _move_accum["x"] += dx
        _move_accum["y"] += dy
        step_x = int(_move_accum["x"])
        step_y = int(_move_accum["y"])
        if step_x or step_y:
            pyautogui.moveRel(step_x, step_y, duration=0)
            _move_accum["x"] -= step_x
            _move_accum["y"] -= step_y

    elif mtype == "click":
        button = msg.get("button", "left")
        double = msg.get("double", False)
        if button == "right":
            pyautogui.click(button="right")
        elif double:
            pyautogui.doubleClick()
        else:
            pyautogui.click()

    elif mtype == "scroll":
        dx, dy = msg.get("dx", 0), msg.get("dy", 0)
        if abs(dy) >= abs(dx):
            pyautogui.scroll(int(-dy))
        else:
            pyautogui.hscroll(int(dx))

    elif mtype == "key":
        key = resolve_key(msg.get("key", ""))
        if len(key) == 1:
            pyautogui.typewrite(key)
        else:
            pyautogui.press(key)

    elif mtype == "key_down":
        pyautogui.keyDown(resolve_key(msg.get("key", "")))

    elif mtype == "key_up":
        pyautogui.keyUp(resolve_key(msg.get("key", "")))

    else:
        log.warning("Unknown message type: %s", mtype)


async def handler(websocket, path=None):
    peer = websocket.remote_address
    log.info("Client connected: %s", peer)
    try:
        async for raw in websocket:
            await handle_message(raw)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        log.info("Client disconnected: %s", peer)


async def main():
    async with websockets.serve(handler, HOST, PORT):
        log.info("Remote Pad server listening on ws://%s:%s/ws", HOST, PORT)
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Stopped.")
