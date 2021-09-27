from abc import *
import line_tracing
import direction_recognition
import arrow_recognition
import room_recognition
from const_variables import const


class RobotStateBase(metaclass=ABCMeta):
    @abstractmethod
    def operation(self, source_image):
        pass

    @abstractmethod
    def state_change(self):
        pass


class DirectionRecognition(RobotStateBase):
    def __init__(self):
        self.tf_model = direction_recognition.DirectionRecognition()
        self.predict_count = 0
        self.predict_value = (0, 0)

    def __str__(self):
        return "Direction Recognition"

    def operation(self, source_image):
        predict_label, predict_accuracy = self.tf_model.predict(source_image)
        if 1 <= predict_label <= 4 and predict_accuracy > self.predict_value[1]:
            self.predict_value = predict_label, predict_accuracy
        self.predict_count += 1
        if self.predict_count < 4:
            return const.MOTION_DIRECTION_UNKNOWN
        else:
            return const.MOTION_DIRECTION_UNKNOWN + self.predict_value[0]

    def state_change(self):
        return LineTracingToDoor()


class LineTracingToDoor(RobotStateBase):
    def __init__(self):
        self.line_tracing = line_tracing.LineTracing()

    def __str__(self):
        return "LineTracing to Door"

    def operation(self, source_image):
        return self.line_tracing.select_line_motion(self.line_tracing.detect_line(source_image))

    def state_change(self):
        return FindCross()


class FindCross(RobotStateBase):
    def __init__(self):
        self.line_tracing = line_tracing.LineTracing()

    def __str__(self):
        return "Find Cross"

    def operation(self, source_image):
        return self.line_tracing.select_corner_motion(self.line_tracing.detect_line(source_image))

    def state_change(self):
        return ArrowRecognition()


class ArrowRecognition(RobotStateBase):
    def __init__(self):
        self.arrow_recognition = arrow_recognition.ArrowRecognition()

    def __str__(self):
        return "Arrow Recognition"

    def operation(self, source_image):
        return self.arrow_recognition.arrow_recognition(source_image)

    def state_change(self):
        return LineTracingToCorner()


class LineTracingToCorner(RobotStateBase):
    def __init__(self):
        self.line_tracing = line_tracing.LineTracing()

    def __str__(self):
        return "LineTracing to Corner"

    def operation(self, source_image):
        return self.line_tracing.select_corner_motion(self.line_tracing.detect_line(source_image))

    def state_change(self):
        return RoomRecognition()


class RoomRecognition(RobotStateBase):
    def __init__(self):
        self.room_recognition = room_recognition.RoomRecognition()

    def __str__(self):
        return "Room Recognition"

    def operation(self, source_image):
        pass

    def state_change(self):
        pass


class RobotStateController:
    def __init__(self):
        self.state = DirectionRecognition()

    def __str__(self):
        return f"now state : {self.state.__str__()}"

    def operation(self, source_image):
        return self.state.operation(source_image)

    def state_change(self):
        self.state = self.state.state_change()
