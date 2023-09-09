import interactions
import json
import random
import requests
from ichingshifa import ichingshifa

#讀取token
with open("token.txt") as f:
    TOKEN = f.readline()

#籤種
fortunesticks = ["超吉", "大吉", "吉", "小吉", "吉哇哇", "微吉", "毫吉", "奈吉", "飛吉", "小凶", "凶", "平凶", "大凶", "超凶", "凶巴巴", "星爆氣流斬"]
#測試用print("1")

#傳送訊息
async def sendmsg(ctx: interactions.SlashContext, text: str):
    print('HERE', text)
    await ctx.channel.send(f"{text}")

#指令回傳
async def commandfeedback(ctx: interactions.SlashContext):
    await ctx.send("successfully conducted", ephemeral=True)


#機器人權限初始設定
bot = interactions.Client(intents=interactions.Intents.ALL)
#測試用print("2")

#機器人啟動
@bot.event
async def on_ready():
    print("bot ready!")


# 傳送指定訊息
@interactions.slash_command(description="make the bot send some message")
@interactions.slash_option(name="message", description="a", required=True, opt_type=interactions.OptionType.STRING)
async def send(ctx: interactions.SlashContext, message: str):
    print(ctx.author, "sended", message)
    await sendmsg(ctx, message)
    await commandfeedback(ctx)

@interactions.slash_command(description="draw a fortune stick")
async def fortune(ctx: interactions.SlashContext):
    poll=random.choice(fortunesticks)
    text=requests.get(url='https://textgen.cqd.tw?format=plain&size=50').content.decode('utf-8')
    RRbutton = interactions.Button(style=interactions.ButtonStyle.LINK, label="點我看詳細解籤", url="https://reurl.cc/2E0R7a")
    await ctx.send(f"今日運勢: {poll} , \n注意事項: {text}", components=[RRbutton])

@interactions.slash_command(description="show some commomly used NTHU related links")
async def usefullink(ctx: interactions.SlashContext):
    buttonSIS = interactions.Button(style=interactions.ButtonStyle.LINK, label="校務資訊系統", url="https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/index.php")
    buttonElearn = interactions.Button(style=interactions.ButtonStyle.LINK, label="Elearn", url="https://elearn.nthu.edu.tw/")
    buttonFC = interactions.Button(style=interactions.ButtonStyle.LINK, label="課程查詢", url="https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.I/JH62i001.php")
    await ctx.send(components=[buttonSIS, buttonElearn, buttonFC])

@interactions.slash_command(description="use Iching to divine")
async def ichingdivine(ctx: interactions.SlashContext):
    result = ichingshifa.Iching().bookgua_details()
    content = ""
    for text in result:
        if type(text) == str:
            content = content + "\n" + text
        elif type(text) == dict:
            for nt in text.values():
                content = content + "\n" + nt
        else:
            for nnt in text:
                content = content + "\n" + nnt
    result = content[7:]
    await ctx.send(result)



bot.start(TOKEN)