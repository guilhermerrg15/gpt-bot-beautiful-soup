import discord
import requests as req
from bs4 import BeautifulSoup
import json

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
API_KEY = "YOUR_OPENAI_API_KEY"
headers = {
  "Authorization": f"Bearer {API_KEY}",
  "Content-Type": "application/json"
}
link = "https://api.openai.com/v1/chat/completions"
model_id = "gpt-3.5-turbo"

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f"{client.user} is running!")


@client.event
async def on_message(msg):
  if msg.author == client.user:
    return

  user_msg = msg.content.lower()

  if "hi" in user_msg:
    await msg.channel.send("what's up!")

  if "!webscraping" in user_msg:
    url = "https://www.worldsurfleague.com/"
    response = req.get(url)
    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
      surfers = soup.find_all("div", {"class": "avatar-text-primary"})

      surfer_names = [surfer.text for surfer in surfers]
      if surfer_names:
        await msg.channel.send("Surfer names:")
        for name in surfer_names:
          await msg.channel.send(name)
      else:
        await msg.channel.send("No surfer found.")
    else:
      await msg.channel.send("Error accessing the website")

  if "!gpt3" in user_msg:
    user_input = user_msg.replace("!gpt3", "").strip()
    if user_input:
      body = {
        "model": model_id,
        "messages": [{
          "role": "user",
          "content": user_input
        }]
      }
      body = json.dumps(body)

      req_gpt = req.post(link, headers=headers, data=body)

      if req_gpt.status_code == 200:
        resp_gpt = req_gpt.json()
        message = resp_gpt["choices"][0]["message"]["content"]
        await msg.channel.send(message)
      else:
        await msg.channel.send("Error processing the request.")
    else:
      await msg.channel.send("Please provide input for GPT-3.")

  req_body = {
    "authorName": msg.author.name,
    "msgContent": msg.content,
    "createdAt": str(msg.created_at)
  }
  response = req.post("https://your-log-endpoint.com/logs", json=req_body)

  if response.status_code == 200:
    print("Log successfully recorded!")
  else:
    print("Error in logging!")


client.run(TOKEN)
