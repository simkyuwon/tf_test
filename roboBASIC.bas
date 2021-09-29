CONST cHEAD_SPEED = 7
CONST cIR_SENSOR_PORT = 4

'********** protocol value begin **********'
CONST cSIGNAL_CHECK = &H40
CONST cSIGNAL_IMAGE = &H41
CONST cSIGNAL_STATE = &H42

CONST cMOTION_LINE_MOVE_FRONT = &H80
CONST cMOTION_LINE_MOVE_BACK = &H81
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
'********** protocol value end **********'

DIM i AS BYTE
DIM rx_data AS BYTE
DIM ir_data AS INTEGER
DIM walking_speed1 AS BYTE
DIM walking_speed2 AS BYTE
DIM walking_count AS INTEGER
DIM head_angle AS BYTE

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


PostureDoor:
    MOVE G6A, 100,  76, 145,  93, 100, 100
    MOVE G6D, 100,  76, 145,  93, 100, 100
    WAIT
    RETURN

PostureHeadCenter:
    SPEED cHEAD_SPEED
    SERVO 11, 100
    DELAY 500
    RETURN

PostureHeadTurn:
    SPEED cHEAD_SPEED
    SERVO 11, head_angle
    DELAY 500
    RETURN

PostureHeadDown:
    SPEED cHEAD_SPEED
    SERVO 16, head_angle
    DELAY 500
    RETURN
    '********** Posture Setting End **********'


    '********** Motion Begin **********'
MotionWalkingFront:
    GOSUB MotorLegMode3
    walking_speed1 = 13
    walking_speed2 = 4
    FOR i = 1 TO walking_count
        SPEED walking_speed2
        MOVE G6A,  88,  74, 144,  95, 110
        MOVE G6D, 108,  76, 146,  93,  96
        MOVE G6B, 100
        MOVE G6C, 100
        WAIT

        SPEED walking_speed1
        MOVE G6A,  90,  90, 120, 105, 110, 100
        MOVE G6D, 110,  76, 147,  93,  96, 100
        MOVE G6B,  90
        MOVE G6C, 110
        WAIT

        SPEED walking_speed1
        MOVE G6A,  86,  56, 145, 115, 110
        MOVE G6D, 108,  76, 147,  93,  96
        WAIT

        SPEED walking_speed2
        MOVE G6A, 110,  76, 147,  93,  96, 100
        MOVE G6D,  86, 100, 145,  69, 110, 100
        WAIT

        SPEED walking_speed1
        MOVE G6A, 110,  76, 147,  93,  96, 100
        MOVE G6D,  90,  90, 120, 105, 110, 100
        MOVE G6B, 110
        MOVE G6C,  90
        WAIT

        MOVE G6D,  86,  56, 145, 115, 110
        MOVE G6A, 108,  76, 147,  93,  96
        WAIT

        SPEED walking_speed2
        MOVE G6D, 110,  76, 147,  93,  96
        MOVE G6A,  86, 100, 145,  69, 110
        WAIT

        SPEED walking_speed1
        MOVE G6A,  90,  90, 120, 105, 110, 100
        MOVE G6D, 110,  76, 146,  93,  96, 100
        MOVE G6B,  90
        MOVE G6C, 110
        WAIT
    NEXT i

    SPEED 2
    GOSUB PostureDefault
    RETURN

MotionWalkingRight:
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
        GOSUB PostureDefault
    NEXT i
    GOSUB MotorAllMode3
    RETURN

MotionWalkingLeft:
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
        GOSUB PostureDefault
    NEXT i
    GOSUB MotorAllMode3
    RETURN

MotionTurnRight:
    MOTORMODE G6A, 3, 3, 3, 3, 2
    MOTORMODE G6D, 3, 3, 3, 3, 2
    FOR i = 1 TO walking_count
        SPEED 8
        MOVE G6D,  93,  96, 145,  73, 105, 100
        MOVE G6A,  95,  56, 145, 113, 105, 100
        MOVE G6B,  90
        MOVE G6C, 110
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
    GOSUB PostureDefault
    RETURN

MotionTurnLeft:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    FOR i = 1 TO walking_count
        SPEED 8
        MOVE G6D,  95,  56, 145, 113, 105, 100
        MOVE G6A,  93,  96, 145,  73, 105, 100
        MOVE G6C,  90
        MOVE G6B, 110
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
    GOSUB PostureDefault
    RETURN

