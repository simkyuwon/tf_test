CONST cHEAD_SPEED = 11
CONST cIR_SENSOR_PORT = 4

'********** protocol value begin **********'
CONST cSIGNAL_CHECK = &H40
CONST cSIGNAL_IMAGE = &H41
CONST cSIGNAL_STATE = &H42

CONST cMOTION_LINE_MOVE_FRONT = &H80
CONST cMOTION_LINE_MOVE_FRONT_SMALL = &H81
CONST cMOTION_LINE_MOVE_LEFT = &H82
CONST cMOTION_LINE_MOVE_RIGHT = &H83
CONST cMOTION_LINE_TURN_LEFT_SMALL = &H84
CONST cMOTION_LINE_TURN_RIGHT_SMALL = &H85
CONST cMOTION_LINE_TURN_LEFT_BIG = &H86
CONST cMOTION_LINE_TURN_RIGHT_BIG = &H87
CONST cMOTION_LINE_LOST = &H88
CONST cMOTION_LINE_STOP = &H89

CONST cMOTION_DIRECTION_UNKNOWN = &H90
CONST cMOTION_DIRECTION_EAST = &H91
CONST cMOTION_DIRECTION_WEST = &H92
CONST cMOTION_DIRECTION_SOUTH = &H93
CONST cMOTION_DIRECTION_NORTH = &H94
CONST cMOTION_DIRECTION_DOOR = &H95

CONST cMOTION_ARROW_UNKNOWN = &HA0
CONST cMOTION_ARROW_LEFT = &HA1
CONST cMOTION_ARROW_RIGHT = &HA2

CONST cMOTION_SECTION_UNKNOWN = &HB0
CONST cMOTION_SECTION_A = &HB1
CONST cMOTION_SECTION_B = &HB2
CONST cMOTION_SECTION_C = &HB3
CONST cMOTION_SECTION_D = &HB4
CONST cMOTION_SECTION_SAFE = &HB5
CONST cMOTION_SECTION_DANGER = &HB6

CONST cMOTION_MILK_NOT_FOUND = &HC0
CONST cMOTION_MILK_FOUND = &HC1
CONST cMOTION_MILK_MOVE_FRONT = &HC2
CONST cMOTION_MILK_MOVE_LEFT = &HC3
CONST cMOTION_MILK_MOVE_RIGHT = &HC4
CONST cMOTION_MILK_IN_SECTION = &HC5
CONST cMOTION_MILK_OUT_SECTION = &HC6
'********** protocol value end **********'

DIM i AS BYTE
DIM j AS BYTE
DIM temp AS BYTE
DIM rx_data AS BYTE
DIM ir_data AS INTEGER
DIM walking_speed1 AS BYTE
DIM walking_speed2 AS BYTE
DIM walking_count AS INTEGER
DIM head_angle AS BYTE
DIM clockwise AS BYTE
DIM section_type AS BYTE
DIM mission_count AS BYTE
DIM section_turn AS BYTE


GOTO Main

'********** Motor Control Begin **********'
MotorAllOn:
    GOSUB MotorGetAndSet

    MOTOR G6B
    DELAY 50
    MOTOR G6C
    DELAY 50
    MOTOR G6A
    DELAY 50
    MOTOR G6D

    GOSUB SoundStart
    RETURN

MotorAllOff:
    MOTOROFF G6B
    MOTOROFF G6C
    MOTOROFF G6A
    MOTOROFF G6D

    GOSUB MotorGetAndSet
    GOSUB SoundFinish
    RETURN

MotorGetAndSet:
    GETMOTORSET G6A, 1, 1, 1, 1, 1, 0
    GETMOTORSET G6B, 1, 1, 1, 0, 0, 1
    GETMOTORSET G6C, 1, 1, 1, 0, 1, 0
    GETMOTORSET G6D, 1, 1, 1, 1, 1, 0
    RETURN

MotorAllMode2:
    MOTORMODE G6A, 2, 2, 2, 2, 2
    MOTORMODE G6D, 2, 2, 2, 2, 2
    MOTORMODE G6B, 2, 2, 2,  ,  , 2
    MOTORMODE G6C, 2, 2, 2,  , 2
    RETURN

MotorAllMode3:
    MOTORMODE G6A, 3, 3, 3, 3, 3
    MOTORMODE G6D, 3, 3, 3, 3, 3
    MOTORMODE G6B, 3, 3, 3,  ,  , 3
    MOTORMODE G6C, 3, 3, 3,  , 3
    RETURN

MotorArmMode1:
    MOTORMODE G6B, 1, 1, 1,  ,  , 1
    MOTORMODE G6C, 1, 1, 1,  , 1
    RETURN

MotorArmMode2:
    MOTORMODE G6B, 2, 2, 2,  ,  , 2
    MOTORMODE G6C, 2, 2, 2,  , 2
    RETURN

MotorArmMode3:
    MOTORMODE G6B, 3, 3, 3,  ,  , 3
    MOTORMODE G6C, 3, 3, 3,  , 3
    RETURN

MotorLegMode1:
    MOTORMODE G6A, 1, 1, 1, 1, 1
    MOTORMODE G6D, 1, 1, 1, 1, 1
    RETURN

MotorLegMode2:
    MOTORMODE G6A, 2, 2, 2, 2, 2
    MOTORMODE G6D, 2, 2, 2, 2, 2
    RETURN

MotorLegMode3:
    MOTORMODE G6A, 3, 3, 3, 3, 3
    MOTORMODE G6D, 3, 3, 3, 3, 3
    RETURN
    '********** Motor Control End **********'


    '********** Posture Setting End **********'
PostureInit:
    MOVE G6A, 100,  76, 145,  93, 100, 100
    MOVE G6D, 100,  76, 145,  93, 100, 100
    MOVE G6B, 100,  35,  90,
    MOVE G6C, 100,  35,  90
    WAIT
    RETURN

PostureDefault:
    MOVE G6A, 100,  76, 145,  93, 100, 100
    MOVE G6D, 100,  76, 145,  93, 100, 100
    MOVE G6B, 100,  30,  80,
    MOVE G6C, 100,  30,  80,
    WAIT
    RETURN

