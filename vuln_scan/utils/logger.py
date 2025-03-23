from rich.console import Console

console = Console()

def log_vulnerability(message, severity="low"):
    colors = {"low": "green", "medium": "yellow", "high": "red"}
    console.print(f"[{colors[severity]}]{message}[/]")
