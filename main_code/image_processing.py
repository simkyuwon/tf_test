from abc import *
import line_tracing
import direction_recognition


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

    def __str__(self):
        return "Direction Recognition"

    def operation(self, source_image):
        return self.tf_model.predict(source_image)

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
