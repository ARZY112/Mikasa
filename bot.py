import discord
from discord.ext import commands
import random
import json
import os
import asyncio
from aiohttp import web
import requests
import base64

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# GitHub API setup
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = "ARZY112/Mikasa"
NSFW_GIF_FILE_PATH = "nsfw_gif_urls.json"
NON_NSFW_GIF_FILE_PATH = "non_nsfw_gif_urls.json"

# NSFW Roleplay responses
roleplay_responses = {
    "assfuck": ["{user} is fucking {target}'s ass hard."],
    "facefuck": ["{user} is fucking {target}'s mouth deep."],
    "squirt": ["{user} is making {target} squirt hard."],
    "dickslap": ["{user} is slapping {target}'s face with their cock."],
    "creampie": ["{user} is filling {target}'s pussy with cum."],
    "fuck": ["{user} is fucking {target} hard."],
    "pussyrub": ["{user} is rubbing {target}'s pussy hard."],
    "69": ["{user} is eating {target} while you suck their cock."],
    "cumshot": ["{user} is cumming all over {target}'s face."],
    "boobsuck": ["{user} is sucking {target}'s tits hard."],
    "boobsgrab": ["{user} is grabbing {target}'s tits tight."],
    "cum": ["{user} is making {target} cum hard."],
    "leash": ["{user} is pulling {target}'s leash tight."],
    "handjob": ["{user} is jerking {target}'s cock fast."],
    "dickride": ["{user} is riding {target}'s cock hard."],
    "facesit": ["{user} is sitting on {target}'s face hard."],
    "pussyeat": ["{user} is eating {target}'s pussy hard."],
    "spank": ["{user} is spanking {target}'s ass hard."],
    "tittyfuck": ["{user} is fucking {target}'s tits hard."],
    "bondage": ["{user} is tying {target} up tight."],
    "blowjob": ["{user} is sucking {target}'s cock deep."],
    "assgrab": ["{user} is grabbing {target}'s ass tight."],
    "finger": ["{user} is fingering {target}'s pussy deep."],
    "footjob": ["{user} is jerking {target}'s cock with their feet."],
    "masturbate": ["{user} is jerking off in front of {target}."],
    "tease": ["{user} is teasing {target}'s pussy with their fingers."],
    "legspread": ["{user} is spreading {target}'s legs wide."],
    "choke": ["{user} is choking {target} tight."],
    "bite": ["{user} is biting {target} hard."],
    "lick": ["{user} is licking {target} hard."],
    "strip": ["{user} is ripping {target}'s clothes off."]
}

# Channel map for NSFW commands
channel_map = {
    "assfuck": "1374374128831697040",
    "facefuck": "1374374913036648498",
    "squirt": "1374745563115028582",
    "dickslap": "1374745632388026429",
    "creampie": "1374745737015070730",
    "fuck": "1374768762007453819",
    "pussyrub": "1374768858191233127",
    "69": "1374768898024673370",
    "cumshot": "1374768938440724490",
    "boobsuck": "1374769020611330088",
    "boobsgrab": "1374768983814963301",
    "cum": "1374769081411960954",
    "leash": "1374769113217630319",
    "handjob": "1374769194431676507",
    "dickride": "1374769362195583207",
    "facesit": "1374769390897201242",
    "pussyeat": "1374769468542161021",
    "spank": "1374769500477591613",
    "tittyfuck": "1374769555834146998",
    "bondage": "1374769594975391926",
    "blowjob": "1374769768560857118",
    "assgrab": "1374374437612421130",
    "finger": "1374769813326528512",
    "footjob": "1374769848680321074",
    "masturbate": "1374769888442187926",
    "tease": "1374997829814063165",
    "legspread": "1374998253426180116",
    "choke": "1374998299702202430",
    "bite": "1374998343956303924",
    "lick": "1374998369373524040",
    "strip": "1374998973739438214"
}

