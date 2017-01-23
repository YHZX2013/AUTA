# /usr/bin/python
#coding:utf-8
import requests
import re
import hashlib
import socket
import sys
from time import sleep
import time

g_main_id = 1462

g_total_re = 3193
g_zan_re = 80

main_file = 'main.csv'
sub_file = 'sub.csv'

last_day = '2015-11-26'

split_char = ','

class paper_info:
    def __init__(self):
        self.id = 'null' #id of the author
        self.time = 'null' #time of the answer
        self.cur_time = 'null' #cur time of the log
        self.content = 'null' #content of the answer
        self.level = 'null' # 0 is the main answer
        self.type = 'null' #where is the paper
        self.ip = 'null' #the author's ip
        self.title = 'null'
        self.user_papers = 'null' #the author's total papers
        self.user_points = 'null' #the author's total points
        #self.user_constellation = 'null' #the author's constellation
        #self.sex = 'null' #male or female
        self.zan = 'null' #the zan's number of the answer
        self.main_id = 'null' #record the main id in main txt

    def print_info(self):
        print self.id, self.ip, self.time, self.type, self.zan, self.level, self.user_papers, self.user_points, self.title, self.content, self.cur_time

    def out_file(self, filepath, mode='a+'):
        f = open(filepath, mode)

        log = self.main_id + split_char + self.type + split_char + '"'+ self.title + '"' + split_char + self.level + split_char + self.time + split_char + self.cur_time + split_char + self.id + split_char +  self.user_papers + split_char + self.user_points + split_char + self.ip + split_char + self.zan + split_char + '"' + self.content + '"'

        f.write(log + '\n')
        f.close()

def get_salt_md5(string):
    salt = 'TSCTF{You_shall_not_pass!}'
    
    myMd5 = hashlib.md5()
    myMd5.update(string + salt)
    myMd5_Digest = myMd5.hexdigest()
    return str(int(myMd5_Digest[12:20], 16))

def calc_time_sub(time_str1, time_str2):
    global last_day
    
    #print time_str1, time_str2
    time_list = re.compile(r"[0-9]+ [0-9:]+ ")
    time1 = time_list.findall(time_str1)[0]
    time2 = time_list.findall(time_str2)[0]
    day1 = int(time1.split(' ')[0])
    day2 = int(time2.split(' ')[0])
    h1 = int(time1.split(' ')[1].split(':')[0])
    h2 = int(time2.split(' ')[1].split(':')[0])

    if day1 != day2:
        h1 += 24
    #print h1-h2
    if h1-h2 == 12:
        return True
    else:
        return False

def get_board_urls(url, cookie, start=0, end=4):
    global last_day
    
    try:
        url_list = []
        for i in range(start, end):
            cur_page = i
            cur_title = i*10
            cur_url = url + '?p=%d&_uid=******' % (i+1)

            s = requests.Session()
            header = {'X-Requested-With': 'XMLHttpRequest', 'Cookie': cookie}
            ret = s.get(cur_url,headers=header)
            main_ret = ret.content

            main_ret = main_ret[main_ret.find('<tbody>')+7:main_ret.find('</tbody>')]
            con_list = main_ret.split('<tr')
        
            for j in range(1, len(con_list)):
                cur_con = con_list[j]

                if '\xd4\xad\xcc\xfb\xd2\xd1\xc9\xbe\xb3\xfd' in cur_con:
                    continue

                find_list = re.compile('<a target="_blank" href="/article/[a-zA-Z]*/[0-9]+" title')

                find = find_list.findall(cur_con)
                #print find
                number_list = re.compile('/[0-9]+"')
                number = number_list.findall(cur_con)[0][1:-1]
                #print number

                no_need_list = re.compile('[0-9]+-[0-9]+-[0-9]+</td>')
                no_need_str = no_need_list.findall(cur_con)

                if len(no_need_str)!=0:
                    #print no_need_str
                    if last_day not in no_need_str[0]:
                        continue

                full_url = url + '/' + number
                full_url = full_url.replace('board', 'article')
                url_list.append(full_url)
            
        #print url_list
        return url_list
    except:
        print sys.exc_info()[0],sys.exc_info()[1]
        print 'except in board'
        return []

