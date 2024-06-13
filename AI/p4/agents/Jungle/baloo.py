#!/usr/bin/env python
""#line:5
import random  # line:8
import sys  # line:9


class Jungle :#line:11
    PIECE_VALUES ={0 :4 ,1 :1 ,2 :2 ,3 :3 ,4 :5 ,5 :7 ,6 :8 ,7 :10 }#line:21
    MAXIMAL_PASSIVE =30 #line:22
    DENS_DIST =0.1 #line:23
    MX =7 #line:24
    MY =9 #line:25
    traps ={(2 ,0 ),(4 ,0 ),(3 ,1 ),(2 ,8 ),(4 ,8 ),(3 ,7 )}#line:26
    ponds ={(OO0O0000OO00OOO00 ,OOO0O0000OOOOOOOO )for OO0O0000OO00OOO00 in [1 ,2 ,4 ,5 ]for OOO0O0000OOOOOOOO in [3 ,4 ,5 ]}#line:27
    dens =[(3 ,8 ),(3 ,0 )]#line:28
    dirs =[(0 ,1 ),(1 ,0 ),(-1 ,0 ),(0 ,-1 )]#line:29
    rat ,cat ,dog ,wolf ,jaguar ,tiger ,lion ,elephant =range (8 )#line:31
    def __init__ (O0O0O0OO000O0O00O ):#line:33
        O0O0O0OO000O0O00O .board =O0O0O0OO000O0O00O .initial_board ()#line:34
        O0O0O0OO000O0O00O .pieces ={0 :{},1 :{}}#line:35
        for O0OOOO0O0OO0O00OO in range (Jungle .MY ):#line:37
            for OO0OO000OO00OOOO0 in range (Jungle .MX ):#line:38
                O00O0OO0OOO0OOO00 =O0O0O0OO000O0O00O .board [O0OOOO0O0OO0O00OO ][OO0OO000OO00OOOO0 ]#line:39
                if O00O0OO0OOO0OOO00 :#line:40
                    O000OO000OOOOO0O0 ,OOO0OOOO000O000O0 =O00O0OO0OOO0OOO00 #line:41
                    O0O0O0OO000O0O00O .pieces [O000OO000OOOOO0O0 ][OOO0OOOO000O000O0 ]=(OO0OO000OO00OOOO0 ,O0OOOO0O0OO0O00OO )#line:42
        O0O0O0OO000O0O00O .curplayer =0 #line:43
        O0O0O0OO000O0O00O .peace_counter =0 #line:44
        O0O0O0OO000O0O00O .winner =None #line:45
    def initial_board (OOOOO0O0OOOOO0OOO ):#line:47
        OO000OO0O0O000O00 ="""
        L.....T
        .D...C.
        R.J.W.E
        .......
        .......
        .......
        e.w.j.r
        .c...d.
        t.....l
        """#line:58
        O0OO00000OOOO00O0 =[OOO000O0O0O000O00 .strip ()for OOO000O0O0O000O00 in OO000OO0O0O000O00 .split ()if len (OOO000O0O0O000O00 )>0 ]#line:60
        O0OO00OO0OOO00OO0 =dict (zip ('rcdwjtle',range (8 )))#line:61
        OO0000O0O00O0OO0O =[]#line:63
        for OOO00O00O0O0O0O00 in range (9 ):#line:64
            OOOOOOOOOO00O00O0 =7 *[None ]#line:65
            for OO000OOO000O0O000 in range (7 ):#line:66
                O0O0OOO0OOO00000O =O0OO00000OOOO00O0 [OOO00O00O0O0O0O00 ][OO000OOO000O0O000 ]#line:67
                if O0O0OOO0OOO00000O !='.':#line:68
                    if 'A'<=O0O0OOO0OOO00000O <='Z':#line:69
                        OOO00OOO0OO0O00O0 =1 #line:70
                    else :#line:71
                        OOO00OOO0OO0O00O0 =0 #line:72
                    OOOOOOOOOO00O00O0 [OO000OOO000O0O000 ]=(OOO00OOO0OO0O00O0 ,O0OO00OO0OOO00OO0 [O0O0OOO0OOO00000O .lower ()])#line:73
            OO0000O0O00O0OO0O .append (OOOOOOOOOO00O00O0 )#line:74
        return OO0000O0O00O0OO0O #line:75
    def random_move (OO0O0OOOO0OOO00OO ,O0OOO000OOOO0OO0O ):#line:77
        OOO000O0OOOOO00O0 =OO0O0OOOO0OOO00OO .moves (O0OOO000OOOO0OO0O )#line:78
        if OOO000O0OOOOO00O0 :#line:79
            return random .choice (OOO000O0OOOOO00O0 )#line:80
        return None #line:81
    def can_beat (OOOO0OOOO0O000O0O ,OO000O0O0OOOOOOO0 ,O0OOO0000OO0OOO00 ,OOO0OOO00O00OO0O0 ,O0OO0O000O00O0OO0 ):#line:83
        if OOO0OOO00O00OO0O0 in Jungle .ponds and O0OO0O000O00O0OO0 in Jungle .ponds :#line:84
            return True #line:85
        if OOO0OOO00O00OO0O0 in Jungle .ponds :#line:86
            return False #line:87
        if OO000O0O0OOOOOOO0 ==Jungle .rat and O0OOO0000OO0OOO00 ==Jungle .elephant :#line:88
            return True #line:89
        if OO000O0O0OOOOOOO0 ==Jungle .elephant and O0OOO0000OO0OOO00 ==Jungle .rat :#line:90
            return False #line:91
        if OO000O0O0OOOOOOO0 >=O0OOO0000OO0OOO00 :#line:92
            return True #line:93
        if O0OO0O000O00O0OO0 in Jungle .traps :#line:94
            return True #line:95
        return False #line:96
    def pieces_comparison (O00O0O0O0000O000O ):#line:98
        for OOOOO0OO0OO000O00 in range (7 ,-1 ,-1 ):#line:99
            O00OO0O00O0OOOO0O =[]#line:100
            for OOO0O0OOO0O0OOOOO in [0 ,1 ]:#line:101
                if OOOOO0OO0OO000O00 in O00O0O0O0000O000O .pieces [OOO0O0OOO0O0OOOOO ]:#line:102
                    O00OO0O00O0OOOO0O .append (OOO0O0OOO0O0OOOOO )#line:103
            if len (O00OO0O00O0OOOO0O )==1 :#line:104
                return O00OO0O00O0OOOO0O [0 ]#line:105
        return None #line:106
    def rat_is_blocking (O0000OO0000OO0OOO ,OO0O00OO0O00OOO0O ,O00O0OO0OO00OO000 ,O000OOO000O0OO000 ,O000O00OO0OOO0O0O ):#line:108
        O0O0O0O000O0OO000 ,OO00OO0O00O00OOO0 =O00O0OO0OO00OO000 #line:109
        OO000O00O000O0O0O =O0O0O0O000O0OO000 +O000OOO000O0OO000 #line:110
        for O0OOO00OOOO000000 in [0 ,1 ]:#line:111
            if Jungle .rat not in O0000OO0000OO0OOO .pieces [1 -O0OOO00OOOO000000 ]:#line:112
                continue #line:113
            O00O0OO000OO0O0O0 ,OOOOO0OOO0O0O000O =O0000OO0000OO0OOO .pieces [1 -O0OOO00OOOO000000 ][Jungle .rat ]#line:114
            if (O00O0OO000OO0O0O0 ,OOOOO0OOO0O0O000O )not in O0000OO0000OO0OOO .ponds :#line:115
                continue #line:116
            if O000O00OO0OOO0O0O !=0 :#line:117
                if O0O0O0O000O0OO000 ==O00O0OO000OO0O0O0 :#line:118
                    return True #line:119
            if O000OOO000O0OO000 !=0 :#line:120
                if OO00OO0O00O00OOO0 ==OOOOO0OOO0O0O000O and abs (O0O0O0O000O0OO000 -O00O0OO000OO0O0O0 )<=2 and abs (OO000O00O000O0O0O -O00O0OO000OO0O0O0 )<=2 :#line:121
                    return True #line:122
        return False #line:123
    def better_random_choice (OO00OO0OO0O0OO0O0 ,O000O0OO00OOO00O0 ):#line:126
        O000O0O00000OO0O0 =[]#line:130
        OO00O0000OO0OOO00 =[]#line:131
        O00OOOOO000OOO000 ,O0O0OOOO00O0O0OO0 =OO00OO0OO0O0OO0O0 .dens [1 -OO00OO0OO0O0OO0O0 .curplayer ]#line:133
        for O0O0O0OOOOO0OO00O ,O00000OOO000OO00O in O000O0OO00OOO00O0 :#line:135
            if O00000OOO000OO00O in OO00OO0OO0O0OO0O0 .dens :#line:136
                return (O0O0O0OOOOO0OO00O ,O00000OOO000OO00O )#line:137
            OO000OO0O0OOO0O0O ,O0O0O00000OO0OO0O =O00000OOO000OO00O #line:138
            O00OO00O00O0O0O00 ,O0OOOO0OO0OO0OO00 =O0O0O0OOOOO0OO00O #line:139
            if OO00OO0OO0O0OO0O0 .board [O0O0O00000OO0OO0O ][OO000OO0O0OOO0O0O ]!=None :#line:140
                O000O0O00000OO0O0 .append ((O0O0O0OOOOO0OO00O ,O00000OOO000OO00O ))#line:141
            OOO00000O0O000OOO =abs (O00OO00O00O0O0O00 -O00OOOOO000OOO000 )+abs (O0OOOO0OO0OO0OO00 -O0O0OOOO00O0O0OO0 )#line:143
            OOO0O00O0O00OOO0O =abs (OO000OO0O0OOO0O0O -O00OOOOO000OOO000 )+abs (O0O0O00000OO0OO0O -O0O0OOOO00O0O0OO0 )#line:144
            if OOO0O00O0O00OOO0O <OOO00000O0O000OOO :#line:147
                OO00O0000OO0OOO00 .append ((O0O0O0OOOOO0OO00O ,O00000OOO000OO00O ))#line:148
        if O000O0O00000OO0O0 :#line:149
            return random .choice (O000O0O00000OO0O0 )#line:151
        if OO00O0000OO0OOO00 :#line:152
            return random .choice (OO00O0000OO0OOO00 )#line:154
        return random .choice (O000O0OO00OOO00O0 )#line:156
    def draw (OOO000O0O00OO0O0O ):#line:158
        OO0O0O0000000OOOO ={0 :'rcdwjtle',1 :'RCDWJTLE'}#line:159
        for O00O00O00000OOO0O in range (Jungle .MY ):#line:160
            OO0O0OO0000O00000 =[]#line:162
            for O0000OO00000O0O00 in range (Jungle .MX ):#line:163
                O0O00OO000OOOOOO0 =OOO000O0O00OO0O0O .board [O00O00O00000OOO0O ][O0000OO00000O0O00 ]#line:164
                if O0O00OO000OOOOOO0 :#line:165
                    O0OO00O0OO00O000O ,O0OOOOOOOOO000O00 =O0O00OO000OOOOOO0 #line:166
                    OO0O0OO0000O00000 .append (OO0O0O0000000OOOO [O0OO00O0OO00O000O ][O0OOOOOOOOO000O00 ])#line:167
                else :#line:168
                    OO0O0OO0000O00000 .append ('.')#line:169
            print (''.join (OO0O0OO0000O00000 ))#line:170
        print ('')#line:171
    def moves (OOOO0O000OOOO0O00 ,OO00000OO000O00O0 ):#line:173
        O0OO00OO00O000O00 =[]#line:174
        for OOO0000O0O0O0000O ,O00O0000O0OO0OOOO in OOOO0O000OOOO0O00 .pieces [OO00000OO000O00O0 ].items ():#line:175
            OO0O0OO00OO0OO0O0 ,O0O0O00O000O0O0OO =O00O0000O0OO0OOOO #line:176
            for (O0OOO0O00O0OOOO0O ,OO0OOOOOOO0O0OO0O )in Jungle .dirs :#line:177
                OO0OO0O0O0O0OOOO0 =(O00OO00OO00OO000O ,OO0O0O0OO0O0OO000 )=(OO0O0OO00OO0OO0O0 +O0OOO0O00O0OOOO0O ,O0O0O00O000O0O0OO +OO0OOOOOOO0O0OO0O )#line:178
                if 0 <=O00OO00OO00OO000O <Jungle .MX and 0 <=OO0O0O0OO0O0OO000 <Jungle .MY :#line:179
                    if Jungle .dens [OO00000OO000O00O0 ]==OO0OO0O0O0O0OOOO0 :#line:180
                        continue #line:181
                    if OO0OO0O0O0O0OOOO0 in OOOO0O000OOOO0O00 .ponds :#line:182
                        if OOO0000O0O0O0000O not in (Jungle .rat ,Jungle .tiger ,Jungle .lion ):#line:183
                            continue #line:184
                        if OOO0000O0O0O0000O ==Jungle .tiger or OOO0000O0O0O0000O ==Jungle .lion :#line:187
                            if O0OOO0O00O0OOOO0O !=0 :#line:188
                                O0OOO0O00O0OOOO0O *=3 #line:189
                            if OO0OOOOOOO0O0OO0O !=0 :#line:190
                                OO0OOOOOOO0O0OO0O *=4 #line:191
                            if OOOO0O000OOOO0O00 .rat_is_blocking (OO00000OO000O00O0 ,O00O0000O0OO0OOOO ,O0OOO0O00O0OOOO0O ,OO0OOOOOOO0O0OO0O ):#line:192
                                continue #line:193
                            OO0OO0O0O0O0OOOO0 =(O00OO00OO00OO000O ,OO0O0O0OO0O0OO000 )=(OO0O0OO00OO0OO0O0 +O0OOO0O00O0OOOO0O ,O0O0O00O000O0O0OO +OO0OOOOOOO0O0OO0O )#line:194
                    if OOOO0O000OOOO0O00 .board [OO0O0O0OO0O0OO000 ][O00OO00OO00OO000O ]is not None :#line:195
                        O000O00OO0OOOO0OO ,OO0O00O00O0OOO00O =OOOO0O000OOOO0O00 .board [OO0O0O0OO0O0OO000 ][O00OO00OO00OO000O ]#line:196
                        if O000O00OO0OOOO0OO ==OO00000OO000O00O0 :#line:197
                            continue #line:198
                        if not OOOO0O000OOOO0O00 .can_beat (OOO0000O0O0O0000O ,OO0O00O00O0OOO00O ,O00O0000O0OO0OOOO ,OO0OO0O0O0O0OOOO0 ):#line:199
                            continue #line:200
                    O0OO00OO00O000O00 .append ((O00O0000O0OO0OOOO ,OO0OO0O0O0O0OOOO0 ))#line:201
        return O0OO00OO00O000O00 #line:202
    def victory (O0OO0O00O0O00OO00 ,OO0OO0O0O000OOOOO ):#line:204
        O0000OO0OOO000O00 =1 -OO0OO0O0O000OOOOO #line:205
        if len (O0OO0O00O0O00OO00 .pieces [O0000OO0OOO000O00 ])==0 :#line:206
            O0OO0O00O0O00OO00 .winner =OO0OO0O0O000OOOOO #line:207
            return True #line:208
        OO0OOO0O0O0000000 ,O0OOOOOOOO0OOO0OO =O0OO0O00O0O00OO00 .dens [O0000OO0OOO000O00 ]#line:210
        if O0OO0O00O0O00OO00 .board [O0OOOOOOOO0OOO0OO ][OO0OOO0O0O0000000 ]:#line:211
            O0OO0O00O0O00OO00 .winner =OO0OO0O0O000OOOOO #line:212
            return True #line:213
        if O0OO0O00O0O00OO00 .peace_counter >=Jungle .MAXIMAL_PASSIVE :#line:215
            O00OOO0OO0O0OO000 =O0OO0O00O0O00OO00 .pieces_comparison ()#line:216
            if O00OOO0OO0O0OO000 is None :#line:217
                O0OO0O00O0O00OO00 .winner =1 #line:218
            else :#line:219
                O0OO0O00O0O00OO00 .winner =O00OOO0OO0O0OO000 #line:220
            return True #line:221
        return False #line:222
    def do_move (OO00O0O000OO000OO ,OOOOOO0000OOO0O00 ):#line:224
        OO00O0O000OO000OO .curplayer =1 -OO00O0O000OO000OO .curplayer #line:225
        if OOOOOO0000OOO0O00 is None :#line:226
            return #line:227
        O000000O000OO0OO0 ,OOO000OO0OOO0OOO0 =OOOOOO0000OOO0O00 #line:228
        OOO0O0O00O000O00O ,O00OO000O00O0OO00 =O000000O000OO0OO0 #line:229
        OO0OOOO000OO00OOO ,OOO0OOO0OO0000OO0 =OO00O0O000OO000OO .board [O00OO000O00O0OO00 ][OOO0O0O00O000O00O ]#line:230
        O0OOOO00O0O0O00OO ,OO0OO0O0O0OOOO0OO =OOO000OO0OOO0OOO0 #line:232
        if OO00O0O000OO000OO .board [OO0OO0O0O0OOOO0OO ][O0OOOO00O0O0O00OO ]:#line:233
            O000OOOOO00OO000O ,OO0OO0000O0O000O0 =OO00O0O000OO000OO .board [OO0OO0O0O0OOOO0OO ][O0OOOO00O0O0O00OO ]#line:234
            del OO00O0O000OO000OO .pieces [O000OOOOO00OO000O ][OO0OO0000O0O000O0 ]#line:235
            OO00O0O000OO000OO .peace_counter =0 #line:236
        else :#line:237
            OO00O0O000OO000OO .peace_counter +=1 #line:238
        OO00O0O000OO000OO .pieces [OO0OOOO000OO00OOO ][OOO0OOO0OO0000OO0 ]=(O0OOOO00O0O0O00OO ,OO0OO0O0O0OOOO0OO )#line:240
        OO00O0O000OO000OO .board [OO0OO0O0O0OOOO0OO ][O0OOOO00O0O0O00OO ]=(OO0OOOO000OO00OOO ,OOO0OOO0OO0000OO0 )#line:241
        OO00O0O000OO000OO .board [O00OO000O00O0OO00 ][OOO0O0O00O000O00O ]=None #line:242
    def better_rollout (O0O000000O0OOOO0O ,OOO00O00O000OOOO0 ):#line:244
        O00O0O0000O0000O0 =random .randint (0 ,1 )#line:245
        O0OOO00O0OO0OOO00 =0 #line:246
        while O0OOO00O0OO0OOO00 <1000 :#line:247
            O0OOO00O0OO0OOO00 +=1 #line:248
            OO0O0OO0OOO0000O0 =O0O000000O0OOOO0O .moves (OOO00O00O000OOOO0 )#line:249
            if len (OO0O0OO0OOO0000O0 )==0 :#line:250
                O00O0O0000O0000O0 =1 -OOO00O00O000OOOO0 #line:251
                break #line:252
            O000O00O0O0OO0O00 =O0O000000O0OOOO0O .better_random_choice (OO0O0OO0OOO0000O0 )#line:253
            O0O000000O0OOOO0O .do_move (O000O00O0O0OO0O00 )#line:254
            if O0O000000O0OOOO0O .victory (OOO00O00O000OOOO0 ):#line:255
                O00O0O0000O0000O0 =OOO00O00O000OOOO0 #line:256
                break #line:257
            OOO00O00O000OOOO0 =1 -OOO00O00O000OOOO0 #line:258
        return O0OOO00O0OO0OOO00 ,O00O0O0000O0000O0 #line:260
    def update (OOO000OO0OOO0O0O0 ,OO00OO00OOO00OO00 ,O0OO00O000OO0O00O ):#line:263
        assert OO00OO00OOO00OO00 ==OOO000OO0OOO0O0O0 .curplayer #line:264
        O0OO0O000OO00OO0O =tuple (int (OOOOO00000OOO000O )for OOOOO00000OOO000O in O0OO00O000OO0O00O .split ())#line:265
        if len (O0OO0O000OO00OO0O )!=4 :#line:266
            raise WrongMove #line:267
        O0OO0OO00O0O0O0OO =OOO000OO0OOO0O0O0 .moves (OO00OO00OOO00OO00 )#line:268
        OO0000OO00OO0OOOO =O0OO0OO00O0O0O0OO #line:269
        if not O0OO0OO00O0O0O0OO :#line:270
            if O0OO0O000OO00OO0O !=(-1 ,-1 ,-1 ,-1 ):#line:271
                raise WrongMove #line:272
            O0OO0O000OO00OO0O =None #line:273
        else :#line:274
            O0OO0O000OO00OO0O =((O0OO0O000OO00OO0O [0 ],O0OO0O000OO00OO0O [1 ]),(O0OO0O000OO00OO0O [2 ],O0OO0O000OO00OO0O [3 ]))#line:275
            if O0OO0O000OO00OO0O not in OO0000OO00OO0OOOO :#line:276
                raise WrongMove #line:277
        OOO000OO0OOO0O0O0 .do_move (O0OO0O000OO00OO0O )#line:278
        if OOO000OO0OOO0O0O0 .victory (OO00OO00OOO00OO00 ):#line:280
            assert OOO000OO0OOO0O0O0 .winner is not None #line:281
            return 2 *OOO000OO0OOO0O0O0 .winner -1 #line:282
        else :#line:283
            return None #line:284
