
import hashlib
import requests


# ── Colors ───────────────────────────────────────────────────
class C:
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    CYAN   = '\033[96m'
    WHITE  = '\033[97m'
    BOLD   = '\033[1m'
    RESET  = '\033[0m'


# ── HIBP API — k-anonymity model ─────────────────────────────
def check_dark_web(password):
    """
    Password dark web pe leaked hai ya nahi check karo.

    k-anonymity model:
    - Password ka SHA1 hash banao
    - Sirf pehle 5 characters API ko bhejo
    - Tera actual password kabhi server pe nahi jaata!

    Returns:
        int — kitni baar leaked (0 = safe)
    """
    try:
        # Step 1 — SHA1 hash banao
        sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

        # Step 2 — sirf pehle 5 chars bhejo (k-anonymity)
        prefix = sha1[:5]
        suffix = sha1[5:]

        # Step 3 — API call
        url      = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        # Step 4 — response mein apna suffix dhundo
        hashes = response.text.splitlines()
        for line in hashes:
            h, count = line.split(':')
            if h == suffix:
                return int(count)

        return 0  # nahi mila — safe hai

    except requests.ConnectionError:
        print(f"{C.RED}Error: Internet connection nahi hai!{C.RESET}")
        return -1
    except requests.Timeout:
        print(f"{C.YELLOW}Error: Server ne respond nahi kiya.{C.RESET}")
        return -1
    except Exception as e:
        print(f"{C.RED}Error: {e}{C.RESET}")
        return -1


# ── Password Strength Check ───────────────────────────────────
def check_strength(password):
    """
    Password kitna strong hai check karo.

    Returns:
        dict — {score, level, suggestions}
    """
    score       = 0
    suggestions = []

    # Length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append("At least 8 characters use karo")

    # Uppercase check
    if any(c.isupper() for c in password):
        score += 1
    else:
        suggestions.append("Ek capital letter add karo (A-Z)")

    # Lowercase check
    if any(c.islower() for c in password):
        score += 1
    else:
        suggestions.append("Ek small letter add karo (a-z)")

    # Number check
    if any(c.isdigit() for c in password):
        score += 1
    else:
        suggestions.append("Ek number add karo (0-9)")

    # Symbol check
    symbols = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    if any(c in symbols for c in password):
        score += 2
    else:
        suggestions.append("Ek symbol add karo (!@#$%)")

    # Level decide karo
    if score >= 6:
        level = "STRONG"
        color = C.GREEN
    elif score >= 4:
        level = "MEDIUM"
        color = C.YELLOW
    else:
        level = "WEAK"
        color = C.RED

    return {
        "score":       score,
        "level":       level,
        "color":       color,
        "suggestions": suggestions
    }


# ── Main Function — cyberjarvis.py yeh call karega ────────────
def check_password(password, speaker=None, dash=None):
    """
    Password check karo — dark web + strength.
    cyberjarvis.py se yeh call hoga.

    Args:
        password : string — check karna hai
        speaker  : win32com speaker (optional — jarvis bolega)
        dash     : dashboard object (optional — alert dikhega)

    Returns:
        dict — {leaked, count, strength}
    """

    def speak(text):
        print(f"{C.CYAN}Jarvis: {text}{C.RESET}")
        if speaker:
            if dash: dash.set_mode("speaking")
            speaker.Speak(text)
            if dash: dash.set_mode("listening")

    print(f"\n{C.BOLD}[ PASSWORD CHECKER ]{C.RESET}")
    print(f"  Checking password... (RAM only — not stored)\n")

    # ── Dark Web Check ────────────────────────────────────────
    speak("Checking dark web sir, please wait")
    count = check_dark_web(password)

    if count == -1:
        speak("Sorry sir, could not connect to dark web database")
        return {"leaked": False, "count": 0, "strength": None}

    # ── Strength Check ────────────────────────────────────────
    strength = check_strength(password)

    # ── Print Results ─────────────────────────────────────────
    print(f"  {'─'*38}")
    print(f"  {'DARK WEB RESULT':}")

    if count > 0:
        print(f"  {C.RED}{C.BOLD}DANGER! Password leaked!{C.RESET}")
        print(f"  Found {C.RED}{count:,}{C.RESET} times on dark web!")
        speak(f"Sir danger! This password was leaked {count:,} times on dark web! Change it immediately!")
        if dash:
            dash.set_mode("alert")
    else:
        print(f"  {C.GREEN}{C.BOLD}SAFE! Not found on dark web{C.RESET}")
        speak("Sir, this password is safe! Not found on dark web.")

    print(f"\n  {'PASSWORD STRENGTH':}")
    sc = strength
    print(f"  Strength : {sc['color']}{C.BOLD}{sc['level']}{C.RESET}")
    print(f"  Score    : {sc['score']}/7")

    if sc['suggestions']:
        print(f"\n  {C.YELLOW}Suggestions:{C.RESET}")
        for s in sc['suggestions']:
            print(f"    → {s}")
        if sc['level'] != 'STRONG':
            speak(f"Password strength is {sc['level']}. " + sc['suggestions'][0] if sc['suggestions'] else "")
    else:
        print(f"  {C.GREEN}Excellent password!{C.RESET}")
        speak("Password strength is excellent sir!")

    print(f"  {'─'*38}\n")

    return {
        "leaked":   count > 0,
        "count":    count,
        "strength": sc
    }


# ── Standalone Test ───────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{C.CYAN}{C.BOLD}")
    print("╔══════════════════════════════════════╗")
    print("║   JARVIS — Dark Web Password Check   ║")
    print("║   RAM Only — No Data Stored          ║")
    print("╚══════════════════════════════════════╝")
    print(C.RESET)

    while True:
        pwd = input(f"{C.YELLOW}Enter password to check (q to quit): {C.RESET}")
        if pwd.lower() == 'q':
            break
        if pwd.strip():
            check_password(pwd)
        print()