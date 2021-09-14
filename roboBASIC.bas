CONST cHEAD_SPEED = 6
CONST cIR_SENSOR_PORT = 4

'********** protocol value begin **********'
CONST cSIGNAL_CHECK = &H40
CONST cSIGNAL_IMAGE = &H41
CONST cSIGNAL_STATE = &H42

CONST cMOTION_LINE_MOVE_FRONT = &H80
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
'********** protocol value end **********'

DIM rx_data AS BYTE
DIM ir_data AS INTEGER
DIM walking_speed AS INTEGER
DIM walking_count AS INTEGER

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

PostureHeadLeft10:
    SPEED cHEAD_SPEED
    SERVO 11, 90
    WAIT
    RETURN

PostureHeadRight10:
    SPEED cHEAD_SPEED
    SERVO 11, 110
    WAIT
    RETURN

PostureHeadDown30:
    SPEED cHEAD_SPEED
    SERVO 16, 35
    WAIT
    RETURN

PostureHeadDown80:
    SPEED cHEAD_SPEED
    SERVO 16, 80
    WAIT
    RETURN
    '********** Posture Setting End **********'


    '********** Motion Begin **********'
MotionOpenDoor:
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

    PRINT "VOLUME 200 !"
    PRINT "SND 12 !"
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
    GOSUB PostureHeadDown80
    GOSUB PostureHeadLeft30
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_DIRECTION_UNKNOWN OR rx_data = cMOTION_DIRECTION_DOOR THEN
        GOSUB PostureHeadRight30
        DELAY 300
        ETX 4800, cSIGNAL_IMAGE
        GOSUB UartRx
    ENDIF

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

    ETX 4800, cSIGNAL_STATE
    GOTO StateLineTracingToDoor

StateLineTracingToDoor:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx
    IF rx_data = cMOTION_LINE_LOST THEN
        GOSUB MotionOpenDoor
        MUSIC "GFEDC"
        STOP 'temp fin'
    ENDIF

    GOTO StateLineTracingToDoor

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