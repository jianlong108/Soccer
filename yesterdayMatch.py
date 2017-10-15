#!/usr/bin/env python
# -*- coding: utf-8 -*-


from SendMail import *
from DBHelper import *

import pycurl
import StringIO
import getHandiOrignalTime
import SoccerRound
import time

import sys

reload(sys)
sys.setdefaultencoding('utf-8')



"""
全局变量定义
"""

AllGames = []
AllBeginTimes = []

'''
主函数
'''
def getYesterdaySoccer(timestr):
    try:
        url = "http://121.10.245.46:8072/phone/scheduleByDate.aspx?an=iosQiuTan&av=6.4&date=" + timestr + '&from=1&kind=3&r=1503367511&subversion=3'
# 'http://121.10.245.46:8072/phone/scheduleByDate.aspx?an=iosQiuTan&av=6.4&date=2017-08-21&from=1&kind=3&r=1503367511&subversion=3'

        print url
    except:
        pass
    c = pycurl.Curl()

    c.setopt(pycurl.URL, url)

    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.perform()
    resultStr = b.getvalue().decode('utf8')

    global AllGames
    global AllBeginTimes

    if resultStr != '':
        # print resultStr
        allArray = resultStr.split('$$')
        leagueStr = ''
        if type == 1:
            leagueStr = allArray[0]
        else:
            leagueStr = allArray[1]

        allLeague = leagueStr.split('!')
        dic = {}
        locationstr = os.path.join(os.path.abspath('.'), 'league.txt')
        leaguelistfile = open(locationstr, 'r+')
        for league in allLeague:
            oneLeague = league.split('^')
            dic[oneLeague[1]] = oneLeague[0]
            # leaguelistfile.write('%s:%s\n'%(oneLeague[1],oneLeague[0]))
        leaguelist = leaguelistfile.readlines()
        # return
        if type == 1:
            gameStr = allArray[1]
        else:
            gameStr = allArray[2]

        games = gameStr.split('!')
        for game in games:
            tempstr_utf_8 =  game.encode('utf-8')
            onegame = FootballGame()
            oneGameArray = tempstr_utf_8.split('^')
            # 0.soccerid
            # 1.联赛id
            # 2. - 1
            # 3.开赛时间
            # 4.下半场开赛时间
            # 5.主队
            # 6.客队
            # 7.主队比分
            # 8.客队比分
            # 9.主队半场比分
            # 10.客队半场比分
            # 11.主队红牌个数
            # 12.客队红牌个数
            # 13.主队黄牌个数
            # 14.客队黄牌个数
            # 15.盘口
            # 赔率
            # 16 胜
            # 17 平
            # 18 负
            try:
                onegame.soccerID = int(oneGameArray[0])
                onegame.leauge = dic.get(oneGameArray[1].encode('utf-8'))
                flag = False
                for leaguestr in leaguelist:
                    if onegame.leauge in leaguestr:
                        flag = True

                if flag is False:
                    continue

                beginTime = oneGameArray[3].encode('utf-8')
                onegame.beginTime = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[
                                                                                                         8:10] + ':' + beginTime[
                                                                                                                       10:12]

                briefTimeStr = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[
                                                                                                    8:10] + ':' + beginTime[
                                                                                                                  10:12]
                if briefTimeStr not in AllBeginTimes:
                    AllBeginTimes.append(briefTimeStr)

                onegame.homeTeam = oneGameArray[5]
                onegame.friendTeam = oneGameArray[6]
                onegame.allHome = int(oneGameArray[7])
                onegame.allFriend = int(oneGameArray[8])
                onegame.halfHome = int(oneGameArray[9])
                onegame.halfFriend = int(oneGameArray[10])

                if oneGameArray[15] != '' and oneGameArray[15] is not None:
                    onegame.bet365Handi = float(oneGameArray[15])
            except ValueError as e:
                onegame = None
                print  e

            except BaseException, e:
                onegame = None
                print e
            else:
                AllGames.append(onegame)
                onegame.oddCompanies = SoccerRound.getOneGameODD(onegame)
                onegame.handiCompanies = SoccerRound.getOneGameHandi(onegame)
                Ori_Handi_result = getHandiProbability(onegame,True)
                Now_Handi_result = getnowHandiProbability(onegame,True)
                Ori_Odd_result = getOrignalODDProbability(onegame,True)
                Now_Odd_result = getnowHandiProbability(onegame,True)

                result_locationstr = os.path.join('/Users/dalong/Desktop', '%s-result.txt' % (timestr,))
                result_leaguelistfile = open(result_locationstr, 'a')
                if Ori_Handi_result[0] > 60 or Ori_Handi_result[1] > 60 or Ori_Handi_result[2] > 60 or Now_Handi_result[0] > 60  or Now_Handi_result[1] > 60 or Now_Handi_result[2] > 60 or Ori_Odd_result[0] > 60  or Ori_Odd_result[1] > 60 or Ori_Odd_result[2] > 60  or Now_Odd_result[0] > 60  or Now_Odd_result[1] > 60 or Now_Odd_result[2] > 60:
                    result_leaguelistfile.write('%s:%s vs %s %d:%d\n初盘:  胜:%s 平:%s 负:%s\n终盘:  胜:%s 平:%s 负:%s\n初赔:  胜:%s 平:%s 负:%s\n终赔:  胜:%s 平:%s 负:%s\n\n'%(onegame.beginTime, onegame.homeTeam, onegame.friendTeam,onegame.allHome,onegame.allFriend,
                                                                                                                     str(Ori_Handi_result[0])[:5],str(Ori_Handi_result[1])[:5],str(Ori_Handi_result[2])[:5],
                                                                                                                     str(Now_Handi_result[0])[:5],str(Now_Handi_result[1])[:5],str(Now_Handi_result[2])[:5],
                                                                                                                     str(Ori_Odd_result[0])[:5],str(Ori_Odd_result[1])[:5],str(Ori_Odd_result[2])[:5],
                                                                                                                     str(Now_Odd_result[0])[:5],str(Now_Odd_result[1])[:5],str(Now_Odd_result[2])[:5],
                                                                                                                     )
                                         )


            time.sleep(1.5)

        insertGameList(AllGames)


def main():
    now = datetime.now()
    aDay = timedelta(days=-1)
    now = now + aDay
    yesterdaystr = now.strftime('%Y-%m-%d')

    getYesterdaySoccer('2017-10-12')


if __name__ == '__main__':
    main()

