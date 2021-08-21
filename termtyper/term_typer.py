#!/usr/bin/env python

import curses
import curses.ascii
from curses import textpad
import time
import json
import random
import platform
import urllib.request
import os
import shutil
from pathlib import Path
import argparse
from datetime import date,datetime,timedelta
import getpass


dw=2
ZERO,ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN,EIGHT,NINE,TEN = tuple(range(0,11))
DEFAULT,GREEN,RED,YELLOW,MAGENTA,CYAN,BLUE,WHITE=tuple(range(1,9))
MAX_WORDS_PER_SECOND = 6
KEYBOARD_WIDTH = 116
KEYBOARD_HEIGHT = 16
KEYBOARD_Y_OFFSET = 11
PAUSED_MSG_Y_OFFSET = 9
termtyper_title="TERMTYPER ⌨️"
LANG_TEXT={"TOP200 WORDS":"top200","TOP500 WORDS":"top500","TOP1000 WORDS":"top1000","TOY STORY":"toy_story","SHREK":"shrek","HAPPY FEET":"happy_feet","KUNGFU PANDA":"kungfu_panda","FROZEN":"frozen","MOANA":"moana","HARRY POTTER":"harry_potter","LORD OF THE RINGS":"lotr","TITANIC":"titanic",
"KOTLIN":"kotlin","C/CPP":"ccpp","GO":"go","HTML":"html","C#":"chash","JAVA":"java","JAVASCRIPT":"java_script","PHP":"php","PYTHON":"python","SWIFT":"swift","RUST":"rust","RUBY":"ruby"}


mac_key_board=[
"~.` !.1 @.2 #.3 $.4 %.5 ^.6 &.7 *.8 (.9 ).0 _.- +.= ;.::::delete ;.home:",
"⇤.⇥::tab:::: ;.Q ;.W ;.E ;.R ;.T ;.Y ;.U ;.I ;.O ;.P {.[ }.] |.\\ ;.:end:",   
"⇪.caps:lock ;.A ;.S ;.D ;.F ;.G ;.H ;.J ;.K ;.L :.; \".\' ;.:::::return page.:up::",
";⇧.shift:::: ;.Z ;.X ;.C ;.V ;.B ;.N ;.M <., >.. ?./ ;;;;;;;⇧;.::::shift ;;↑;;.::::: page.down:",
";⌃;;.ctrl ;⌥;;;.option ;⌘;.cmd ;.::::::::::::::::::::::::::::::::::::::::: ;⌘;.cmd ;;;;⌥;.option ;;←;;.::::: ;;↓;;.::::: ;;→;;.:::::"
]

other_key_board=[
"~.` !.1 @.2 #.3 $.4 %.5 ^.6 &.7 *.8 (.9 ).0 _.- +.= ;.:Backsapce ;.Home:",
"⇤.⇥::Tab:::: ;.Q ;.W ;.E ;.R ;.T ;.Y ;.U ;.I ;.O ;.P {.[ }.] |.\\ ;.:End:",   
"⇪.Caps:Lock ;.A ;.S ;.D ;.F ;.G ;.H ;.J ;.K ;.L :.; \".\' ;.::::⏎:Enter Page.:Up::",
";⇧.Shift:::: ;.Z ;.X ;.C ;.V ;.B ;.N ;.M <., >.. ?./ ;;;;;;;⇧;.::::Shift ;;↑;;.::::: Page.Down:",
";.Ctrl ;.:⌹⌹: ;.:Alt ;.::::::::::::::::::::::::::::::::::::::::::: ;.:Alt ;.Ctrl ;;←;;.::::: ;;↓;;.::::: ;;→;;.:::::"
]


key_Board=[
    [(ord("~"),ord("`")),(ord("!"),ord("1")), (ord("@"),ord("2")), (ord("#"),ord("3")), (ord("$"),ord("4")),(ord("%"),ord("5")), (ord("^"),ord("6")), (ord("&"),ord("7")), (ord("*"),ord("8")), (ord("("),ord("9")), (ord(")"),ord("0")), (ord("_"),ord("-")),(ord("+"),ord("=")), 
    (curses.ascii.DEL,curses.KEY_BACKSPACE,curses.ascii.BS),(curses.KEY_HOME,)],
    [(curses.ascii.TAB,9),(ord("Q"),ord("q")), (ord("W"),ord("w")),(ord("E"),ord("e")),(ord("R"),ord("r")),(ord("T"),ord("t")),(ord("Y"),ord("y")),(ord("U"),ord("u")),(ord("I"),ord("i")),(ord("O"),ord("o")),(ord("P"),ord("p")),(ord("{"),ord("[")),(ord("}"),ord("]")),(ord("|"),ord("\\")),
    (curses.KEY_END,)],
    [("Caps Lock",), (ord("A"),ord("a")),(ord("S"),ord("s")),(ord("D"),ord("d")),(ord("F"),ord("f")),(ord("G"),ord("g")),(ord("H"),ord("h")),(ord("J"),ord("j")),(ord("K"),ord("k")), (ord("L"),ord("l")),(ord(":"),ord(";")), (ord("\""),ord("'")), (curses.KEY_ENTER,10,13),(curses.KEY_PPAGE,)],
    [("Shift",),(ord("Z"),ord("z")), (ord("X"),ord("x")), (ord("C"),ord("c")), (ord("V"),ord("v")),(ord("B"),ord("b")), (ord("N"),ord("n")), (ord("M"),ord("m")), (ord("<"),ord(",")), (ord(">"),ord(".")), (ord("?"),ord("/")), ("Shift",),(curses.KEY_UP,),(curses.KEY_NPAGE,)],
    [("Ctrl",),("Alt","Win"),("Command","Alt",curses.KEY_COMMAND),(curses.ascii.SP,32),("Command","Alt"),("Alt","Win"),(curses.KEY_LEFT,),(curses.KEY_DOWN,),(curses.KEY_RIGHT,)]
]
enter_key=""
osname = platform.system()
username =  getpass.getuser().capitalize()

if  osname == 'Darwin':
    key_board = mac_key_board
    enter_key = "return"
else:
    key_board = other_key_board
    enter_key = "Enter"

# functions dealing with wpm stats

def hLine(stdscr,y,x,ch,n):
    for i in range(n):
        stdscr.addch(y,x+i,ch)

def vLine(stdscr,y,x,ch,n):
    for i in range(n):
        stdscr.addch(y-i,x,ch)
def bar(stdscr,y,x, height,color,y_max=1.0):
    ch='#'
    ht = int((1/y_max)*20*height)
    ft = round((1/y_max)*20*height -ht,3)

    if ht==0:
        if 0.01<=height<= 0.02:
            ht=1
            ch='_'
        elif 0.02<height<=0.03:
            ht=1
            ch='-' 
        elif 0.03<height<=0.04:
            ht=1
            ch='=' 
        else:
            ht=1
    for i in range(ht):
        stdscr.addch(y-i,x,ch,color) 

    if height >= 0.05:
        if ft < 0.5:
            stdscr.addch(y-ht,x,'_',color) 
        else:
            stdscr.addch(y-ht,x,'=',color) 



