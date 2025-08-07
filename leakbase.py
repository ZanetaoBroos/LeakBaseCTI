import csv
import os
import requests
import webbrowser
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

# ASCII
ASCII_ART = '''
[bold blue]

__     _______ ____ _____ ____ _____ 
\ \   / / ____/ ___| ____|  _ \_   _|
 \ \ / /|  _|| |   |  _| | |_) || |  
  \ V / | |__| |___| |___|  _ < | |  
   \_/  |_____\____|_____|_| \_\|_|  

         VECERT - Security Research Tool
 For Educational Use Only | Cybercrime Investigation



[/bold blue]
'''

# Files
USER_CSV = "leakbase_users.csv"
POST_CSVS = ["big_leaks.csv", "chuki.csv", "private.csv", "stealer.csv"]
EXPORT_FILENAME = "breach_info.csv"

EMAIL_DOMAINS = [
    "protonmail.com", "protonmail.ch", "tutanota.com", "tuta.io", "tutanota.de",
    "outlook.com", "outlook.es", "hotmail.com", "hotmail.co.uk", "yahoo.com",
    "yandex.com", "riseup.net", "mailfence.com", "pm.me", "cock.li", "safe-mail.net",
    "guerrillamail.com", "disroot.org", "secmail.pro", "proton.me"
]

def load_csv(file):
    if not os.path.exists(file):
        console.print(f"[red]File not found:[/] {file}")
        return []
    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        return list(csv.DictReader(f))