PostureSit:
    MOVE G6A, 100, 145,  28, 145, 100, 100
    MOVE G6D, 100, 145,  28, 145, 100, 100
    MOVE G6B, 100,  30,  80
    MOVE G6C, 100,  30,  80
    WAIT
    RETURN

PostureDoor:
    MOVE G6A, 100,  76, 145,  93, 100, 100
    MOVE G6D, 100,  76, 145,  93, 100, 100
    MOVE G6B, 190,  15,  55,  ,  ,
    MOVE G6C, 190,  15,  55,  ,  ,
    WAIT
    RETURN

PostureMilkHigh:
    MOVE G6A, 100,  76, 145,  93, 100, 100
    MOVE G6D, 100,  76, 145,  93, 100, 100
    MOVE G6B, 190,  15,  55,    ,    ,
    MOVE G6C, 190,  15,  55,    ,    ,
    WAIT
    RETURN

PostureMilkLow:
    MOVE G6A, 100,  76, 145,  93, 100, 100
    MOVE G6D, 100,  76, 145,  93, 100, 100
    MOVE G6B, 140,  15,  55,    ,    ,
    MOVE G6C, 140,  15,  55,    ,    ,
    WAIT
    RETURN

PostureHeadTurn:
    SPEED cHEAD_SPEED
    SERVO 11, head_angle
    DELAY 400
    RETURN

PostureHeadDown:
    SPEED cHEAD_SPEED
    SERVO 16, head_angle
    DELAY 400
    RETURN
    '********** Posture Setting End **********'


    '********** Motion Begin **********'
MotionWalkingFront:
    GOSUB MotorAllMode3
    SPEED 14
    MOVE G6D,  95,  76, 147,  93, 95
    MOVE G6A, 101,  76, 147,  93, 98
    MOVE G6B, 100
    MOVE G6C, 100
    WAIT

    FOR i = 1 TO walking_count
        MOVE G6A,  85,  90, 125, 100, 109
        MOVE G6D, 104,  77, 147,  93,  97
        MOVE G6B,  85
        MOVE G6C, 115
        WAIT

        MOVE G6A, 103,  73, 140, 103, 100
        MOVE G6D,  95,  85, 147,  85, 102
        WAIT

        MOVE G6D,  85,  90, 125, 100, 109
        MOVE G6A, 104,  77, 147,  93,  97
        MOVE G6C,  85
        MOVE G6B, 115
        WAIT

        MOVE G6D, 103,  73, 140, 103, 100
        MOVE G6A,  95,  85, 147,  85, 102
        WAIT
    NEXT i

    SPEED 10
    MOVE G6A,  85,  90, 125,  95, 104
    MOVE G6D, 102,  76, 145,  91, 102
    MOVE G6B, 100
    MOVE G6C, 100
    WAIT

    GOSUB PostureDefault
    RETURN

MotionWalkingRight:
    MOTORMODE G6A, 3, 3, 3, 3, 2
    MOTORMODE G6D, 3, 3, 3, 3, 2

    FOR i = 1 TO walking_count
        SPEED 12
        MOVE G6D,  93,  90, 120, 105, 104, 100
        MOVE G6A, 103,  76, 145,  93, 104, 100
        WAIT

        MOVE G6D, 102,  77, 145,  93, 100, 100
        MOVE G6A,  90,  80, 140,  95, 107, 100
        WAIT

        SPEED 15
        MOVE G6D,  98,  76, 145,  93, 100, 100
        MOVE G6A,  98,  76, 145,  93, 100, 100
        WAIT

        SPEED 8
        GOSUB PostureDefault
    NEXT i
    GOSUB MotorAllMode3
    RETURN

MotionWalkingRightBig:
    GOSUB MotorAllMode3

    FOR i = 1 TO walking_count
        SPEED 4
        MOVE G6D, 88,  71, 152,  91, 110, '60
        MOVE G6A,108,  76, 146,  93,  92, '60
        MOVE G6C,100,  40,  80
        MOVE G6B,100,  40,  80
        WAIT

        SPEED 6
        MOVE G6D, 85,  80, 140, 95, 114, 100
        MOVE G6A,112,  76, 146,  93, 98, 100
        MOVE G6C,100,  40,  80
        MOVE G6B,100,  40,  80
        WAIT

        MOVE G6A,110,  92, 124,  97,  93,  100
        MOVE G6D, 76,  72, 160,  77, 128,  100
        MOVE G6C,100,  40,  80, , , ,
        MOVE G6B,100,  40,  80, , , ,
        WAIT

        MOVE G6D,94,  76, 145,  93, 106, 100
        MOVE G6A,94,  76, 145,  93, 106, 100
        MOVE G6C,100,  40,  80
        MOVE G6B,100,  40,  80
        WAIT	

        MOVE G6D,110,  92, 124,  97,  93,  100
        MOVE G6A, 76,  72, 160,  82, 120,  100
        MOVE G6C,100,  40,  80, , , ,
        MOVE G6B,100,  40,  80, , , ,
        WAIT

        SPEED 5
        MOVE G6A, 90,  80, 140, 95, 110, 100
        MOVE G6D,112,  76, 146,  93, 98, 100
        MOVE G6C,100,  40,  80
        MOVE G6B,100,  40,  80
        WAIT

        SPEED 4
        MOVE G6A, 88,  71, 152,  91, 110, '60
        MOVE G6D,108,  76, 146,  93,  92, '60
        MOVE G6C,100,  40,  80
        MOVE G6B,100,  40,  80
        WAIT

        SPEED 2
        GOSUB PostureDefault
    NEXT i
    RETURN

MotionWalkingLeft:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    FOR i = 1 TO walking_count
        SPEED 12
        MOVE G6A,  93,  90, 120, 105, 104, 100
        MOVE G6D, 103,  76, 145,  93, 104, 100
        WAIT

        MOVE G6A, 102,  77, 145,  93, 100, 100
        MOVE G6D,  90,  80, 140,  95, 107, 100
        WAIT

        SPEED 15
        MOVE G6A,  98,  76, 145,  93, 100, 100
        MOVE G6D,  98,  76, 145,  93, 100, 100
        WAIT

        SPEED 8
        GOSUB PostureDefault
    NEXT i

    GOSUB MotorAllMode3
    RETURN