# Non-NSFW responses
non_nsfw_responses = {
    "kiss": "{user} is kissing {target} softly. 💋",
    "cuddle": "{user} is cuddling {target} warmly. 🥰",
    "hug": "{user} is hugging {target} tightly. 🤗",
    "cry": "{user} is crying on {target}'s shoulder. 😢",
    "slap": "{user} slaps {target} playfully. 👋"
}

# Non-NSFW channel map
non_nsfw_channel_map = {
    "kiss": "1374992686808957050",
    "cuddle": "1374992738264813589",
    "hug": "1374992767234867273",
    "cry": "1374992832418414613",
    "slap": "1374992799178559549"
}

# Fetch URLs using GitHub API for private repo
async def fetch_urls(file_path, max_retries=3):
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN not set. Cannot fetch URLs from GitHub.")
        return {cmd: [] for cmd in (list(roleplay_responses.keys()) if file_path == NSFW_GIF_FILE_PATH else list(non_nsfw_responses.keys()))}
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}?ref=main"
    
    for attempt in range(max_retries):
        try:
            response = await asyncio.to_thread(requests.get, url, headers=headers, timeout=10)
            response.raise_for_status()
            file_data = response.json()
            content = base64.b64decode(file_data["content"]).decode("utf-8")
            print(f"Successfully fetched {file_path} from GitHub API")
            return json.loads(content)
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed to fetch {file_path} from GitHub API: {e}")
            if hasattr(response, 'status_code'):
                print(f"Response status: {response.status_code}, Response text: {response.text}")
            if attempt == max_retries - 1:
                print(f"All attempts failed for {file_path}")
                return {cmd: [] for cmd in (list(roleplay_responses.keys()) if file_path == NSFW_GIF_FILE_PATH else list(non_nsfw_responses.keys()))}
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

# Update GitHub file
def update_github_file(file_path, content, commit_message):
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN not set. Cannot update GitHub file.")
        return
    
    try:
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
        response = requests.get(url, headers=headers)
        if response.status_code == 404:  # File doesn't exist, create it
            data = {
                "message": commit_message,
                "content": base64.b64encode(json.dumps(content, indent=4).encode()).decode(),
                "branch": "main"
            }
            response = requests.put(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"Created {file_path} on GitHub")
            return
        
        response.raise_for_status()
        sha = response.json()["sha"]

        data = {
            "message": commit_message,
            "content": base64.b64encode(json.dumps(content, indent=4).encode()).decode(),
            "sha": sha,
            "branch": "main"
        }
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Updated {file_path} on GitHub")
    except Exception as e:
        print(f"Failed to update {file_path} on GitHub: {e}")

# Load URLs
async def load_urls():
    global nsfw_gif_urls, non_nsfw_gif_urls
    nsfw_gif_urls = await fetch_urls(NSFW_GIF_FILE_PATH)
    non_nsfw_gif_urls = await fetch_urls(NON_NSFW_GIF_FILE_PATH)

# Periodic GIF reload task
async def reload_gif_urls():
    while True:
        await asyncio.sleep(300)  # Check every 5 minutes
        await load_urls()
        print("GIF URLs reloaded")

# Handle message events
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Handle GIF uploads
    for command, channel_id in channel_map.items():
        if str(message.channel.id) == channel_id and message.attachments:
            for attachment in message.attachments:
                if attachment.filename.endswith((".gif", ".png", ".jpg", ".jpeg")):
                    if command not in nsfw_gif_urls:
                        nsfw_gif_urls[command] = []
                    if attachment.url not in nsfw_gif_urls[command]:
                        nsfw_gif_urls[command].append(attachment.url)
                        update_github_file(NSFW_GIF_FILE_PATH, nsfw_gif_urls, f"Add GIF for {command}")
                        await message.channel.send(f"Added {attachment.filename} to {command} GIFs!")
                    break

    for command, channel_id in non_nsfw_channel_map.items():
        if str(message.channel.id) == channel_id and message.attachments:
            for attachment in message.attachments:
                if attachment.filename.endswith((".gif", ".png", ".jpg", ".jpeg")):
                    if command not in non_nsfw_gif_urls:
                        non_nsfw_gif_urls[command] = []
                    if attachment.url not in non_nsfw_gif_urls[command]:
                        non_nsfw_gif_urls[command].append(attachment.url)
                        update_github_file(NON_NSFW_GIF_FILE_PATH, non_nsfw_gif_urls, f"Add GIF for {command}")
                        await message.channel.send(f"Added {attachment.filename} to {command} GIFs!")
                    break

