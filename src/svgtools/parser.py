from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg

def parse_string(svg: str):
    return Document(
        svg=Svg(
            children=(),
        )
    )
