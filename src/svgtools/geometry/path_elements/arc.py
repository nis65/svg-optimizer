import math
from dataclasses import dataclass
from typing import ClassVar

from ..point import Point
from .path_element_abc import PathElement


@dataclass(frozen=True, slots=True)
class Arc(PathElement):
    parameter_counts: ClassVar[dict[str, int]] = {
        "A": 7,
        "a": 7,
    }

    rx: float
    ry: float
    phi: float
    large_arc_flag: int
    sweep_flag: int
    # sweep_flag 0: svg negative (counterclockwise)
    # sweep_flag 1: svg positive (clockwise)
    end: Point
    representation: str

    def __post_init__(self) -> None:
        if not self.representation in {"a", "A"}:
            raise ValueError(
                f"Arc can only be represented by one of 'aA', not {self.representation}"
            )

    @property
    def endpoint(self) -> Point:
        return self.end

    @staticmethod
    def _point_at(  # noqa: PLR0913 PLR0917
        center: Point,
        lrx: float,
        lry: float,
        theta_start: float,
        delta_theta: float,
        cos_rphi: float,
        sin_rphi: float,
        t: float,
    ) -> Point:

        cos_param_phi = math.cos(theta_start + t * delta_theta)
        sin_param_phi = math.sin(theta_start + t * delta_theta)

        rx_cos_param_phi = lrx * cos_param_phi
        ry_sin_param_phi = lry * sin_param_phi

        new_x = center.x + rx_cos_param_phi * cos_rphi - ry_sin_param_phi * sin_rphi
        new_y = center.y + rx_cos_param_phi * sin_rphi + ry_sin_param_phi * cos_rphi

        return Point(x=new_x, y=new_y)

    def points_for_bounding_box(self, start: Point, count: int) -> set[Point]:  # noqa: PLR0914

        rphi = math.radians(self.phi)
        cos_rphi = math.cos(rphi)
        sin_rphi = math.sin(rphi)

        transformed_point = Point(
            x=cos_rphi * (start.x - self.end.x) / 2
            + sin_rphi * (start.y - self.end.y) / 2,
            y=-sin_rphi * (start.x - self.end.x) / 2
            + cos_rphi * (start.y - self.end.y) / 2,
        )

        if self.large_arc_flag == self.sweep_flag:
            sign = -1
        else:
            sign = 1

        # special case if radii are too short, makes expression for squareroot positive
        check_lambda = (transformed_point.x * transformed_point.x) / (
            self.rx * self.rx
        ) + (transformed_point.y * transformed_point.y) / (self.ry * self.ry)
        if check_lambda > 1:
            sqrt_lambda = math.sqrt(check_lambda)
            lrx = self.rx * sqrt_lambda
            lry = self.ry * sqrt_lambda
        else:
            lrx = self.rx
            lry = self.ry
        squareroot = math.sqrt(
            (
                lrx * lrx * lry * lry
                - lrx * lrx * transformed_point.y * transformed_point.y
                - lry * lry * transformed_point.x * transformed_point.x
            )
            / (
                lrx * lrx * transformed_point.y * transformed_point.y
                + lry * lry * transformed_point.x * transformed_point.x
            )
        )
        transformed_center = Point(
            x=sign * squareroot * lrx * transformed_point.y / lry,
            y=-sign * squareroot * lry * transformed_point.x / lrx,
        )
        center = Point(
            x=cos_rphi * transformed_center.x
            - sin_rphi * transformed_center.y
            + (start.x + self.end.x) / 2,
            y=sin_rphi * transformed_center.x
            + cos_rphi * transformed_center.y
            + (start.y + self.end.y) / 2,
        )

        transformed_start = Point(
            x=(cos_rphi * (start.x - center.x) + sin_rphi * (start.y - center.y)) / lrx,
            y=(-sin_rphi * (start.x - center.x) + cos_rphi * (start.y - center.y))
            / lry,
        )
        transformed_end = Point(
            x=(cos_rphi * (self.end.x - center.x) + sin_rphi * (self.end.y - center.y))
            / lrx,
            y=(-sin_rphi * (self.end.x - center.x) + cos_rphi * (self.end.y - center.y))
            / lry,
        )

        theta_start = math.atan2(transformed_start.y, transformed_start.x)
        delta_theta = math.atan2(
            transformed_start.x * transformed_end.y
            - transformed_start.y * transformed_end.x,
            transformed_start.x * transformed_end.x
            + transformed_start.y * transformed_end.y,
        )

        if self.sweep_flag == 0 and delta_theta > 0:
            delta_theta -= 2 * math.pi
        if self.sweep_flag == 1 and delta_theta < 0:
            delta_theta += 2 * math.pi

        points = []
        for i in range(count + 1):
            t = i / count
            points.append(
                self._point_at(
                    center, lrx, lry, theta_start, delta_theta, cos_rphi, sin_rphi, t
                )
            )
        return set(points)
