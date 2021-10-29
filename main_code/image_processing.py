from abc import *
import numpy as np
import line_tracing
import direction_recognition
import arrow_recognition
import section_recognition
import section_mission
from const_variables import const


class RobotStateBase(metaclass=ABCMeta):
    def __init__(self, next_state):
        self.next_state = next_state

    @abstractmethod
    def operation(self, source_image):
        pass

    @abstractmethod
    def state_change(self):
        pass


class DirectionRecognition(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.tf_model = direction_recognition.DirectionRecognition()
        self.predict_count = 0
        self.predict_value = np.zeros(6)

    def __str__(self):
        return "Direction Recognition"

    def operation(self, source_image):
        self.predict_value += self.tf_model.predict(source_image)
        self.predict_count += 1
        if self.predict_count < 4:
            return const.MOTION_DIRECTION_UNKNOWN
        else:
            label = np.argmax(self.predict_value[1:5])
            self.predict_count = 0
            self.predict_value = np.zeros(6)
            return const.MOTION_DIRECTION_EAST + label

    def state_change(self):
        return self.next_state


class LineTracingToArrow(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.line_tracing = line_tracing.LineTracing()

    def __str__(self):
        return "Line Tracing to Arrow"

    def operation(self, source_image):
        return self.line_tracing.select_cross_motion(
            self.line_tracing.detect_line(self.line_tracing.skeletonization(source_image)))

    def state_change(self):
        return self.next_state


class ArrowRecognition(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.arrow_recognition = arrow_recognition.ArrowRecognition()

    def __str__(self):
        return "Arrow Recognition"

    def operation(self, source_image):
        return self.arrow_recognition.arrow_recognition(source_image)

    def state_change(self):
        return self.next_state


class LineTracingToCorner(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.line_tracing = line_tracing.LineTracing()
        self.mission_count = 0

    def __str__(self):
        return "LineTracing to Corner"

    def operation(self, source_image):
        return self.line_tracing.select_corner_motion(
            self.line_tracing.detect_line(self.line_tracing.skeletonization(source_image)))

    def state_change(self):
        self.mission_count += 1
        if self.mission_count <= 3:
            self.next_state[0].init()
            return self.next_state[0]
        else:
            return self.next_state[1]


class SectionRecognition(RobotStateBase):
    def __init__(self, next_state, controller):
        super().__init__(next_state)
        self.section_recognition = section_recognition.SectionRecognition()
        self.controller = controller
        self.predict_count = -1
        self.predict_value = np.zeros(5)
        self.section_type = None
        self.color = {"RED": 0, "BLUE": 0, "": 0}

    def __str__(self):
        return "Section Recognition"

    def init(self):
        self.predict_count = -1
        self.predict_value = np.zeros(5)
        self.section_type = None
        self.color = {"RED": 0, "BLUE": 0, "": 0}

    def operation(self, source_image):
        self.predict_count += 1

        if self.predict_count == 0:
            self.section_type = self.section_recognition.check_section_type(source_image)
            return self.section_type

        predict = self.section_recognition.predict(source_image)
        self.predict_value += predict[0]
        self.color[predict[1]] += 1

        if self.predict_count < 3:
            return const.MOTION_SECTION_UNKNOWN
        else:
            section_name = np.argmax(self.predict_value[:4]) + const.MOTION_SECTION_A
            if self.section_type == const.MOTION_SECTION_DANGER:
                self.controller.section_name.append(section_name)
            return section_name

    def state_change(self):
        next_state = self.next_state[0 if self.section_type == const.MOTION_SECTION_SAFE else 1]
        next_state.set_section_color("RED" if self.color["RED"] > self.color["BLUE"] else "BLUE")
        return next_state


class SafeSectionFind(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.safe_section_find = section_mission.SectionFind("SAFE")
        self.ret_val = None

    def __str__(self):
        return f"find the {self.safe_section_find.section_color} milk carton outside Safe Section"

    def set_next_state(self, next_state):
        self.next_state = next_state

    def set_section_color(self, color):
        self.safe_section_find.set_section_color(color)
        self.next_state[1].set_section_color(color)

    def operation(self, source_image):
        self.ret_val = self.safe_section_find.find_milk_carton(source_image)
        return self.ret_val

    def state_change(self):
        return self.next_state[0 if self.ret_val == const.MOTION_MILK_NOT_FOUND else 1]


class DangerSectionFind(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.danger_section_find = section_mission.SectionFind("DANGER")
        self.ret_val = None

    def __str__(self):
        return f"find the {self.danger_section_find.section_color} milk carton inside Danger Section"

    def set_next_state(self, next_state):
        self.next_state = next_state

    def set_section_color(self, color):
        self.danger_section_find.set_section_color(color)
        self.next_state[1].set_section_color(color)

    def operation(self, source_image):
        self.ret_val = self.danger_section_find.find_milk_carton(source_image)
        return self.ret_val

    def state_change(self):
        return self.next_state[0 if self.ret_val == const.MOTION_MILK_NOT_FOUND else 1]


class SafeSectionCatch(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.safe_section_catch = section_mission.SectionCatch("SAFE")

    def __str__(self):
        return f"catch the {self.safe_section_catch.section_color} milk carton outside Safe Section"

    def set_section_color(self, color):
        self.safe_section_catch.set_section_color(color)

    def operation(self, source_image):
        return self.safe_section_catch.select_motion(source_image)

    def state_change(self):
        self.next_state.line_tracing.init()
        return self.next_state


class DangerSectionCatch(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.danger_section_catch = section_mission.SectionCatch("DANGER")

    def __str__(self):
        return f"catch the {self.danger_section_catch.section_color} milk carton inside Danger Section"

    def set_section_color(self, color):
        self.danger_section_catch.set_section_color(color)

    def operation(self, source_image):
        return self.danger_section_catch.select_motion(source_image)

    def state_change(self):
        self.next_state.line_tracing.init()
        return self.next_state


class SafeSectionPut(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.line_tracing = line_tracing.LineTracing(height_size=const.HEIGHT_SIZE - 40,
                                                     width_size=const.WIDTH_SIZE - 20)

    def __str__(self):
        return "put the milk carton inside Safe Section"

    def operation(self, source_image):
        return self.line_tracing.select_section_motion(
            self.line_tracing.detect_line(self.line_tracing.detect_outline(source_image[:-40, 10:-10], "SAFE")))

    def state_change(self):
        self.next_state.line_tracing.init()
        return self.next_state


class DangerSectionPut(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.line_tracing = line_tracing.LineTracing(height_size=const.HEIGHT_SIZE - 80,
                                                     width_size=const.WIDTH_SIZE - 20)

    def __str__(self):
        return "put the milk carton outside Danger Section"

    def operation(self, source_image):
        return self.line_tracing.select_section_motion(
            self.line_tracing.detect_line(self.line_tracing.detect_outline(source_image[20:-60, 10:-10], "DANGER")))

    def state_change(self):
        self.next_state.line_tracing.init()
        return self.next_state


class SafeSectionComeback(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.line_tracing = line_tracing.LineTracing(height_size=const.HEIGHT_SIZE - 60)

    def __str__(self):
        return "comeback from Safe Section to Line"

    def operation(self, source_image):
        return self.line_tracing.select_corner_motion(
            self.line_tracing.detect_line(self.line_tracing.detect_outline(source_image[20:-40], "SAFE")))

    def set_next_state(self, next_state):
        self.next_state = next_state

    def state_change(self):
        self.next_state.line_tracing.init()
        return self.next_state


class DangerSectionComeback(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.line_tracing = line_tracing.LineTracing(height_size=const.HEIGHT_SIZE - 40)

    def __str__(self):
        return "comeback from Danger Section to Line"

    def operation(self, source_image):
        return self.line_tracing.select_corner_motion(
            self.line_tracing.detect_line(self.line_tracing.detect_outline(source_image[:-40], "DANGER")))

    def set_next_state(self, next_state):
        self.next_state = next_state

    def state_change(self):
        self.next_state.line_tracing.init()
        return self.next_state


class LineTracingToCross(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.line_tracing = line_tracing.LineTracing()

    def __str__(self):
        return "Line Tracing to Last Cross"

    def operation(self, source_image):
        return self.line_tracing.select_cross_motion(
            self.line_tracing.detect_line(self.line_tracing.skeletonization(source_image)))

    def state_change(self):
        return self.next_state


class LineTracingToGoal(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.line_tracing = line_tracing.LineTracing()

    def __str__(self):
        return "Line Tracing to Last Goal"

    def operation(self, source_image):
        return self.line_tracing.select_line_motion(
            self.line_tracing.detect_line(self.line_tracing.skeletonization(source_image)))

    def state_change(self):
        return self.next_state


class SpeakSectionName(RobotStateBase):
    def __init__(self, next_state, controller):
        super().__init__(next_state)
        self.controller = controller
        self.index = 0

    def __str__(self):
        return "Speak Section Name"

    def operation(self, source_image):
        print(self.controller.section_name)
        if self.index >= len(self.controller.section_name):
            return const.MOTION_SECTION_UNKNOWN
        section_name = self.controller.section_name[self.index]
        self.index += 1
        return section_name

    def state_change(self):
        return self.next_state


class RobotStateController:
    def __init__(self):
        self.speak_section_name = SpeakSectionName(None, self)
        self.line_tracing_to_goal = LineTracingToGoal(self.speak_section_name)
        self.line_tracing_to_cross = LineTracingToCross(self.line_tracing_to_goal)
        self.danger_section_comeback = DangerSectionComeback(None)
        self.safe_section_comeback = SafeSectionComeback(None)
        self.danger_section_put = DangerSectionPut(self.danger_section_comeback)
        self.safe_section_put = SafeSectionPut(self.safe_section_comeback)
        self.danger_section_catch = DangerSectionCatch(self.danger_section_put)
        self.safe_section_catch = SafeSectionCatch(self.safe_section_put)
        self.danger_section_find = DangerSectionFind(None)
        self.safe_section_find = SafeSectionFind(None)
        self.section_recognition = SectionRecognition([self.safe_section_find, self.danger_section_find], self)
        self.line_tracing_to_corner = LineTracingToCorner([self.section_recognition, self.line_tracing_to_cross])
        self.arrow_recognition = ArrowRecognition(self.line_tracing_to_corner)
        self.line_tracing_to_arrow = LineTracingToArrow(self.arrow_recognition)

        self.danger_section_comeback.set_next_state(self.line_tracing_to_corner)
        self.safe_section_comeback.set_next_state(self.line_tracing_to_corner)
        self.danger_section_find.set_next_state([self.line_tracing_to_corner, self.danger_section_catch])
        self.safe_section_find.set_next_state([self.line_tracing_to_corner, self.safe_section_catch])

        self.state = DirectionRecognition(self.line_tracing_to_arrow)
        self.section_name = []

    def __str__(self):
        return f"now state : {self.state.__str__()}"

    def operation(self, source_image):
        return self.state.operation(source_image)

    def state_change(self):
        self.state = self.state.state_change()