MotionWalkingLeftBig:
    GOSUB MotorAllMode3

    FOR i = 1 TO walking_count
        SPEED 4
        MOVE G6A, 88,  71, 152,  91, 110, '60
        MOVE G6D,108,  76, 146,  93,  92, '60
        MOVE G6B,100,  40,  80
        MOVE G6C,100,  40,  80
        WAIT

        SPEED 6
        MOVE G6A, 90,  80, 140, 95, 114, 100
        MOVE G6D,112,  76, 146,  93, 98, 100
        MOVE G6B,100,  40,  80
        MOVE G6C,100,  40,  80
        WAIT

        MOVE G6D,110,  92, 124,  97,  93,  100
        MOVE G6A, 76,  72, 160,  77, 128,  100
        MOVE G6B,100,  40,  80, , , ,
        MOVE G6C,100,  40,  80, , , ,
        WAIT

        MOVE G6A,94,  76, 145,  93, 106, 100
        MOVE G6D,94,  76, 145,  93, 106, 100
        MOVE G6B,100,  40,  80
        MOVE G6C,100,  40,  80
        WAIT	

        MOVE G6A,110,  92, 124,  97,  93,  100
        MOVE G6D, 76,  72, 160,  82, 120,  100
        MOVE G6B,100,  40,  80, , , ,
        MOVE G6C,100,  40,  80, , , ,
        WAIT

        SPEED 5
        MOVE G6D, 85,  80, 140, 95, 110, 100
        MOVE G6A,112,  76, 146,  93, 98, 100
        MOVE G6B,100,  40,  80
        MOVE G6C,100,  40,  80
        WAIT

        SPEED 4
        MOVE G6D, 88,  71, 152,  91, 110, '60
        MOVE G6A,108,  76, 146,  93,  92, '60
        MOVE G6B,100,  40,  80
        MOVE G6C,100,  40,  80
        WAIT

        SPEED 2
        GOSUB PostureDefault
    NEXT i
    RETURN

MotionTurnRight:
    MOTORMODE G6A, 3, 3, 3, 3, 2
    MOTORMODE G6D, 3, 3, 3, 3, 2
    FOR i = 1 TO walking_count
        SPEED 8
        MOVE G6A,100,  56, 145,  113, 100, 100
        MOVE G6D,100,  96, 145,  73, 100, 100
        MOVE G6B,90
        MOVE G6C,110
        WAIT

        SPEED 12
        MOVE G6A,98,  56, 145,  113, 100, 100
        MOVE G6D,98,  96, 145,  73, 100, 100
        WAIT

        SPEED 6
        MOVE G6A,101,  76, 146,  93, 98, 100
        MOVE G6D,101,  76, 146,  93, 98, 100
        WAIT

        GOSUB PostureDefault
        DELAY 100
    NEXT i

    RETURN

MotionTurnLeft:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    FOR i = 1 TO walking_count
        SPEED 8
        MOVE G6D, 100,  56, 145, 113, 100,  100
        MOVE G6A, 100,  96, 145,  73, 100,  100
        MOVE G6B, 110
        MOVE G6C,  90

        SPEED 12
        MOVE G6D,98,  56, 145,  113, 100, 100
        MOVE G6A,98,  96, 145,  73, 100, 100
        WAIT
        SPEED 6

        MOVE G6D,101,  76, 146,  93, 98, 100
        MOVE G6A,101,  76, 146,  93, 98, 100
        WAIT

        GOSUB PostureDefault
        DELAY 100
    NEXT i

    RETURN

MotionTurnRightBig:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    FOR i = 1 TO walking_count
        SPEED 15
        MOVE G6A,  95,  36, 145, 133, 105, 100
        MOVE G6D,  95, 116, 145,  53, 105, 100
        WAIT

        MOVE G6A,  90,  36, 145, 133, 105, 100
        MOVE G6D,  90, 116, 145,  53, 105, 100
        WAIT

        SPEED 9
        GOSUB PostureDefault
        DELAY 500
    NEXT i
    RETURN

MotionTurnLeftBig:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    FOR i = 1 TO walking_count
        SPEED 15
        MOVE G6A,95,  116, 145,  53, 105, 100
        MOVE G6D,95,  36, 145,  133, 105, 100
        WAIT

        MOVE G6A,90,  116, 145,  53, 105, 100
        MOVE G6D,90,  36, 145,  133, 105, 100
        WAIT

        SPEED 9
        GOSUB PostureDefault
        DELAY 500
    NEXT i
    RETURN

MotionWalkingFrontDoor:
    GOSUB MotorAllMode3
    SPEED 10
    MOVE G6A,  95,  76, 147,  88, 101
    MOVE G6D, 101,  76, 147,  88,  98
    MOVE G6B, 190,  15,  55,  ,  ,
    MOVE G6C, 190,  15,  55,  ,  ,
    WAIT

    FOR i = 1 TO walking_count
        MOVE G6A,  90,  90, 125,  95, 109,
        MOVE G6D, 104,  77, 147,  88,  97,
        WAIT


        MOVE G6A, 103,  73, 140,  98, 100
        MOVE G6D,  95,  85, 147,  80, 102
        WAIT

        MOVE G6D,  90,  90, 125,  95, 109,
        MOVE G6A, 104,  77, 147,  88,  97,
        WAIT

        MOVE G6D, 103,  73, 140,  98, 100
        MOVE G6A,  95,  85, 147,  80, 102
        WAIT
    NEXT i

    MOVE G6A,  85,  90, 125,  95, 104
    MOVE G6D, 102,  76, 145,  91, 102
    WAIT

    SPEED 15
    GOSUB PostureDoor
    RETURN

MotionWalkingRightDoor:
    MOTORMODE G6A, 3, 3, 3, 3, 2
    MOTORMODE G6D, 3, 3, 3, 3, 2
    FOR i = 1 TO walking_count
        SPEED 12
        MOVE G6D,  95,  90, 125, 100, 104, 100
        MOVE G6A, 105,  76, 146,  93, 104, 100
        WAIT

        MOVE G6D, 102,  77, 145,  93, 100, 100
        MOVE G6A,  90,  80, 140,  95, 107, 100
        WAIT

        SPEED 10
        MOVE G6D,  95,  76, 145,  93, 102, 100
        MOVE G6A,  95,  76, 145,  93, 102, 100
        WAIT

        SPEED 8
        GOSUB PostureDoor
    NEXT i
    GOSUB MotorAllMode3
    RETURN

