import os
import subprocess
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Ensure this is set in your Railway environment

# For AbuseIPDB and VirusTotal reporting (if needed)
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")
VT_API_KEY = os.getenv("VT_API_KEY")

# Set up intents (adjust as needed)
intents = discord.Intents.default()
intents.message_content = True

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Sync the slash commands when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Helper function: run a command and return its output
def run_command(cmd_list, label):
    try:
        result = subprocess.check_output(cmd_list, stderr=subprocess.STDOUT)
        output = result.decode()
        return f"{label}:\n{output}"
    except Exception as e:
        return f"{label} error: {e}"

# /whois command
@bot.tree.command(name="whois", description="Perform a WHOIS lookup")
@app_commands.describe(target="Target IP or domain")
async def whois(interaction: discord.Interaction, target: str):
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except discord.errors.NotFound:
        pass
    output = run_command(["whois", target], "Whois")
    if len(output) > 1900:
        output = output[:1900] + "\n...Output truncated."
    await interaction.followup.send(f"```{output}```")

# /traceroute command
@bot.tree.command(name="traceroute", description="Run traceroute on a target")
@app_commands.describe(target="Target IP address or domain")
async def traceroute(interaction: discord.Interaction, target: str):
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except discord.errors.NotFound:
        pass
    output = run_command(["traceroute", target], "Traceroute")
    if len(output) > 1900:
        output = output[:1900] + "\n...Output truncated."
    await interaction.followup.send(f"```{output}```")

# /dig command
@bot.tree.command(name="dig", description="Run a DNS lookup using dig")
@app_commands.describe(domain="Domain to query")
async def dig(interaction: discord.Interaction, domain: str):
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except discord.errors.NotFound:
        pass
    output = run_command(["dig", domain], "Dig")
    if len(output) > 1900:
        output = output[:1900] + "\n...Output truncated."
    await interaction.followup.send(f"```{output}```")

# /ipinfo command
@bot.tree.command(name="ipinfo", description="Get IP info from ipinfo.io")
@app_commands.describe(ip="Target IP address")
async def ipinfo(interaction: discord.Interaction, ip: str):
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except discord.errors.NotFound:
        pass
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json")
        output = f"IPInfo:\n{res.text}"
    except Exception as e:
        output = f"IPInfo error: {e}"
    if len(output) > 1900:
        output = output[:1900] + "\n...Output truncated."
    await interaction.followup.send(f"```{output}```")

# /geoip command
@bot.tree.command(name="geoip", description="Get geo-location info")
@app_commands.describe(ip="Target IP address")
async def geoip(interaction: discord.Interaction, ip: str):
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except discord.errors.NotFound:
        pass
    try:
        res = requests.get(f"https://geolocation-db.com/json/{ip}&position=true").json()
        output = f"GeoIP:\n{res}"
    except Exception as e:
        output = f"GeoIP error: {e}"
    if len(output) > 1900:
        output = output[:1900] + "\n...Output truncated."
    await interaction.followup.send(f"```{output}```")

# /brute command
@bot.tree.command(name="brute", description="Run a port scan using masscan")
@app_commands.describe(ip="Target IP address")
async def brute(interaction: discord.Interaction, ip: str):
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except discord.errors.NotFound:
        pass
    output = run_command(["masscan", ip, "-p1-1000", "--rate", "1000"], "Masscan")
    if len(output) > 1900:
        output = output[:1900] + "\n...Output truncated."
    await interaction.followup.send(f"```{output}```")

# /emailleaks command
@bot.tree.command(name="emailleaks", description="Check for email leaks")
@app_commands.describe(email="Email address to check")
async def emailleaks(interaction: discord.Interaction, email: str):
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except discord.errors.NotFound:
        pass
    try:
        res = requests.get(f"https://leakcheck.net/api/public?check={email}")
        if res.status_code == 200:
            output = f"Email Leak Report:\n{res.text}"
        else:
            output = f"LeakCheck error: {res.status_code}"
    except Exception as e:
        output = f"Email leak check error: {e}"
    if len(output) > 1900:
        output = output[:1900] + "\n...Output truncated."
    await interaction.followup.send(f"```{output}```")

