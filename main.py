import ctypes
import sys
import time

# --- Självhöjning till admin ---
def _is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def _elevate():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable,
        " ".join(f'"{a}"' for a in sys.argv),
        None, 1
    )
    sys.exit(0)

if not _is_admin():
    print("Startar om som administratör...")
    _elevate()

# --- Resten av scriptet ---
import winreg
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05


def disable_uac():
    path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
    with winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(key, "ConsentPromptBehaviorAdmin", 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(key, "PromptOnSecureDesktop", 0, winreg.REG_DWORD, 0)
    print("UAC avstängt (kräver omstart för full effekt).")


def disable_defender():
    pyautogui.hotkey("win", "r")
    time.sleep(0.3)
    pyautogui.write("windowsdefender://threat", interval=0.03)
    pyautogui.press("enter")
    time.sleep(2.5)

    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(2.0)

    pyautogui.press("space")
    time.sleep(1.5)

    pyautogui.press("tab")
    time.sleep(1.5)
    pyautogui.press("tab")
    time.sleep(1.5)
    pyautogui.press("tab")
    time.sleep(1.5)
    pyautogui.press("space")
    time.sleep(1.5)

    pyautogui.press("tab")
    time.sleep(1.5)
    pyautogui.press("space")
    time.sleep(1.5)

    pyautogui.press("tab")
    time.sleep(1.5)
    pyautogui.press("tab")
    time.sleep(1.5)
    pyautogui.press("space")
    time.sleep(1.5)


if __name__ == "__main__":
    print(
        "Startar om 3 sekunder. Flytta musen till övre vänstra hörnet för att avbryta."
    )
    time.sleep(3)

    print("Steg 1: Stänger av UAC...")
    disable_uac()
    time.sleep(3)

    print("Steg 2: Stänger av Windows Defender realtidsskydd...")
    disable_defender()
    time.sleep(3)

    print("Klart.")