class ConstantVariable:
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise Exception('변수에 값을 할당할 수 없습니다.')
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise Exception('변수를 삭제할 수 없습니다.')


const = ConstantVariable()

const.BPS = 4800

const.HEIGHT_SIZE = 240
const.WIDTH_SIZE = 320
const.FPS = 30

const.RED_RANGE1 = [(0, 90, 50), (20, 255, 255)]
const.RED_RANGE2 = [(160, 90, 50), (180, 255, 255)]
const.GREEN_RANGE = [(50, 70, 50), (80, 255, 255)]
const.BLUE_RANGE = [(100, 60, 50), (120, 255, 255)]
const.WHITE_RANGE = [(0, 0, 120), (180, 60, 255)]
const.BLACK_RANGE = [(0, 0, 0), (180, 50, 60)]

const.SIGNAL_CHECK = 0x40
const.SIGNAL_IMAGE = 0x41
const.SIGNAL_STATE = 0x42

const.MOTION_LINE_MOVE_FRONT = 0x80
const.MOTION_LINE_MOVE_FRONT_SMALL = 0x81
const.MOTION_LINE_MOVE_LEFT = 0x82
const.MOTION_LINE_MOVE_RIGHT = 0x83
const.MOTION_LINE_TURN_LEFT_SMALL = 0x84
const.MOTION_LINE_TURN_RIGHT_SMALL = 0x85
const.MOTION_LINE_TURN_LEFT_BIG = 0x86
const.MOTION_LINE_TURN_RIGHT_BIG = 0x87
const.MOTION_LINE_LOST = 0x88
const.MOTION_LINE_STOP = 0x89

const.MOTION_DIRECTION_UNKNOWN = 0x90
const.MOTION_DIRECTION_EAST = 0x91
const.MOTION_DIRECTION_WEST = 0x92
const.MOTION_DIRECTION_SOUTH = 0x93
const.MOTION_DIRECTION_NORTH = 0x94
const.MOTION_DIRECTION_DOOR = 0x95

const.MOTION_ARROW_UNKNOWN = 0xA0
const.MOTION_ARROW_LEFT = 0xA1
const.MOTION_ARROW_RIGHT = 0xA2

const.MOTION_SECTION_UNKNOWN = 0xB0
const.MOTION_SECTION_A = 0xB1
const.MOTION_SECTION_B = 0xB2
const.MOTION_SECTION_C = 0xB3
const.MOTION_SECTION_D = 0xB4
const.MOTION_SECTION_SAFE = 0xB5
const.MOTION_SECTION_DANGER = 0xB6

const.MOTION_MILK_NOT_FOUND = 0xC0
const.MOTION_MILK_FOUND = 0xC1
const.MOTION_MILK_MOVE_FRONT = 0xC2
const.MOTION_MILK_MOVE_LEFT = 0xC3
const.MOTION_MILK_MOVE_RIGHT = 0xC4
const.MOTION_MILK_IN_SECTION = 0xC5
const.MOTION_MILK_OUT_SECTION = 0xC6