MotionWalkingLeftDoor:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    FOR i = 1 TO walking_count
        SPEED 12
        MOVE G6A,  95,  90, 125, 100, 104, 100
        MOVE G6D, 105,  76, 145,  93, 104, 100
        WAIT

        SPEED 12
        MOVE G6A, 102,  77, 145,  93, 100, 100
        MOVE G6D,  90,  80, 140,  95, 107, 100
        WAIT

        SPEED 10
        MOVE G6A,  95,  76, 145,  93, 102, 100
        MOVE G6D,  95,  76, 145,  93, 102, 100
        WAIT

        SPEED 8
        GOSUB PostureDoor
    NEXT i
    GOSUB MotorAllMode3
    RETURN

MotionTurnRightDoor:
    MOTORMODE G6A, 3, 3, 3, 3, 2
    MOTORMODE G6D, 3, 3, 3, 3, 2
    FOR i = 1 TO walking_count
        SPEED 8
        MOVE G6D,  93,  96, 145,  73, 105, 100
        MOVE G6A,  95,  56, 145, 113, 105, 100
        WAIT

        SPEED 6
        MOVE G6D,  93,  96, 145,  73, 105, 100
        MOVE G6A,  94,  56, 145, 113, 105, 100
        WAIT

        SPEED 7
        MOVE G6D,  93,  96, 145,  73, 105, 100
        MOVE G6A,  93,  56, 145, 113, 105, 100
        WAIT

        SPEED 6
        MOVE G6D, 100,  76, 146,  93,  98, 100
        MOVE G6A, 101,  76, 146,  93,  98, 100
        WAIT
    NEXT i
    GOSUB PostureDoor
    RETURN

MotionTurnLeftDoor:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    FOR i = 1 TO walking_count
        SPEED 8
        MOVE G6D,  95,  56, 145, 113, 105, 100
        MOVE G6A,  93,  96, 145,  73, 105, 100
        WAIT

        SPEED 6
        MOVE G6D,  94,  56, 145, 113, 105, 100
        MOVE G6A,  93,  96, 145,  73, 105, 100
        WAIT

        SPEED 7
        MOVE G6D,  93,  56, 145, 113, 105, 100
        MOVE G6A,  93,  96, 145,  73, 105, 100
        WAIT

        SPEED 6
        MOVE G6D, 101,  76, 146,  93,  98, 100
        MOVE G6A, 101,  76, 146,  93,  98, 100
        WAIT
    NEXT i
    GOSUB PostureDoor
    RETURN

MotionOpenDoor:
    SPEED 8
    MOVE G6B, 180,  20,  50
    MOVE G6C, 180,  20,  50
    WAIT

    MOVE G6B, 190,  15,  55
    MOVE G6C, 190,  15,  55
    WAIT
    RETURN

MotionCatchMilk:
    GOSUB MotorAllMode3

    SPEED 6
    GOSUB PostureSit

    SPEED 12	
    MOVE G6B, 160,  30, 100
    MOVE G6C, 160,  30, 100
    WAIT	

    SPEED 3
    MOVE G6A,  85, 150,  31, 152, 115,
    MOVE G6D,  85, 150,  31, 152, 115,
    WAIT

    SPEED 10
    MOVE G6B, 155,  17,  60,  ,  ,
    MOVE G6C, 155,  17,  60,  ,  ,
    WAIT

    MOVE G6B, 150,  15,  55,  ,  ,
    MOVE G6C, 150,  15,  55,  ,  ,
    WAIT

    MOVE G6B, 150,  20, 100
    MOVE G6C, 150,  20, 100
    WAIT

    SPEED 5
    MOVE G6B, 145,  15,  55,  ,  ,
    MOVE G6C, 145,  15,  55,  ,  ,
    WAIT

    SPEED 6
    MOVE G6A, 100, 145,  28, 145, 100,
    MOVE G6D, 100, 145,  28, 145, 100,
    WAIT

    SPEED 5
    MOVE G6A, 100,  76, 145,  93, 100, 100
    MOVE G6D, 100,  76, 145,  93, 100, 100
    WAIT

    MOVE G6B, 190,  15,  55,  ,  ,
    MOVE G6C, 190,  15,  55,  ,  ,
    WAIT

    RETURN

MotionPutMilk:
    GOSUB MotorLegMode3

    SPEED 5
    MOVE G6D, 100,  71, 145,  93, 100, 100
    MOVE G6A, 100,  71, 145,  93, 100, 100
    WAIT

    SPEED 9
    MOVE G6A, 100, 140,  37, 145, 100, 100
    MOVE G6D, 100, 140,  37, 145, 100, 100
    WAIT

    MOVE G6A,  87, 145,  28, 159, 115,
    MOVE G6D,  87, 145,  28, 159, 115,
    WAIT

    GOSUB MotorArmMode3

    MOVE G6B, 153,  15,  55,  ,  ,
    MOVE G6C, 153,  15,  55,  ,  ,
    WAIT

    MOVE G6B, 165, 30, 100
    MOVE G6C, 165, 30, 100
    WAIT

    SPEED 6
    MOVE G6A, 100, 145,  28, 145, 100,
    MOVE G6D, 100, 145,  28, 145, 100,
    WAIT

    MOVE G6B, 100,  30,  80
    MOVE G6C, 100,  30,  80
    WAIT

    GOSUB PostureDefault
    RETURN

MotionWalkingFrontWithMilk:
    GOSUB MotorAllMode3
    SPEED 7

    MOVE G6A,  95,  76, 147,  83, 101
    MOVE G6D, 101,  76, 147,  83,  98
    MOVE G6B, 190,  15,  55,    ,    ,
    MOVE G6C, 190,  15,  55,    ,    ,
    WAIT

    FOR i = 1 TO walking_count
        MOVE G6A,  95,  95, 125,  85, 104
        MOVE G6D, 104,  80, 147,  68, 102
        WAIT

        MOVE G6A, 103,  80, 140,  90, 100
        MOVE G6D,  95,  90, 147,  73, 102
        WAIT

        MOVE G6D,  95,  90, 125,  85, 104
        MOVE G6A, 104,  80, 147,  68, 102
        WAIT

        MOVE G6D, 103,  80, 140,  90, 100
        MOVE G6A,  95,  95, 147,  73, 102
        WAIT
    NEXT i

    MOVE G6A,  95,  90, 125,  85, 104
    MOVE G6D, 104,  76, 145,  81, 102
    WAIT

    SPEED 10
    GOSUB PostureMilkHigh
    RETURN

