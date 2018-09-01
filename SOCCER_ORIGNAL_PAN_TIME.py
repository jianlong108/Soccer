#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time

from GetData.SOCCER_MODELS import FootballGame
from BEAUTIFUL_SOUP_HELPER import SoupHelper,getelementlistwithlabel,isTagClass
from NetWorkTools import get_resultstr_with_url



def gethandiTime(soccerid=0):

    # url = 'http://www.310win.com/info/1x2exchange.aspx?id=' + str(soccerid) + '&cids=,' + str(companyid) + ',&type=3'
    url = 'http://www.310win.com/handicap/' + str(soccerid) + '.html'

    soupInstance = SoupHelper(url)
    tablelist = soupInstance.gethtmllistwithlabel('table', {'width': '860', 'class':'socai'})
    try :
        trlist = getelementlistwithlabel(tablelist[0], 'tr')
        count = len(trlist)
        tr = trlist[count - 1]
        if isTagClass(tr):
            tdlist = tr.contents
            if len(tdlist) > 0:
                flag = tdlist[0].get_text()
                if flag.strip() != u'' and flag.strip() != u'澳门':
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    except IndexError as e:
        print url
        print e
        return False


def getTodaySoccer(soccer_type = 0):
    typeStr = ''
    if isinstance(soccer_type,int):
        typeStr = str(soccer_type)
    # type == 3 竞彩
    # type == 1 精简
    # type == 2 十四场

    url = "http://27.45.161.37:8071/phone/schedule_0_" + typeStr + ".txt?an=iosQiuTan&av=6.2&from=2&r=" + str(int(time.time()))
    # url = "http://112.91.160.49:8071/phone/schedule_0_" + str(type) + ".txt?an=iosQiuTan&av=5.9&from=2&r=1494229747"


    print url
    # c = pycurl.Curl()
    #
    # c.setopt(pycurl.URL, url)
    #
    # b = StringIO.StringIO()
    # c.setopt(pycurl.WRITEFUNCTION, b.write)
    # c.setopt(pycurl.FOLLOWLOCATION, 1)
    # c.setopt(pycurl.MAXREDIRS, 5)
    # c.perform()
    # resultStr = b.getvalue().decode('utf8')

    resultStr = get_resultstr_with_url(url)
    AllGames = []
    AllBeginTimes = []

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
        for league in allLeague:
            oneLeague = league.split('^')
            dic[oneLeague[1]] = oneLeague[0].encode('utf-8')

        gameStr = ''
        if type == 1:
            gameStr = allArray[1]
        else:
            gameStr = allArray[2]

        games = gameStr.split('!')
        firstobject = games[0]
        for game in games:
            # if game is not firstobject:
            #     continue;
            onegame = FootballGame()
            oneGameArray = game.split('^')
            oneGameArray.remove('')
            onegame.soccerID = int(oneGameArray[0])
            onegame.leauge = dic.get(oneGameArray[1])
            beginTime = oneGameArray[3].encode('utf-8')
            onegame.beginTime = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[
                                                                                                     8:10] + ':' + beginTime[
                                                                                                                   10:12]

            briefTimeStr = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[
                                                                                                8:10] + ':' + beginTime[
                                                                                                              10:12]
            if briefTimeStr not in AllBeginTimes:
                AllBeginTimes.append(briefTimeStr)

            if oneGameArray[4].isdigit() or oneGameArray[4] == '':
                onegame.homeTeam = oneGameArray[5].encode('utf-8')
                onegame.friendTeam = oneGameArray[6].encode('utf-8')
            else:
                onegame.homeTeam = oneGameArray[4].encode('utf-8')
                onegame.friendTeam = oneGameArray[5].encode('utf-8')


            # 获取开盘时间
            flag = gethandiTime(onegame.soccerID)
            if flag:
                print onegame.soccerID
                print ''.join([str(onegame.beginTime), ':', onegame.leauge, ':', onegame.homeTeam, 'vs', onegame.friendTeam])

            else:
                pass
            time.sleep(3)





if __name__ == '__main__':
    getTodaySoccer(1)