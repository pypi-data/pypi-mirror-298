from typing import Iterable
import math


class Color:
    black = '\033[30m'
    dust = '\033[37m'
    base = '\033[97m'
    base_d = '\033[37m\033[1m'
    thick = '\033[1m'
    tilt = '\033[3m\033[1m'
    red = '\033[91m\033[1m'
    red_d = '\033[31m\033[1m'
    pink = '\033[95m\033[1m'
    pink_d = '\033[35m\033[1m'
    yellow = '\033[93m\033[1m'
    yellow_d = '\033[33m\033[1m'
    green = '\033[92m\033[1m'
    green_d = '\033[32m\033[1m'
    sky = '\033[96m\033[1m'
    sky_d = '\033[36m\033[1m'
    blue = '\033[94m\033[1m'
    blue_d = '\033[34m\033[1m'
    clear = '\033[0m'


class DPoint(tuple):
    def __new__(
            cls,
            *args,
            to: tuple[int, int] | None = None
    ):
        instance = super().__new__(cls, args)
        instance.args = args
        instance.to = to
        return instance

    def __eq__(self, other):
        return (
                isinstance(other, type(self)) and
                self.args == other.args and
                self.to == other.to
        )


class Box:

    def __init__(
            self,
            startpoint: DPoint[int, int] | tuple[int, int],
            text_iter: Iterable,
            text_color: str = Color.base,
            edge_color: str = Color.base,
            margins: int = 1
    ):
        self.startpoint = startpoint
        self.text_iter = text_iter
        self.text_color = text_color
        self.edge_color = edge_color
        self.margins = margins
        self.endpoint: tuple[DPoint, DPoint, DPoint, DPoint] | None = None

    def __eq__(self, other):
        return (
                isinstance(other, type(self)) and
                self.startpoint == other.startpoint and
                self.text_iter == other.text_iter
        )


class Line:

    def __init__(
            self,
            startpoint: DPoint[int, int, tuple[int, int]],
            line_len: int,
            endpoint_style: str = '·',
            color: str = Color.base,
            end_to: tuple[int, int] | None = None
    ):
        self.startpoint = startpoint
        self.line_len = line_len
        self.endpoint_style = endpoint_style
        self.color = color
        self.end_to = end_to
        self.endpoint: DPoint | None = None

    def __eq__(self, other):
        return (
                isinstance(other, type(self)) and
                self.startpoint == other.startpoint and
                self.line_len == other.line_len and
                self.end_to == other.end_to
        )