MotionWalkingFrontDoor:
    GOSUB MotorLegMode3
    walking_speed1 = 13
    walking_speed2 = 3
	
    FOR i = 1 TO walking_count
        SPEED walking_speed2
        MOVE G6A,  88,  74, 143,  96, 110
        MOVE G6D, 108,  76, 145,  94,  96
        WAIT

        SPEED walking_speed1
        MOVE G6A,  90,  90, 120, 105, 110, 100
        MOVE G6D, 110,  76, 147,  93,  96, 100
        WAIT

        MOVE G6A,  86,  56, 145, 115, 110
        MOVE G6D, 108,  76, 147,  93,  96
        WAIT

        SPEED walking_speed2
        MOVE G6A, 110,  76, 146,  94,  96, 100
        MOVE G6D,  86, 100, 144,  70, 110, 100
        WAIT

        SPEED walking_speed1
        MOVE G6A, 110,  76, 147,  93,  96, 100
        MOVE G6D,  90,  90, 120, 105, 110, 100
        WAIT

        MOVE G6A, 108,  76, 147,  93,  96
        MOVE G6D,  86,  56, 145, 115, 110
        WAIT

        SPEED walking_speed2
        MOVE G6A,  86, 100, 144,  70, 110
        MOVE G6D, 110,  76, 146,  94,  96
        WAIT

        SPEED walking_speed1
        MOVE G6A,  90,  90, 120, 105, 110, 100
        MOVE G6D, 110,  76, 146,  93,  96, 100
        WAIT
    NEXT i
    
    SPEED 2
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
        MOVE G6B,  90
        MOVE G6C, 110
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
        MOVE G6C,  90
        MOVE G6B, 110
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
    walking_count = 1
    GOSUB MotionWalkingFront
        
    SPEED 8
    MOVE G6B, 180,  20,  50
	MOVE G6C, 180,  20,  50
	WAIT
	
    MOVE G6B, 180,  20,  75
	MOVE G6C, 180,  20,  75
	WAIT
    
    walking_count = 2
    GOSUB MotionWalkingFrontDoor
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

    GOTO StateLinetracingToDoorInit

StateLinetracingToDoorInit:
    ETX 4800, cSIGNAL_STATE

    GOSUB PostureHeadCenter
    
    head_angle = 30
    GOSUB PostureHeadDown

StateLinetracingToDoor:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_LINE_LOST THEN
        GOTO StateFindCrossInit
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT THEN
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

    GOTO StateLinetracingToDoor


StateFindCrossInit:
    ETX 4800, cSIGNAL_STATE
    
    MUSIC "EDCDEEE"
    GOSUB MotionOpenDoor

StateFindCross:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_LINE_STOP THEN
        GOTO StateArrowRecognitionInit
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT THEN
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

    GOTO StateFindCross
    
StateArrowRecognitionInit:
    ETX 4800, cSIGNAL_STATE
    
    
    SPEED 8
    MOVE G6B, 150,  30,  80
	MOVE G6C, 150,  30,  80
	WAIT
	
	GOSUB PostureDefault
    
	head_angle = 110
	GOSUB PostureHeadDown

StateArrowRecognition:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_ARROW_UNKNOWN THEN
    	'walking_count = 1
    	'GOSUB MotionWalkingBack
    	'GOTO StateArrowRecognition
    ELSEIF rx_data = cMOTION_ARROW_LEFT THEN
		walking_count = 3
		GOSUB MotionWalkingFront
	    
        walking_count = 4
        GOSUB MotionTurnLeft
    ELSEIF rx_data = cMOTION_ARROW_RIGHT THEN
		walking_count = 3
		GOSUB MotionWalkingFront
    
        walking_count = 4
        GOSUB MotionTurnRight
    ENDIF
    
    GOTO StateLinetracingToCornerInit

StateLinetracingToCornerInit:
    ETX 4800, cSIGNAL_STATE

    head_angle = 30
    GOSUB PostureHeadDown
    
    walking_count = 2
    GOSUB MotionWalkingFront

StateLinetracingToCorner:
    ETX 4800, cSIGNAL_IMAGE
    GOSUB UartRx

    IF rx_data = cMOTION_LINE_STOP THEN
	    head_angle = 100
	    GOSUB PostureHeadDown
        walking_count = 2
        GOSUB MotionWalkingFront
        MUSIC "CFCFCF"
        DELAY 1000
        GOTO Main
    ELSEIF rx_data = cMOTION_LINE_MOVE_FRONT THEN
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