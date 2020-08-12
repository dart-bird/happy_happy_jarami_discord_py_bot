import discord
import time
import random
import requests
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
prefix = "!"

class rspData():
    rsp_author = []
    currentChannel = None
    serverName = ""
    dmChannel_1 = None
    dmChannel_2 = None
    gameResultStr = ""

rd = rspData()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user:
            return
            
        if message.content.startswith('%shelp' % prefix):
            randomMsg = random.randint(0,3)
            if randomMsg == 3:
                await message.channel.send('나는 너한테 아낌없이 주는데 나한테 주는게 없다니 ,,,, 안알려줌')
                return
            elif randomMsg== 2:
                await message.channel.send('안알려줌')
                return
            elif randomMsg == 2:
                await message.channel.send('왜 싫어')
                return
            elif randomMsg == 1:
                await message.channel.send('?')
                return
            else:
                embedVar = discord.Embed(title="나는야 나무", description="아낌없이 주는 자람이야.\n 아래와 같이 명령어를 사용해볼래?", color=0x00ff00)
                embedVar.add_field(name="%shelp"%prefix, value="지금 보는 것 처럼 내가 할 수 있는 일을 알 수 있지!", inline=False)
                embedVar.add_field(name="%srsp"%prefix, value="친구 두명을 @멘션 하면 내가 가위바위보 심판을 할 수 있어\n`%srsp @닉네임 @닉넹임 start`"%prefix, inline=False)
                embedVar.add_field(name="%s너의전적은?"%prefix, value="롤 닉네임을 검색해서 전적조회가 가능해\n`%s너의전적은? 롤닉네임`"%prefix, inline=False)
                embedVar.add_field(name="%s실검"%prefix, value="네이버 실시간 검색어를 불러와요.\n`%s실검`"%prefix, inline=False)
                embedVar.add_field(name="잠수누구인가?", value="오프라인 사람들 호출\n`잠수누구인가?`", inline=False)
                await message.channel.send(embed=embedVar)

        if message.content.startswith('%shello' % prefix):
            await message.channel.send('Hello!')
        
        cmd = "너의전적은?"
        if message.content.startswith(prefix + cmd):

            args = message.content[len(prefix+cmd):].strip()
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
            summonerName = urllib.parse.quote(args)
            req = urllib.request.urlopen(url="http://www.op.gg/summoner/userName=%s" % summonerName)

            data = req.read()
            
            soup = BeautifulSoup(data, "html.parser")
            rankType = soup.find('div', class_='RankType').text
            tierRank = soup.find('div', class_='TierRank').text.strip()
            if tierRank =="Unranked":
                level = soup.find('span', class_='Level').text
                embedVar = discord.Embed(title="너의 롤 전적은?", description="롤 전적으로 보여줘요\n\n언랭이네요. 랭크좀 돌리세요,,,\n레벨이라도 알려드릴게요.", color=0x00ff00)
                embedVar.add_field(name="레벨", value=level, inline=False)
                await message.channel.send(embed=embedVar)
                return
            leaguePoints = soup.find('span', class_='LeaguePoints').text
            wins = soup.find('span', class_='wins').text
            losses = soup.find('span', class_='losses').text
            winratio = soup.find('span', class_='winratio').text
        
            summonerInfo = (rankType, tierRank, leaguePoints, wins, losses, winratio)
            summonerInfoNames = ("랭크 타입", "랭크 티어", "LP", "승리 횟수", "패배 횟수", "승률")
            embedVar = discord.Embed(title="너의 롤 전적은?", description="롤 전적으로 보여줘요\n\n", color=0x00ff00)

            for idx in range(len(summonerInfo)):
                embedVar.add_field(name=summonerInfoNames[idx], value=summonerInfo[idx], inline=False)
            
            await message.channel.send(embed=embedVar)

        if message.content.startswith('%s실검' % prefix):
             
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
            
            html = requests.get('https://datalab.naver.com/keyword/realtimeList.naver?age=all', headers = headers)
            
            soup = BeautifulSoup(html.content, 'html.parser')
            titles = soup.find_all("span", {"class": "item_title"})
            naver_ranked = ""
            links =""

            for idx in range(len(titles)):
                naver_ranked += "["+str(idx+1)+"] "+ titles[idx].get_text() + "\n"
                links +="[link]" + "https://search.naver.com/search.naver?where=nexearch&query=" + str(urllib.parse.quote(str(titles[idx].get_text())))+ "\n"
                
            embedVar = discord.Embed(title="실검에 오를 것이다~", description="요즘 핫한 키워드를 보여줘요", color=0x00ff00)
            embedVar.add_field(name="네이버 실시간 검색어", value=naver_ranked, inline=False)

            embedVar2 = discord.Embed(title="실검에 오를 것이다~", description="요즘 핫한 키워드를 보여줘요", color=0x00ff00)
            for idx in range(len(titles)):
                naver_ranked = "["+str(idx+1)+"] "+ titles[idx].get_text()
                link ="[link] " + "https://search.naver.com/search.naver?where=nexearch&query=" + str(urllib.parse.quote(str(titles[idx].get_text())))
                embedVar2.add_field(name=naver_ranked, value=link, inline=False)

            await message.channel.send(embed=embedVar)
            await message.channel.send(embed=embedVar2)

        if message.content.startswith('잠수누구인가?'):
            sleep_members = []
            tmpStr = ""
            
            for member in client.get_all_members():
                
                if str(member.status) == "offline":
                    if member.bot == True:
                        continue
                    sleep_members.append(member.id)

            for sleep_member in sleep_members:
                tmpStr += "<@!" + str(sleep_member) + "> "

            embedVar = discord.Embed(title="지금 누가 쿨쿨 자고있나?", description="자고 있는 사람 누구인가?", color=0x00ff00)
            embedVar.set_image(url="https://pds.joins.com/news/component/htmlphoto_mmdata/201904/23/29e0472f-b406-4bab-aab5-764b643fc012.jpg")
            embedVar.add_field(name="관심법", value="보아하니 %s 자고 있구만" %tmpStr, inline=False)
            await message.channel.send(embed=embedVar)
            await message.channel.send(file=discord.File('yellow.jpg'))

        if message.content.startswith('%srsp' % prefix):
            args = message.content.split(' ')[1:]
            rsp_s = ('가위','찌','시저','씨저')
            rsp_r = ('바위','롹','주먹','돌','락','묵')
            rsp_p = ('보','페이퍼','보자기','빠','종이')
            try:
                author = message.author

                tmpArgs = []
                for arg in args:
                    if arg != " ":
                        tmpArgs.append(arg)
                args = tmpArgs
                
                if len(args) == 3 and str(args[2]) == "start":
                    rd.currentChannel = client.get_channel(id=message.channel.id) # 계속해서 알림을 보낼 채널 ID 받아오기
                    rd.serverName = message.guild # 서버이름 저장
                    
                    tmpStr = (str(rsp_r)+str(rsp_s)+str(rsp_p)).replace(")",", ").replace("(","")
                    tmpStr = tmpStr[0:len(tmpStr)-2].replace("'","")

                    for member in message.guild.members:
                        if str(args[0]) == '<@!'+str(member.id)+'>':
                            rd.dmChannel_1 = client.get_user(member.id)
                            await rd.dmChannel_1.send('게임을 시작하지, 가위, 바위, 보 중 하나를 입력하시오.'+'`'+tmpStr+'`'+' **사용가능**')
                    for member in message.guild.members:
                        if str(args[1]) == '<@!'+str(member.id)+'>':
                            rd.dmChannel_2 = client.get_user(member.id)
                            await rd.dmChannel_2.send('게임을 시작하지, 가위, 바위, 보 중 하나를 입력하시오.'+'`'+tmpStr+'`'+' **사용가능**')
                            return
                    return
                if message.guild == rd.serverName:
                    await message.channel.send("노노 여기서는 안돼~")
                    return
                if len(args) == 0:
                    await message.channel.send("가위, 바위, 보 중에 하나를 입력하세요~"+'`'+tmpStr+'`'+' **사용가능**') 
                    return
                if args[0] in rsp_s or args[0] in rsp_r or args[0] in rsp_p: # prefix + rsp2 가위 | 바위 | 보
                    if len(rd.rsp_author) <= 2:
                        rd.rsp_author.append([author.id,args[0]])
                        await message.channel.send('<가위 바위 보 게임>\n'+'<@!'+str(author.id)+'>'+' 참여 완료!')
                        await rd.currentChannel.send('<가위 바위 보 게임>\n'+'<@!'+str(author.id)+'>'+' 참여 완료!')
                    
                        if len(rd.rsp_author) == 2:
                            await rd.dmChannel_1.send("과연 결과는 ? 두구두구두구두구")
                            await rd.dmChannel_2.send("과연 결과는 ? 두구두구두구두구")
                            await rd.currentChannel.send("과연 결과는 ? 두구두구두구두구")

                            for count in range(3, 0, -1):
                                time.sleep(1)
                                await rd.dmChannel_1.send(count)
                                await rd.dmChannel_2.send(count)
                                await rd.currentChannel.send(count)

                            player_1 = rd.rsp_author[0]
                            player_2 = rd.rsp_author[1]

                            if player_1[1] in rsp_s:
                                if player_2[1] in rsp_r:
                                    rd.gameResultStr = '<@!'+ str(player_1[0]) + '> ('+ player_1[1] +') **패**, <@!'+ str(player_2[0])+ '> (' + player_2[1] +') **승**'
                                elif player_2[1] in rsp_p:
                                    rd.gameResultStr = '<@!'+ str(player_1[0]) + '> ('+ player_1[1] +') **승**, <@!'+ str(player_2[0])+ '> (' + player_2[1] +') **패**'
                                elif player_2[1] in rsp_s:
                                    rd.gameResultStr = '<@!'+ str(player_1[0]) + '> ('+ player_1[1] +') <@!'+ str(player_2[0])+ '> (' + player_2[1] +') 아이쿠, **비겼네** ... 다시!'
                            if player_1[1] in rsp_r:
                                if player_2[1] in rsp_p:
                                    rd.gameResultStr = '<@!'+ str(player_1[0]) + '> ('+ player_1[1] +') **패**, <@!'+ str(player_2[0]) + '> (' + player_2[1] +') **승**'
                                elif player_2[1] in rsp_s:
                                    rd.gameResultStr ='<@!'+ str(player_1[0]) + '> ('+ player_1[1] +') **승**, <@!'+ str(player_2[0]) + '> (' + player_2[1] +') **패**'
                                elif player_2[1] in rsp_r:
                                    rd.gameResultStr ='<@!'+ str(player_1[0]) + '> ('+ player_1[1] +') <@!'+ str(player_2[0])+'> (' + player_2[1] +') 아이쿠, **비겼네** ... 다시!'
                            if player_1[1] in rsp_p:
                                if player_2[1] in rsp_s:
                                    rd.gameResultStr = '<@!'+ str(player_1[0]) + '> ('+ player_1[1] +') **패**, <@!'+ str(player_2[0]) + '> (' + player_2[1] +') **승**'
                                elif player_2[1] in rsp_r:
                                    rd.gameResultStr ='<@!'+ str(player_1[0]) + '> ('+ player_1[1] +') **승**, <@!'+ str(player_2[0]) + '> (' + player_2[1] +') **패**'
                                elif player_2[1] in rsp_p:
                                    rd.gameResultStr ='<@!'+ str(player_1[0]) + '> ('+ player_1[1] +') <@!'+ str(player_2[0]) + '> (' + player_2[1] +') 아이쿠, **비겼네** ... 다시!'

                            embedVar = discord.Embed(title="🎮🎮 가위바위보 게임 결과 ✌️ ✊ ✋", description=" :tada: :tada: ~ 축하드립니다 ~ :tada: :tada: \n%s"%rd.gameResultStr, color=0x00ff00)

                            await rd.dmChannel_1.send(embed = embedVar)
                            await rd.dmChannel_2.send(embed = embedVar)
                            await rd.currentChannel.send(embed = embedVar)
                            rd.rsp_author = []
                else:
                    await message.channel.send("가위, 바위, 보 중에 하나를 입력하세요~ 다른건 안돼요~"+'`'+tmpStr+'`'+'**사용가능**')
            except Exception as e:
                print(e)
                await rd.dmChannel_1.send("예외가 발생했어요.")
                await rd.dmChannel_2.send("예외가 발생했어요.")
                await rd.currentChannel.send("예외가 발생했어요.")



client = MyClient()
client.run('your token')