MotionTurnRightWithMilk:
    GOSUB MotorLegMode2
    FOR i = 1 TO walking_count
        SPEED 8
        MOVE G6D,  93,  96, 145,  73, 105, 100
        MOVE G6A,  95,  56, 145, 113, 105, 100
        WAIT

        SPEED 6
        MOVE G6D,  93,  96, 145,  73, 105, 100
        MOVE G6A,  94,  56, 145, 113, 105, 100
        WAIT

        SPEED 7
        MOVE G6D,  93,  96, 145,  73, 105, 100
        MOVE G6A,  93,  56, 145, 113, 105, 100
        WAIT

        SPEED 6
        MOVE G6D, 100,  76, 146,  93,  98, 100
        MOVE G6A, 101,  76, 146,  93,  98, 100
        WAIT
        DELAY 200
    NEXT i

    SPEED 10
    GOSUB PostureMilkLow
    RETURN

MotionTurnLeftWithMilk:
    GOSUB MotorLegMode2
    FOR i = 1 TO walking_count
        SPEED 8
        MOVE G6D,  95,  56, 145, 113, 105, 100
        MOVE G6A,  93,  96, 145,  73, 105, 100
        WAIT

        SPEED 6
        MOVE G6D,  94,  56, 145, 113, 105, 100
        MOVE G6A,  93,  96, 145,  73, 105, 100
        WAIT

        SPEED 7
        MOVE G6D,  93,  56, 145, 113, 105, 100
        MOVE G6A,  93,  96, 145,  73, 105, 100
        WAIT

        SPEED 6
        MOVE G6D, 101,  76, 146,  93,  98, 100
        MOVE G6A, 101,  76, 146,  93,  98, 100
        WAIT
        DELAY 200
    NEXT i


    SPEED 10
    GOSUB PostureMilkLow
    RETURN
    '********** Motion End **********'


    '********** Sound Begin **********'
SoundStart:
    TEMPO 220
    MUSIC "O23EAB7EA>3#C"
    RETURN

SoundFinish:
    TEMPO 220
    MUSIC "O38GD<BGD<BG"
    RETURN

SoundError:
    TEMPO 250
    MUSIC "FFF"
    RETURN
    '********** Sound End **********'


    '********** Function Begin **********'
Initiate:
    PTP SETON
    PTP ALLON

    DIR G6A, 1, 0, 0, 1, 0, 0
    DIR G6D, 0, 1, 1, 0, 1, 1
    DIR G6B, 1, 1, 1, 1, 1, 1
    DIR G6C, 0, 0, 0, 0, 1, 0

    OUT 52, 0

    TEMPO 230
    MUSIC "CDEFG"

    SPEED 50
    GOSUB MotorAllOn

    SERVO 11, 100
    SERVO 16, 100

    GOSUB PostureInit
    GOSUB PostureDefault

    PRINT "OPEN 20GongMo.mrs !"
    PRINT "VOLUME 200 !"
    PRINT "SND 12 !"

    mission_count = 0

    GOSUB MotorAllMode3
    RETURN

UartRx:
    rx_data = 0
    DELAY 10
    ERX 4800, rx_data, UartRx
    RETURN

UartConnectWait:
    ETX 4800, cSIGNAL_CHECK
    DELAY 200
    ERX 4800, rx_data, UartConnectWait
    IF rx_data = cSIGNAL_CHECK THEN
        RETURN
    ENDIF
    GOTO UartConnectWait
    '********** Function End **********'


    '********** State Begin **********'
StateDirectionRecognition:
    head_angle = 75
    GOSUB PostureHeadDown

    FOR i = 0 TO 3
        head_angle = i * 12 + 82
        GOSUB PostureHeadTurn
        ETX 4800, cSIGNAL_IMAGE
        GOSUB UartRx
    NEXT i

    GOSUB MotorArmMode3
    SPEED 15
    IF rx_data = cMOTION_DIRECTION_EAST THEN
        MOVE G6B, 100,  30,  80
        MOVE G6C, 190,  10, 100
        DELAY 200
        PRINT "SND 0 !"
    ELSEIF rx_data = cMOTION_DIRECTION_WEST THEN
        MOVE G6B, 190,  10, 100
        MOVE G6C, 100,  30,  80
        DELAY 200
        PRINT "SND 1 !"
    ELSEIF rx_data = cMOTION_DIRECTION_SOUTH THEN
        MOVE G6B,  10,  10, 100
        MOVE G6C,  10,  10, 100
        DELAY 200
        PRINT "SND 2 !"
    ELSEIF rx_data = cMOTION_DIRECTION_NORTH THEN
        MOVE G6B, 190,  10, 100
        MOVE G6C, 190,  10, 100
        DELAY 200
        PRINT "SND 3 !"
    ENDIF
    GOSUB PostureDefault
    GOSUB MotorArmMode1

    GOTO StateLinetracingToArrowInit


StateLinetracingToArrowInit:
    ETX 4800, cSIGNAL_STATE
    GOSUB MotionOpenDoor

    head_angle = 100
    GOSUB PostureHeadTurn

    head_angle = 30
    GOSUB PostureHeadDown

StateLinetracingToArrow:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_LINE_STOP THEN
        GOTO StateArrowRecognitionInit
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT THEN
        walking_count = 2
        GOSUB MotionWalkingFrontDoor
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT_SMALL THEN
        walking_count = 1
        GOSUB MotionWalkingFrontDoor
    ELSEIF rx_data = cMOTION_LINE_MOVE_LEFT THEN
        walking_count = 1
        GOSUB MotionWalkingLeftDoor
    ELSEIF rx_data = cMOTION_LINE_MOVE_RIGHT THEN
        walking_count = 1
        GOSUB MotionWalkingRightDoor
    ELSEIF rx_data = cMOTION_LINE_TURN_LEFT_SMALL THEN
        walking_count = 1
        GOSUB MotionTurnLeftDoor
    ELSEIF rx_data = cMOTION_LINE_TURN_RIGHT_SMALL THEN
        walking_count = 1
        GOSUB MotionTurnRightDoor
    ENDIF

    GOTO StateLinetracingToArrow

