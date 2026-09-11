from .defs import Defs
from .group import Group
from .preserved_subtree import PreservedSubtree
from .shape import Shape
from .use import Use

type SvgNestables = Defs | Group | Shape | Use

type SvgChildren = SvgNestables | PreservedSubtree
