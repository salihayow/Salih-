import discord
from discord.ext import commands
import requests
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

TOKEN = "MTUwNjYwMDIxNTgzNzE0NzE2Nw.GYaZ5b.OYfoe8iLgYN9QznkuhLwsYqacb4C93WHJquas4"  # <--- YOU MUST CHANGE THIS

intents = discord.Intents.default()
intents.message_content = True  # FIX: enables message content intent

bot = commands.Bot(command_prefix="/", intents=intents)

def clean_ad_link(url):
    try:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        resp = session.get(url, allow_redirects=True, timeout=10)
        final_url = resp.url

        parsed = urlparse(final_url)
        query = parse_qs(parsed.query)
        remove_keys = ['ref', 'source', 'utm_source', 'utm_medium', 'utm_campaign', 'click_id', 'sub_id', 'aff_id', 'sid', 'ad_id', 'zone_id']
        for key in remove_keys:
            query.pop(key, None)

        clean_query = urlencode(query, doseq=True)
        parsed = parsed._replace(query=clean_query)
        final_url = urlunparse(parsed)

        if "free-content.pro" in final_url:
            html = session.get(final_url, timeout=10).text
            match = re.search(r"window\.location\.(?:href|replace)\(['\"]([^'\"]+)", html)
            if not match:
                match = re.search(r'<meta http-equiv="refresh" content="\d+;url=([^"]+)"', html)
            if match:
                final_url = match.group(1)
                return clean_ad_link(final_url)

        return final_url
    except Exception as e:
        return f"Error: {str(e)}"

@bot.command(name="bypass")
async def bypass(ctx, link: str):
    await ctx.send(f"Bypassing: {link}")
    result = clean_ad_link(link)
    await ctx.send(f"Result: {result}")

@bot.event
async def on_ready():
    print(f"NullizePmo ready as {bot.user}")

bot.run(TOKEN)