def spider_paper(url, cookie):
    global g_main_id
    global g_total_re
    global g_zan_re

    try:
        u = url + '?_uid=******'

        s = requests.Session()
        header = {'X-Requested-With': 'XMLHttpRequest', 'Cookie': cookie}
        ret = s.get(u,headers=header)

        main_ret = ret.content

        mlist = re.compile(r"<li class=\"page-pre\">\xcc\xf9\xca\xfd:<i>[0-9]*")
        #print main_ret
        p =  mlist.findall(main_ret)[0]
        answers = int(p.split('<i>')[-1])
        pages = answers / 10 + 1

        #print answers
        #if answers == 1:
        #    return False
    
        #print pages, answers
        cur_page = 0

        name_list = re.compile(r"<a href=\"/user/query/[0-9a-zA-Z]*\">")
        #sex_list = re.compile(r"<span class=\"a-u-sex\" ><samp title=\"")
        user_papers_list = re.compile(r"</dd><dt>\xce\xc4\xd5\xc2</dt><dd>[0-9]*")
        user_points_list = re.compile(r"</dd><dt>\xbb\xfd\xb7\xd6</dt><dd>[0-9]*")
        #user_constellation_list = re.compile(r"</dd><dt>\xd0\xc7\xd7\xf9</dt><dd>")
        title_list = re.compile(r"<br />\xb1\xea&nbsp;&nbsp;\xcc\xe2:")
        content_list = re.compile(r"\xd5\xbe\xc4\xda<br /><br />")
        ip_list = re.compile(r"\[FROM: ")
        time_list = re.compile(r"\xb7\xa2\xd0\xc5\xd5\xbe: \xb1\xb1\xd3\xca\xc8\xcb\xc2\xdb\xcc\xb3 \(")
        type_list = re.compile(r"\xd0\xc5\xc7\xf8: ")
        content_name_list = re.compile(r"\xa1\xbe \xd4\xda [0-9a-zA-Z]+[\s\S]* \xb5\xc4\xb4\xf3\xd7\xf7\xd6\xd0\xcc\xe1\xb5\xbd: \xa1\xbf")
    
        while 1:
            add_a = 10 * cur_page
            cur_answer = 10

            #last page
            if cur_page == pages-1:
                cur_answer = answers - add_a
                #print cur_answer

            indexs = []
            for i in range(0, cur_answer):
                want = '<a name="a%d"></a>' % (i+add_a)
                #print want
                index = main_ret.find(want)
                indexs.append(index)
            indexs.append(len(main_ret)-1)

            #print indexs

            for i in range(0, cur_answer):
                cur_paper_info = paper_info()        
                cur_ret = main_ret[indexs[i]:indexs[i+1]]
                cur_ret = cur_ret.replace('\r', '<br />')
                cur_ret = cur_ret.replace('\n', '<br />')
                cur_ret = cur_ret.replace(',', '\xa3\xac')
                #print cur_ret
                #print cur_ret.replace(',', '\xa3\xac')
                #break
            
                if i+add_a==0:
                    zan_list = re.compile(r"</samp>\xc2\xa5\xd6\xf7\xba\xc3\xc6\xc0 \(\+[0-9]*\)")
                else:
                    zan_list = re.compile(r"</samp>\xd4\xde\([0-9]*\)")

                zan_str = zan_list.findall(cur_ret)[0]
                #print zan_str
                #print cur_ret
                cur_paper_info.zan = zan_str.split('(')[1].split('+')[-1].split(')')[0]
                cur_paper_info.id = name_list.findall(cur_ret)
                if len(cur_paper_info.id) == 0:
                    return False
                cur_paper_info.id = cur_paper_info.id[0][21:-2]
                cur_paper_info.id = get_salt_md5(cur_paper_info.id)
                #cur_paper_info.sex = sex_list.split(cur_ret)[1][:4]
                cur_paper_info.level = str(i+add_a)
                cur_paper_info.user_papers = user_papers_list.findall(cur_ret)[0].split('<dd>')[-1]
                cur_paper_info.user_points = user_points_list.findall(cur_ret)[0].split('<dd>')[-1]
                #cur_paper_info.user_constellation = user_constellation_list.split(cur_ret)[1].split('</dd>')[0]
                cur_paper_info.title = title_list.split(cur_ret)[1].split('<br />')[0]
                cur_paper_info.content = content_list.split(cur_ret)[1].split('<br />--<br />')[0]

                cur_paper_info.ip = ip_list.split(cur_ret)
                if len(cur_paper_info.ip) == 1:
                    cur_paper_info.ip = 'null'
                else:
                    #print cur_paper_info.ip
                    cur_paper_info.ip = cur_paper_info.ip[1].split(']')[0]
            
                cur_paper_info.time = time_list.split(cur_ret)[1].split(')')[0]
                cur_paper_info.type = type_list.split(cur_ret)[1].split('<br />')[0]
                cur_paper_info.cur_time = time.ctime()
                cur_paper_info.main_id = str(g_main_id)

                if (i+add_a==0):
                    if not calc_time_sub(cur_paper_info.cur_time, cur_paper_info.time):
                        return False

                change = content_name_list.findall(cur_paper_info.content)
                if len(change)!=0:
                    c_str = change[0]
                    c_list = re.compile(r"[0-9a-zA-Z]+")
                    c_id = c_list.findall(c_str)[0]
                    md5_id = get_salt_md5(c_id)
                    #print c_id, md5_id, 
                    cur_paper_info.content = cur_paper_info.content.replace(c_id, md5_id)
            
                if i+add_a == 0:
                    cur_paper_info.out_file(main_file)
                else:
                    g_total_re += 1
                    if cur_paper_info.zan != '0':
                        g_zan_re += 1
                    cur_paper_info.out_file(sub_file)
            
                #cur_paper_info.print_info()

            cur_page += 1

            if cur_page == pages:
                break

            s = requests.Session()
            u = url + '?p=%d&_uid=zhulan1991' % (cur_page+1)
            #print u
            header = {'X-Requested-With': 'XMLHttpRequest', 'Cookie': cookie}
            #sleep(1)
            ret = s.get(u,headers=header)

            main_ret = ret.content
            #print main_ret
        return True
    except Exception:
        #print Exception
        print sys.exc_info()[0],sys.exc_info()[1]
        print 'except in url'
        #print main_ret
        return True

