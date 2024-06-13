#!/usr/bin/env python
""#line:5
import sys  # line:6

M =8 #line:8
MAX_DEPTH =int (sys .argv [1 ])#line:9
CORNER =8 #line:11
BAD_CORNER =-3 #line:12
MOVES =0.8 #line:13
BC2 =[((0 ,7 ),(1 ,7 )),((0 ,7 ),(0 ,6 )),((0 ,0 ),(1 ,0 )),((0 ,0 ),(0 ,1 )),((7 ,0 ),(7 ,1 )),((7 ,0 ),(6 ,0 )),((7 ,7 ),(6 ,7 )),((7 ,7 ),(7 ,6 ))]#line:25
INFTY =999999999 #line:27
import random  # line:29
import sys  # line:30


def parameter_mult ():#line:33
    return 0.8 +0.4 *random .random ()#line:34
class Reversi :#line:37
    M =8 #line:38
    DIRS =[(0 ,1 ),(1 ,0 ),(-1 ,0 ),(0 ,-1 ),(1 ,1 ),(-1 ,-1 ),(1 ,-1 ),(-1 ,1 )]#line:40
    def __init__ (O0000O00O0O0OO0OO ):#line:42
        O0000O00O0O0OO0OO .board =O0000O00O0O0OO0OO .initial_board ()#line:43
        O0000O00O0O0OO0OO .fields =set ()#line:44
        O0000O00O0O0OO0OO .move_list =[]#line:45
        O0000O00O0O0OO0OO .history =[]#line:46
        for O0000O00OO0OO0O0O in range (O0000O00O0O0OO0OO .M ):#line:47
            for OOO0O0OO00000O0OO in range (O0000O00O0O0OO0OO .M ):#line:48
                if O0000O00O0O0OO0OO .board [O0000O00OO0OO0O0O ][OOO0O0OO00000O0OO ]is None :#line:49
                    O0000O00O0O0OO0OO .fields .add ((OOO0O0OO00000O0OO ,O0000O00OO0OO0O0O ))#line:50
        O0000O00O0O0OO0OO .CORNER =CORNER *parameter_mult ()#line:52
        O0000O00O0O0OO0OO .BAD_CORNER =BAD_CORNER *parameter_mult ()#line:53
        O0000O00O0O0OO0OO .MOVES =MOVES *parameter_mult ()#line:54
    def initial_board (OO0O000OO0000O00O ):#line:56
        OO0O0OO0000000OOO =[[None ]*OO0O000OO0000O00O .M for _O0O0000O0OO0O0O0O in range (OO0O000OO0000O00O .M )]#line:57
        OO0O0OO0000000OOO [3 ][3 ]=1 #line:58
        OO0O0OO0000000OOO [4 ][4 ]=1 #line:59
        OO0O0OO0000000OOO [3 ][4 ]=0 #line:60
        OO0O0OO0000000OOO [4 ][3 ]=0 #line:61
        return OO0O0OO0000000OOO #line:62
    def draw (OOO0O0O0OO0OOOOOO ):#line:64
        for OOOOO000O000O00OO in range (OOO0O0O0OO0OOOOOO .M ):#line:65
            OO000OO00000OO00O =[]#line:66
            for O000OO0O0O0OOOO0O in range (OOO0O0O0OO0OOOOOO .M ):#line:67
                OOOO00OOOOO000OOO =OOO0O0O0OO0OOOOOO .board [OOOOO000O000O00OO ][O000OO0O0O0OOOO0O ]#line:68
                if OOOO00OOOOO000OOO is None :#line:69
                    OO000OO00000OO00O .append ('.')#line:70
                elif OOOO00OOOOO000OOO ==1 :#line:71
                    OO000OO00000OO00O .append ('#')#line:72
                else :#line:73
                    OO000OO00000OO00O .append ('o')#line:74
            print (''.join (OO000OO00000OO00O ))#line:75
        print ('')#line:76
    def moves (O0O00OO0OOO0O0OOO ,O000OOOOO00OOOOO0 ):#line:78
        OO00O000OOOO0000O =[]#line:79
        for (O0O000OO0O00O0000 ,O000OO00OOOO0OOO0 )in O0O00OO0OOO0O0OOO .fields :#line:80
            if any (O0O00OO0OOO0O0OOO .can_beat (O0O000OO0O00O0000 ,O000OO00OOOO0OOO0 ,O0O0O0O00OOOOO00O ,O000OOOOO00OOOOO0 )for O0O0O0O00OOOOO00O in O0O00OO0OOO0O0OOO .DIRS ):#line:82
                OO00O000OOOO0000O .append ((O0O000OO0O00O0000 ,O000OO00OOOO0OOO0 ))#line:83
        if OO00O000OOOO0000O ==[]:#line:85
            return [None ]#line:86
        return OO00O000OOOO0000O #line:87
    def can_beat (O000OOO0OO00O00OO ,OOOOO000O0OOO00O0 ,OO00O0OOO0000OO00 ,OO00000OOOO00000O ,OO0OO000OOO00O000 ):#line:89
        O0OOOO00O00O0O00O ,OOOO0O0OOO0O00000 =OO00000OOOO00000O #line:90
        OOOOO000O0OOO00O0 +=O0OOOO00O00O0O00O #line:91
        OO00O0OOO0000OO00 +=OOOO0O0OOO0O00000 #line:92
        O000O00OOO00OO00O =0 #line:93
        while O000OOO0OO00O00OO .get (OOOOO000O0OOO00O0 ,OO00O0OOO0000OO00 )==1 -OO0OO000OOO00O000 :#line:94
            OOOOO000O0OOO00O0 +=O0OOOO00O00O0O00O #line:95
            OO00O0OOO0000OO00 +=OOOO0O0OOO0O00000 #line:96
            O000O00OOO00OO00O +=1 #line:97
        return O000O00OOO00OO00O >0 and O000OOO0OO00O00OO .get (OOOOO000O0OOO00O0 ,OO00O0OOO0000OO00 )==OO0OO000OOO00O000 #line:98
    def get (OOOO000OOOOOOO0OO ,O000O00000O0OOOOO ,OOO00O000OOOOO00O ):#line:100
        if 0 <=O000O00000O0OOOOO <OOOO000OOOOOOO0OO .M and 0 <=OOO00O000OOOOO00O <OOOO000OOOOOOO0OO .M :#line:101
            return OOOO000OOOOOOO0OO .board [OOO00O000OOOOO00O ][O000O00000O0OOOOO ]#line:102
        return None #line:103
    def do_move (OO0OO00O000O0OOOO ,O000OO000O0O0000O ,OO00OO0000O0OO0O0 ):#line:105
        assert OO00OO0000O0OO0O0 ==len (OO0OO00O000O0OOOO .move_list )%2 #line:106
        OO0OO00O000O0OOOO .history .append ([O000000O0O0O00O0O [:]for O000000O0O0O00O0O in OO0OO00O000O0OOOO .board ])#line:107
        OO0OO00O000O0OOOO .move_list .append (O000OO000O0O0000O )#line:108
        if O000OO000O0O0000O is None :#line:110
            return #line:111
        OOO00O00OOOOOOO0O ,OOO00O0O0O000O0OO =O000OO000O0O0000O #line:112
        OOO00O0O0OO000O0O ,O00OOOO00OO0OO00O =O000OO000O0O0000O #line:113
        OO0OO00O000O0OOOO .board [OOO00O0O0O000O0OO ][OOO00O00OOOOOOO0O ]=OO00OO0000O0OO0O0 #line:114
        OO0OO00O000O0OOOO .fields -=set ([O000OO000O0O0000O ])#line:115
        for O0OO0OOO00OOOO0O0 ,OO00O0OO0OOO0O0O0 in OO0OO00O000O0OOOO .DIRS :#line:116
            OOO00O00OOOOOOO0O ,OOO00O0O0O000O0OO =OOO00O0O0OO000O0O ,O00OOOO00OO0OO00O #line:117
            O0OO0OO00O00OOOO0 =[]#line:118
            OOO00O00OOOOOOO0O +=O0OO0OOO00OOOO0O0 #line:119
            OOO00O0O0O000O0OO +=OO00O0OO0OOO0O0O0 #line:120
            while OO0OO00O000O0OOOO .get (OOO00O00OOOOOOO0O ,OOO00O0O0O000O0OO )==1 -OO00OO0000O0OO0O0 :#line:121
                O0OO0OO00O00OOOO0 .append ((OOO00O00OOOOOOO0O ,OOO00O0O0O000O0OO ))#line:122
                OOO00O00OOOOOOO0O +=O0OO0OOO00OOOO0O0 #line:123
                OOO00O0O0O000O0OO +=OO00O0OO0OOO0O0O0 #line:124
            if OO0OO00O000O0OOOO .get (OOO00O00OOOOOOO0O ,OOO00O0O0O000O0OO )==OO00OO0000O0OO0O0 :#line:125
                for (OOOOOO000O0000000 ,OO00OOO00O00OOOO0 )in O0OO0OO00O00OOOO0 :#line:126
                    OO0OO00O000O0OOOO .board [OO00OOO00O00OOOO0 ][OOOOOO000O0000000 ]=OO00OO0000O0OO0O0 #line:127
    def result (O00O0000O0000O00O ):#line:129
        O00O00OOO0O0O0O00 =0 #line:130
        for O0O000OO00O0OO0O0 in range (O00O0000O0000O00O .M ):#line:131
            for O00OOOOOOO00O000O in range (O00O0000O0000O00O .M ):#line:132
                O00O000OO0OOOOOOO =O00O0000O0000O00O .board [O0O000OO00O0OO0O0 ][O00OOOOOOO00O000O ]#line:133
                if O00O000OO0OOOOOOO ==0 :#line:134
                    O00O00OOO0O0O0O00 -=1 #line:135
                elif O00O000OO0OOOOOOO ==1 :#line:136
                    O00O00OOO0O0O0O00 +=1 #line:137
        return O00O00OOO0O0O0O00 #line:138
    def terminal (O00000O00OOO000OO ):#line:140
        if not O00000O00OOO000OO .fields :#line:141
            return True #line:142
        if len (O00000O00OOO000OO .move_list )<2 :#line:143
            return False #line:144
        return O00000O00OOO000OO .move_list [-1 ]is None and O00000O00OOO000OO .move_list [-2 ]is None #line:145
    def in_corner (O00OOOOO000OO00OO ,OO0OOOOOOO0O000O0 ):#line:147
        OOOO00OO0000O0000 =0 #line:148
        for OOOOO00O00OO0O0O0 ,O0O0OO00OOO00O0O0 in [(0 ,7 ),(0 ,0 ),(7 ,0 ),(7 ,7 )]:#line:149
            if O00OOOOO000OO00OO .board [O0O0OO00OOO00O0O0 ][OOOOO00O00OO0O0O0 ]==OO0OOOOOOO0O000O0 :#line:150
                OOOO00OO0000O0000 +=1 #line:151
        return OOOO00OO0000O0000 #line:152
    def bad_corner (OO00000OOOOO000O0 ,O00OOOOOO00000OO0 ):#line:154
        OO00O0O0OOOOO000O =0 #line:155
        for OOOO00OOOOOOOO00O ,OO0OOO0O00OO0000O in [((0 ,7 ),(1 ,6 )),((0 ,0 ),(1 ,1 )),((7 ,0 ),(6 ,1 )),((7 ,7 ),(6 ,6 ))]+BC2 :#line:160
            O0OOOO0OOO0000O00 ,O00O0O0OOOOOO0OOO =OOOO00OOOOOOOO00O #line:161
            O0O0OO0OO000OO0O0 ,O00OOOO0000OO0OO0 =OO0OOO0O00OO0000O #line:162
            if OO00000OOOOO000O0 .board [O00OOOO0000OO0OO0 ][O0O0OO0OO000OO0O0 ]==O00OOOOOO00000OO0 and OO00000OOOOO000O0 .board [O00O0O0OOOOOO0OOO ][O0OOOO0OOO0000O00 ]==None :#line:163
                OO00O0O0OOOOO000O +=1 #line:164
        return OO00O0O0OOOOO000O #line:165
    def score (O0O0000O000OOOOO0 ):#line:167
        O000OOO00OO000000 =(len (O0O0000O000OOOOO0 .move_list )+10 )/60 #line:168
        O00O0000OOOOO0O00 =O000OOO00OO000000 *O0O0000O000OOOOO0 .result ()#line:169
        O00O0000OOOOO0O00 -=O0O0000O000OOOOO0 .CORNER *O0O0000O000OOOOO0 .in_corner (0 )#line:171
        O00O0000OOOOO0O00 +=O0O0000O000OOOOO0 .CORNER *O0O0000O000OOOOO0 .in_corner (1 )#line:172
        O00O0000OOOOO0O00 -=O0O0000O000OOOOO0 .BAD_CORNER *O0O0000O000OOOOO0 .bad_corner (0 )#line:174
        O00O0000OOOOO0O00 +=O0O0000O000OOOOO0 .BAD_CORNER *O0O0000O000OOOOO0 .bad_corner (1 )#line:175
        O00O0000OOOOO0O00 -=O0O0000O000OOOOO0 .MOVES *len (O0O0000O000OOOOO0 .moves (0 ))#line:177
        O00O0000OOOOO0O00 +=O0O0000O000OOOOO0 .MOVES *len (O0O0000O000OOOOO0 .moves (1 ))#line:178
        return O00O0000OOOOO0O00 #line:180
    def undo_last_move (OO000O0O0O0O0000O ):#line:182
        O0O0O0OOO0OOOOO0O =OO000O0O0O0O0000O .move_list [-1 ]#line:183
        OO000O0O0O0O0000O .board =OO000O0O0O0O0000O .history [-1 ]#line:184
        del OO000O0O0O0O0000O .history [-1 ]#line:185
        del OO000O0O0O0O0000O .move_list [-1 ]#line:186
        if O0O0O0OOO0OOOOO0O !=None :#line:187
            OO000O0O0O0O0000O .fields .add (O0O0O0OOO0OOOOO0O )#line:188
    def minmax (OOOOOOO00O0O00OOO ,OO000O0O00OOO0OO0 ,OOOOO00O00O0O000O ):#line:191
        if OOOOOOO00O0O00OOO .terminal ():#line:192
            return 1000 *OOOOOOO00O0O00OOO .result ()#line:193
        if OOOOO00O00O0O000O ==0 :#line:195
            return OOOOOOO00O0O00OOO .score ()#line:196
        O00OO000O00O0O00O =[]#line:198
        for O00OO00000OO0000O in OOOOOOO00O0O00OOO .moves (OO000O0O00OOO0OO0 ):#line:200
            OOOOOOO00O0O00OOO .do_move (O00OO00000OO0000O ,OO000O0O00OOO0OO0 )#line:201
            O00OO000O00O0O00O .append (OOOOOOO00O0O00OOO .minmax (1 -OO000O0O00OOO0OO0 ,OOOOO00O00O0O000O -1 ))#line:202
            OOOOOOO00O0O00OOO .undo_last_move ()#line:203
        if len (O00OO000O00O0O00O )==0 :#line:205
            return None #line:206
        if OO000O0O00OOO0OO0 ==1 :#line:208
            return max (O00OO000O00O0O00O )#line:209
        else :#line:210
            return min (O00OO000O00O0O00O )#line:211
    def max_value (OO00000OOOOOOO0OO ,O0000O0000000000O ,O0OO0O000O000O000 ,O0O0O000O0O000OO0 ):#line:215
        if OO00000OOOOOOO0OO .terminal ():return utility (state )#line:216
        if O0O0O000O0O000OO0 ==0 :return OO00000OOOOOOO0OO .score ()#line:217
        OOO000O00OOOOOOOO =-INFTY #line:218
        for O00OOOO00OOO00000 in OO00000OOOOOOO0OO .moves (player ):#line:220
            OO00000OOOOOOO0OO .do_move (O00OOOO00OOO00000 ,player )#line:221
            OOO000O00OOOOOOOO =max (OOO000O00OOOOOOOO ,OO00000OOOOOOO0OO .min_value (O0000O0000000000O ,O0OO0O000O000O000 ,O0O0O000O0O000OO0 -1 ))#line:222
            OO00000OOOOOOO0OO .undo_last_move ()#line:223
            if OOO000O00OOOOOOOO >=O0OO0O000O000O000 :#line:225
                return OOO000O00OOOOOOOO #line:226
            O0000O0000000000O =max (O0000O0000000000O ,OOO000O00OOOOOOOO )#line:227
        return OOO000O00OOOOOOOO #line:228
    def min_value (O000OO0OO000OOOO0 ,OOO0O0000OO00OOOO ,OO000OO000O0O0O00 ,OO000000OOOO0OOOO ):#line:231
        if O000OO0OO000OOOO0 .terminal ():return utility (state )#line:232
        if OO000000OOOO0OOOO ==0 :return O000OO0OO000OOOO0 .score ()#line:233
        O000OOOO0O0O00O0O =+INFTY #line:234
        for OO0OOOOOOOO0OOO00 in O000OO0OO000OOOO0 .moves (player ):#line:236
            O000OO0OO000OOOO0 .do_move (OO0OOOOOOOO0OOO00 ,player )#line:237
            O000OOOO0O0O00O0O =min (O000OOOO0O0O00O0O ,O000OO0OO000OOOO0 .min_value (OOO0O0000OO00OOOO ,OO000OO000O0O0O00 ,OO000000OOOO0OOOO -1 ))#line:238
            O000OO0OO000OOOO0 .undo_last_move ()#line:239
            if O000OOOO0O0O00O0O <=OOO0O0000OO00OOOO :#line:241
                return O000OOOO0O0O00O0O #line:242
            OO000OO000O0O0O00 =min (OO000OO000O0O0O00 ,O000OOOO0O0O00O0O )#line:243
        return O000OOOO0O0O00O0O #line:245
    def best_move (OO0OOOO00O00000O0 ,O0OO0O000OOOO00O0 ,O0O00O000OOO00000 ):#line:247
        O00000O00000OOO00 =0 #line:248
        """
        if len(self.move_list) > 50:
            deepening = 2
        if len(self.move_list) > 52:
            deepening = 4
        if len(self.move_list) > 54:
            deepening = 6
        """#line:256
        if len (OO0OOOO00O00000O0 .move_list )>54 :#line:259
            O00000O00000OOO00 =10 #line:260
        O00000O0000000OO0 =[]#line:263
        for O00O0O00O0O000OOO in OO0OOOO00O00000O0 .moves (O0OO0O000OOOO00O0 ):#line:264
            OO0OOOO00O00000O0 .do_move (O00O0O00O0O000OOO ,O0OO0O000OOOO00O0 )#line:265
            O00000O0000000OO0 .append ((OO0OOOO00O00000O0 .minmax (1 -O0OO0O000OOOO00O0 ,O0O00O000OOO00000 +O00000O00000OOO00 ),O00O0O00O0O000OOO ))#line:266
            OO0OOOO00O00000O0 .undo_last_move ()#line:267
        if O0OO0O000OOOO00O0 ==1 :#line:268
            OO0OOO000OOO0OO00 ,O0O0OOOO0OOO0OO0O =max (O00000O0000000OO0 )#line:269
        else :#line:270
            OO0OOO000OOO0OO00 ,O0O0OOOO0OOO0OO0O =min (O00000O0000000OO0 )#line:271
        O00000OOOOOO000O0 =[OO0OO00O0OOO0O00O for (OO00OO0OOO0OO00O0 ,OO0OO00O0OOO0O00O )in O00000O0000000OO0 if OO00OO0OOO0OO00O0 ==OO0OOO000OOO0OO00 ]#line:273
        return random .choice (O00000OOOOOO000O0 )#line:275
