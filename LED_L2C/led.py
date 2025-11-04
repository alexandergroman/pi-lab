from signal import signal,SIGTERM,SIGHUP,pause
from rpi_lcd import LCD

lcd = LCD(address=0x3F)

def safe_exit(signum,frame):
    lcd.clear()
    exit(0)

def show_text(line1="", line2=""):
    lcd.clear()
    if line1:
        lcd.text(line1[:16], 1)
    if line2:
        lcd.text(line2[:16], 2)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

if __name__ == "__main__":
    try:
        show_text("yabba", "dabba")
        input("Press Enter to clear and exit...")
        lcd.clear()
    except KeyboardInterrupt:
        pass
    finally:
        lcd.clear()