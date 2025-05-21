import discord
from discord.ext import commands
import random
import json
import os

bot = commands.Bot(command_prefix="!")

roleplay_responses = {
    "assfuck": [
        "{user} is gripping {target}'s hips tight, slamming into your ass with deep, relentless thrusts. 😈",
        "{target}, {user} is fucking your ass hard, each stroke making your body shake with pleasure. 🔥",
        "{user} is pinning {target} down, pounding your tight ass while you moan uncontrollably. 💦",
        "{target}, {user} is driving into your ass, their hands squeezing you as you beg for more. 😏",
        "{user} is taking {target}'s ass with raw passion, every thrust pushing you closer to the edge. 🔥",
        "{target}, {user} is owning your ass, their rhythm so intense you’re trembling with every hit. 😈",
        "{user} is fucking {target}'s ass slow then fast, making you gasp as you feel every inch. 💋"
    ],
    "facefuck": [
        "{user} is holding {target}'s head, thrusting deep into your mouth, making your eyes water. 😈",
        "{target}, {user} is fucking your face, their cock hitting the back of your throat. 🔥",
        "{user} is gripping {target}'s hair, pushing their dick deeper as you gag with pleasure. 💦",
        "{target}, {user} is using your mouth, each thrust making your lips quiver. 😏",
        "{user} is facefucking {target} with intensity, your moans muffled by their cock. 🔥",
        "{target}, {user} is dominating your face, their thrusts relentless as you take it all. 😈"
    ],
    "squirt": [
        "{user} is fingering {target} so good, you’re squirting all over, soaking everything. 😈",
        "{target}, {user} is making your pussy gush, your body shaking as you squirt hard. 🔥",
        "{user} is eating {target}'s pussy, pushing you to squirt with every flick of their tongue. 💦",
        "{target}, {user} is driving you wild, your juices squirting as you scream their name. 😏",
        "{user} is fucking {target} so deep, you can’t hold back, squirting uncontrollably. 🔥",
        "{target}, {user} is teasing your clit, making you squirt in waves of pleasure. 😈"
    ],
    "dickslap": [
        "{user} is slapping {target}'s face with their hard cock, teasing you with every naughty smack. 😈",
        "{target}, {user} is dickslapping your cheeks, your lips parted, begging for more. 🔥",
        "{user} is playfully smacking {target}'s face with their dick, making you blush. 💦",
        "{target}, {user} is tapping their cock on your face, each slap driving you wild. 😏",
        "{user} is dickslapping {target}, your eyes locked on them as you crave it. 🔥",
        "{target}, {user} is teasing you with cock slaps, making your face tingle with desire. 😈"
    ],
    "creampie": [
        "{user} is filling {target}'s pussy with hot cum, leaving you dripping and satisfied. 😈",
        "{target}, {user} is pumping their load deep inside you, your pussy overflowing. 🔥",
        "{user} is thrusting into {target}, cumming hard, filling you with every drop. 💦",
        "{target}, {user} is creampieing you, their warm cum leaking out as you moan. 😏",
        "{user} is burying their cock in {target}, unloading a creamy mess inside you. 🔥",
        "{target}, {user} is leaving a thick creampie in you, your body trembling with pleasure. 😈"
    ],
    "fuck": [
        "{user} is fucking {target} senseless, your pussy clenching around their cock. 😈",
        "{target}, {user} is pounding you hard, each thrust hitting all the right spots. 🔥",
        "{user} is slamming into {target}, your moans echoing as they fuck you deep. 💦",
        "{target}, {user} is railing you, their cock stretching you with every move. 😏",
        "{user} is fucking {target} with wild abandon, your body shaking with pleasure. 🔥",
        "{target}, {user} is taking you hard, fucking you until you can’t think straight. 😈"
    ],
    "pussyrub": [
        "{user} is rubbing {target}'s pussy, teasing your clit with slow, sensual circles. 🔥",
        "{target}, {user} is sliding their fingers over your wet pussy, making you moan. 😈",
        "{user} is gently rubbing {target}'s clit, your hips bucking against their hand. 💦",
        "{target}, {user} is playing with your pussy, their touch driving you crazy. 😏",
        "{user} is massaging {target}'s pussy, your juices coating their fingers. 🔥",
        "{target}, {user} is teasing your clit, rubbing you until you’re trembling. 😈"
    ],
    "69": [
        "{user} and {target} are in a steamy 69, your mouths working each other’s sensitive spots. 😈",
        "{target}, {user} is licking your pussy while you suck their cock, both of you moaning. 🔥",
        "{user} is eating {target} out in 69, your tongue teasing their dick in return. 💦",
        "{target}, you and {user} are locked in 69, your bodies trembling with mutual pleasure. 😏",
        "{user} is devouring {target}'s pussy in 69, while you take their cock deep. 🔥",
        "{target}, {user} is in 69 with you, both of you lost in each other’s taste. 😈"
    ],
    "cumshot": [
        "{user} is shooting their load all over {target}'s face, leaving you sticky and satisfied. 😈",
        "{target}, {user} is cumming hard, their hot cum splattering across your body. 🔥",
        "{user} is unloading on {target}, their cum dripping down your chest. 💦",
        "{target}, {user} is giving you a massive cumshot, covering you in their release. 😏",
        "{user} is spraying {target} with cum, your skin glistening with their load. 🔥",
        "{target}, {user} is exploding over you, their cumshot leaving you marked. 😈"
    ],
    "boobsuck": [
        "{user} is sucking {target}'s nipples, their tongue swirling over your sensitive tits. 😈",
        "{target}, {user} is latched onto your boobs, sucking hard as you moan. 🔥",
        "{user} is teasing {target}'s nipples with their mouth, making your body arch. 💦",
        "{target}, {user} is worshipping your tits, their lips tugging at your nipples. 😏",
        "{user} is sucking {target}'s boobs, your gasps filling the air with every lick. 🔥",
        "{target}, {user} is devouring your nipples, sending shivers through you. 😈"
    ],
    "boobsgrab": [
        "{user} is grabbing {target}'s tits, squeezing them firmly as you gasp. 😈",
        "{target}, {user} is groping your boobs, their hands kneading your soft curves. 🔥",
        "{user} is cupping {target}'s breasts, teasing your nipples with their thumbs. 💦",
        "{target}, {user} is holding your tits, their grip making you squirm. 😏",
        "{user} is fondling {target}'s boobs, your body responding to every touch. 🔥",
        "{target}, {user} is squeezing your breasts, driving you wild with desire. 😈"
    ],
    "cum": [
        "{user} is making {target} cum hard, your body shaking as you release. 😈",
        "{target}, {user} is pushing you over the edge, your orgasm crashing through you. 🔥",
        "{user} is teasing {target} until you cum, your moans filling the air. 💦",
        "{target}, {user} is driving you to climax, your body trembling with pleasure. 😏",
        "{user} is making {target} explode in ecstasy, your cum soaking everything. 🔥",
        "{target}, {user} is bringing you to a shuddering orgasm, leaving you breathless. 😈"
    ],
    "leash": [
        "{user} is tugging {target}'s leash, pulling you closer as you obey. 😈",
        "{target}, {user} is holding your leash tight, guiding you with every yank. 🔥",
        "{user} is leading {target} by the leash, your body eager to please them. 💦",
        "{target}, {user} is controlling you with a leash, making you their pet. 😏",
        "{user} is pulling {target}'s leash, your submission turning them on. 🔥",
        "{target}, {user} is dominating you with a leash, every tug making you shiver. 😈"
    ],
    "handjob": [
        "{user} is stroking {target}'s cock, their hand gliding over your hard shaft. 😈",
        "{target}, {user} is giving you a handjob, their grip tight and teasing. 🔥",
        "{user} is jerking {target} off, your dick throbbing in their skilled hand. 💦",
        "{target}, {user} is working your cock, their strokes driving you wild. 😏",
        "{user} is giving {target} a slow, sensual handjob, making you beg for release. 🔥",
        "{target}, {user} is pumping your dick, your moans growing louder. 😈"
    ],
    "dickride": [
        "{user} is riding {target}'s cock, bouncing hard as you fill them up. 😈",
        "{target}, {user} is grinding on your dick, their pussy gripping you tight. 🔥",
        "{user} is sliding up and down {target}'s shaft, moaning with every thrust. 💦",
        "{target}, {user} is riding you like a pro, their hips rocking against you. 😏",
        "{user} is bouncing on {target}'s cock, your dick hitting all their spots. 🔥",
        "{target}, {user} is taking your dick deep, riding you until you both cum. 😈"
    ],
    "facesit": [
        "{user} is sitting on {target}'s face, grinding their pussy against your mouth. 😈",
        "{target}, {user} is smothering you with their wet pussy, your tongue buried inside. 🔥",
        "{user} is riding {target}'s face, their juices dripping as you lick eagerly. 💦",
        "{target}, {user} is facesitting you, their thighs clamping around your head. 😏",
        "{user} is grinding on {target}'s tongue, moaning as you worship their pussy. 🔥",
        "{target}, {user} is dominating you with their pussy, facesitting you into bliss. 😈"
    ],
    "pussyeat": [
        "{user} is eating {target}'s pussy, their tongue flicking your clit with precision. 😈",
        "{target}, {user} is devouring your pussy, making you squirm with every lick. 🔥",
        "{user} is buried between {target}'s thighs, sucking your clit until you scream. 💦",
        "{target}, {user} is licking your pussy, their mouth driving you to the edge. 😏",
        "{user} is feasting on {target}'s pussy, your moans filling the air. 🔥",
        "{target}, {user} is eating you out, their tongue sending you into ecstasy. 😈"
    ],
    "spank": [
        "{user} is slapping {target}'s ass, each spank sending a jolt to your pussy. 🔥",
        "{target}, {user} is spanking you hard, your cheeks glowing red with every hit. 😈",
        "{user} is bending {target} over, delivering sharp spanks that make you squirm. 💦",
        "{target}, {user} is smacking your ass, each strike leaving you begging for more. 😏",
        "{user} is spanking {target} with a wicked grin, your moans filling the air. 🔥",
        "{target}, {user} is punishing your ass with firm, teasing slaps. 😈",
        "{user} is giving {target}'s ass a playful yet firm spank, making you shiver. 💋"
    ],
    "tittyfuck": [
        "{user} is sliding their cock between {target}'s tits, your boobs squeezing them tight. 😈",
        "{target}, {user} is tittyfucking you, their dick gliding through your soft breasts. 🔥",
        "{user} is thrusting between {target}'s boobs, your cleavage perfect for them. 💦",
        "{target}, {user} is fucking your tits, their cock throbbing against your skin. 😏",
        "{user} is using {target}'s breasts, tittyfucking you with slow, teasing thrusts. 🔥",
        "{target}, {user} is lost in your tits, their dick pulsing as they fuck them. 😈"
    ],
    "bondage": [
        "{user} is tying {target} up, ropes binding your wrists as you surrender. 😈",
        "{target}, {user} is wrapping you in bondage, your body helpless under their control. 🔥",
        "{user} is securing {target} with ropes, your skin tingling with every knot. 💦",
        "{target}, {user} is binding you tight, your submission turning them on. 😏",
        "{user} is restraining {target} in bondage, your body exposed for their pleasure. 🔥",
        "{target}, {user} is dominating you with ropes, every tie making you theirs. 😈"
    ],
    "blowjob": [
        "{user} is guiding {target}'s head, your lips wrapping tightly around their throbbing cock. 😈",
        "{target}, {user} is moaning as you suck them deep, your tongue teasing every inch. 🔥",
        "{user} is thrusting gently into {target}'s mouth, your warm wetness driving them wild. 💦",
        "{target}, {user} is watching you kneel, your mouth working their dick with skill. 😏",
        "{user} is tangling their fingers in {target}'s hair, loving every second of your blowjob. 🔥",
        "{target}, {user} is groaning as you take their cock deeper, your lips so perfect. 😈",
        "{user} is shivering as {target}'s tongue swirls around their tip, begging for more. 💋"
    ],
    "assgrab": [
        "{user} is grabbing {target}'s ass, their hands squeezing your cheeks firmly. 😈",
        "{target}, {user} is groping your ass, their fingers digging into your soft flesh. 🔥",
        "{user} is smacking and grabbing {target}'s ass, making you gasp with every touch. 💦",
        "{target}, {user} is holding your ass tight, their grip sending shivers through you. 😏",
        "{user} is fondling {target}'s ass, your curves driving them wild. 🔥",
        "{target}, {user} is squeezing your ass, teasing you with every naughty grab. 😈"
    ],
    "finger": [
        "{user} is fingering {target}'s pussy, their fingers curling inside you perfectly. 😈",
        "{target}, {user} is sliding their fingers deep into your wet pussy, making you moan. 🔥",
        "{user} is teasing {target}'s clit with their fingers, your body trembling. 💦",
        "{target}, {user} is fingering you hard, their fingers hitting all your spots. 😏",
        "{user} is working {target}'s pussy with their fingers, driving you to the edge. 🔥",
        "{target}, {user} is exploring your pussy with their fingers, your juices flowing. 😈"
    ],
    "footjob": [
        "{user} is rubbing {target}'s cock with their feet, teasing you with every stroke. 😈",
        "{target}, {user} is giving you a footjob, their toes curling around your dick. 🔥",
        "{user} is sliding their feet over {target}'s shaft, making you throb with pleasure. 💦",
        "{target}, {user} is using their feet to jerk you off, driving you wild. 😏",
        "{user} is teasing {target}'s cock with their soft feet, your moans filling the air. 🔥",
        "{target}, {user} is giving you a naughty footjob, your dick pulsing under their toes. 😈"
    ],
    "masturbate": [
        "{user} is masturbating in front of {target}, their hand working their cock/pussy fast. 😈",
        "{target}, {user} is touching themselves, their moans making you hot and bothered. 🔥",
        "{user} is pleasuring themselves for {target}, their body trembling with every stroke. 💦",
        "{target}, {user} is masturbating, their eyes locked on you as they cum. 😏",
        "{user} is rubbing themselves in front of {target}, driving you wild with their show. 🔥",
        "{target}, {user} is getting off for you, their climax leaving you speechless. 😈"
    ]
}

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
    "masturbate": "1374769888442187926"
}