class Player (object ):#line:279
    def __init__ (OOOO00O0OOO00OO00 ):#line:280
        OOOO00O0OOO00OO00 .reset ()#line:281
    def reset (O0O0OO000O00O00OO ):#line:283
        O0O0OO000O00O00OO .game =Reversi ()#line:284
        O0O0OO000O00O00OO .my_player =1 #line:285
        O0O0OO000O00O00OO .say ('RDY')#line:286
    def say (OO0O0OO0O000OO00O ,OO00OO00O00OO0O0O ):#line:288
        sys .stdout .write (OO00OO00O00OO0O0O )#line:289
        sys .stdout .write ('\n')#line:290
        sys .stdout .flush ()#line:291
    def hear (O0OO00O00OO00O000 ):#line:293
        O0O0OOOOO0OOO0O00 =sys .stdin .readline ().split ()#line:294
        return O0O0OOOOO0OOO0O00 [0 ],O0O0OOOOO0OOO0O00 [1 :]#line:295
    def loop (O00O00OOO00O0O000 ):#line:297
        while True :#line:298
            O00O000O0OO0O000O ,OO0OOOOOO0O000O0O =O00O00OOO00O0O000 .hear ()#line:299
            if O00O000O0OO0O000O =='HEDID':#line:300
                OO00OO0O0OOO0000O ,O000000O0OO0OOO00 =OO0OOOOOO0O000O0O [:2 ]#line:301
                OOO00O0OO000OOO0O =tuple ((int (O0O00O00O00O0OOO0 )for O0O00O00O00O0OOO0 in OO0OOOOOO0O000O0O [2 :]))#line:302
                if OOO00O0OO000OOO0O ==(-1 ,-1 ):#line:303
                    OOO00O0OO000OOO0O =None #line:304
                O00O00OOO00O0O000 .game .do_move (OOO00O0OO000OOO0O ,1 -O00O00OOO00O0O000 .my_player )#line:305
            elif O00O000O0OO0O000O =='ONEMORE':#line:306
                O00O00OOO00O0O000 .reset ()#line:307
                continue #line:308
            elif O00O000O0OO0O000O =='BYE':#line:309
                break #line:310
            else :#line:311
                assert O00O000O0OO0O000O =='UGO'#line:312
                assert not O00O00OOO00O0O000 .game .move_list #line:313
                O00O00OOO00O0O000 .my_player =0 #line:314
            OOO00O0OO000OOO0O =O00O00OOO00O0O000 .game .best_move (O00O00OOO00O0O000 .my_player ,MAX_DEPTH )#line:316
            O00O00OOO00O0O000 .game .do_move (OOO00O0OO000OOO0O ,O00O00OOO00O0O000 .my_player )#line:317
            if OOO00O0OO000OOO0O ==None :#line:318
                OOO00O0OO000OOO0O =(-1 ,-1 )#line:319
            O00O00OOO00O0O000 .say ('IDO %d %d'%OOO00O0OO000OOO0O )#line:321
if __name__ =='__main__':#line:324
    player =Player ()#line:325
    player .loop ()
