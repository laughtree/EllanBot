import interactions
import json
import random
import requests
from ichingshifa import ichingshifa
import tracemalloc

#讀取token
with open("token.txt") as f:
    TOKEN = f.readline()

#1A2B猜測次數
global guessCount
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
@interactions.listen()
async def on_ready():
    print("bot ready!")


# 傳送指定訊息
@interactions.slash_command(description="make the bot send some message")
@interactions.slash_option(name="message", description="a", required=True, opt_type=interactions.OptionType.STRING)
async def send(ctx: interactions.SlashContext, message: str):
    print(ctx.author, "sended", message)
    await sendmsg(ctx, message)
    await commandfeedback(ctx)

#運勢抽籤
@interactions.slash_command(description="draw a fortune stick")
async def fortune(ctx: interactions.SlashContext):
    poll=random.choice(fortunesticks)
    text=requests.get(url='https://textgen.cqd.tw?format=plain&size=50').content.decode('utf-8')
    RRbutton = interactions.Button(style=interactions.ButtonStyle.LINK, label="點我看詳細解籤", url="https://reurl.cc/2E0R7a")
    await ctx.send(f"今日運勢: {poll} , \n注意事項: {text}", components=[RRbutton])

#常用連結
@interactions.slash_command(description="show some commomly used NTHU related links")
async def usefullink(ctx: interactions.SlashContext):
    buttonSIS = interactions.Button(style=interactions.ButtonStyle.LINK, label="校務資訊系統", url="https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/index.php")
    buttonElearn = interactions.Button(style=interactions.ButtonStyle.LINK, label="Elearn", url="https://elearn.nthu.edu.tw/")
    buttonFC = interactions.Button(style=interactions.ButtonStyle.LINK, label="課程查詢", url="https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.I/JH62i001.php")
    await ctx.send(components=[buttonSIS, buttonElearn, buttonFC])

#易經卜卦
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


#1A2B

#遊戲開始指令(要重新一定要再打一次) /game_start
@interactions.slash_command(description="1A2B game")
async def game_start(ctx: interactions.SlashContext):
    global answer
    global guessCount
    guessCount = 0
    answer = ""
    while(len(answer)<4):
        x= str(random.randint(0,9))
        if x not in answer:
            answer = answer + x
    print(f'{ctx.author} 開始了新遊戲')
    print(f'本次題目為{answer}')
    await ctx.send(f'{ctx.author.mention} 開始了新遊戲')
    await ctx.channel.send(f"請輸入 /guess 四個數字!!")

#猜數字指令/guess XXXX
@interactions.slash_command(description="guess numbers")
@interactions.slash_option(name="arg", description="input", required=True, opt_type=interactions.OptionType.STRING)
async def guess(ctx: interactions.SlashContext, arg:str):
    global guessCount
    guessCount = guessCount +1
    answer_A =0
    answer_B =0
    for i in range(4):
        if(arg[i]==answer[i]):
            answer_A = answer_A +1 
        elif(arg[i]!=answer[i] and arg[i] in answer):
            answer_B = answer_B +1
    if answer_A==4:
        await ctx.send(f"終於答對啦!!!你總共猜了{guessCount}次")
    else :
        await ctx.send(f"{ctx.author} 猜了 {arg} {answer_A}A{answer_B}B")

@interactions.slash_command(description="search for imformation of weather")
async def weather(ctx: interactions.SlashContext):
    tracemalloc.start()
    location_select = interactions.StringSelectMenu(
        "基隆", "新北", "台北", "桃園", "新竹", "苗栗", "台中", "彰化", "雲林", "嘉義", "台南", "高雄", "屏東", "台東", "花蓮", "宜蘭", "南投", "蘭嶼", "澎湖", "金門", "馬祖", "東沙島",
        placeholder="選擇地區",
    )
    interactions.ActionRow()
    await ctx.send(components=[location_select])

#選單監聽
@interactions.listen()
async def on_select(ctx: interactions.SlashContext):
    print(ctx)

bot.start(TOKEN)