def hist(stdscr,y_offset,x_offset,max_wpm,title,data={}):
    
    y_max=1.0
    try:
        ymax = max(data.values())
    except:
        ymax = 1.0

    if 0.25<ymax <= 0.5:
        y_max = 0.5
    elif 0.1< ymax <= 0.25:
        y_max = 0.25
    elif 0.05 < ymax <= 0.1:
        y_max = 0.1
    elif 0.025 < ymax <= 0.05:
        y_max = 0.05
    elif  ymax <= 0.025:
        y_max = 0.025

    max_wpm =max(10*(max_wpm//10)+10,100)
    stdscr.addstr(y_offset-21,x_offset+max_wpm//4 -len(title)//2,title[:title.index('(')],curses.color_pair(RED)|curses.A_BOLD)
    stdscr.addstr(y_offset-21,x_offset+max_wpm//4 -len(title)//2+len(title[:title.index('(')]),title[title.index('('):],curses.color_pair(DEFAULT))
    hLine(stdscr,y_offset,x_offset,'_',max_wpm//2 )
    stdscr.addstr(y_offset+2,x_offset+max_wpm//4,"WPM",curses.color_pair(BLUE))
    vLine(stdscr,y_offset,x_offset-1,'|',21)
    for ix,x in enumerate([str(10*i) for i in range(0,max_wpm//10 +1)]):
        stdscr.addch(y_offset,x_offset+5*(ix),'.')
        stdscr.addstr(y_offset+1,x_offset+5*(ix),x)
    dy=y_max/10

    for iy, y in enumerate([f"{round(i*dy,4)}" for i in range(0,11)]):
        stdscr.addch(y_offset-2*(iy),x_offset-1,'_')
        stdscr.addstr(y_offset-2*(iy),x_offset-len(str(y))-2,str(y))

    for k,v in data.items():
        bar(stdscr,y_offset,x_offset+int(k)//2,v,curses.color_pair(GREEN),y_max)
    


def split_text(text,n):
    text_list=[]
    line=text[0]
    for word in text[1:]:
        if len(line)+len(word)+1 < n:
            line += " "+word
        else:
            text_list.append(line+" ")
            line = word
    text_list.append(line)
    return text_list

def print_input_text(stdscr,ip_text,time_left): # prints the text that is being typed
    _, sw = stdscr.getmaxyx()
    time_left_s = int(time_left)
    time_left_ms = int((time_left - time_left_s)*100)

    stdscr.addstr(dw+6,dw+1,">"+ip_text+"|",curses.color_pair(CYAN))
    stdscr.chgat(dw+6,dw+1+len(ip_text)+1,1,curses.A_BLINK|curses.color_pair(CYAN))
    stdscr.addstr(1,dw+1,f"{(time_left_s//60)//10}{(time_left_s//60)%10}:{(time_left_s%60)//10}{(time_left_s%60)%10}:{time_left_ms//10}{time_left_ms%10}",curses.A_BOLD)
    stdscr.chgat(1,dw+1,2,curses.color_pair(BLUE)|curses.A_BOLD)
    stdscr.chgat(1,dw+3,1,curses.color_pair(DEFAULT)|curses.A_BOLD)
    stdscr.chgat(1,dw+4,2,curses.color_pair(MAGENTA)|curses.A_BOLD)
    stdscr.chgat(1,dw+6,1,curses.color_pair(DEFAULT)|curses.A_BOLD)
    stdscr.chgat(1,dw+7,2,curses.color_pair(YELLOW)|curses.A_BOLD)
    
    # Title
    stdscr.addstr(0,sw//2 - len(termtyper_title)//2, termtyper_title,curses.color_pair(RED)|curses.A_BOLD)

    msg = "Press F2 to customize test; F3 to toggle onscreen keyboard; F4 to pause/resume; F5 to Refresh; and Esc to quit;"
    if  len(msg) < sw-2:
        stdscr.addstr(curses.LINES-1,1,msg,curses.color_pair(DEFAULT))
        for opt in ["F2","F3","F4","F5","Esc"]:
            stdscr.chgat(curses.LINES-1,msg.index(opt)+1,len(opt),curses.A_BOLD|curses.color_pair(BLUE))
    else:
        stdscr.addstr(curses.LINES-1,1,"Terminal window size should be at least 120x36",curses.color_pair(YELLOW))



def print_text(stdscr,text_list,color_dict,l=0): # prints three lines of text to be typed

    _, sw = stdscr.getmaxyx()
    for i in range(3):
        stdscr.addstr(dw+1+i,dw+1,(sw-dw-4)*' ')
    text_list_ = text_list[3*(l//3):3*(l//3)+3]
    for i,text in enumerate(text_list_):
        i_=3*(l//3)+i
        stdscr.move(dw+i+1,dw+1) 
        for j in range(len(text)):
            stdscr.addch(text[j],color_dict[(i_,j)]) 
    show_user(stdscr)

def can_dispay_keyboard(stdscr): # returns true if keyboard fit in screen
    sh,sw = stdscr.getmaxyx()
    return (sw > KEYBOARD_WIDTH) and (sh > KEYBOARD_HEIGHT + KEYBOARD_Y_OFFSET)

def hist_data(stats,start_day,num_days):
    hdata ={"total_time":0,"avg_speed":0,"top_speed":0,"start_date":str(date.fromisoformat(start_day)+timedelta(days=-num_days)),"data":{}}
    sum=0
    max_speed = 0
    for d in range(num_days):
        day=str(date.fromisoformat(start_day)+timedelta(days=-d))
        if not day in stats:
            continue
        for k in stats[day]:
            if int(k) > max_speed:
                max_speed = int(k)
            kk = str((int(k)//2)*2+1)
            hdata["data"][kk]=hdata["data"].get(kk,0)+stats[day][k]
            hdata["total_time"]+=stats[day][k]
            sum += int(k)*stats[day][k]

    hdata["top_speed"] = max_speed
    for kk in hdata["data"]:
        try:
            hdata["data"][kk]=hdata["data"][kk]/hdata["total_time"]
        except ZeroDivisionError:
           hdata["data"][kk] = 0
    try:
         hdata["avg_speed"]=round(sum/hdata["total_time"],2)
    except ZeroDivisionError:
         hdata["avg_speed"]=0
    return hdata
# Word per minute histogram
def wpm_histogram(stdscr,stats):

    sh,sw = stdscr.getmaxyx()
    today = str(date.today())
    LIFE_TIME_DAYS = days_difference(min(stats.keys()),max(stats.keys()))+1
    CELL_WIDTH = 23
    BOX_START_X = 30
    BOX_START_Y = 6
    TITLE_X = 15
    TITLE_Y = 30
    DAY = min(1,LIFE_TIME_DAYS)
    WEEK = min(7,LIFE_TIME_DAYS)
    MONTH = min(30,LIFE_TIME_DAYS)
    ALLTIME = LIFE_TIME_DAYS
    stdscr.clear()
    stats_categories = [(" All-time Statistics ",ALLTIME), (" Month Statistics    ",MONTH),(" Week Statistics     ",WEEK),(" Day Statistics      ",DAY)]
    histogram_data = (hist_data(stats,today,ALLTIME),hist_data(stats,today,MONTH),hist_data(stats,today,WEEK),hist_data(stats,today,DAY))
    cix=0
    while True:
        if sw < max(histogram_data[0]["top_speed"]//2+20,110) or sh < 36:
            stdscr.clear()
            stdscr.addstr(curses.LINES-1,1, f"Terminal window size is too small.",curses.color_pair(YELLOW))
        else:
                
            for ix, statCat in enumerate(stats_categories):
                if ix == cix:
                    stdscr.addstr(2+ix,2,f"{statCat[0]}",curses.color_pair(YELLOW)|curses.A_REVERSE)
                    stdscr.addstr(2+ix,25," ->",curses.color_pair(BLUE))
                else:
                    stdscr.addstr(2+ix,2,f"{statCat[0]}",curses.color_pair(YELLOW))

            for i in [2,4,6]:
                hLine(stdscr,i,BOX_START_X,'-',70)
            for i in range(4):
                vLine(stdscr,BOX_START_Y,30+i*CELL_WIDTH,'|',5)
            for ix,hx in enumerate([('Total Time (Minutes)',MAGENTA,'total_time'),('Top Speed (WPM)',GREEN,'top_speed'),('Average Speed (WPM)',CYAN,'avg_speed')]):
                stdscr.addstr(3,BOX_START_X+2+CELL_WIDTH*ix+CELL_WIDTH//2-len(hx[0])//2-1,hx[0],curses.A_BOLD|curses.color_pair(hx[1]))
                stdscr.addstr(5,BOX_START_X+2+CELL_WIDTH*ix+CELL_WIDTH//2-len(str(histogram_data[cix][hx[2]]))//2,f'{histogram_data[cix][hx[2]]}')   
 
            start_day = str(date.fromisoformat(today) - timedelta(days= (stats_categories[cix][1]-1)))
            hist(stdscr,TITLE_Y,TITLE_X,histogram_data[cix]["top_speed"], f"Typing Speed Histogram ({start_day} to {today})", histogram_data[cix]["data"])
            show_user(stdscr)

            # Title

            stdscr.addstr(0,sw//2 - len(termtyper_title)//2, termtyper_title,curses.color_pair(RED)|curses.A_BOLD)
            msg = f"Use (↑,↓) to navigate; Press {enter_key} to continue with another test; and Esc to quit."
            stdscr.addstr(curses.LINES-1,1,msg,curses.color_pair(DEFAULT))
            for m in ["(↑,↓)",enter_key,"Esc"]:
                stdscr.chgat(curses.LINES-1,1+msg.index(m),len(m),curses.A_BOLD|curses.color_pair(BLUE))
            stdscr.refresh()
        key1=stdscr.getch()
        if key1 not in [curses.KEY_UP,curses.KEY_DOWN,10,13,curses.KEY_ENTER,curses.ascii.CR,curses.KEY_RESIZE,curses.ascii.ESC,27]:
            continue
        if key1 == curses.KEY_RESIZE:
            if (sh,sw) != stdscr.getmaxyx():
                sh,sw = stdscr.getmaxyx()
                curses.resizeterm(sh,sw) 
                stdscr.clear()
                continue
        elif key1 == curses.KEY_UP and cix > 0 :
            cix -=1
            stdscr.clear()
        elif key1 == curses.KEY_DOWN and cix < (len(stats_categories)-1):
            cix +=1 
            stdscr.clear() 
        elif key1 in [10,13,curses.KEY_ENTER,curses.ascii.CR]:
            return False
        elif key1 in [curses.ascii.ESC,27]:
            return True





def show_user(stdscr):
    _,sw = stdscr.getmaxyx()
    stdscr.addstr(0,sw-len(username)-5,"👤")
    stdscr.addstr(0,sw-len(username)-2,username,curses.color_pair(DEFAULT))

def days_difference(day1,day2):
    if day1 == day2:
        return 0
    else:
        return int(str(date.fromisoformat(day2)-date.fromisoformat(day1)).split(' ')[0])

def increment_date(day,k):
    return str(date.fromisoformat(day)+timedelta(days=k))

def print_result(stdscr,result,language,stats): # prints the performance result
    sh, sw = stdscr.getmaxyx()
    max_time = language["max_time"]
    unit_time = 60
    minutes = max_time//unit_time
    tks = result['total_key_strokes'] 
    cks = result['total_key_strokes']- result['wrong_key_strokes'] 
    wks = result['wrong_key_strokes'] 
    ctw = result['total_words_typed'] - result['wrong_words_typed'] 
    wtw = result['wrong_words_typed'] 
    wpm = ctw//(max_time//unit_time)
    try:
        accuracy = (round(cks/tks, 2))*100
    except:
        accuracy = 0
    stdscr.clear()
    today = str(date.today())
    wpm_key = str(wpm)

    if today not in stats:
        stats[today]={wpm_key:minutes}

    else:
        stats[today][wpm_key]=stats[today].get(wpm_key,0)+minutes

    stats_data_to_dump = json.dumps(stats)
    Path(__file__).parent.joinpath("wpm_statistics.json").write_text(stats_data_to_dump) 

    
    while True:
        box_begin_y = dw+sh//2-10
        box_begin_x = dw+sw//2-20
        box_width = 38
        box_height = 18
        if sw < 85 or sh < 24:
            stdscr.clear()
            stdscr.addstr(curses.LINES-1,1,"Terminal window size is too small.",curses.color_pair(YELLOW))
        else:
            textpad.rectangle(stdscr,box_begin_y,box_begin_x,box_begin_y+box_height,box_begin_x+box_width)
            stdscr.hline(dw+sh//2-7,dw+sw//2-19,'_',box_width-1)

            stdscr.addstr(box_begin_y + dw, box_begin_x+box_width//2-len("RESULT")//2, "RESULT",curses.A_BOLD | curses.color_pair(DEFAULT))


            stdscr.addstr(box_begin_y + 5,box_begin_x +4,f"Challange     :")
            stdscr.addstr(box_begin_y + 5,box_begin_x + 22,f"{language['challange']}",curses.color_pair(YELLOW))
            stdscr.addstr(box_begin_y + 7,box_begin_x +4,f"WPM           :")
            stdscr.addstr(box_begin_y + 7,box_begin_x + 22,f"{wpm}",curses.color_pair(BLUE))
            stdscr.addstr(box_begin_y + 9,box_begin_x + 4,f"Keystrokes    :")
            ksmsg =f"({cks}|{wks}) {tks}"
            stdscr.addstr(box_begin_y + 9,box_begin_x+ 21,ksmsg,curses.color_pair(DEFAULT))
            for i,st in enumerate([(cks,GREEN,'('),(wks,RED,'|'),(tks,MAGENTA,')')]):
                stdscr.chgat(box_begin_y+2 + 7,box_begin_x + 20+2+i//2+ksmsg.index(str(st[2])),len(str(st[0])),curses.color_pair(st[1]))

            stdscr.addstr(box_begin_y + 11,box_begin_x + 4,f"Accuracy      :")
            stdscr.addstr(box_begin_y + 11,box_begin_x + 21,f"{accuracy}%",curses.color_pair(CYAN))
            stdscr.addstr(box_begin_y + 13,box_begin_x + 4, f"Correct words :")
            stdscr.addstr(box_begin_y + 13,box_begin_x + 21,f"{ctw}",curses.color_pair(GREEN))
            stdscr.addstr(box_begin_y + 15,box_begin_x + 4,f"Wrong words   :")
            stdscr.addstr(box_begin_y + 15,box_begin_x + 21,f"{wtw}",curses.color_pair(RED))

            # Title
            stdscr.addstr(0,sw//2 - len(termtyper_title)//2, termtyper_title,curses.color_pair(RED)|curses.A_BOLD)
            msg = f"Press F6 to see performance statistics; {enter_key} to continue with another test; and Esc to quit."
            stdscr.addstr(curses.LINES-1,1,msg,curses.color_pair(DEFAULT))
            for m in ["F6",enter_key,"Esc"]:
                stdscr.chgat(curses.LINES-1,1+msg.index(m),len(m),curses.A_BOLD|curses.color_pair(BLUE))
            stdscr.refresh()
      



        key = stdscr.getch()
        if key not in [curses.KEY_RESIZE, curses.KEY_ENTER,10,13,curses.ascii.CR,curses.KEY_F6, curses.ascii.ESC,27]:
            stdscr.refresh()
            continue
        if key == curses.KEY_RESIZE:
            if (sh,sw) != stdscr.getmaxyx():
                sh,sw = stdscr.getmaxyx()
                curses.resizeterm(sh,sw) 
                stdscr.clear()
        elif key == curses.KEY_F6:
            stdscr.clear()
            break_it = wpm_histogram(stdscr,stats)
            return break_it
        elif key in[curses.ascii.ESC,27]:
            return True

        elif key in [10,13,curses.KEY_ENTER,curses.ascii.CR]:
            stdscr.clear()
            return False

    
        

def termtyper(stdscr,language,stats):

    sh, sw = stdscr.getmaxyx()

    color_dict={}
    abs_color_dict={} 
    cum_line_lengths={}
    space_locations = []
    ch_ix=0
    sp_ix=0
    refresh = False
    max_time = language["max_time"]
    time_left = max_time
    # unit_time = 60
    number_of_words = max_time*MAX_WORDS_PER_SECOND
    key_map={}
    text=Path(__file__).parent.joinpath("data").joinpath(LANG_TEXT[language["cat"]]+".txt").read_text()
    if language["cat"] in ["SHREK","HAPPY FEET","LORD OF THE RINGS","TOY STORY","KUNGFU PANDA","FROZEN","MOANA","HARRY POTTER","TITANIC"]:
        rix= random.randint(0,len(text.split(' '))-number_of_words-1)
        random_text = text.split(' ')[rix:rix+number_of_words]
    else:
        random_text = random.choices(text.split(' '),k=number_of_words)
    textlist = split_text(random_text,sw-3*dw)
    on_screen_kbd = True
    pause_typing = False
    cum_line_lengths[-1]=0
    for i,tex in enumerate(textlist):
        cum_line_lengths[i]=cum_line_lengths[i-1]+len(textlist[i])

        spacelocations=[]
        for j in range(len(tex)):
            abs_color_dict[cum_line_lengths[i-1]+j] = curses.color_pair(DEFAULT)
            color_dict[(i,j)]= abs_color_dict[cum_line_lengths[i-1]+j]
            if tex[j] == ' ':
                spacelocations.append(j)
        space_locations.append(spacelocations)

    ip_text = ""
    ip_text_ix = 0


    print_text(stdscr,textlist,color_dict,l=0)
    print_input_text(stdscr, ip_text,time_left)
    mssg = "Paused! Press F4 to resume back to typing."
    if on_screen_kbd and can_dispay_keyboard(stdscr):
        keyboard(stdscr,KEYBOARD_Y_OFFSET,(sw-KEYBOARD_WIDTH)//2,key_map)

    start_time= time.time()
    now = start_time
    started = False
    word_got_wrong = False
    result = {
        "wrong_key_strokes" : 0,
        "total_key_strokes" : 0,
        "wrong_words_typed" : 0,
        "total_words_typed": 0,
    }
    i,j,l = 0,0,0
    a,b = 0,0
    pkey = None


    while True:
        
        if time_left <=0:

            break_it = print_result(stdscr,result,language,stats)
            if break_it:
                break

            result = {
                "wrong_key_strokes" : 0,
                "total_key_strokes" : 0,
                "wrong_words_typed" : 0,
                "total_words_typed": 0,
            }
            refresh = True
            started = False
            time_left=max_time
            start_time = time.time()
            now = start_time
            if language["cat"] in ["SHREK","HAPPY FEET","LORD OF THE RINGS","TOY STORY","KUNGFU PANDA","FROZEN","MOANA","HARRY POTTER","TITANIC"]:
              rix= random.randint(0,len(text.split(' '))-number_of_words-1)
              random_text = text.split(' ')[rix:rix+number_of_words]
            else:
                random_text = random.choices(text.split(' '),k=number_of_words)

            textlist = split_text(random_text,sw-3*dw)
            cum_line_lengths = {}
            space_locations = []
            sp_ix =0
            ch_ix =0
            cum_line_lengths[-1]=0
            for i,tex in enumerate(textlist):
                cum_line_lengths[i]=cum_line_lengths[i-1]+len(textlist[i])

                spacelocations=[]
                for j in range(len(tex)):
                    abs_color_dict[cum_line_lengths[i-1]+j] = curses.color_pair(DEFAULT)
                    color_dict[(i,j)]= abs_color_dict[cum_line_lengths[i-1]+j]
                    if tex[j] == ' ' :
                        spacelocations.append(j)
                space_locations.append(spacelocations)

            ip_text = ""
            ip_text_ix = 0

            a,b,i,j,l = 0,0,0,0,0
            continue

        aa = a
        bb = b
        l_=l
        if i  >= len(textlist[l]):
            l_=l
            l=l+1
            i,j=0,0
            a,b = 0,0
            ip_text = ""
            ip_text_ix = 0

        if l%3 == 0:
           print_text(stdscr,textlist,color_dict,l) 
        if j == 0:
            a,b = 0, space_locations[l][0]
        elif j == len(space_locations[l]):
            a,b = space_locations[l][j-1],space_locations[l][j-1]
        else:
            a,b = space_locations[l][j-1],space_locations[l][j]
        
        _1 = 1   
        if j==0:
            _1=0
        
        for k in range(aa,bb):
            stdscr.addch(dw+1+l_%3,dw+1+k,textlist[l_][k],color_dict[(l_,k)]) 

        for k in range(a+_1,b):
            stdscr.addch(dw+1+l%3,dw+1+k,textlist[l][k],color_dict[(l,k)]|curses.A_REVERSE) 


        key = stdscr.getch()



        if not started and key != curses.ERR and key != curses.KEY_MOUSE and key != curses.KEY_RESIZE:
            start_time= time.time()
            now = start_time
            started = True

        if pkey != None and  started and on_screen_kbd and can_dispay_keyboard(stdscr):
            typed_effect(stdscr,key_map,pkey)



        if pause_typing:
            stdscr.addstr(PAUSED_MSG_Y_OFFSET,sw//2-len(mssg)//2,mssg,curses.color_pair(DEFAULT))
            stdscr.chgat(PAUSED_MSG_Y_OFFSET,sw//2-len(mssg)//2+ mssg.index('Paused'),len('Paused!'),curses.color_pair(RED)|curses.A_BOLD)
            stdscr.chgat(PAUSED_MSG_Y_OFFSET,sw//2-len(mssg)//2+ mssg.index('F4'),len('F4'),curses.color_pair(BLUE)|curses.A_BOLD)
        else:
            stdscr.move(PAUSED_MSG_Y_OFFSET,sw//2-len(mssg)//2)
            stdscr.clrtoeol()
        stdscr.refresh()

        if key == curses.KEY_RESIZE or refresh or key == curses.KEY_F3:
            if (sh,sw) != stdscr.getmaxyx():
                sh,sw = stdscr.getmaxyx()
                curses.resizeterm(sh,sw) 
            refresh = False

            textlist = split_text(random_text,sw-3*dw)
            color_dict={}
            space_locations=[]
            cum_line_lengths={}

            cum_line_lengths[-1]=0
            for ii,tex in enumerate(textlist):
                cum_line_lengths[ii]=cum_line_lengths[ii-1]+len(textlist[ii]) 
                spacelocations=[]
                for jj in range(len(tex)):
                    color_dict[(ii,jj)]=  abs_color_dict[cum_line_lengths[ii-1]+jj]
                    if tex[jj] == ' ':
                        spacelocations.append(jj)
                space_locations.append(spacelocations)

            inx=0
            while ch_ix > cum_line_lengths[inx]:
                 inx += 1
            l=inx

            i=ch_ix - cum_line_lengths[l-1]

            s_ix=0
            sn = len(space_locations[s_ix])
            sn_1 = 0
            while sp_ix > sn :
                s_ix += 1
                sn_1 = sn
                sn += len(space_locations[s_ix])
            j= sp_ix - sn_1
            if j == 0:
                a,b = 0, space_locations[l][0]
            elif j == len(space_locations[l]):
                a,b = space_locations[l][j-1],space_locations[l][j-1]
            else:
                a,b = space_locations[l][j-1],space_locations[l][j]

            if i  >= len(textlist[l]):
                l=l+1
                i,j=0,0
            stdscr.clear()
            print_text(stdscr,textlist,color_dict,l)
            print_input_text(stdscr, ip_text,time_left)
            if key == curses.KEY_F3:
                on_screen_kbd = not on_screen_kbd
            if  on_screen_kbd and can_dispay_keyboard(stdscr):
                keyboard(stdscr,KEYBOARD_Y_OFFSET,(sw-KEYBOARD_WIDTH)//2,key_map)
            stdscr.refresh()
            
        
        elif  key in [curses.ascii.ESC,27]:     # quit
            break


        elif key == ord(textlist[l][i]) and key != curses.ascii.SP and not pause_typing:
            if not word_got_wrong:
                color_dict[(l,i)]=curses.color_pair(GREEN) 
                abs_color_dict[cum_line_lengths[l-1]+i] = color_dict[(l,i)]
            ip_text = ip_text[:ip_text_ix] + chr(key)+ip_text[ip_text_ix:]
            i=i+1
            ip_text_ix += 1
            result["total_key_strokes"] += 1
  
            if j == 0:
                a = 0
            else:
                a=space_locations[l][j-1]+1

            if textlist[l][a:a+len(ip_text)] == ip_text:
                for k in range(a,b):
                    if k < a+len(ip_text):
                        color_dict[(l,k)]=curses.color_pair(GREEN)  
                        abs_color_dict[cum_line_lengths[l-1]+k] = color_dict[(l,k)]

                    else:
                        color_dict[(l,k)]=curses.color_pair(DEFAULT)  
                        abs_color_dict[cum_line_lengths[l-1]+k] = color_dict[(l,k)]
                word_got_wrong = False
            if on_screen_kbd and can_dispay_keyboard(stdscr):
                typed_effect(stdscr,key_map,key,GREEN)




        elif key in [curses.ascii.SP,ord(' ')] and not pause_typing:    # key is space
            if j == 0:
                a = 0
            else:
                a=space_locations[l][j-1]+1
            if textlist[l][a:b] != ip_text: 
                word_got_wrong = True
                for k in range(a,b):
                    color_dict[(l,k)]=curses.color_pair(RED)
                    abs_color_dict[cum_line_lengths[l-1]+k] = color_dict[(l,k)]


            ip_text = ""
            ip_text_ix = 0
            if word_got_wrong:
                result["wrong_words_typed"] += 1
                result["wrong_key_strokes"] += 1
    
            result["total_key_strokes"] += 1
            result["total_words_typed"] += 1 
            i=space_locations[l][j]+1
  
            j=j+1
            word_got_wrong = False
            if on_screen_kbd and can_dispay_keyboard(stdscr):
                typed_effect(stdscr,key_map,key,BLUE)




        elif key in [curses.ascii.DEL,curses.KEY_BACKSPACE,curses.ascii.BS] and  not pause_typing:    # key delete or back space ,
            if on_screen_kbd and can_dispay_keyboard(stdscr):
                typed_effect(stdscr,key_map,key,MAGENTA)

            if len(ip_text)==0:
                word_got_wrong = False

                for k in range(a,b):
                    color_dict[(l,k)]=curses.color_pair(DEFAULT)
                    abs_color_dict[cum_line_lengths[l-1]+k] = color_dict[(l,k)]
            else:
                ip_text = ip_text[:ip_text_ix-1]+ip_text[ip_text_ix:]

                ip_text_ix -= 1
                i=i-1
                if j == 0:
                    a = 0
                else:
                    a=space_locations[l][j-1]+1
                if textlist[l][a:a+len(ip_text)] == ip_text:
                    for k in range(a,b):
                        if k < a+len(ip_text):
                            color_dict[(l,k)]=curses.color_pair(GREEN)  
                            abs_color_dict[cum_line_lengths[l-1]+k] = color_dict[(l,k)]

                        else:
                            color_dict[(l,k)]=curses.color_pair(DEFAULT)  
                            abs_color_dict[cum_line_lengths[l-1]+k] = color_dict[(l,k)]
                    word_got_wrong = False

        elif key in [curses.KEY_F5,curses.KEY_F2]:
            if key == curses.KEY_F2:
                break_it = option_display(stdscr,language)
                if break_it:
                    break

            result = {
                "wrong_key_strokes" : 0,
                "total_key_strokes" : 0,
                "wrong_words_typed" : 0,
                "total_words_typed": 0,
            }
            refresh = True
            started = False
            pause_typing = False

            pkey = None
            max_time=language["max_time"]
            time_left = max_time
            number_of_words = max_time*MAX_WORDS_PER_SECOND
            start_time = time.time()
            now = start_time
            text=Path(__file__).parent.joinpath("data").joinpath(LANG_TEXT[language["cat"]]+".txt").read_text()
            if language["cat"] in ["SHREK","HAPPY FEET","LORD OF THE RINGS","TOY STORY","KUNGFU PANDA","FROZEN","MOANA","HARRY POTTER","TITANIC"]:
                rix= random.randint(0,len(text.split(' '))-number_of_words-1)
                random_text = text.split(' ')[rix:rix+number_of_words]
            else:
                random_text = random.choices(text.split(' '),k=number_of_words)

            textlist = split_text(random_text,sw-3*dw)
            cum_line_lengths = {}
            space_locations = []
            sp_ix =0
            ch_ix =0
            cum_line_lengths[-1]=0
            for i,tex in enumerate(textlist):
                cum_line_lengths[i]=cum_line_lengths[i-1]+len(textlist[i])

                spacelocations=[]
                for j in range(len(tex)):
                    abs_color_dict[cum_line_lengths[i-1]+j] = curses.color_pair(DEFAULT)
                    color_dict[(i,j)]= abs_color_dict[cum_line_lengths[i-1]+j]
                    if tex[j] == ' ':
                        spacelocations.append(j)
                space_locations.append(spacelocations)

            ip_text = ""
            a,b,i,j,l = 0,0,0,0,0
            continue
        elif key == curses.KEY_F3:  # key is F3
            on_screen_kbd = not on_screen_kbd

        elif key == curses.KEY_F4:

            # mssg = "Paused. Press F4 to resume to typing"
            if not pause_typing:
                stdscr.addstr(PAUSED_MSG_Y_OFFSET,sw//2-len(mssg)//2,mssg,curses.color_pair(DEFAULT))
                stdscr.chgat(PAUSED_MSG_Y_OFFSET,sw//2-len(mssg)//2+ mssg.index('Paused'),len('Paused!'),curses.color_pair(RED)|curses.A_BOLD)
                stdscr.chgat(PAUSED_MSG_Y_OFFSET,sw//2-len(mssg)//2+ mssg.index('F4'),len('F4'),curses.color_pair(BLUE)|curses.A_BOLD)
            else:
                stdscr.move(PAUSED_MSG_Y_OFFSET,sw//2-len(mssg)//2)
                stdscr.clrtoeol()

            pause_typing = not pause_typing

        elif key == curses.KEY_LEFT and not pause_typing:   # key <-

            if on_screen_kbd and can_dispay_keyboard(stdscr):
                typed_effect(stdscr,key_map,key,YELLOW)
                
            if ip_text_ix > 0:
                ip_text_ix -= 1
                i -= 1

        elif key == curses.KEY_RIGHT and not pause_typing: # key ->

            if on_screen_kbd and can_dispay_keyboard(stdscr):
                typed_effect(stdscr,key_map,key,YELLOW)
            if ip_text_ix <len(ip_text):
                ip_text_ix += 1
                i += 1
        elif key in [curses.KEY_UP,curses.KEY_DOWN,curses.KEY_HOME,curses.KEY_PPAGE,
                curses.KEY_NPAGE,curses.KEY_END,10,13,curses.KEY_ENTER,curses.ascii.TAB]:
                if on_screen_kbd and can_dispay_keyboard(stdscr):
                    typed_effect(stdscr,key_map,key,YELLOW)


        elif ord(' ') <= key <= ord('~') and not pause_typing:
            ip_text = ip_text[:ip_text_ix] + chr(key)+ip_text[ip_text_ix:]
            ip_text_ix += 1

            if not word_got_wrong:
                for k in range(a,b):
                    color_dict[(l,k)]=curses.color_pair(RED)  
                    abs_color_dict[cum_line_lengths[l-1]+k] = color_dict[(l,k)]
            i=i+1
            result["wrong_key_strokes"] += 1
            result["total_key_strokes"] += 1
            if on_screen_kbd and can_dispay_keyboard(stdscr):
                typed_effect(stdscr,key_map,key,RED) 
            word_got_wrong = True 
            
 
        ch_ix = cum_line_lengths[l-1]+i
        sp_ix = 0
        for cx in range(l):
            sp_ix += len(space_locations[cx])
        sp_ix += j
        iip_text=ip_text[:ip_text_ix]+'|'+ip_text[ip_text_ix:]
        stdscr.move(dw+6,dw+1+1)
        stdscr.clrtoeol()
        stdscr.addstr(dw+6,dw+1+1,iip_text,curses.color_pair(SIX))
        stdscr.chgat(dw+6,dw+1+ip_text_ix+1,1,curses.A_BLINK|curses.color_pair(SIX))

    
        if started and not pause_typing:
            time_left -= (time.time()-now)
            now = time.time()
        elif started and pause_typing:
            now = time.time()

        if  key in list(range(ord(' '),ord('~')+1))+[curses.KEY_BACKSPACE,curses.ascii.BS,curses.ascii.DEL, curses.KEY_LEFT,curses.KEY_RIGHT,curses.KEY_UP,curses.KEY_DOWN,curses.KEY_HOME,curses.KEY_PPAGE,
                curses.KEY_NPAGE,curses.KEY_END,10,13,curses.KEY_ENTER,curses.ascii.TAB]:
            if not pause_typing:
                pkey = key
            else:
                pkey = ord(' ')

        time_left_s = int(time_left)
        time_left_ms = int((time_left - time_left_s)*100)


        stdscr.addstr(1,dw+1,f"{(time_left_s//60)//10}{(time_left_s//60)%10}:{(time_left_s%60)//10}{(time_left_s%60)%10}:{time_left_ms//10}{time_left_ms%10}",curses.A_BOLD)
        stdscr.chgat(1,dw+1,2,curses.color_pair(BLUE)|curses.A_BOLD)
        stdscr.chgat(1,dw+3,1,curses.color_pair(DEFAULT)|curses.A_BOLD)
        stdscr.chgat(1,dw+4,2,curses.color_pair(MAGENTA)|curses.A_BOLD)
        stdscr.chgat(1,dw+6,1,curses.color_pair(DEFAULT)|curses.A_BOLD)
        stdscr.chgat(1,dw+7,2,curses.color_pair(YELLOW)|curses.A_BOLD) 
        stdscr.refresh()


# Display language options
def lang_option(stdscr,language):
    stdscr.clear()
    MAX_ROWS = 6
    sh,sw = stdscr.getmaxyx()
    lang_cat={"ENGLISH":["TOP200 WORDS","TOP500 WORDS","TOP1000 WORDS","TOY STORY","SHREK","HAPPY FEET","KUNGFU PANDA","FROZEN","MOANA","HARRY POTTER","LORD OF THE RINGS","TITANIC"],
    "PROGRAMMING":["C/CPP","C#","JAVA","PYTHON","SWIFT","HTML","JAVASCRIPT","GO","PHP","RUBY","KOTLIN","RUST"]}
    selected_lang = language["lang"]
    selected_lang_cat =language["cat"]
    langs = sorted(lang_cat.keys())
    on_langs = True
    lix=0
    cix =0
    lang_option_displayed= False
    if language["lang"] == "ENGLISH":
        lix=0
    else:
        lix=1
    while True:
        key = stdscr.getch()
        if key == curses.ERR and lang_option_displayed:
            stdscr.refresh()
            continue
        lang_option_displayed = True
        stdscr.clear()
        if key == curses.ascii.ESC:
            language_data_to_dump = json.dumps(language)
            Path(__file__).parent.joinpath("config.json").write_text(language_data_to_dump)
            return True
        elif key in [ord('b'),ord('B')]:
            language_data_to_dump = json.dumps(language)
            Path(__file__).parent.joinpath("config.json").write_text(language_data_to_dump)
            return False
        elif key == curses.KEY_RESIZE:
            if (sh,sw) != stdscr.getmaxyx():
                sh,sw = stdscr.getmaxyx()
                curses.resizeterm(sh,sw) 
                stdscr.refresh()
        elif key == curses.KEY_DOWN:
            if on_langs:
                if lix < len(langs)-1:
                    lix += 1
                    selected_lang = "PROGRAMMING"
            else:
                if cix < len(lang_cat[selected_lang])-1:
                    cix += 1
                    selected_lang_cat = lang_cat[selected_lang][cix] 
    
        elif key == curses.KEY_UP:
            if on_langs:
                if lix > 0:
                    lix -= 1
                    selected_lang = "ENGLISH"
            else:
                if cix > 0:
                    cix -= 1
                    selected_lang_cat = lang_cat[selected_lang][cix]
                

        elif key == curses.KEY_RIGHT:
            if on_langs:
                on_langs = False
                cix=0
                selected_lang_cat = lang_cat[selected_lang][cix]

            elif not on_langs and cix < MAX_ROWS:
                cix += MAX_ROWS
                selected_lang_cat = lang_cat[selected_lang][cix]
                

        elif key == curses.KEY_LEFT:
            if not on_langs and cix < MAX_ROWS:
                on_langs = True
                selected_lang = "ENGLISH"
                lix=0
            elif not on_langs and cix >= MAX_ROWS:
                on_langs = False
                cix -= MAX_ROWS
            
        elif key in [curses.KEY_ENTER,10,13]:
            if not on_langs:
                language["lang"]=selected_lang
                language["cat"]=selected_lang_cat
    

        sh,sw = stdscr.getmaxyx()
        y=sh//2-len(lang_cat[selected_lang])//2 
        x=sw//2

        for ilx,lang in enumerate(langs):
            if ilx == lix and on_langs and lang != language["lang"] :
                stdscr.addstr(sh//2-1+2*ilx,sw//4,lang,curses.color_pair(YELLOW)|curses.A_REVERSE)
                stdscr.addstr(sh//2-1+2*ilx,sw//4+len(lang)+4,"->",curses.color_pair(BLUE))
            elif ilx == lix and on_langs and lang == language["lang"] :
                stdscr.addstr(sh//2-1+2*ilx,sw//4,lang,curses.color_pair(YELLOW)|curses.A_REVERSE)
                stdscr.addstr(sh//2-1+2*ilx,sw//4+len(lang)," ✔︎",curses.color_pair(YELLOW))
                stdscr.addstr(sh//2-1+2*ilx,sw//4+len(lang)+4,"->",curses.color_pair(BLUE))
            elif ilx == lix and lang == language["lang"] :
                stdscr.addstr(sh//2-1+2*ilx,sw//4,lang+" ✔︎",curses.color_pair(YELLOW)|curses.A_BOLD)
                stdscr.addstr(sh//2-1+2*ilx,sw//4+len(lang)+4,"->",curses.color_pair(BLUE))
            elif ilx == lix :
                stdscr.addstr(sh//2-1+2*ilx,sw//4,lang,curses.color_pair(YELLOW))
                stdscr.addstr(sh//2-1+2*ilx,sw//4+len(lang)+4,"->",curses.color_pair(BLUE))
            
            elif lang == language["lang"]:
                stdscr.addstr(sh//2-1+2*ilx,sw//4,lang+" ✔︎",curses.color_pair(YELLOW)|curses.A_BOLD)
            else :
                stdscr.addstr(sh//2-1+2*ilx,sw//4,lang,curses.color_pair(YELLOW))
        dw_=0
        iccx = 0
        for icx, cat in enumerate(lang_cat[selected_lang]):
            if icx>=MAX_ROWS:
                dw_= sw//4
                iccx=icx-MAX_ROWS
            else:
                dw_=0
                iccx=icx

            if cix == icx and not on_langs and cat != language['cat']:
                stdscr.addstr(y+2*iccx,dw_+x,cat,curses.color_pair(CYAN)|curses.A_REVERSE)
            elif cix == icx and not on_langs and cat == language['cat']:
                stdscr.addstr(y+2*iccx,dw_+x,cat+" ✔︎",curses.color_pair(CYAN)|curses.A_REVERSE)
            elif cat == language['cat']:
                stdscr.addstr(y+2*iccx,dw_+x,cat+" ✔︎",curses.color_pair(CYAN))
            else:
                stdscr.addstr(y+2*iccx,dw_+x,cat,curses.color_pair(CYAN))  

        # Show Name with user emoji
        show_user(stdscr)

        # Title
        stdscr.addstr(0,sw//2 - len(termtyper_title)//2, termtyper_title,curses.color_pair(RED)|curses.A_BOLD) 
        if sw > 80 and sh > 24:
            msg = f"Use (↑,↓,←,→) to navigate; Press 'b' to go back; and Esc to quit"
            stdscr.addstr(curses.LINES-1,1,msg,curses.color_pair(DEFAULT))
            for m in ["(↑,↓,←,→)","'b'","Esc"]:
                stdscr.chgat(curses.LINES-1,1+msg.index(m),len(m),curses.A_BOLD|curses.color_pair(BLUE))
            stdscr.refresh()
        else:
            stdscr.addstr(curses.LINES-1,1,"Terminal window size is too small.",curses.color_pair(YELLOW))
        stdscr.refresh()      

# Display challenge options
def print_options(stdscr,selected_row_ix,challenges_types,language):
    stdscr.clear()
    sh,sw = stdscr.getmaxyx()
    stdscr.addstr(sh//2-len(challenges_types)//2-2,sw//2-len("CHALLANGES")//2,"CHALLANGES",curses.color_pair(YELLOW)|curses.A_BOLD)
    for ix,row in enumerate(challenges_types):
        x=sw//2 - len(row)//2
        y=sh//2 -len(challenges_types)//2 + ix
        if ix == selected_row_ix:
            if row  == 'Go':
                stdscr.addstr(y,x,row,curses.color_pair(GREEN)|curses.A_REVERSE)
            else:
                if row == language["challange"]:
                    stdscr.addstr(y,x,row+" ✔︎",curses.color_pair(CYAN)|curses.A_REVERSE)
                else:
                    stdscr.addstr(y,x,row,curses.color_pair(CYAN)|curses.A_REVERSE) 
        else:
            if row  == 'Go':
                stdscr.addstr(y,x,row,curses.color_pair(GREEN))
            else:
                if row == language["challange"]:
                    stdscr.addstr(y,x,row+" ✔︎",curses.color_pair(CYAN))
                else:
                    stdscr.addstr(y,x,row,curses.color_pair(CYAN))

    # Show Name with user emoji
    show_user(stdscr) 
    # Title
    stdscr.addstr(0,sw//2 - len(termtyper_title)//2, termtyper_title,curses.color_pair(RED)|curses.A_BOLD)
    if sw > 80 and sh > 24:
        msg = f"Use (↑,↓) to navigate; Press F1 for more language options; and Esc to quit."
        stdscr.addstr(curses.LINES-1,1,msg,curses.color_pair(DEFAULT))
        for m in ["(↑,↓)","F1","Esc"]:
            stdscr.chgat(curses.LINES-1,1+msg.index(m),len(m),curses.A_BOLD|curses.color_pair(BLUE))
        stdscr.refresh()

    else:
        stdscr.addstr(curses.LINES-1,1,"Terminal window size is too small.",curses.color_pair(YELLOW))

    stdscr.refresh()


def option_display(stdscr,language):

    ONE_MINUTE = 60
    TWO_MINUTE = 120
    THREE_MINUTE = 180
    FIVE_MINUTE =  300
    TEN_MINUTE = 600
    FIFTEEN_MINUTE = 900
    THIRTY_MINUTE = 1800

    sh,sw = stdscr.getmaxyx()
    current_row_ix = 0
    if language["challange"] == "01 Minute Test":
        current_row_ix= 0
    elif language["challange"] == "02 Minute Test":
        current_row_ix= 1 
    elif language["challange"] == "03 Minute Test":
        current_row_ix= 2
    elif language["challange"] == "05 Minute Test":
        current_row_ix= 3 
    elif language["challange"] == "10 Minute Test":
        current_row_ix= 4
    elif language["challange"] == "15 Minute Test":
        current_row_ix= 5


    challenges_types = ['01 Minute Test', '02 Minute Test', '03 Minute Test', '05 Minute Test','10 Minute Test','15 Minute Test','','Go']
    print_options(stdscr,current_row_ix,challenges_types,language)
    option_displayed = False
    sh,sw = stdscr.getmaxyx()
    while True:
        key = stdscr.getch()
        if key == curses.ERR and option_displayed: 
            stdscr.refresh()
            continue
        option_displayed = True
        stdscr.clear()
        if key == curses.KEY_RESIZE:
            if (sh,sw) != stdscr.getmaxyx():
                sh,sw=stdscr.getmaxyx()
                curses.resizeterm(sh,sw) 
                print_options(stdscr,current_row_ix,challenges_types,language)
                stdscr.refresh()
        if key == curses.ascii.ESC:
            return True

        elif key == curses.KEY_UP and current_row_ix > 0:

            if current_row_ix == len(challenges_types)-1:
                current_row_ix -= 2
            else:
                 current_row_ix -= 1
        elif key == curses.KEY_DOWN and current_row_ix < len(challenges_types)-1:
            if current_row_ix == len(challenges_types)-3:
                current_row_ix += 2
            else:
                current_row_ix += 1 
        elif key == curses.KEY_F1:
            break_it = lang_option(stdscr,language)
            if break_it:
                return True
          

        elif key in [curses.KEY_ENTER,10,13]:
            if challenges_types[current_row_ix] == 'Go':
                language_data_to_dump = json.dumps(language)
                Path(__file__).parent.joinpath("config.json").write_text(language_data_to_dump)
                return False
            elif challenges_types[current_row_ix] == "01 Minute Test":
                language["max_time"]= ONE_MINUTE
                language["challange"]="01 Minute Test"

            elif challenges_types[current_row_ix] == "02 Minute Test":
                language["max_time"]= TWO_MINUTE
                language["challange"]="02 Minute Test"

            elif challenges_types[current_row_ix] == "03 Minute Test":
                language["max_time"] = THREE_MINUTE
                language["challange"]="03 Minute Test"

            elif challenges_types[current_row_ix] == "05 Minute Test":
                language["max_time"] = FIVE_MINUTE
                language["challange"]="05 Minute Test"

            elif challenges_types[current_row_ix] == "10 Minute Test":
                language["max_time"] = TEN_MINUTE 
                language["challange"]="10 Minute Test"
            elif challenges_types[current_row_ix] == "15 Minute Test":
                language["max_time"] = FIFTEEN_MINUTE 
                language["challange"]="15 Minute Test"


        print_options(stdscr,current_row_ix,challenges_types,language)
        stdscr.refresh()


def typed_effect(stdscr,key_map,key,color=DEFAULT):
    y,x,dx = key_map[key]
    stdscr.chgat(y,x,dx,curses.color_pair(color)|curses.A_REVERSE)
    stdscr.chgat(y+1,x,dx,curses.color_pair(color)|curses.A_REVERSE)

def keyboard(stdscr,kbd_y_offset,kbd_x_offset,key_map):
    curses.use_default_colors()

    keybd_dict = {}
    for i,row in enumerate([keyrow.split(' ') for keyrow in key_board]):

        xl= kbd_x_offset
        for j,c in enumerate(row):
            c1,c2 = c[:c.index('.')],c[c.index('.')+1:]
            nn=2
            if len(c2)>1:
                nn=1
            keybd_dict[(kbd_y_offset+3*(i+1),xl)]=(nn*" "+c1+(len(c2)-len(c1)+nn)*" ",nn*" "+c2+nn*" ")
            for k in key_Board[i][j]:
                key_map[k] = (kbd_y_offset+3*(i+1),xl,len(c2)+2*nn)

            xl += len(nn*" "+c2+nn*" ")+2


    for key in keybd_dict:
        y,x = key[0],key[1]
        if ';' in keybd_dict[key][0]:
            kk0 = keybd_dict[key][0].replace(';',' ')
        else:
            kk0 = keybd_dict[key][0] 

        if ':' in keybd_dict[key][1]:
            kk1 = keybd_dict[key][1].replace(':',' ')
        else:
            kk1 = keybd_dict[key][1] 

        stdscr.addstr(y,x,f"{kk0}",curses.color_pair(DEFAULT)|curses.A_REVERSE)
        stdscr.addstr(y+1,x,f"{kk1}",curses.color_pair(DEFAULT)|curses.A_REVERSE)
    


# Main

VERSION_NUMBER = '2.0.5'

def latest_version(pkg_name='termtyper'):
    try:
        url = f"https://pypi.org/pypi/{pkg_name}/json"
        data = json.load(urllib.request.urlopen(url))
        versions = sorted(list(data["releases"].keys()))
        return versions[-1]
    except Exception as e:
        print()
        print("Attempted to check for latest updates. But could not get the latest vesion information.")
        print("Due to the following Error:")
        print(e)
        print(10*"-")
        print("Please wait. termtyper will open in 5 seconds...")
        time.sleep(5)
        return VERSION_NUMBER


def termtyper_main(stdscr):
    curses.curs_set(False)
    curses.mousemask(True)
    stdscr.nodelay(True)
    stdscr.timeout(100)
    curses.use_default_colors()
    curses.init_pair(1,-1,-1)
    curses.init_pair(2,curses.COLOR_GREEN,-1)
    curses.init_pair(3,curses.COLOR_RED,-1)
    curses.init_pair(4,curses.COLOR_YELLOW,-1)
    curses.init_pair(5,curses.COLOR_MAGENTA,-1)
    curses.init_pair(6,curses.COLOR_CYAN,-1)
    curses.init_pair(7,curses.COLOR_BLUE,-1)
    curses.init_pair(8,curses.COLOR_WHITE,curses.COLOR_BLACK)



    stats_data = Path(__file__).parent.joinpath("wpm_statistics.json").read_text()
    stats = json.loads(stats_data)
    if len(stats) == 0:
        try:
            p=Path.home()/'termtyper_wpm_statistics_backup_DO_NOT_DELETE_IT'
            stats_data=p.joinpath('wpm_statistics.json').read_text()
            stats = json.loads(stats_data)
            shutil.rmtree(p)
        except:
            pass
    language_data = Path(__file__).parent.joinpath("config.json").read_text()
    language = json.loads(language_data)



    termtyper(stdscr,language,stats)

    language_data_to_dump = json.dumps(language)
    Path(__file__).parent.joinpath("config.json").write_text(language_data_to_dump)

    stats_data_to_dump = json.dumps(stats)
    Path(__file__).parent.joinpath("wpm_statistics.json").write_text(stats_data_to_dump)


def upgrade(update):
    try:
        stats_data = Path(__file__).parent.joinpath("wpm_statistics.json").read_text()
        if len(stats_data.strip()) > 2:
            p=Path.home()/'termtyper_wpm_statistics_backup_DO_NOT_DELETE_IT'
            p.mkdir(parents=True,exist_ok=True)
            p.joinpath('wpm_statistics.json').write_text(stats_data)
        os.system("pip uninstall termtyper -y")
        print(10*"-")
        os.system("pip install termtyper")
        print("termtyper is successfully upgraded to latest version!")

    except:
        print(f"Could not upgrade to latest version number: {update['number']}")

def run():
    today=str(date.today())
    parser = argparse.ArgumentParser(
        prog='termtyper',
        description='A terminal based typing practice application.'
    )
    parser.add_argument('--version',default=False,action="store_true",help='Show program version')
    parser.add_argument('--upgrade',default=False,action="store_true",help='Upgrade to latest version')
    args = parser.parse_args()

    update_data = Path(__file__).parent.joinpath("update.json").read_text()
    update = json.loads(update_data)
    latestVersion = VERSION_NUMBER
    
    if update["check_date"] == "" or (days_difference(update["check_date"],today) > 7 and not update["available"]):
         latestVersion = latest_version()
         if latestVersion > VERSION_NUMBER:
             update["available"]=True
             update["number"]=latestVersion
         update["check_date"]=today
    update_data_to_dump = json.dumps(update)
    Path(__file__).parent.joinpath("update.json").write_text(update_data_to_dump)

    if update["available"] and (update["last_shown"] == "" or days_difference(update["last_shown"],today) >=1):
        update["last_shown"]=today
        update_data_to_dump = json.dumps(update)
        Path(__file__).parent.joinpath("update.json").write_text(update_data_to_dump)
        print(f"Update: termtyper {latestVersion} is available!")
        ip=input("Do you want to upgrade? (Y/n):")
        if ip in ['y','Y']:
            upgrade(update)
            update["last_shown"]=""
            update["available"]=False
            update_data_to_dump = json.dumps(update)
            Path(__file__).parent.joinpath("update.json").write_text(update_data_to_dump)
            return

    if args.version or args.upgrade:
        if args.version:
            print(f"termtyper {VERSION_NUMBER}")
        if args.upgrade:
            try:
                latestVersion = latest_version()
                if latestVersion > VERSION_NUMBER :
                    upgrade(update)
                elif latestVersion == VERSION_NUMBER:
                    print("termtyper is up to date.")
            except:
                print("Could not get the latest version information.")
    else:
        curses.wrapper(termtyper_main)


if __name__ == '__main__':
    run()