def keep_session(cookie, cur_time):
    try:
        alarm = 5
        url = 'http://bbs.byr.cn/article/Security/39668'
        
        for i in range(0, cur_time/alarm):
            s = requests.Session()
            header = {'X-Requested-With': 'XMLHttpRequest', 'Cookie': cookie}
            ret = s.get(url,headers=header)
            sleep(alarm)
            print url

            if '\xc7\xeb\xce\xf0\xc6\xb5\xb7\xb1\xb5\xc7\xc2\xbd' in ret.content:
                print 'keep failed!'
                return
            
            ctime_str = time.ctime()
            if ':00:' in ctime_str:
                return
    except:
        print sys.exc_info()[0],sys.exc_info()[1]
        print 'keep failed!'

def test():
    url = 'http://bbs.byr.cn/article/CPP/89542'
    cookie = '******'

    print url
    spider_paper(url, cookie)
    #keep_session(cookie, 1000)

def main():
    global g_main_id
    global g_zan_re
    global g_total_re
    global last_day
    
    board_list = ['nVote', 'WOW', 'Xyq', 'Job', 'WE', 'Volleyball', 'ComputerTrade', 'Advertising', 'ID', 'Friends', 'Anhui', 'Hearthstone', 'WorkLife', 'ParttimeJob', 'JobInfo', 'AimGraduate', 'Picture', 'VideoCool', 'Financial', 'Travel', 'Talking', 'Pet', 'Joke', 'FamilyLife', 'Taekwondo', 'Beauty', 'Swim', 'cnAnnounce', 'Home', 'Ad_Agent', 'CStrike', 'TVGame', 'Feeling', 'Food', 'Zhejiang', 'Debate', 'Java', 'Health', 'Gymnasium', 'MobileTerminalAT', 'Dota', 'TV', 'Tshirt', 'DigiLife', 'Football', 'Basketball', 'AimBUPT', 'Ticket', 'Shuttlecock', 'Photo', 'KaraOK', 'CampusCard', 'Music', 'SuperStar', 'Clothing', 'StudyShare', 'WWWTechnology', 'Constellations', 'AutoMotor', 'Ghost', 'Guitar', 'Henan', 'Tabletennis', 'Billiards', 'LOL', 'STE', 'Movie', 'ACM_ICPC', 'Focus', 'GoAbroad', 'HardWare', 'Cycling', 'CivilServant', 'Entrepreneurship', 'Sk', 'BM_Apply', 'Board_Document', 'OnlineGame', 'Comic', 'Japanese', 'GraduateSch', 'Quyi', 'Rugby', 'Python', 'ML_DM', 'Dancing', 'PCGame', 'Windows', 'GraduateUnion', 'BookTrade', 'Shandong', 'GSpeed', 'Jump', 'KillBar', 'Athletics', 'Score', 'Diablo', 'House_Agent', 'BuptAssociation', 'Badminton', 'Cantonese', 'Xinjiang', 'Jiangxi', 'BBShelp', 'NorthEast', 'Sichuan', 'INTR', 'Blessing', 'Hubei', 'Shanxi', 'SICE', 'PopKart', 'Gansu', 'Jiangsu', 'Security', 'SCS', 'dotNET', 'Economics', 'BoardManager', 'PMatBUPT', 'ScienceFiction', 'Chongqing', 'Notebook', 'Astronomy', 'cnLists', 'CPP', 'PsyHealthOnline', 'NetLiterature', 'DIYLife', 'Shaanxi', 'Weather', 'cnAdmin', 'Circuit', 'Certification', 'KoreanWind', 'Guizhou', 'IT', 'BTadvice', 'Kungfu', 'Hebei', 'BUPTDiscount', 'BNU', 'LostandFound', 'MathModel', 'BoardGame', 'Guangxi', 'Hero', 'Poetry', 'sysop', 'Tennis', 'HongFu', 'WOWBuptGuild', 'BYR_Bulletin', 'Embedded_System', 'Innovation', 'SoftDesign', 'EnglishBar', 'Flash', 'InnerMongolia', 'ACETeam', 'MobileInternet', 'Fujian', 'BYRatSH', 'Paper', 'Recommend', 'IS', 'Peking', 'Philharmonic', 'SEE', 'SSE', 'Hainan', 'daonian', 'Skating', 'OfficeTool', 'BUPTDNF', 'Environment', 'BUPTStudentUnion', 'Orchestra', 'Board_Management', 'Database', 'SEM', 'FootballManager', 'DV', 'Redcross', 'BTbt', 'Overseas', 'Consulting', 'IPOC', 'ForumCommittee', 'Linux', 'SS', 'Selfsupport', 'Hunan', 'BYRatSZ', 'BUPTSTV', 'SA', 'BuptWeekly', 'SIE', 'Financecareer', 'NetResources', 'Board_Apply', 'Communications', 'Tianjin', 'Qinghai', 'SL', 'SICA', 'BYR', 'Chess', 'BUPTMSTC', 'Advice', 'vote', 'Matlab', 'Plant', 'SearchEngine', 'Bet', 'BBSOpenAPI', 'Announce', 'BBSMan_Dev', 'Showcase', 'Cooperation', 'SH', 'RadioOnline', 'BM_Market', 'notepad', 'BUPT_Internet_Club', 'buptAUTA', 'SCDA', 'OutstandingBM', 'EID', 'BTannounce', 'OracleClub', 'ChineseOrchestra', 'BUPTNU', 'BYR', 'MyBUPT', 'DMDA', 'Progress', 'ShaHe', 'Makerclub', 'SPM', 'BYRStar']
    cookie = '******'
    while True:
        keep_session(cookie, 3300)
        cur_time = time.ctime()
        if ' 1 ' in cur_time:
            last_day = '2015-12-31'
        elif ' 2 ' in cur_time:
            last_day = '2016-01-01'
        elif ' 3 ' in cur_time:
            last_day = '2016-01-02'
        elif ' 4 ' in cur_time:
            last_day = '2016-01-03'
        elif ' 5 ' in cur_time:
            last_day = '2016-01-04'
        elif ' 6 ' in cur_time:
            last_day = '2016-01-05'
        elif ' 7 ' in cur_time:
            last_day = '2016-01-06'
        elif ' 8 ' in cur_time:
            last_day = '2016-01-07'
        elif ' 9 ' in cur_time:
            last_day = '2016-01-08'
        elif ' 10 ' in cur_time:
            last_day = '2016-01-09'
        elif ' 11 ' in cur_time:
            last_day = '2016-01-10'
        elif ' 12 ' in cur_time:
            last_day = '2016-01-11'
        elif ' 13 ' in cur_time:
            last_day = '2016-01-12'
        elif ' 14 ' in cur_time:
            last_day = '2016-01-13'
        elif ' 15 ' in cur_time:
            last_day = '2016-01-14'
        elif ' 16 ' in cur_time:
            last_day = '2016-01-15'
        elif ' 17 ' in cur_time:
            last_day = '2016-01-16'
        elif ' 18 ' in cur_time:
            last_day = '2016-01-17'
        elif ' 19 ' in cur_time:
            last_day = '2016-01-18'
        elif ' 20 ' in cur_time:
            last_day = '2015-12-19'
        elif ' 21 ' in cur_time:
            last_day = '2015-12-20'
        elif ' 22 ' in cur_time:
            last_day = '2015-12-21'
        elif ' 23 ' in cur_time:
            last_day = '2015-12-22'
        elif ' 24 ' in cur_time:
            last_day = '2015-12-23'
        elif ' 25 ' in cur_time:
            last_day = '2015-12-24'
        elif ' 26 ' in cur_time:
            last_day = '2015-12-25'
        elif ' 27 ' in cur_time:
            last_day = '2015-12-26'
        elif ' 28 ' in cur_time:
            last_day = '2015-12-27'
        elif ' 29 ' in cur_time:
            last_day = '2015-12-28'
        elif ' 30 ' in cur_time:
            last_day = '2015-12-29'
        elif ' 31 ' in cur_time:
            last_day = '2015-12-30'
        
        
        print 'start:' + cur_time
        for board in board_list:
            board_url = 'http://bbs.byr.cn/board/%s' % board
            sleep(0.1)
    
            #spider_paper(url, cookie)
            urls = get_board_urls(board_url, cookie)

            #print urls
            for url in urls:
                sleep(0.5)
                print url,
                if spider_paper(url, cookie)==True:
                    g_main_id += 1
                    print g_main_id
                else:
                    print 'None'
        print 'fini:' + time.ctime()
        print g_total_re, g_zan_re

        ff = open('count.txt', 'w+')
        ff.write(str(g_total_re) + ' ' + str(g_zan_re)+ ' ' + str(g_main_id-1))
        ff.close()
        #sleep(3600)

if __name__ == '__main__':
    main()
    #test()
    #print get_salt_md5('admin')