# /abuseip command
@bot.tree.command(name="abuseip", description="Get an AbuseIPDB report")
@app_commands.describe(ip="Target IP address")
async def abuseip(interaction: discord.Interaction, ip: str):
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except discord.errors.NotFound:
        pass
    try:
        headers = {
            'Key': ABUSEIPDB_API_KEY,
            'Accept': 'application/json'
        }
        res = requests.get(f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}", headers=headers)
        data = res.json()['data']
        output = (
            f"AbuseIPDB Report:\nIP: {data['ipAddress']}\n"
            f"Abuse Score: {data['abuseConfidenceScore']}\n"
            f"Total Reports: {data['totalReports']}\n"
            f"Country: {data['countryCode']}"
        )
    except Exception as e:
        output = f"AbuseIPDB error: {e}"
    if len(output) > 1900:
        output = output[:1900] + "\n...Output truncated."
    await interaction.followup.send(f"```{output}```")

# /virustotal command
@bot.tree.command(name="virustotal", description="Get a VirusTotal IP report")
@app_commands.describe(ip="Target IP address")
async def virustotal(interaction: discord.Interaction, ip: str):
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except discord.errors.NotFound:
        pass
    try:
        headers = {"x-apikey": VT_API_KEY}
        res = requests.get(f"https://www.virustotal.com/api/v3/ip_addresses/{ip}", headers=headers)
        data = res.json()['data']['attributes']
        detected = data['last_analysis_stats']['malicious']
        harmless = data['last_analysis_stats']['harmless']
        output = (
            f"VirusTotal Report:\nMalicious: {detected}\nHarmless: {harmless}\n"
            f"ASN: {data.get('asn')}\nOrg: {data.get('as_owner')}"
        )
    except Exception as e:
        output = f"VirusTotal error: {e}"
    if len(output) > 1900:
        output = output[:1900] + "\n...Output truncated."
    await interaction.followup.send(f"```{output}```")

# /torvpn command
@bot.tree.command(name="torvpn", description="Check if an IP is using TOR/VPN/proxy")
@app_commands.describe(ip="Target IP address")
async def torvpn(interaction: discord.Interaction, ip: str):
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except discord.errors.NotFound:
        pass
    try:
        res = requests.get(f"https://ipapi.co/{ip}/json/")
        data = res.json()
        sec = data.get("security", {})
        is_vpn = sec.get("vpn", False)
        is_proxy = sec.get("proxy", False)
        is_tor = sec.get("tor", False)
        output = f"TOR/VPN Check:\nVPN: {is_vpn}\nProxy: {is_proxy}\nTOR: {is_tor}"
    except Exception as e:
        output = f"TOR/VPN detection error: {e}"
    if len(output) > 1900:
        output = output[:1900] + "\n...Output truncated."
    await interaction.followup.send(f"```{output}```")

# /commands command to list available commands
@bot.tree.command(name="commands", description="List available commands")
async def commands_list(interaction: discord.Interaction):
    help_text = (
        "**Available Commands:**\n"
        "/whois target:<ip_or_domain>          → WHOIS lookup\n"
        "/traceroute target:<ip_or_domain>     → Trace route\n"
        "/dig domain:<domain>                  → DNS lookup\n"
        "/ipinfo ip:<ip_address>               → IPInfo lookup\n"
        "/geoip ip:<ip_address>                → Geo-location lookup\n"
        "/brute ip:<ip_address>                → Masscan port scan\n"
        "/emailleaks email:<email_address>     → Check for email leaks\n"
        "/abuseip ip:<ip_address>              → AbuseIPDB report\n"
        "/virustotal ip:<ip_address>           → VirusTotal IP report\n"
        "/torvpn ip:<ip_address>               → Check for TOR/VPN/proxy\n"
        "/commands                           → Show this commands list"
    )
    await interaction.response.send_message(f"```{help_text}```")

bot.run(TOKEN)
