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
    def __init__ (O000O0OOO00O0OO00 ):#line:42
        O000O0OOO00O0OO00 .board =O000O0OOO00O0OO00 .initial_board ()#line:43
        O000O0OOO00O0OO00 .fields =set ()#line:44
        O000O0OOO00O0OO00 .move_list =[]#line:45
        O000O0OOO00O0OO00 .history =[]#line:46
        for OO00000OOO00O0O0O in range (O000O0OOO00O0OO00 .M ):#line:47
            for O00O0OOOO0OOOO0OO in range (O000O0OOO00O0OO00 .M ):#line:48
                if O000O0OOO00O0OO00 .board [OO00000OOO00O0O0O ][O00O0OOOO0OOOO0OO ]is None :#line:49
                    O000O0OOO00O0OO00 .fields .add ((O00O0OOOO0OOOO0OO ,OO00000OOO00O0O0O ))#line:50
        O000O0OOO00O0OO00 .CORNER =CORNER *parameter_mult ()#line:52
        O000O0OOO00O0OO00 .BAD_CORNER =BAD_CORNER *parameter_mult ()#line:53
        O000O0OOO00O0OO00 .MOVES =MOVES *parameter_mult ()#line:54
    def initial_board (O00OOO00OO0O0000O ):#line:56
        OOO00000OO000O0O0 =[[None ]*O00OOO00OO0O0000O .M for _O0000O0O00OO000OO in range (O00OOO00OO0O0000O .M )]#line:57
        OOO00000OO000O0O0 [3 ][3 ]=1 #line:58
        OOO00000OO000O0O0 [4 ][4 ]=1 #line:59
        OOO00000OO000O0O0 [3 ][4 ]=0 #line:60
        OOO00000OO000O0O0 [4 ][3 ]=0 #line:61
        return OOO00000OO000O0O0 #line:62
    def draw (OO00OOO0O000OO000 ):#line:64
        for OOO0O00OOOO000O0O in range (OO00OOO0O000OO000 .M ):#line:65
            O0OOOOO000OOO0000 =[]#line:66
            for O000OOO00OOOOOO0O in range (OO00OOO0O000OO000 .M ):#line:67
                O0O0OOOOOOO0O00OO =OO00OOO0O000OO000 .board [OOO0O00OOOO000O0O ][O000OOO00OOOOOO0O ]#line:68
                if O0O0OOOOOOO0O00OO is None :#line:69
                    O0OOOOO000OOO0000 .append ('.')#line:70
                elif O0O0OOOOOOO0O00OO ==1 :#line:71
                    O0OOOOO000OOO0000 .append ('#')#line:72
                else :#line:73
                    O0OOOOO000OOO0000 .append ('o')#line:74
            print (''.join (O0OOOOO000OOO0000 ))#line:75
        print ('')#line:76
    def moves (OO0000O0OO0O00000 ,O0O0OO00O0OOOOOO0 ):#line:78
        OOO000OOOO00O0000 =[]#line:79
        for (O0OOO0O0000OO0O00 ,O0OO000OOOO00O0O0 )in OO0000O0OO0O00000 .fields :#line:80
            if any (OO0000O0OO0O00000 .can_beat (O0OOO0O0000OO0O00 ,O0OO000OOOO00O0O0 ,O00O00OOO0OO0000O ,O0O0OO00O0OOOOOO0 )for O00O00OOO0OO0000O in OO0000O0OO0O00000 .DIRS ):#line:82
                OOO000OOOO00O0000 .append ((O0OOO0O0000OO0O00 ,O0OO000OOOO00O0O0 ))#line:83
        if OOO000OOOO00O0000 ==[]:#line:85
            return [None ]#line:86
        return OOO000OOOO00O0000 #line:87
    def can_beat (OO000O00O0O000OOO ,O000O0O0OOO0O0000 ,OO00O0O000O00O000 ,OOOO0OOOO0OO0OO00 ,OO000O00OOOOOOO0O ):#line:89
        O0OO00OO0O0O00000 ,O000OO0O0OOO0O0OO =OOOO0OOOO0OO0OO00 #line:90
        O000O0O0OOO0O0000 +=O0OO00OO0O0O00000 #line:91
        OO00O0O000O00O000 +=O000OO0O0OOO0O0OO #line:92
        O0000000O00O0000O =0 #line:93
        while OO000O00O0O000OOO .get (O000O0O0OOO0O0000 ,OO00O0O000O00O000 )==1 -OO000O00OOOOOOO0O :#line:94
            O000O0O0OOO0O0000 +=O0OO00OO0O0O00000 #line:95
            OO00O0O000O00O000 +=O000OO0O0OOO0O0OO #line:96
            O0000000O00O0000O +=1 #line:97
        return O0000000O00O0000O >0 and OO000O00O0O000OOO .get (O000O0O0OOO0O0000 ,OO00O0O000O00O000 )==OO000O00OOOOOOO0O #line:98
    def get (OOO000OO0000O0O0O ,OO0O0O00OOO0000OO ,OOOO00OO0OO0OO0O0 ):#line:100
        if 0 <=OO0O0O00OOO0000OO <OOO000OO0000O0O0O .M and 0 <=OOOO00OO0OO0OO0O0 <OOO000OO0000O0O0O .M :#line:101
            return OOO000OO0000O0O0O .board [OOOO00OO0OO0OO0O0 ][OO0O0O00OOO0000OO ]#line:102
        return None #line:103
    def do_move (O0OOO0000OOOOOOO0 ,OOOOO0O0O0OO00OO0 ,OOOO0OOO000O0O000 ):#line:105
        assert OOOO0OOO000O0O000 ==len (O0OOO0000OOOOOOO0 .move_list )%2 #line:106
        O0OOO0000OOOOOOO0 .history .append ([OO0O000O0O0O00O00 [:]for OO0O000O0O0O00O00 in O0OOO0000OOOOOOO0 .board ])#line:107
        O0OOO0000OOOOOOO0 .move_list .append (OOOOO0O0O0OO00OO0 )#line:108
        if OOOOO0O0O0OO00OO0 is None :#line:110
            return #line:111
        O0OO0OOO0OO0OO00O ,O00OO0O0O000O00O0 =OOOOO0O0O0OO00OO0 #line:112
        OOOO0000OOOO0OOO0 ,O0OO0O00OOO0OOOOO =OOOOO0O0O0OO00OO0 #line:113
        O0OOO0000OOOOOOO0 .board [O00OO0O0O000O00O0 ][O0OO0OOO0OO0OO00O ]=OOOO0OOO000O0O000 #line:114
        O0OOO0000OOOOOOO0 .fields -=set ([OOOOO0O0O0OO00OO0 ])#line:115
        for O0O000000OOO00O0O ,OOO0OO00OO0OOOOOO in O0OOO0000OOOOOOO0 .DIRS :#line:116
            O0OO0OOO0OO0OO00O ,O00OO0O0O000O00O0 =OOOO0000OOOO0OOO0 ,O0OO0O00OOO0OOOOO #line:117
            O000OO0O00OO00O00 =[]#line:118
            O0OO0OOO0OO0OO00O +=O0O000000OOO00O0O #line:119
            O00OO0O0O000O00O0 +=OOO0OO00OO0OOOOOO #line:120
            while O0OOO0000OOOOOOO0 .get (O0OO0OOO0OO0OO00O ,O00OO0O0O000O00O0 )==1 -OOOO0OOO000O0O000 :#line:121
                O000OO0O00OO00O00 .append ((O0OO0OOO0OO0OO00O ,O00OO0O0O000O00O0 ))#line:122
                O0OO0OOO0OO0OO00O +=O0O000000OOO00O0O #line:123
                O00OO0O0O000O00O0 +=OOO0OO00OO0OOOOOO #line:124
            if O0OOO0000OOOOOOO0 .get (O0OO0OOO0OO0OO00O ,O00OO0O0O000O00O0 )==OOOO0OOO000O0O000 :#line:125
                for (OO0O000OOO0O00O00 ,O00O00O0OOOOO0OO0 )in O000OO0O00OO00O00 :#line:126
                    O0OOO0000OOOOOOO0 .board [O00O00O0OOOOO0OO0 ][OO0O000OOO0O00O00 ]=OOOO0OOO000O0O000 #line:127
    def result (OO00O00O00OO000OO ):#line:129
        O000O0O0OO0O0O00O =0 #line:130
        for O0OO00O0OO000000O in range (OO00O00O00OO000OO .M ):#line:131
            for O0O0000O0000O0O0O in range (OO00O00O00OO000OO .M ):#line:132
                OO0O00O0000O00000 =OO00O00O00OO000OO .board [O0OO00O0OO000000O ][O0O0000O0000O0O0O ]#line:133
                if OO0O00O0000O00000 ==0 :#line:134
                    O000O0O0OO0O0O00O -=1 #line:135
                elif OO0O00O0000O00000 ==1 :#line:136
                    O000O0O0OO0O0O00O +=1 #line:137
        return O000O0O0OO0O0O00O #line:138
    def terminal (OOOOOO0O00O000O00 ):#line:140
        if not OOOOOO0O00O000O00 .fields :#line:141
            return True #line:142
        if len (OOOOOO0O00O000O00 .move_list )<2 :#line:143
            return False #line:144
        return OOOOOO0O00O000O00 .move_list [-1 ]is None and OOOOOO0O00O000O00 .move_list [-2 ]is None #line:145
    def in_corner (OOOOOO0000OOO0O00 ,OO00O00OO0O000OO0 ):#line:147
        O0O000OOOOO00O00O =0 #line:148
        for OOO000OOOOOO0O0OO ,OO0OO00OOO000000O in [(0 ,7 ),(0 ,0 ),(7 ,0 ),(7 ,7 )]:#line:149
            if OOOOOO0000OOO0O00 .board [OO0OO00OOO000000O ][OOO000OOOOOO0O0OO ]==OO00O00OO0O000OO0 :#line:150
                O0O000OOOOO00O00O +=1 #line:151
        return O0O000OOOOO00O00O #line:152
    def bad_corner (OOOOO0OO00O0O00O0 ,OO00O000OOO000O00 ):#line:154
        O000O000O0OOO00OO =0 #line:155
        for OOO0O0000OOOOOOO0 ,OOOOOO0O000OOOOO0 in [((0 ,7 ),(1 ,6 )),((0 ,0 ),(1 ,1 )),((7 ,0 ),(6 ,1 )),((7 ,7 ),(6 ,6 ))]+BC2 :#line:160
            OO0O0000O000O00OO ,O0OOO0OO0OO00O0O0 =OOO0O0000OOOOOOO0 #line:161
            O000O0000OOOO00O0 ,O0O000O0O000O0000 =OOOOOO0O000OOOOO0 #line:162
            if OOOOO0OO00O0O00O0 .board [O0O000O0O000O0000 ][O000O0000OOOO00O0 ]==OO00O000OOO000O00 and OOOOO0OO00O0O00O0 .board [O0OOO0OO0OO00O0O0 ][OO0O0000O000O00OO ]==None :#line:163
                O000O000O0OOO00OO +=1 #line:164
        return O000O000O0OOO00OO #line:165
    def score (OO00O000O000OOO0O ):#line:167
        OO0OO0OOO000OO000 =(len (OO00O000O000OOO0O .move_list )+10 )/60 #line:168
        O0O0000OOO0OOO0O0 =OO0OO0OOO000OO000 *OO00O000O000OOO0O .result ()#line:169
        O0O0000OOO0OOO0O0 -=OO00O000O000OOO0O .CORNER *OO00O000O000OOO0O .in_corner (0 )#line:171
        O0O0000OOO0OOO0O0 +=OO00O000O000OOO0O .CORNER *OO00O000O000OOO0O .in_corner (1 )#line:172
        O0O0000OOO0OOO0O0 -=OO00O000O000OOO0O .BAD_CORNER *OO00O000O000OOO0O .bad_corner (0 )#line:174
        O0O0000OOO0OOO0O0 +=OO00O000O000OOO0O .BAD_CORNER *OO00O000O000OOO0O .bad_corner (1 )#line:175
        O0O0000OOO0OOO0O0 -=OO00O000O000OOO0O .MOVES *len (OO00O000O000OOO0O .moves (0 ))#line:177
        O0O0000OOO0OOO0O0 +=OO00O000O000OOO0O .MOVES *len (OO00O000O000OOO0O .moves (1 ))#line:178
        return O0O0000OOO0OOO0O0 #line:180
    def undo_last_move (OO0O00OO000O0O0O0 ):#line:182
        OOOO00OO0O0OO00OO =OO0O00OO000O0O0O0 .move_list [-1 ]#line:183
        OO0O00OO000O0O0O0 .board =OO0O00OO000O0O0O0 .history [-1 ]#line:184
        del OO0O00OO000O0O0O0 .history [-1 ]#line:185
        del OO0O00OO000O0O0O0 .move_list [-1 ]#line:186
        if OOOO00OO0O0OO00OO !=None :#line:187
            OO0O00OO000O0O0O0 .fields .add (OOOO00OO0O0OO00OO )#line:188
    def minmax (OOOOO0OOO00O00000 ,OOOOO0O0OOO0O0OO0 ,O0O0OO0OO00OO0O00 ):#line:191
        if OOOOO0OOO00O00000 .terminal ():#line:192
            return 1000 *OOOOO0OOO00O00000 .result ()#line:193
        if O0O0OO0OO00OO0O00 ==0 :#line:195
            return OOOOO0OOO00O00000 .score ()#line:196
        OO00OOO000000OOOO =[]#line:198
        for O00000O0O000O0000 in OOOOO0OOO00O00000 .moves (OOOOO0O0OOO0O0OO0 ):#line:200
            OOOOO0OOO00O00000 .do_move (O00000O0O000O0000 ,OOOOO0O0OOO0O0OO0 )#line:201
            OO00OOO000000OOOO .append (OOOOO0OOO00O00000 .minmax (1 -OOOOO0O0OOO0O0OO0 ,O0O0OO0OO00OO0O00 -1 ))#line:202
            OOOOO0OOO00O00000 .undo_last_move ()#line:203
        if len (OO00OOO000000OOOO )==0 :#line:205
            return None #line:206
        if OOOOO0O0OOO0O0OO0 ==1 :#line:208
            return max (OO00OOO000000OOOO )#line:209
        else :#line:210
            return min (OO00OOO000000OOOO )#line:211
    def max_value (O0OO0OO00O0OO000O ,O0OO00O00000000O0 ,O0OOO00OO00OO0OOO ,O0OOOOOOO00O0000O ):#line:215
        O0OO00O000O00O0O0 =1 #line:216
        if O0OO0OO00O0OO000O .terminal ():#line:217
            return 1000 *O0OO0OO00O0OO000O .result ()#line:218
        if O0OOOOOOO00O0000O ==0 :#line:220
            return O0OO0OO00O0OO000O .score ()#line:221
        OOOOOOOO0O000000O =-INFTY #line:223
        for OO0000OOOO0O0OOO0 in O0OO0OO00O0OO000O .moves (O0OO00O000O00O0O0 ):#line:225
            O0OO0OO00O0OO000O .do_move (OO0000OOOO0O0OOO0 ,O0OO00O000O00O0O0 )#line:226
            OOOOOOOO0O000000O =max (OOOOOOOO0O000000O ,O0OO0OO00O0OO000O .min_value (O0OO00O00000000O0 ,O0OOO00OO00OO0OOO ,O0OOOOOOO00O0000O -1 ))#line:227
            O0OO0OO00O0OO000O .undo_last_move ()#line:228
            if OOOOOOOO0O000000O >=O0OOO00OO00OO0OOO :#line:230
                return OOOOOOOO0O000000O #line:231
            O0OO00O00000000O0 =max (O0OO00O00000000O0 ,OOOOOOOO0O000000O )#line:232
        return OOOOOOOO0O000000O #line:233
    def min_value (OOO0000O0OOOOOOO0 ,OOO00OO0OOOOO00OO ,OOOOOOO0OO00000O0 ,OOO0OO0OO0OOOOOOO ):#line:236
        OOOO000O00OO0OO0O =0 #line:237
        if OOO0000O0OOOOOOO0 .terminal ():#line:238
            return 1000 *OOO0000O0OOOOOOO0 .result ()#line:239
        if OOO0OO0OO0OOOOOOO ==0 :#line:241
            return OOO0000O0OOOOOOO0 .score ()#line:242
        OO0O0O0OOOO0OO0O0 =+INFTY #line:244
        for O00O0OO0OOOO00O0O in OOO0000O0OOOOOOO0 .moves (OOOO000O00OO0OO0O ):#line:246
            OOO0000O0OOOOOOO0 .do_move (O00O0OO0OOOO00O0O ,OOOO000O00OO0OO0O )#line:247
            OO0O0O0OOOO0OO0O0 =min (OO0O0O0OOOO0OO0O0 ,OOO0000O0OOOOOOO0 .max_value (OOO00OO0OOOOO00OO ,OOOOOOO0OO00000O0 ,OOO0OO0OO0OOOOOOO -1 ))#line:248
            OOO0000O0OOOOOOO0 .undo_last_move ()#line:249
            if OO0O0O0OOOO0OO0O0 <=OOO00OO0OOOOO00OO :#line:251
                return OO0O0O0OOOO0OO0O0 #line:252
            OOOOOOO0OO00000O0 =min (OOOOOOO0OO00000O0 ,OO0O0O0OOOO0OO0O0 )#line:253
        return OO0O0O0OOOO0OO0O0 #line:255
    def best_move (O0O000OO0OOO00O0O ,O0O0OOOO0000O0000 ,O0OO0O000O00O00OO ):#line:257
        OOOO000O0O000000O =0 #line:258
        """
        if len(self.move_list) > 50:
            deepening = 2
        if len(self.move_list) > 52:
            deepening = 4
        if len(self.move_list) > 54:
            deepening = 6
        """#line:266
        if len (O0O000OO0OOO00O0O .move_list )>54 :#line:269
            OOOO000O0O000000O =10 #line:270
        if O0O0OOOO0000O0000 ==1 :#line:273
            OOO0000O0OOO00O0O =O0O000OO0OOO00O0O .min_value #line:274
        else :#line:275
            OOO0000O0OOO00O0O =O0O000OO0OOO00O0O .max_value #line:276
        O00O000O0O00O00O0 =[]#line:278
        for OOO000OO000OOOOOO in O0O000OO0OOO00O0O .moves (O0O0OOOO0000O0000 ):#line:280
            O0O000OO0OOO00O0O .do_move (OOO000OO000OOOOOO ,O0O0OOOO0000O0000 )#line:281
            O00O000O0O00O00O0 .append ((OOO0000O0OOO00O0O (-INFTY ,INFTY ,O0OO0O000O00O00OO +OOOO000O0O000000O ),OOO000OO000OOOOOO ))#line:282
            O0O000OO0OOO00O0O .undo_last_move ()#line:283
        if O0O0OOOO0000O0000 ==1 :#line:285
            O0OOO0O0O000OO0OO ,O00000O0O00O000OO =max (O00O000O0O00O00O0 )#line:286
        else :#line:287
            O0OOO0O0O000OO0OO ,O00000O0O00O000OO =min (O00O000O0O00O00O0 )#line:288
        O00O000OOOOO0OO00 =[O00OO0OOO00O00OOO for (OOO00O00O0O0OOO00 ,O00OO0OOO00O00OOO )in O00O000O0O00O00O0 if OOO00O00O0O0OOO00 ==O0OOO0O0O000OO0OO ]#line:290
        return random .choice (O00O000OOOOO0OO00 )#line:292
