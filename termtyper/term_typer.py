#!/usr/bin/env python

import curses
from curses import textpad
import time
import json
import random
import platform
from pathlib import Path


dw=2
ZERO,ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN,EIGHT,NINE,TEN = tuple(range(0,11))
DEFAULT,GREEN,RED,YELLOW,MAGENTA,CYAN,BLUE,WHITE=tuple(range(1,9))
MAX_WORDS_PER_SECOND = 5
KEYBOARD_WIDTH = 116
KEYBOARD_HEIGHT = 16
KEYBOARD_Y_OFFSET = 12

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
    (curses.ascii.DEL,curses.KEY_BACKSPACE),(curses.KEY_HOME,)],
    [(curses.ascii.TAB,9),(ord("Q"),ord("q")), (ord("W"),ord("w")),(ord("E"),ord("e")),(ord("R"),ord("r")),(ord("T"),ord("t")),(ord("Y"),ord("y")),(ord("U"),ord("u")),(ord("I"),ord("i")),(ord("O"),ord("o")),(ord("P"),ord("p")),(ord("{"),ord("[")),(ord("}"),ord("]")),(ord("|"),ord("\\")),
    (curses.KEY_END,)],
    [("Caps Lock",), (ord("A"),ord("a")),(ord("S"),ord("s")),(ord("D"),ord("d")),(ord("F"),ord("f")),(ord("G"),ord("g")),(ord("H"),ord("h")),(ord("J"),ord("j")),(ord("K"),ord("k")), (ord("L"),ord("l")),(ord(":"),ord(";")), (ord("\""),ord("'")), (curses.KEY_ENTER,10,13),(curses.KEY_PPAGE,)],
    [("Shift",),(ord("Z"),ord("z")), (ord("X"),ord("x")), (ord("C"),ord("c")), (ord("V"),ord("v")),(ord("B"),ord("b")), (ord("N"),ord("n")), (ord("M"),ord("m")), (ord("<"),ord(",")), (ord(">"),ord(".")), (ord("?"),ord("/")), ("Shift",),(curses.KEY_UP,),(curses.KEY_NPAGE,)],
    [("Ctrl",),("Alt","Win"),("Command","Alt"),(curses.ascii.SP,32),("Command","Alt"),("Alt","Win"),(curses.KEY_LEFT,),(curses.KEY_DOWN,),(curses.KEY_RIGHT,)]
]

osname = platform.system()
if  osname == 'Darwin':
    key_board = mac_key_board
else:
    key_board = other_key_board

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
    sh, sw = stdscr.getmaxyx()
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

    msg = "Press F5 to Refresh; F2 to customize the test; F3 to toggle onscreen keyboard; and Esc to quit; "
    if  len(msg) < sw-2:
        stdscr.addstr(curses.LINES-1,1,msg,curses.color_pair(DEFAULT))
        for opt in ["F5","F2","F3","Esc"]:
            stdscr.chgat(curses.LINES-1,msg.index(opt)+1,len(opt),curses.A_BOLD|curses.color_pair(BLUE))