StateArrowRecognitionInit:
    ETX 4800, cSIGNAL_STATE

    SPEED 8
    MOVE G6B, 150,  30,  80
    MOVE G6C, 150,  30,  80
    WAIT

    GOSUB PostureDefault

    walking_count = 2
    GOSUB MotionWalkingFront

    head_angle = 110
    GOSUB PostureHeadDown


StateArrowRecognition:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    walking_count = 5
    GOSUB MotionWalkingFront

    IF rx_data = cMOTION_ARROW_UNKNOWN THEN
        'walking_count = 1
        'GOSUB MotionWalkingBack
        'GOTO StateArrowRecognition
    ELSEIF rx_data = cMOTION_ARROW_LEFT THEN
        clockwise = 1
        walking_count = 2
        GOSUB MotionTurnLeftBig
    ELSEIF rx_data = cMOTION_ARROW_RIGHT THEN
        clockwise = 0
        walking_count = 2
        GOSUB MotionTurnRightBig
    ENDIF

    GOTO StateLinetracingToCornerInit

StateLinetracingToCornerInit:
    ETX 4800, cSIGNAL_STATE
    mission_count = mission_count + 1

    head_angle = 100
    GOSUB PostureHeadTurn

    head_angle = 30
    GOSUB PostureHeadDown

    IF mission_count >= 4 THEN
        GOTO StateLinetracingToCrossInit
    ENDIF

    walking_count = 3
    GOSUB MotionWalkingFront

StateLinetracingToCorner:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_LINE_STOP THEN
        head_angle = 100
        GOSUB PostureHeadDown
        walking_count = 4
        GOSUB MotionWalkingFront
        GOTO StateSectionRecognitionInit
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT THEN
        walking_count = 2
        GOSUB MotionWalkingFront
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT_SMALL THEN
        walking_count = 1
        GOSUB MotionWalkingFront
    ELSEIF rx_data = cMOTION_LINE_MOVE_LEFT THEN
        walking_count = 2
        GOSUB MotionWalkingLeft
    ELSEIF rx_data = cMOTION_LINE_MOVE_RIGHT THEN
        walking_count = 2
        GOSUB MotionWalkingRight
    ELSEIF rx_data = cMOTION_LINE_TURN_LEFT_SMALL THEN
        walking_count = 1
        GOSUB MotionTurnLeft
    ELSEIF rx_data = cMOTION_LINE_TURN_RIGHT_SMALL THEN
        walking_count = 1
        GOSUB MotionTurnRight
    ENDIF

    GOTO StateLinetracingToCorner

StateSectionRecognitionInit:
    ETX 4800, cSIGNAL_STATE

StateSectionRecognition:
    head_angle = 70
    GOSUB PostureHeadDown
    IF clockwise = 1 THEN
        head_angle = 45
    ELSE
        head_angle = 145
    ENDIF
    GOSUB PostureHeadTurn

    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_SECTION_SAFE THEN
        section_type = 1
        PRINT "SND 4 !"
    ELSEIF rx_data = cMOTION_SECTION_DANGER THEN
        section_type = 0
        PRINT "SND 5 !"
    ENDIF

    head_angle = 90
    GOSUB PostureHeadDown
    FOR i = 0 TO 2
        head_angle = 10 * i + 90
        GOSUB PostureHeadTurn

        ETX 4800, cSIGNAL_IMAGE
        GOSUB UartRx
    NEXT i

    IF section_type = 1 THEN
        GOTO StateSafeSectionFindMilkInit
    ELSE
        GOTO StateDangerSectionFindMilkInit
    ENDIF

StateSafeSectionFindMilkInit:
    ETX 4800, cSIGNAL_STATE
    head_angle = 100
    GOSUB PostureHeadTurn

    head_angle = 60
    GOSUB PostureHeadDown

StateSafeSectionFindMilk:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    section_turn = 0
    IF rx_data = cMOTION_MILK_FOUND THEN
        GOTO StateSafeSectionCatchMilkInit
    ELSE
        walking_count = 2
        section_turn = 1
        IF clockwise = 1 THEN
            GOSUB MotionTurnLeftBig
        ELSE
            GOSUB MotionTurnRightBig
        ENDIF

        ETX 4800, cSIGNAL_IMAGE
        GOSUB UartRx

        IF rx_data = cMOTION_MILK_FOUND THEN
            GOTO StateSafeSectionCatchMilkInit
        ELSE
            walking_count = 4
            GOSUB MotionTurnLeftBig
            GOTO StateLinetracingToCornerInit
        ENDIF
    ENDIF

StateSafeSectionCatchMilkInit:
    ETX 4800, cSIGNAL_STATE

StateSafeSectionCatchMilk:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRX

    IF rx_data = cMOTION_MILK_NOT_FOUND THEN
        IF head_angle = 60 THEN
            head_angle = 30
            GOSUB PostureHeadDown
            walking_count = 3
            GOSUB MotionWalkingFront
        ELSE
            GOTO StateSafeSectionPutMilkInit
        ENDIF
    ELSEIF rx_data = cMOTION_MILK_MOVE_FRONT THEN
        IF head_angle = 60 THEN
            walking_count = 3
        ELSE
            walking_count = 1
        ENDIF
        GOSUB MotionWalkingFront
    ELSEIF rx_data = cMOTION_MILK_MOVE_LEFT THEN
        walking_count = 1
        IF head_angle = 60 THEN
            GOSUB MotionWalkingLeftBig
        ELSE
            GOSUB MotionWalkingLeft
        ENDIF
    ELSEIF rx_data = cMOTION_MILK_MOVE_RIGHT THEN
        walking_count = 1
        IF head_angle = 60 THEN
            GOSUB MotionWalkingRightBig
        ELSE
            GOSUB MotionWalkingRight
        ENDIF
    ENDIF

    GOTO StateSafeSectionCatchMilk

