import sys, os

PROJECT_ROOT = "/home/admin/Development/pi-lab"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse



app = FastAPI()
BASE_DIR = os.path.dirname(__file__)

#default endpoint
@app.get("/")
async def serve_root():
    return FileResponse(os.path.join(BASE_DIR,"statics","waby.html"))

#health endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "FastAPI is alive"}

#endpoint to update LED
@app.post("/display")
async def display_text(line1: str = Form(""), line2: str = Form("")):
    from LED_L2C.led import show_text
    show_text(line1, line2)
    return RedirectResponse(url="/", status_code=303)

'''
@app.post("/display")
async def display_text(line1: str = Form(""), line2: str = Form("")):
    print("🛰️ Received POST:", line1, line2, flush=True)
    # show_text(line1, line2)  # Temporarily disabled
    return {"status": "received", "line1": line1, "line2": line2}
'''