def export_csv(data, fields):
    with open(EXPORT_FILENAME, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
    console.print(f"[green]✅ Exported to:[/] {EXPORT_FILENAME}")

def parse_date(text):
    try:
        return datetime.fromisoformat(text)
    except:
        return datetime.min

def verify_api_x(email):
    url = f"https://api.x.com/i/users/email_available.json?email={email}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return "✅ Account not exists" if data.get("valid") and not data.get("taken") else "❌ Account exists"
        else:
            return f"⚠️ HTTP {r.status_code}"
    except Exception as e:
        return f"⚠️ Error: {e}"

def show_post_results(results):
    table = Table(title="📁 Matching Posts", title_style="bold magenta", show_lines=True)
    table.add_column("📌 Title", style="cyan")
    table.add_column("🔗 URL", style="blue")
    table.add_column("🏷️ Prefixes", style="yellow")
    table.add_column("✍️ Author", style="green")
    table.add_column("🆔 ID", justify="right")
    table.add_column("📅 Created", style="white")
    table.add_column("💬 Replies", justify="right")
    table.add_column("👁️ Views", justify="right")
    table.add_column("💬 Last by", style="green")
    table.add_column("🆔 Last ID", justify="right")
    table.add_column("⏱️ Last Replied", style="white")

    for row in results:
        table.add_row(
            row.get("title", ""),
            row.get("thread_url", ""),
            row.get("prefixes", ""),
            row.get("author_username", ""),
            row.get("author_id", ""),
            row.get("created_at", ""),
            row.get("replies", ""),
            row.get("views", ""),
            row.get("last_username", ""),
            row.get("last_user_id", ""),
            row.get("last_replied_at", "")
        )
    console.print(table)
    if Prompt.ask("Export these results to CSV? (y/n)", choices=["y", "n"]) == "y":
        export_csv(results, list(results[0].keys()))

def show_user_results(results):
    table = Table(title="👤 Matching Users", title_style="bold green")
    table.add_column("👤 Username", style="cyan")
    table.add_column("🔗 Profile")
    table.add_column("🆔 ID", justify="right")
    table.add_column("📷 Avatar")
    table.add_column("✉️ Messages", justify="right")
    table.add_column("💬 Reactions", justify="right")
    for row in results:
        table.add_row(
            row.get("username", ""),
            row.get("profile_url", ""),
            row.get("user_id", ""),
            row.get("avatar_url", ""),
            row.get("messages", ""),
            row.get("reaction_score", "")
        )
    console.print(table)
    if Prompt.ask("Export these users to CSV? (y/n)", choices=["y", "n"]) == "y":
        export_csv(results, list(results[0].keys()))

def show_osint_links(username):
    links = [
        ["🔗 Telegram Profile", f"https://t.me/{username}"],
        ["🔎 WhatsMyName", f"https://whatsmyname.app/?q={username}"],
        ["🔎 IDCrawl", f"https://www.idcrawl.com/u/{username}"],
        ["🔎 Social Searcher", f"https://www.social-searcher.com/google-social-search/?q={username}"],
        ["💥 BreachForums", f"https://bf.based.re/search/{username}"],
        ["🕵️ Telegram History", "https://t.me/unamer_news"]
    ]
    table = Table(title=f"🌐 OSINT Links for: {username}", title_style="bold white")
    table.add_column("Tool")
    table.add_column("URL", style="cyan")
    for label, url in links:
        table.add_row(label, url)
    console.print(table)

def discover_known_emails(username):
    console.print(f"\n📧 Checking known emails for: [bold cyan]{username}[/bold cyan]")
    found = []
    for domain in EMAIL_DOMAINS:
        email = f"{username}@{domain}"
        result = verify_api_x(email)
        if "exists" in result and "not" not in result:
            found.append({"email": email, "status": result})
    if found:
        table = Table(title="📧 Existing Emails", title_style="bold blue")
        table.add_column("Email", style="cyan")
        table.add_column("Status", style="green")
        for row in found:
            table.add_row(row["email"], row["status"])
        console.print(table)
        if Prompt.ask("Export email results? (y/n)", choices=["y", "n"]) == "y":
            export_csv(found, ["email", "status"])
    else:
        console.print("[red]No active emails found.[/red]")

def search_posts_by_author(username):
    posts = []
    for file in POST_CSVS:
        posts.extend(load_csv(file))
    results = [p for p in posts if p.get("author_username", "").lower() == username.lower()]
    results.sort(key=lambda r: parse_date(r.get("created_at", "")), reverse=True)

    if results:
        console.print(f"\n📄 Posts by {username}")
        show_post_results(results)
        discover_known_emails(username)
        show_osint_links(username)
    else:
        console.print(f"[red]No posts found for {username}.[/red]")

def search_users():
    users = load_csv(USER_CSV)
    if not users:
        return
    while True:
        term = Prompt.ask("🔍 Enter username to search")
        results = [u for u in users if term.lower() in u["username"].lower()]
        if results:
            show_user_results(results)
            selected = results[0]["username"] if len(results) == 1 else Prompt.ask("Enter exact username to view posts")
            search_posts_by_author(selected)
        else:
            console.print("[red]No users found.[/red]")
        if Prompt.ask("Search another user? (y/n)", choices=["y", "n"]) == "n":
            break

def search_posts():
    posts = []
    for file in POST_CSVS:
        posts.extend(load_csv(file))
    if not posts:
        return
    while True:
        term = Prompt.ask("🔍 Search posts by title or author")
        results = [p for p in posts if term.lower() in p["title"].lower() or term.lower() in p["author_username"].lower()]
        results.sort(key=lambda r: parse_date(r.get("created_at", "")), reverse=True)
        if results:
            show_post_results(results)
        else:
            console.print("[red]No posts found.[/red]")
        if Prompt.ask("Search another post? (y/n)", choices=["y", "n"]) == "n":
            break

def search_post_by_id():
    user_id = Prompt.ask("Enter user ID to search online")
    url = f"https://leakbase.la/search/member?user_id={user_id}"
    console.print(f"🌐 Opening browser to: {url}")
    webbrowser.open(url)

def discover_email_by_username():
    username = Prompt.ask("Enter a username to check email availability")
    discover_known_emails(username)

def main():
    while True:
        console.print(ASCII_ART)
        console.print(Panel.fit(
            "📂 [bold cyan]Main Menu[/bold cyan]\n\n"
            "1. 🔍 Search Users\n"
            "2. 🧵 Search Posts\n"
            "3. 🔎 Search Post by ID (online)\n"
            "4. ✉️ Discover Emails by Username\n"
            "5. 🚪 Exit",
            title="Leakbase Intelligence",
            title_align="left"
        ))

        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5"])
        if choice == "1":
            search_users()
        elif choice == "2":
            search_posts()
        elif choice == "3":
            search_post_by_id()
        elif choice == "4":
            discover_email_by_username()
        elif choice == "5":
            console.print("[green]Goodbye![/green]")
            break

        if Prompt.ask("Return to main menu? (y/n)", choices=["y", "n"]) == "n":
            break

if __name__ == "__main__":
    main()