def print_text(stdscr,text_list,color_dict,l=0): # prints three lines of text to be typed

    sh, sw = stdscr.getmaxyx()
    for i in range(3):
        stdscr.addstr(dw+1+i,dw+1,(sw-dw-4)*' ')
    text_list_ = text_list[3*(l//3):3*(l//3)+3]
    for i,text in enumerate(text_list_):
        i_=3*(l//3)+i
        stdscr.move(dw+i+1,dw+1) 
        for j in range(len(text)):
            stdscr.addch(text[j],color_dict[(i_,j)]) 

  
def can_dispay_keyboard(stdscr): # returns true if keyboard fit in screen
    sh,sw = stdscr.getmaxyx()
    return (sw > KEYBOARD_WIDTH) and (sh > KEYBOARD_HEIGHT + KEYBOARD_Y_OFFSET)

def print_result(stdscr,result,unit_time,language): # prints the performance result

    sh, sw = stdscr.getmaxyx()
    max_time = language["max_time"]
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
    box_begin_y = dw+sh//2-10
    box_begin_x = dw+sw//2-20
    box_width = 38
    box_height = 18

    textpad.rectangle(stdscr,box_begin_y,box_begin_x,box_begin_y+box_height,box_begin_x+box_width)
    stdscr.hline(dw+sh//2-7,dw+sw//2-19,'_',box_width-1)

    stdscr.addstr(box_begin_y + dw, box_begin_x+15, "RESULT",curses.A_BOLD | curses.color_pair(DEFAULT))


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
    msg = "Press Enter to continue."
    stdscr.addstr(curses.LINES-1,1,msg,curses.color_pair(DEFAULT))
    stdscr.chgat(curses.LINES-1,1+msg.index("Enter"),5,curses.A_BOLD|curses.color_pair(BLUE))
    stdscr.refresh()
    #curses.doupdate()

    while True:
        key = stdscr.getch()
        if key in [10,13,curses.KEY_ENTER,curses.ascii.CR]:
            stdscr.clear()
            break
        

def termtyper(stdscr,language,words):

    sh, sw = stdscr.getmaxyx()

    text = words[language["lang"]][language["cat"]]
    color_dict={}
    abs_color_dict={} 
    cum_line_lengths={}
    space_locations = []
    ch_ix=0
    sp_ix=0
    refresh = False
    max_time = language["max_time"]
    time_left = max_time
    unit_time = 60
    number_of_words = max_time*MAX_WORDS_PER_SECOND
    key_map={}
    random_text = random.choices(text.split(' '),k=number_of_words)
    textlist = split_text(random_text,sw-3*dw)
    on_screen_kbd = True
    kbd_click_sounds = False
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
    if on_screen_kbd and can_dispay_keyboard(stdscr):
        keyboard(stdscr,KEYBOARD_Y_OFFSET,(sw-KEYBOARD_WIDTH)//2,key_map)

    start_time= time.time()
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

            print_result(stdscr,result,unit_time,language)


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
            started = True

        if pkey != None and  started and on_screen_kbd and can_dispay_keyboard(stdscr):
            typed_effect(stdscr,key_map,pkey)
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



        elif key == ord(textlist[l][i]) and key != curses.ascii.SP :
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




        elif key in [curses.ascii.SP,32]:    # key is space
            if j == 0:
                a = 0
            else:
                a=space_locations[l][j-1]+1
            if textlist[l][a:b] != ip_text: 
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




        elif key in [curses.ascii.DEL,curses.KEY_BACKSPACE]:    # key delete or back space ,
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
                option_display(stdscr,language)

            result = {
                "wrong_key_strokes" : 0,
                "total_key_strokes" : 0,
                "wrong_words_typed" : 0,
                "total_words_typed": 0,
            }
            refresh = True
            started = False
            pkey = None
            max_time=language["max_time"]
            time_left = max_time
            number_of_words = max_time*MAX_WORDS_PER_SECOND
            start_time = time.time()
            text = words[language["lang"]][language["cat"]]
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
            kbd_click_sounds = not kbd_click_sounds


        elif key == curses.KEY_LEFT:   # key <-

            if on_screen_kbd and can_dispay_keyboard(stdscr):
                typed_effect(stdscr,key_map,key,YELLOW)
                
            if ip_text_ix > 0:
                ip_text_ix -= 1
                i -= 1

        elif key == curses.KEY_RIGHT: # key ->

            if on_screen_kbd and can_dispay_keyboard(stdscr):
                typed_effect(stdscr,key_map,key,YELLOW)
            if ip_text_ix <len(ip_text):
                ip_text_ix += 1
                i += 1
        elif key in [curses.KEY_UP,curses.KEY_DOWN,curses.KEY_HOME,curses.KEY_PPAGE,
                curses.KEY_NPAGE,curses.KEY_END,10,13,curses.KEY_ENTER,curses.KEY_DC,curses.KEY_IC]:
                if on_screen_kbd and can_dispay_keyboard(stdscr):
                    typed_effect(stdscr,key_map,key,YELLOW)


        elif ord(' ') <= key <= ord('~'):
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
        stdscr.addstr(dw+6,dw+1+1,sw//2*' ',curses.color_pair(DEFAULT))
        stdscr.addstr(dw+6,dw+1+1,iip_text,curses.color_pair(SIX))
        stdscr.chgat(dw+6,dw+1+ip_text_ix+1,1,curses.A_BLINK|curses.color_pair(SIX))


        time_left_s = int(time_left)
        time_left_ms = int((time_left - time_left_s)*100)

        stdscr.addstr(1,dw+1,f"{(time_left_s//60)//10}{(time_left_s//60)%10}:{(time_left_s%60)//10}{(time_left_s%60)%10}:{time_left_ms//10}{time_left_ms%10}",curses.A_BOLD)
        stdscr.chgat(1,dw+1,2,curses.color_pair(BLUE)|curses.A_BOLD)
        stdscr.chgat(1,dw+3,1,curses.color_pair(DEFAULT)|curses.A_BOLD)
        stdscr.chgat(1,dw+4,2,curses.color_pair(MAGENTA)|curses.A_BOLD)
        stdscr.chgat(1,dw+6,1,curses.color_pair(DEFAULT)|curses.A_BOLD)
        stdscr.chgat(1,dw+7,2,curses.color_pair(YELLOW)|curses.A_BOLD) 
    
        if started:
            time_left = max_time - (time.time()-start_time)
        if  key in list(range(ord(' '),ord('~')+1))+[curses.KEY_BACKSPACE,curses.ascii.DEL,curses.KEY_LEFT,curses.KEY_RIGHT,curses.KEY_UP,curses.KEY_DOWN,curses.KEY_HOME,curses.KEY_PPAGE,
                curses.KEY_NPAGE,curses.KEY_END,10,13,curses.KEY_ENTER,curses.KEY_DC,curses.KEY_IC]:
            pkey = key
        stdscr.refresh()



def lang_option(stdscr,language):
    MAX_ROWS = 6
    h,w = stdscr.getmaxyx()
    lang_cat={"ENGLISH":["TOP50 WORDS","TOP100 WORDS","TOP200 WORDS","TOP300 WORDS","TOP500 WORDS","TOP1000 WORDS"],
    "PROGRAMMING":["C/CPP","C#","JAVA","PYTHON","SWIFT","HTML","JAVASCRIPT","GO","PHP","RUBY","KOTLIN","RUST"]}
    selected_lang = language["lang"]
    selected_lang_cat =language["cat"]
    langs = sorted(lang_cat.keys())
    on_langs = True
    lix=0
    cix =0
    lang_options_displayed = False
    if language["lang"] == "ENGLISH":
        lix=0
    else:
        lix=1
    while True:
        key = stdscr.getch()
        if key == -1 and lang_options_displayed:
            continue
        lang_options_displayed=True
        stdscr.clear()
        if key == curses.ascii.ESC:
            break
        if key == curses.KEY_RESIZE:
            if (h,w) != stdscr.getmaxyx():
                h,w = stdscr.getmaxyx()
                curses.resizeterm(h,w) 
        if key == curses.KEY_DOWN:
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

            elif not on_langs and cix < MAX_ROWS and selected_lang != "ENGLISH":
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
            language["lang"]=selected_lang
            language["cat"]=selected_lang_cat
    

        h,w = stdscr.getmaxyx()
        if selected_lang == "ENGLISH":
            y=h//2-len(lang_cat[selected_lang])
        else:
           y=h//2-len(lang_cat[selected_lang])//2 
        x=w//2

        for ilx,lang in enumerate(langs):
            if ilx == lix and on_langs and lang != language["lang"] :
                stdscr.addstr(h//2-1+2*ilx,w//4,lang,curses.color_pair(YELLOW)|curses.A_REVERSE)
                stdscr.addstr(h//2-1+2*ilx,w//4+len(lang)+4,"->",curses.color_pair(BLUE))
            elif ilx == lix and on_langs and lang == language["lang"] :
                stdscr.addstr(h//2-1+2*ilx,w//4,lang,curses.color_pair(YELLOW)|curses.A_REVERSE)
                stdscr.addstr(h//2-1+2*ilx,w//4+len(lang)," ✔︎",curses.color_pair(YELLOW))
                stdscr.addstr(h//2-1+2*ilx,w//4+len(lang)+4,"->",curses.color_pair(BLUE))
            elif ilx == lix and lang == language["lang"] :
                stdscr.addstr(h//2-1+2*ilx,w//4,lang+" ✔︎",curses.color_pair(YELLOW)|curses.A_BOLD)
                stdscr.addstr(h//2-1+2*ilx,w//4+len(lang)+4,"->",curses.color_pair(BLUE))
            elif ilx == lix :
                stdscr.addstr(h//2-1+2*ilx,w//4,lang,curses.color_pair(YELLOW))
                stdscr.addstr(h//2-1+2*ilx,w//4+len(lang)+4,"->",curses.color_pair(BLUE))
            
            elif lang == language["lang"]:
                stdscr.addstr(h//2-1+2*ilx,w//4,lang+" ✔︎",curses.color_pair(YELLOW)|curses.A_BOLD)
            else :
                stdscr.addstr(h//2-1+2*ilx,w//4,lang,curses.color_pair(YELLOW))
        dw_=0
        iccx = 0
        for icx, cat in enumerate(lang_cat[selected_lang]):
            if icx>=MAX_ROWS:
                dw_= w//4
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
        stdscr.addstr(curses.LINES-1,1,"Press ESC to go back",curses.color_pair(DEFAULT))
        stdscr.chgat(curses.LINES-1,7,3,curses.A_BOLD|curses.color_pair(BLUE))
        stdscr.refresh()
      

def print_options(stdscr,selected_row_ix,challenges_types,language):
    stdscr.clear()
    h,w = stdscr.getmaxyx()
    stdscr.addstr(h//2-len(challenges_types)//2-2,w//2-len("CHALLANGES")//2,"CHALLANGES",curses.color_pair(YELLOW)|curses.A_BOLD)
    for ix,row in enumerate(challenges_types):
        x=w//2 - len(row)//2
        y=h//2 -len(challenges_types)//2 + ix
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

    stdscr.addstr(curses.LINES-1,1,"Press F1 for more language options.",curses.color_pair(1))
    stdscr.chgat(curses.LINES-1,7,2,curses.A_BOLD|curses.color_pair(BLUE))
    stdscr.refresh()


def option_display(stdscr,language):
    # curses.curs_set(0)
    ONE_MINUTE = 60
    TWO_MINUTE = 120
    THREE_MINUTE = 180
    FIVE_MINUTE =  300
    TEN_MINUTE = 600

    h,w = stdscr.getmaxyx()
    current_row_ix = 0
    if language["challange"] == "1 Minute Test":
        current_row_ix= 0
    elif language["challange"] == "2 Minute Test":
        current_row_ix= 1 
    elif language["challange"] == "3 Minute Test":
        current_row_ix= 2
    elif language["challange"] == "5 Minute Test":
        current_row_ix= 3 
    elif language["challange"] == "10 Minute Test":
        current_row_ix= 4

    challenges_types = ['1 Minute Test', '2 Minute Test', '3 Minute Test', '5 Minute Test','10 Minute Test',"",'Go']
    print_options(stdscr,current_row_ix,challenges_types,language)
    options_displayed = False
    while True:
        key = stdscr.getch()
        if key == -1 and options_displayed:
            continue
        options_displayed=True
        stdscr.clear()
        if key == curses.KEY_RESIZE:
            if (h,w) != stdscr.getmaxyx():
                h,w=stdscr.getmaxyx()
                curses.resizeterm(h,w) 
        elif key == curses.KEY_UP and current_row_ix > 0:

            if current_row_ix == len(challenges_types)-1:
                current_row_ix -= 2
            else:
                 current_row_ix -= 1
        elif key == curses.KEY_DOWN and current_row_ix < len(challenges_types)-1:
            prev_row_ix = current_row_ix
            if current_row_ix == len(challenges_types)-3:
                current_row_ix += 2
            else:
                current_row_ix += 1 
        elif key == curses.KEY_F1:
            lang_option(stdscr,language)

        elif key in [curses.KEY_ENTER,10,13]:
            if challenges_types[current_row_ix] == 'Go':
                break
            elif challenges_types[current_row_ix] == "1 Minute Test":
                language["max_time"]= ONE_MINUTE
                language["challange"]="1 Minute Test"

            elif challenges_types[current_row_ix] == "2 Minute Test":
                language["max_time"]= TWO_MINUTE
                language["challange"]="2 Minute Test"

            elif challenges_types[current_row_ix] == "3 Minute Test":
                language["max_time"] = THREE_MINUTE
                language["challange"]="3 Minute Test"

            elif challenges_types[current_row_ix] == "5 Minute Test":
                language["max_time"] = FIVE_MINUTE
                language["challange"]="5 Minute Test"

            elif challenges_types[current_row_ix] == "10 Minute Test":
                language["max_time"] = TEN_MINUTE 
                language["challange"]="10 Minute Test"


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
    
    words_data = Path(__file__).parent.joinpath("data").joinpath("words.json").read_text()
    words = json.loads(words_data)

    language_data = Path(__file__).parent.joinpath("config.json").read_text()
    language = json.loads(language_data)

    termtyper(stdscr,language,words)

    language_data_to_dump = json.dumps(language)
    Path(__file__).parent.joinpath("config.json").write_text(language_data_to_dump)

def run():
    curses.wrapper(termtyper_main)


if __name__ == '__main__':
    run()