StateSafeSectionPutMilkInit:
    ETX 4800, cSIGNAL_STATE
    walking_count = 1
    GOSUB MotionWalkingFront
    GOSUB MotionCatchMilk
    GOSUB PostureMilkLow

    head_angle = 100
    GOSUB PostureHeadTurn

    head_angle = 65
    GOSUB PostureHeadDown


StateSafeSectionPutMilk:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF head_angle = 65 THEN
        IF rx_data = cMOTION_MILK_IN_SECTION THEN
            head_angle = 24
            GOSUB PostureHeadDown
            GOSUB PostureMilkHigh
        ELSE
            walking_count = 1
            temp = clockwise XOR section_turn
            IF temp = 1 THEN
                GOSUB MotionTurnLeftWithMilk
            ELSE
                GOSUB MotionTurnRightWithMilk
            ENDIF
            GOSUB PostureMilkLow
        ENDIF
    ELSE
        IF rx_data = cMOTION_MILK_IN_SECTION THEN
            walking_count = 2
            GOSUB MotionWalkingFrontWithMilk
            GOSUB MotionPutMilk
            GOTO StateComebackFromSafeInit
        ELSE
            walking_count = 2
            GOSUB MotionWalkingFrontWithMilk
        ENDIF
    ENDIF

    GOTO StateSafeSectionPutMilk

StateComebackFromSafeInit:
    ETX 4800, cSIGNAL_STATE

    IF temp = 1 THEN
        walking_count = 3
        GOSUB MotionWalkingRightBig
        walking_count = 2
        GOSUB MotionTurnLeftBig
    ELSE
        walking_count = 3
        GOSUB MotionWalkingLeftBig
        walking_count = 2
        GOSUB MotionTurnRightBig
    ENDIF

    head_angle = 100
    GOSUB PostureHeadTurn

    head_angle = 30
    GOSUB PostureHeadDown

StateComebackFromSafe:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_LINE_STOP THEN
        IF section_turn = 1 THEN
            walking_count = 6
            GOSUB MotionWalkingFront
            IF clockwise = 1 THEN
                GOSUB MotionWalkingRightBig
            ELSE
                GOSUB MotionWalkingLeftBig
            ENDIF
            walking_count = 6
            GOSUB MotionWalkingFront
        ELSEIF clockwise = 1 THEN
            walking_count = 8
            GOSUB MotionWalkingFront
            walking_count = 2
            GOSUB MotionTurnLeftBig
            walking_count = 5
            GOSUB MotionWalkingFront
        ELSE
            walking_count = 8
            GOSUB MotionWalkingFront
            walking_count = 2
            GOSUB MotionTurnRightBig
            walking_count = 5
            GOSUB MotionWalkingFront
        ENDIF

        GOTO StateLinetracingToCornerInit
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT THEN
        walking_count = 2
        GOSUB MotionWalkingFront
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT_SMALL THEN
        walking_count = 1
        GOSUB MotionWalkingFront
    ELSEIF rx_data = cMOTION_LINE_MOVE_LEFT THEN
        walking_count = 1
        GOSUB MotionWalkingLeft
    ELSEIF rx_data = cMOTION_LINE_MOVE_RIGHT THEN
        walking_count = 1
        GOSUB MotionWalkingRight
    ELSEIF rx_data = cMOTION_LINE_TURN_LEFT_SMALL THEN
        walking_count = 1
        GOSUB MotionTurnLeft
    ELSEIF rx_data = cMOTION_LINE_TURN_RIGHT_SMALL THEN
        walking_count = 1
        GOSUB MotionTurnRight
    ENDIF

    GOTO StateComebackFromSafe

StateDangerSectionFindMilkInit:
    ETX 4800, cSIGNAL_STATE
    walking_count = 1
    IF clockwise = 1 THEN
        GOSUB MotionTurnLeftBig
    ELSE
        GOSUB MotionTurnRightBig
    ENDIF

    head_angle = 65
    GOSUB PostureHeadDown

    head_angle = 85
    GOSUB PostureHeadTurn

StateDangerSectionFindMilk:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_MILK_NOT_FOUND THEN
        IF head_angle = 85 THEN
            head_angle = 115
            GOSUB PostureHeadTurn
            GOTO StateDangerSectionFindMilk
        ELSE
            walking_count = 3
            IF clockwise = 1 THEN
                GOSUB MotionTurnRightBig
            ELSE
                GOSUB MotionTurnLeftBig
            ENDIF
            GOTO StateLinetracingToCornerInit
        ENDIF
    ELSE
        GOTO StateDangerSectionCatchMilkInit
    ENDIF

StateDangerSectionCatchMilkInit:
    ETX 4800, cSIGNAL_STATE
    walking_count = 1
    IF head_angle = 85 THEN
        GOSUB MotionWalkingLeftBig
    ELSE
        GOSUB MotionWalkingRightBig
    ENDIF

    head_angle = 100
    GOSUB PostureHeadTurn

    head_angle = 60
    GOSUB PostureHeadDown

StateDangerSectionCatchMilk:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_MILK_NOT_FOUND THEN
        IF head_angle = 60 THEN
            head_angle = 30
            GOSUB PostureHeadDown
            walking_count = 3
            GOSUB MotionWalkingFront
        ELSE
            GOTO StateDangerSectionPutMilkInit
        ENDIF
    ELSEIF rx_data = cMOTION_MILK_MOVE_FRONT THEN
        IF head_angle = 60 THEN
            walking_count = 2
        ELSE
            walking_count = 1
        ENDIF
        GOSUB MotionWalkingFront
    ELSEIF rx_data = cMOTION_MILK_MOVE_LEFT THEN
        walking_count = 1
        IF head_angle = 60 THEN
            GOSUB MotionWalkingLeftBig
        ELSE
            GOSUB MotionWalkingLeft
        ENDIF
    ELSEIF rx_data = cMOTION_MILK_MOVE_RIGHT THEN
        walking_count = 1
        IF head_angle = 60 THEN
            GOSUB MotionWalkingRightBig
        ELSE
            GOSUB MotionWalkingRight
        ENDIF
    ENDIF

    GOTO StateDangerSectionCatchMilk

