import requests
import time
import os
import sys
from colorama import init, Fore, Style

init(autoreset=True)

# ================= UTIL =================
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def log(msg, color=Fore.WHITE):
    print(color + f"[LOG] {msg}")


def title(text):
    print(Fore.CYAN + Style.BRIGHT + f"\n=== {text} ===\n")


def slow_print(text, delay=0.01, color=Fore.WHITE):
    for c in text:
        sys.stdout.write(color + c)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def progress_bar(current, total, length=30):
    percent = current / total
    filled = int(length * percent)
    bar = "█" * filled + "-" * (length - filled)
    print(f"\r[{bar}] {current}/{total}", end="")


# ================= WEBHOOK =================
def validate(url):
    return url.startswith("https://discord.com/api/webhooks/")


def send_message(webhook, content):
    try:
        r = requests.post(webhook, json={"content": content})

        if r.status_code in (200, 204):
            return "success"
        elif r.status_code == 429:
            return "ratelimited"
        else:
            return f"fail:{r.status_code}"
    except:
        return "error"


def send_embed(webhook, title, desc, color=3447003):
    payload = {
        "embeds": [
            {
                "title": title,
                "description": desc,
                "color": color
            }
        ]
    }

    try:
        r = requests.post(webhook, json=payload)
        return r.status_code in (200, 204)
    except:
        return False


# ================= UI =================
def banner():
    clear()
    print(Fore.MAGENTA + r"""
██╗    ██╗███████╗██████╗ ██╗  ██╗ ██████╗ ███████╗██╗   ██╗
██║    ██║██╔════╝██╔══██╗██║  ██║██╔═══██╗██╔════╝╚██╗ ██╔╝
██║ █╗ ██║█████╗  ██████╔╝███████║██║   ██║███████╗ ╚████╔╝ 
██║███╗██║██╔══╝  ██╔═══╝ ██╔══██║██║   ██║╚════██║  ╚██╔╝  
╚███╔███╔╝███████╗██║     ██║  ██║╚██████╔╝███████║   ██║   
 ╚══╝╚══╝ ╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   
""")
    slow_print("Webhook Control Panel v2.0", 0.02, Fore.CYAN)


# ================= MAIN =================
def main():
    banner()

    webhook = input(Fore.CYAN + "Enter webhook URL > ").strip()

    if not validate(webhook):
        log("Invalid webhook URL", Fore.RED)
        return

    while True:
        title("MENU")
        print("1. Send Messages")
        print("2. Send Embed")
        print("3. Exit\n")

        choice = input(Fore.YELLOW + "> ").strip()

        # ================= SEND MESSAGE =================
        if choice == "1":
            try:
                amount = int(input("How many messages? (1-100) > "))
                delay = float(input("Delay per message (sec) > "))
            except:
                log("Invalid input", Fore.RED)
                continue

            message = input("Message > ")

            success = 0
            fail = 0

            clear()
            title("SENDING MESSAGES")

            for i in range(1, amount + 1):
                result = send_message(webhook, message)

                if result == "success":
                    success += 1
                    log(f"{i}/{amount} SENT", Fore.GREEN)

                elif result == "ratelimited":
                    log("Rate limited - sleeping 2s", Fore.YELLOW)
                    time.sleep(2)

                else:
                    fail += 1
                    log(f"{i}/{amount} FAILED ({result})", Fore.RED)

                progress_bar(i, amount)
                time.sleep(delay)

            print("\n\nDONE")
            log(f"Success: {success}", Fore.GREEN)
            log(f"Fail: {fail}", Fore.RED)

            input("\nPress Enter...")

        # ================= EMBED =================
        elif choice == "2":
            title_text = input("Embed Title > ")
            desc = input("Embed Description > ")

            ok = send_embed(webhook, title_text, desc)

            if ok:
                log("Embed sent successfully", Fore.GREEN)
            else:
                log("Failed to send embed", Fore.RED)

            input("\nPress Enter...")

        # ================= EXIT =================
        elif choice == "3":
            log("Exiting...", Fore.CYAN)
            break

        else:
            log("Invalid option", Fore.RED)
            time.sleep(1)


if __name__ == "__main__":
    main()