class Player (object ):#line:287
    def __init__ (OOO0OO0O00O000OO0 ):#line:288
        OOO0OO0O00O000OO0 .reset ()#line:289
    def reset (O0000O00OOO0OO00O ):#line:291
        O0000O00OOO0OO00O .game =Jungle ()#line:292
        O0000O00OOO0OO00O .my_player =1 #line:293
        O0000O00OOO0OO00O .say ('RDY')#line:294
    def say (O0OOO00OO0OO0O0O0 ,O0OOOOO00OO0OOOO0 ):#line:296
        sys .stdout .write (O0OOOOO00OO0OOOO0 )#line:297
        sys .stdout .write ('\n')#line:298
        sys .stdout .flush ()#line:299
    def hear (OO0O00OO00OOO00OO ):#line:301
        O0O0OOO00OO00OOOO =sys .stdin .readline ().split ()#line:302
        return O0O0OOO00OO00OOOO [0 ],O0O0OOO00OO00OOOO [1 :]#line:303
    def loop (OO00OO00O000O0OOO ):#line:305
        while True :#line:306
            OO000000O000OO0O0 ,OO000000OOO0O0O0O =OO00OO00O000O0OOO .hear ()#line:307
            if OO000000O000OO0O0 =='HEDID':#line:308
                OO00OO00O0OO0OOO0 ,O00000000OOO0O0OO =OO000000OOO0O0O0O [:2 ]#line:309
                O0O00O0O0000OOO00 =tuple ((int (OO0OOO0O00OO0O000 )for OO0OOO0O00OO0O000 in OO000000OOO0O0O0O [2 :]))#line:310
                if O0O00O0O0000OOO00 ==(-1 ,-1 ,-1 ,-1 ):#line:311
                    O0O00O0O0000OOO00 =None #line:312
                else :#line:313
                    O0O0OOO0O0000O000 ,OO00OOOOO0OOO000O ,OOOO000O0O0OO0OO0 ,OO000OO0O0O0O0O0O =O0O00O0O0000OOO00 #line:314
                    O0O00O0O0000OOO00 =((O0O0OOO0O0000O000 ,OO00OOOOO0OOO000O ),(OOOO000O0O0OO0OO0 ,OO000OO0O0O0O0O0O ))#line:315
                OO00OO00O000O0OOO .game .do_move (O0O00O0O0000OOO00 )#line:317
            elif OO000000O000OO0O0 =='ONEMORE':#line:318
                OO00OO00O000O0OOO .reset ()#line:319
                continue #line:320
            elif OO000000O000OO0O0 =='BYE':#line:321
                break #line:322
            else :#line:323
                assert OO000000O000OO0O0 =='UGO'#line:324
                OO00OO00O000O0OOO .my_player =0 #line:326
            OOO0O0O000000O0O0 =OO00OO00O000O0OOO .game .moves (OO00OO00O000O0OOO .my_player )#line:328
            if OOO0O0O000000O0O0 :#line:329
                O0O00O0O0000OOO00 =OO00OO00O000O0OOO .game .better_random_choice (OOO0O0O000000O0O0 )#line:330
                OO00OO00O000O0OOO .game .do_move (O0O00O0O0000OOO00 )#line:331
                O0O00O0O0000OOO00 =(O0O00O0O0000OOO00 [0 ][0 ],O0O00O0O0000OOO00 [0 ][1 ],O0O00O0O0000OOO00 [1 ][0 ],O0O00O0O0000OOO00 [1 ][1 ])#line:332
            else :#line:333
                OO00OO00O000O0OOO .game .do_move (None )#line:334
                O0O00O0O0000OOO00 =(-1 ,-1 ,-1 ,-1 )#line:335
            OO00OO00O000O0OOO .say ('IDO %d %d %d %d'%O0O00O0O0000OOO00 )#line:336
if __name__ =='__main__':#line:339
    player =Player ()#line:340
    player .loop ()