StateDangerSectionPutMilkInit:
    ETX 4800, cSIGNAL_STATE
    GOSUB MotionCatchMilk

    head_angle = 100
    GOSUB PostureHeadTurn

    head_angle = 24
    GOSUB PostureHeadDown

    walking_count = 1
    GOSUB MotionWalkingFrontWithMilk

    walking_count = 5
    IF clockwise = 1 THEN
        GOSUB MotionTurnLeftWithMilk
    ELSE
        GOSUB MotionTurnRightWithMilk
    ENDIF
    GOSUB PostureMilkHigh

StateDangerSectionPutMilk:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_MILK_OUT_SECTION THEN
        walking_count = 2
        GOSUB MotionWalkingFrontWithMilk
        GOSUB MotionPutMilk
        GOTO StateComebackFromDangerInit
    ELSE
        walking_count = 2
        GOSUB MotionWalkingFrontWithMilk
    ENDIF

    GOTO StateDangerSectionPutMilk

StateComebackFromDangerInit:
    ETX 4800, cSIGNAL_STATE
    IF clockwise = 1 THEN
        walking_count = 3
        GOSUB MotionWalkingRightBig
        walking_count = 2
        GOSUB MotionTurnLeftBig
    ELSE
        walking_count = 3
        GOSUB MotionWalkingLeftBig
        walking_count = 2
        GOSUB MotionTurnRightBig
    ENDIF

    head_angle = 100
    GOSUB PostureHeadTurn

    head_angle = 30
    GOSUB PostureHeadDown

StateComebackFromDanger:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_LINE_STOP THEN
        walking_count = 5
        GOSUB MotionWalkingFront
        walking_count = 3
        IF clockwise = 1 THEN
            GOSUB MotionWalkingRightBig
        ELSE
            GOSUB MotionWalkingLeftBig
        ENDIF
        walking_count = 5
        GOSUB MotionWalkingFront
        GOTO StateLinetracingToCornerInit
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT THEN
        walking_count = 2
        GOSUB MotionWalkingFront
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT_SMALL THEN
        walking_count = 1
        GOSUB MotionWalkingFront
    ELSEIF rx_data = cMOTION_LINE_MOVE_LEFT THEN
        walking_count = 2
        GOSUB MotionWalkingLeft
    ELSEIF rx_data = cMOTION_LINE_MOVE_RIGHT THEN
        walking_count = 2
        GOSUB MotionWalkingRight
    ELSEIF rx_data = cMOTION_LINE_TURN_LEFT_SMALL THEN
        walking_count = 1
        GOSUB MotionTurnLeft
    ELSEIF rx_data = cMOTION_LINE_TURN_RIGHT_SMALL THEN
        walking_count = 1
        GOSUB MotionTurnRight
    ENDIF

    GOTO StateComebackFromDanger

StateLinetracingToCrossInit:
    ETX 4800, cSIGNAL_STATE

    head_angle = 100
    GOSUB PostureHeadTurn

    head_angle = 30
    GOSUB PostureHeadDown

    walking_count = 2
    GOSUB MotionWalkingFront

StateLinetracingToCross:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_LINE_STOP THEN
        GOTO StateLinetracingToGoalInit
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT THEN
        walking_count = 2
        GOSUB MotionWalkingFront
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT_SMALL THEN
        walking_count = 1
        GOSUB MotionWalkingFront
    ELSEIF rx_data = cMOTION_LINE_MOVE_LEFT THEN
        walking_count = 2
        GOSUB MotionWalkingLeft
    ELSEIF rx_data = cMOTION_LINE_MOVE_RIGHT THEN
        walking_count = 2
        GOSUB MotionWalkingRight
    ELSEIF rx_data = cMOTION_LINE_TURN_LEFT_SMALL THEN
        walking_count = 1
        GOSUB MotionTurnLeft
    ELSEIF rx_data = cMOTION_LINE_TURN_RIGHT_SMALL THEN
        walking_count = 1
        GOSUB MotionTurnRight
    ENDIF

    GOTO StateLinetracingToCross

StateLinetracingToGoalInit:
    ETX 4800, cSIGNAL_STATE

    walking_count = 2
    GOSUB MotionWalkingFront

    IF clockwise = 1 THEN
        GOSUB MotionTurnLeftBig
    ELSE
        GOSUB MotionTurnRightBig
    ENDIF

    GOSUB MotionWalkingFront
    GOSUB PostureDoor

StateLinetracingToGoal:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_LINE_LOST THEN
        GOTO StateSpeakSectionNameInit
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT THEN
        walking_count = 2
        GOSUB MotionWalkingFrontDoor
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT_SMALL THEN
        walking_count = 1
        GOSUB MotionWalkingFrontDoor
    ELSEIF rx_data = cMOTION_LINE_MOVE_LEFT THEN
        walking_count = 1
        GOSUB MotionWalkingLeftDoor
    ELSEIF rx_data = cMOTION_LINE_MOVE_RIGHT THEN
        walking_count = 1
        GOSUB MotionWalkingRightDoor
    ELSEIF rx_data = cMOTION_LINE_TURN_LEFT_SMALL THEN
        walking_count = 1
        GOSUB MotionTurnLeftDoor
    ELSEIF rx_data = cMOTION_LINE_TURN_RIGHT_SMALL THEN
        walking_count = 1
        GOSUB MotionTurnRightDoor
    ENDIF

    GOTO StateLinetracingToGoal

StateSpeakSectionNameInit:
    ETX 4800, cSIGNAL_STATE

    PRINT "OPEN M_ABCD.mrs !"
    PRINT "VOLUME 200 !"

StateSpeakSectionName:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_SECTION_UNKNOWN THEN
        STOP
    ELSEIF rx_data = cMOTION_SECTION_A THEN
        PRINT "SND 0 !"
    ELSEIF rx_data = cMOTION_SECTION_B THEN
        PRINT "SND 1 !"
    ELSEIF rx_data = cMOTION_SECTION_C THEN
        PRINT "SND 2 !"
    ELSEIF rx_data = cMOTION_SECTION_D THEN
        PRINT "SND 3 !"
    ENDIF

	DELAY 200

    GOTO StateSpeakSectionName
    '********** State End **********'


    '********** Main Begin **********'
Main:
    GOSUB Initiate
    GOSUB UartConnectWait
    GOTO StateDirectionRecognition
    '********** Main End **********'

ErrorOccurred:
    GOSUB SoundError
    STOP