class Canvas:

    def __init__(self, width, height, unit=' '):
        self.width = width
        self.height = height
        self.space = [[unit for _ in range(self.width)] for _ in range(self.height)]

    def _draw_box(
            self,
            box: Box,
    ):
        x, y = box.startpoint[0], box.startpoint[1]
        text_iter = box.text_iter
        text_color = box.text_color
        edge_color = box.edge_color
        margins = box.margins

        text_iter = [f"{' ' * margins}{text}{' ' * margins}" for text in text_iter]
        max_len = max(len(text) for text in text_iter)
        count_text = len(text_iter)

        self.space[y][x] = f'{edge_color}+'
        self.space[y][x + max_len + 1] = f'+{Color.clear}'

        for i in range(1, max_len + 1):
            self.space[y][x + i] = '-'
            self.space[y + count_text + 1][x + i] = '-'

        self.space[y + count_text + 1][x] = f'{edge_color}+'
        self.space[y + count_text + 1][x + max_len + 1] = f'+{Color.clear}'

        for j, text in enumerate(text_iter):
            self.space[y + j + 1][x] = f'{edge_color}|{Color.clear}'
            self.space[y + j + 1][x + max_len + 1] = f'{edge_color}|{Color.clear}'
            for k, char in enumerate(text):
                self.space[y + j + 1][x + k + 1] = f'{text_color}{char}{Color.clear}'

        box.endpoint = (
            DPoint(
                round((x + x + max_len + 1) / 2),
                y,
                to=(0, -1)
            ),
            DPoint(
                round((x + x + max_len + 1) / 2),
                y + count_text + 1,
                to=(0, 1)
            ),
            DPoint(
                x,
                round((y + y + count_text + 1) / 2),
                to=(-1, 0)
            ),
            DPoint(
                x + max_len + 1,
                round((y + y + count_text + 1) / 2),
                to=(1, 0)
            ),
        )

        return box.endpoint

    def _draw_line(
            self,
            line: Line,
    ):
        x, y = line.startpoint[0], line.startpoint[1]
        to = line.startpoint.to
        line_len = line.line_len
        endpoint_style = line.endpoint_style
        color = line.color

        _x, _y = x, y
        match to:
            case (0, -1) | (0, 1):
                base_line = f"{'|' * line_len}{endpoint_style}"
            case (-1, 0) | (1, 0):
                base_line = f"{'-' * line_len}{endpoint_style}"
            case _:
                raise ValueError('line.startpoint.to should in [(0, -1), (0, 1), (-1, 0), (1, 0)]')
        for i, sub_line in enumerate(base_line):
            _x, _y = x + to[0] * (i + 1), y + to[1] * (i + 1)
            self.space[_y][_x] = f"{color}{sub_line}{Color.clear}"
        line.endpoint = DPoint(_x, _y, to=line.end_to)
        return line.endpoint

    @staticmethod
    def _point_match(point_tuple_1: tuple[DPoint, ...], point_tuple_2: tuple[DPoint, ...]):
        may_match = {}
        sign = 0
        for p1 in point_tuple_1:
            for p2 in point_tuple_2:
                _x1, _y1 = p1[0], p1[1]
                _to1 = p1.to
                _x2, _y2 = p2[0], p2[1]
                _to2 = p2.to
                _may_point = [(_x1, _y2), (_x2, _y1)]

                for _p in _may_point:
                    if (
                            (
                                    _p[0] - _x1,
                                    _p[1] - _y1
                            )
                            ==
                            (
                                    abs(_p[0] - _x1) * _to1[0],
                                    abs(_p[1] - _y1) * _to1[1]
                            )
                            and
                            (
                                    _p[0] - _x2,
                                    _p[1] - _y2
                            )
                            ==
                            (
                                    abs(_p[0] - _x2) * _to2[0],
                                    abs(_p[1] - _y2) * _to2[1]
                            )
                    ):
                        to_p_x = int((_x2 - _p[0]) / abs(_x2 - _p[0]) if abs(_x2 - _p[0]) != 0 else 0)
                        to_p_y = int((_y2 - _p[1]) / abs(_y2 - _p[1]) if abs(_y2 - _p[1]) != 0 else 0)
                        if (to_p_x, to_p_y) != (0, 0):
                            _mid_point = DPoint(_p[0], _p[1], to=(to_p_x, to_p_y))
                            may_match[(math.sqrt(((_x1 - _x2) ** 2 + (_y1 - _y2))), sign)] = (p1, _mid_point, p2)
                            sign += 1
        return [may_match[match_distance] for match_distance in sorted(may_match.keys())]

    @staticmethod
    def point_match(point_tuple_1: tuple[DPoint, ...], point_tuple_2: tuple[DPoint, ...]):
        return Canvas._point_match(point_tuple_1, point_tuple_2)

    def draw(self, obj: Box | Line):
        if isinstance(obj, Box):
            return self._draw_box(obj)
        elif isinstance(obj, Line):
            return self._draw_line(obj)

    def connect(
            self,
            start_point: DPoint,
            end_point: DPoint,
            color: str = Color.base,
            endpoint_style: str = '·'
    ):
        match_list = self._point_match(point_tuple_1=(start_point,), point_tuple_2=(end_point,))
        points = match_list[0]

        endpoint = None
        for index in range(len(points) - 1):
            start_p = points[index]
            end_p = points[index + 1]
            if start_p != end_p:
                if index == len(points) - 2:
                    line_len = int(abs((end_p[0] - start_p[0]) + (end_p[1] - start_p[1])) - 2)
                    line = Line(startpoint=start_p, line_len=line_len, endpoint_style=endpoint_style, color=color,
                                end_to=end_p.to)
                else:
                    line_len = int(abs((end_p[0] - start_p[0]) + (end_p[1] - start_p[1])) - 1)
                    line = Line(startpoint=start_p, line_len=line_len, color=color, end_to=end_p.to)
                endpoint = self._draw_line(line=line)
        return endpoint

    def render(self):
        for row in self.space:
            print("".join(row))