class Player (object ):#line:296
    def __init__ (OOO0000O0O00O00OO ):#line:297
        OOO0000O0O00O00OO .reset ()#line:298
    def reset (OOO0O000O0O0OOOO0 ):#line:300
        OOO0O000O0O0OOOO0 .game =Reversi ()#line:301
        OOO0O000O0O0OOOO0 .my_player =1 #line:302
        OOO0O000O0O0OOOO0 .say ('RDY')#line:303
    def say (OOOOOOO0O000OOOOO ,O000O0OOO00O00O00 ):#line:305
        sys .stdout .write (O000O0OOO00O00O00 )#line:306
        sys .stdout .write ('\n')#line:307
        sys .stdout .flush ()#line:308
    def hear (O0OO0OO0OO00OOO00 ):#line:310
        O000O0OO00OO0OOOO =sys .stdin .readline ().split ()#line:311
        return O000O0OO00OO0OOOO [0 ],O000O0OO00OO0OOOO [1 :]#line:312
    def loop (O0OO0OO000000O0O0 ):#line:314
        while True :#line:315
            OO000OO0O00OOO00O ,O0O0OOOO000OOOOOO =O0OO0OO000000O0O0 .hear ()#line:316
            if OO000OO0O00OOO00O =='HEDID':#line:317
                OOO0OOO00O000OO0O ,OOO0OOO00O00O0000 =O0O0OOOO000OOOOOO [:2 ]#line:318
                OOOOO0OO00OOO0O0O =tuple ((int (OOO0O000O00OO000O )for OOO0O000O00OO000O in O0O0OOOO000OOOOOO [2 :]))#line:319
                if OOOOO0OO00OOO0O0O ==(-1 ,-1 ):#line:320
                    OOOOO0OO00OOO0O0O =None #line:321
                O0OO0OO000000O0O0 .game .do_move (OOOOO0OO00OOO0O0O ,1 -O0OO0OO000000O0O0 .my_player )#line:322
            elif OO000OO0O00OOO00O =='ONEMORE':#line:323
                O0OO0OO000000O0O0 .reset ()#line:324
                continue #line:325
            elif OO000OO0O00OOO00O =='BYE':#line:326
                break #line:327
            else :#line:328
                assert OO000OO0O00OOO00O =='UGO'#line:329
                assert not O0OO0OO000000O0O0 .game .move_list #line:330
                O0OO0OO000000O0O0 .my_player =0 #line:331
            OOOOO0OO00OOO0O0O =O0OO0OO000000O0O0 .game .best_move (O0OO0OO000000O0O0 .my_player ,MAX_DEPTH )#line:333
            O0OO0OO000000O0O0 .game .do_move (OOOOO0OO00OOO0O0O ,O0OO0OO000000O0O0 .my_player )#line:334
            if OOOOO0OO00OOO0O0O ==None :#line:335
                OOOOO0OO00OOO0O0O =(-1 ,-1 )#line:336
            O0OO0OO000000O0O0 .say ('IDO %d %d'%OOOOO0OO00OOO0O0O )#line:338
if __name__ =='__main__':#line:341
    player =Player ()#line:342
    player .loop ()