# NSFW roleplay command
for cmd in roleplay_responses.keys():
    async def roleplay_command(ctx, member: discord.Member = None, cmd=cmd):  # Capture cmd in closure
        print(f"Processing NSFW command: {cmd} by {ctx.author}")
        if not ctx.channel.nsfw:
            await ctx.send("This command can only be used in NSFW channels! 🔞")
            return
        if member is None:
            await ctx.send(f"Please mention someone to {cmd}!")
            return
        try:
            response = random.choice(roleplay_responses[cmd]).format(user=ctx.author.mention, target=member.mention)
            embed = discord.Embed(title=f"{cmd.capitalize()}!", description=response, color=discord.Color.red())
            if nsfw_gif_urls.get(cmd) and len(nsfw_gif_urls[cmd]) > 0:
                gif = random.choice(nsfw_gif_urls[cmd])
                embed.set_image(url=gif)
            else:
                embed.set_footer(text="No GIFs found for this command!")
                embed.set_image(url="https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif")
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in NSFW command {cmd}: {e}")
            await ctx.send("An error occurred while processing the command.")
    bot.command(name=cmd)(roleplay_command)

# Non-NSFW command
for cmd in non_nsfw_responses.keys():
    async def non_nsfw_command(ctx, member: discord.Member = None, cmd=cmd):  # Capture cmd in closure
        print(f"Processing non-NSFW command: {cmd} by {ctx.author}")
        if member is None:
            await ctx.send(f"Please mention someone to {cmd}!")
            return
        try:
            response = non_nsfw_responses[cmd].format(user=ctx.author.mention, target=member.mention)
            embed = discord.Embed(title=f"{cmd.capitalize()}!", description=response, color=discord.Color.blue())
            if non_nsfw_gif_urls.get(cmd) and len(non_nsfw_gif_urls[cmd]) > 0:
                gif = random.choice(non_nsfw_gif_urls[cmd])
                embed.set_image(url=gif)
            else:
                embed.set_footer(text="No GIFs found for this command!")
                embed.set_image(url="https://media.giphy.com/media/26ufnwz3wDUli7GU0/giphy.gif")
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in non-NSFW command {cmd}: {e}")
            await ctx.send("An error occurred while processing the command.")
    bot.command(name=cmd)(non_nsfw_command)

# Help command
@bot.command()
async def help(ctx):
    print(f"Processing help command by {ctx.author}")
    embed = discord.Embed(title="Mikasa Command List 📜", color=discord.Color.green())
    nsfw_commands = sorted(roleplay_responses.keys())
    non_nsfw_commands = sorted(non_nsfw_responses.keys())
    all_commands = nsfw_commands + non_nsfw_commands
    embed.add_field(name="Commands", value="\n".join([f"`{cmd}`" for cmd in all_commands]), inline=False)
    embed.set_footer(text="Use !command @user to interact! Example: !kiss @user")
    await ctx.send(embed=embed)

# On ready event
@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready and online!")
    await load_urls()  # Load URLs on startup
    bot.loop.create_task(reload_gif_urls())  # Start GIF reload task

# Health check
async def health_check(request):
    return web.Response(text="Bot is healthy!")

# Start health server
async def start_health_server():
    app = web.Application()
    app.add_routes([web.get('/', health_check)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()

# Main function
async def main():
    if not os.getenv("DISCORD_TOKEN"):
        print("DISCORD_TOKEN not set. Cannot start the bot.")
        return
    await asyncio.gather(
        bot.start(os.getenv("DISCORD_TOKEN")),
        start_health_server()
    )

if __name__ == "__main__":
    asyncio.run(main())