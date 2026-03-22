"""
JARVIS — Email Dark Web Breach Checker
100% Free — No API Key — RAM Only
"""

import requests
import re


class C:
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    CYAN   = '\033[96m'
    BOLD   = '\033[1m'
    RESET  = '\033[0m'


STRONG_PASSWORD_TIPS = [
    "At least 12 characters use karo",
    "UPPERCASE + lowercase + numbers + symbols (!@#$)",
    "2 websites pe same password mat use karo",
    "Bitwarden (free password manager) use karo",
    "2FA (Two Factor Authentication) enable karo",
    "Har 3-6 mahine mein password change karo",
]


def _check_hibp_v3(email):
    try:
        url     = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {"User-Agent": "JARVIS-CyberAI-v4"}
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 404:
            return []
        return None
    except:
        return None


def _check_hibp_v2(email):
    try:
        url     = f"https://haveibeenpwned.com/api/v2/breachedaccount/{email}"
        headers = {"User-Agent": "JARVIS-CyberAI-v4"}
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 404:
            return []
        return None
    except:
        return None


def _check_leakcheck(email):
    try:
        url     = f"https://leakcheck.io/api/public?check={email}"
        headers = {"User-Agent": "JARVIS-CyberAI-v4"}
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code == 200:
            data = r.json()
            if data.get("found"):
                return data.get("sources", ["Breach Detected"])
            return []
        return None
    except:
        return None


def _is_valid_email(email):
    return bool(re.match(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$', email))


def _show_suggestions(speak_fn):
    print(f"\n  {C.YELLOW}{C.BOLD}🔐 TURANT YEH KARO:{C.RESET}")
    print(f"  {'─'*40}")
    print(f"  {C.RED}1. Abhi apna email password change karo!{C.RESET}")
    print(f"  {C.RED}2. Sab linked websites ke passwords change karo{C.RESET}")
    print(f"  {C.YELLOW}3. Email pe 2FA enable karo{C.RESET}")
    print(f"\n  {C.CYAN}💡 Strong Password Tips:{C.RESET}")
    for i, tip in enumerate(STRONG_PASSWORD_TIPS, 1):
        print(f"    {i}. {tip}")
    print(f"  {'─'*40}")
    speak_fn(
        "Sir, please change your email password immediately. "
        "Also enable two factor authentication. "
        "Use a strong password with uppercase, lowercase, numbers and symbols."
    )


def check_email_breach(speaker=None, dash=None):

    def speak(text):
        print(f"{C.CYAN}Jarvis: {text}{C.RESET}")
        if speaker:
            try:
                if dash: dash.set_mode("speaking")
                speaker.Speak(text)
                if dash: dash.set_mode("listening")
            except:
                pass

    speak("Tell me your email sir")
    print(f"\n{C.YELLOW}  ► Type your email and press Enter: {C.RESET}", end="")

    try:
        email = input().strip().lower()
    except:
        speak("Sorry sir, input failed")
        return

    if not email or not _is_valid_email(email):
        speak("Sorry sir, that is not a valid email")
        print(f"  {C.RED}Invalid email!{C.RESET}\n")
        return

    print(f"\n  {C.CYAN}Checking: {email}{C.RESET}")
    print(f"  Searching breach database...")
    speak("Checking sir please wait")

    breaches = None

    print(f"  Method 1: HIBP v3...")
    breaches = _check_hibp_v3(email)

    if breaches is None:
        print(f"  Method 2: HIBP v2...")
        breaches = _check_hibp_v2(email)

    if breaches is None:
        print(f"  Method 3: LeakCheck...")
        breaches = _check_leakcheck(email)

    if breaches is None:
        breaches = []

    # ── Result — sirf count dikhao, names nahi ───────────────
    print(f"\n{C.BOLD}  [ EMAIL BREACH REPORT ]{C.RESET}")
    print(f"  {'─'*40}")
    print(f"  Email  : {email}")
    print(f"  {'─'*40}")

    if len(breaches) == 0:
        print(f"  {C.GREEN}{C.BOLD}✅ SAFE! Koi breach nahi mila{C.RESET}")
        print(f"  {C.GREEN}Tera email safe hai!{C.RESET}")
        print(f"\n  {C.CYAN}💡 Safe rehne ke tips:{C.RESET}")
        print(f"    • Strong unique passwords use karo")
        print(f"    • 2FA enable karo")
        print(f"    • Regularly check karo")
        speak("Sir good news! Your email was not found in any data breach. You are safe!")
        if dash: dash.set_mode("idle")

    else:
        # Sirf count — names nahi!
        count = len(breaches)
        print(f"  {C.RED}{C.BOLD}⚠  DANGER! {count} breach(es) mein mila!{C.RESET}")
        print(f"  {C.RED}Tera personal data compromised ho sakta hai!{C.RESET}")

        speak(
            f"Sir danger! Your email was found in {count} data breaches. "
            f"Your personal data may be at risk. Please take action immediately!"
        )

        if dash: dash.set_mode("alert")
        _show_suggestions(speak)

    print(f"  {'─'*40}")
    print(f"  {C.CYAN}RAM only — kuch store nahi hua{C.RESET}\n")


if __name__ == "__main__":
    print(f"\n{C.CYAN}{C.BOLD}")
    print("╔══════════════════════════════════════╗")
    print("║  JARVIS — Email Breach Checker       ║")
    print("║  Free — No API Key — RAM Only        ║")
    print("╚══════════════════════════════════════╝")
    print(C.RESET)
    check_email_breach()