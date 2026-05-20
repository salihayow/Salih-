import discord
from discord.ext import commands
import requests
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

TOKEN = "YOUR_BOT_TOKEN_HERE"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

def clean_ad_link(url):
    try:
        # Follow redirects (stop after 5 hops to avoid loops)
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        resp = session.get(url, allow_redirects=True, timeout=10)
        final_url = resp.url

        # Remove tracking/ref/source parameters from common ad platforms
        parsed = urlparse(final_url)
        query = parse_qs(parsed.query)
        remove_keys = ['ref', 'source', 'utm_source', 'utm_medium', 'utm_campaign', 'click_id', 'sub_id', 'aff_id', 'sid', 'ad_id', 'zone_id']
        for key in remove_keys:
            query.pop(key, None)

        # Rebuild URL
        clean_query = urlencode(query, doseq=True)
        parsed = parsed._replace(query=clean_query)
        final_url = urlunparse(parsed)

        # If it's still free-content.pro, try to extract direct link from HTML (naive)
        if "free-content.pro" in final_url:
            html = session.get(final_url, timeout=10).text
            # Look for "window.location" or meta refresh
            match = re.search(r"window\.location\.(?:href|replace)\(['\"]([^'\"]+)", html)
            if not match:
                match = re.search(r'<meta http-equiv="refresh" content="\d+;url=([^"]+)"', html)
            if match:
                final_url = match.group(1)
                # Recursively clean again
                return clean_ad_link(final_url)

        return final_url
    except Exception as e:
        return f"Error during bypass: {str(e)}"

@bot.command(name="bypass")
async def bypass(ctx, link: str):
    await ctx.send(f"Attempting to bypass: {link}")
    result = clean_ad_link(link)
    await ctx.send(f"Bypassed result: {result}")

@bot.event
async def on_ready():
    print(f"NullizePmo bot ready as {bot.user}")

bot.run(TOKEN)