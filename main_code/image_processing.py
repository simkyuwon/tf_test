from abc import *
import numpy as np
import line_tracing
import direction_recognition
import arrow_recognition
import section_recognition
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


class LineTracingToDoor(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.line_tracing = line_tracing.LineTracing()

    def __str__(self):
        return "LineTracing to Door"

    def operation(self, source_image):
        return self.line_tracing.select_line_motion(self.line_tracing.detect_line(source_image))

    def state_change(self):
        return self.next_state


class FindCross(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)
        self.line_tracing = line_tracing.LineTracing()

    def __str__(self):
        return "Find Cross"

    def operation(self, source_image):
        return self.line_tracing.select_cross_motion(self.line_tracing.detect_line(source_image))

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

    def __str__(self):
        return "LineTracing to Corner"

    def operation(self, source_image):
        return self.line_tracing.select_corner_motion(self.line_tracing.detect_line(source_image))

    def state_change(self):
        return self.next_state


class SectionRecognition(RobotStateBase):
    def __init__(self, next_state, controller):
        super().__init__(next_state)
        self.section_recognition = section_recognition.SectionRecognition()
        self.controller = controller
        self.predict_count = -1
        self.predict_value = np.zeros(5)
        self.color = {"RED": 0, "BLUE": 0, "NOT FOUND": 0}
        self.section_type = None

    def __str__(self):
        return "Section Recognition"

    def operation(self, source_image):
        self.predict_count += 1

        if self.predict_count == 0:
            self.section_type = self.section_recognition.check_section_type(source_image)
            return self.section_type

        self.predict_value += self.section_recognition.predict(source_image)
        if self.predict_count < 4:
            self.color[self.section_recognition.check_section_color(source_image)] += 1
            return const.MOTION_SECTION_UNKNOWN
        else:
            label = np.argmax(self.predict_value[:4])
            self.controller.section_name.append(label)
            self.predict_count = 0
            self.predict_value = np.zeros(5)
            if self.color["RED"] > self.color["BLUE"]:
                print("RED")
            else:
                print("BLUE")
            return const.MOTION_SECTION_A + label

    def state_change(self):
        if self.section_type == const.MOTION_SECTION_SAFE:
            return self.next_state[0]
        else:
            return self.next_state[1]


class SafeSection(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)

    def __str__(self):
        return "Safe Section"

    def operation(self, source_image):
        pass

    def state_change(self):
        pass


class DangerSection(RobotStateBase):
    def __init__(self, next_state):
        super().__init__(next_state)

    def __str__(self):
        return "Danger Section"

    def operation(self, source_image):
        pass

    def state_change(self):
        pass


class RobotStateController:
    def __init__(self):
        self.danger_section = None
        self.safe_section = None
        self.section_recognition = SectionRecognition([self.safe_section, self.danger_section], self)
        self.line_tracing_to_corner = LineTracingToCorner(self.section_recognition)
        self.arrow_recognition = ArrowRecognition(self.line_tracing_to_corner)
        self.find_cross = FindCross(self.arrow_recognition)
        self.line_tracing_to_door = LineTracingToDoor(self.find_cross)
        self.state = DirectionRecognition(self.line_tracing_to_door)

        self.section_name = []

    def __str__(self):
        return f"now state : {self.state.__str__()}"

    def operation(self, source_image):
        return self.state.operation(source_image)

    def state_change(self):
        self.state = self.state.state_change()