def save_urls(gif_urls):
    with open("gif_urls.json", "w") as f:
        json.dump(gif_urls, f, indent=4)

def load_urls():
    if os.path.exists("gif_urls.json"):
        with open("gif_urls.json", "r") as f:
            return json.load(f)
    return {cmd: [] for cmd in roleplay_responses.keys()}

gif_urls = load_urls()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    for command, channel_id in channel_map.items():
        if str(message.channel.id) == channel_id:
            for attachment in message.attachments:
                if attachment.filename.endswith((".gif", ".png", ".jpg", ".jpeg")):
                    if command not in gif_urls:
                        gif_urls[command] = []
                    if attachment.url not in gif_urls[command]:
                        gif_urls[command].append(attachment.url)
                        save_urls(gif_urls)
                        await message.channel.send(f"Added {attachment.filename} to {command} GIFs!")
                    break
    await bot.process_commands(message)

def is_nsfw_channel():
    async def predicate(ctx):
        if not ctx.channel.nsfw:
            await ctx.send("This command can only be used in NSFW channels! 🔞")
            return False
        return True
    return commands.check(predicate)

def create_roleplay_command(command_name):
    async def roleplay_command(ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(f"Please mention someone to {command_name}! 😊")
            return
        response = random.choice(roleplay_responses[command_name]).format(user=ctx.author.mention, target=member.mention)
        embed = discord.Embed(
            title=f"{command_name.capitalize()}! 🔥",
            description=response,
            color=discord.Color.red()
        )
        if gif_urls.get(command_name) and len(gif_urls[command_name]) > 0:
            gif = random.choice(gif_urls[command_name])
            embed.set_image(url=gif)
        else:
            embed.set_footer(text="No GIFs found for this command!")
            embed.set_image(url="https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif")
        await ctx.send(embed=embed)
    roleplay_command.__name__ = command_name
    return roleplay_command

for cmd in roleplay_responses.keys():
    bot.command(aliases=[cmd])(is_nsfw_channel()(create_roleplay_command(cmd)))

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready and online!")

bot.run(os.getenv("DISCORD_TOKEN"))