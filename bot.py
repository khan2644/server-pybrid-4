from telethon import TelegramClient, events, Button
import requests
import random

# Telegram API credentials
api_id = 27126070
api_hash = '2736a5470b54818cd301d0cd088eb8f2'
bot_token = '7685145117:AAEQGaF9IgcAqJ4CqJ7DVv1twPIEVsEBN8U'

# Affiliaters API Token
API_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2ODRkNjc5OGY3ZDZiM2I0ZDczOTY2MWEiLCJlYXJua2FybyI6IjQzOTM4NDAiLCJpYXQiOjE3NDk5ODc1NzV9.pwRjmRedcXdNR7H0n2MJ-fkvHsW7-VoycX708wsHrgI'

DEST_CHANNEL = 'GalaxyZmart'

AI_REPLIES = [
    "Welcome bhai! 🔥 Apka personal assistant hoon.",
    "Aap bas link do, main convert karke dunga 😄",
    "Affiliate link chahiye? Paste your link ✅",
    "Kya dhoond rahe ho? Deal bana deta hoon 😎",
    "Apka bhai Zaid ka bot tayar hai, link bhejo!"
]

client = TelegramClient('affiliate_session', api_id, api_hash).start(bot_token=bot_token)

# Affiliate link conversion
def convert_affiliate_link(text):
    url = "https://ekaro-api.affiliaters.in/api/converter/public"
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {"deal": text, "convert_option": "convert_only"}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") == 1:
                return data.get("data")
    except Exception as e:
        print(f"API Error: {e}")
    return None

# Main message handler
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    text = event.raw_text

    if 'http://' in text or 'https://' in text:
        converted = convert_affiliate_link(text)
        if converted:
            await event.reply(
                f"✅ Bhai ye rahi tumhari affiliate link:\n{converted}\n\n👀 Kya isko apne channel par post karein?",
                buttons=[
                    [Button.inline("✅ Haan Post Karo", data=f"yes|{converted}"),
                     Button.inline("❌ Nahi Bhai", data="no")]
                ]
            )
        else:
            await event.reply("❌ Maaf karna bhai! Link convert nahi hua.")
    else:
        reply = random.choice(AI_REPLIES)
        await event.reply(reply)

# Handle button click
@client.on(events.CallbackQuery)
async def callback(event):
    data = event.data.decode("utf-8")
    if data.startswith("yes|"):
        _, link = data.split("|", 1)
        await client.send_message(DEST_CHANNEL, f"🔗 Auto-Posted Link:\n{link}")
        await event.edit("✅ Post channel pe kar diya gaya!")
    elif data == "no":
        await event.edit("❌ Theek hai bhai, post nahi kiya.")

print("🚀 Zaid Bhai Bot Ready Always...")
client.run_until_disconnected()