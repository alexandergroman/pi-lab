import sys, os
from datetime import datetime
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, RedirectResponse

# Ensure project root is importable (so LED_L2C works)
PROJECT_ROOT = "/home/admin/Development/pi-lab"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from LED_L2C.led import show_text  # Import once, at startup (faster + cleaner)

# --- App setup ---
app = FastAPI()
BASE_DIR = os.path.dirname(__file__)
LOG_PATH = "/home/admin/Development/pi-lab/WebServer/submissions.log"


# --- Root endpoint (serves HTML) ---
@app.get("/")
async def serve_root():
    return FileResponse(os.path.join(BASE_DIR, "statics", "waby.html"))


# --- Health check endpoint ---
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "FastAPI is alive"}


# --- LED update endpoint ---
@app.post("/display")
async def display_text(
    request: Request,
    line1: str = Form(""),
    line2: str = Form("")
):
    # Extract client IP (Cloudflare-aware)
    ip = (
        request.headers.get("cf-connecting-ip")
        or request.headers.get("x-forwarded-for")
        or (request.client.host if request.client else "unknown")
    )
    if ip and "," in ip:
        ip = ip.split(",")[0].strip()

    # Prepare log entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} | {ip} | Line1: {line1} | Line2: {line2}\n"

    # Append to log file safely
    try:
        os.makedirs(BASE_DIR, exist_ok=True)
        with open(LOG_PATH, "a") as f:
            f.write(entry)
    except Exception as e:
        print(f"Failed to write log: {e}")

    # Display on LCD
    try:
        show_text(line1, line2)
    except Exception as e:
        print(f"[ERROR] Failed to update LCD: {e}")

    # Redirect back to root (form resets)
    return RedirectResponse(url="/", status_code=303)


import html

@app.get("/logs")
async def get_logs():
    try:
        with open(LOG_PATH, "r") as f:
            lines = f.readlines()

        display_lines = []
        for line in reversed(lines):
            parts = line.strip().split("|")
            if len(parts) >= 4:
                timestamp = html.escape(parts[0].strip())
                line1 = html.escape(parts[2].replace("Line1:", "").strip())
                line2 = html.escape(parts[3].replace("Line2:", "").strip())
                display_lines.append(f"{timestamp} → {line1} | {line2}")
            else:
                display_lines.append(html.escape(line.strip()))

        return {"logs": display_lines}

    except FileNotFoundError:
        return {"logs": []}