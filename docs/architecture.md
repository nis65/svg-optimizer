# Architecture

See also the [Style Guide](./style-guide.md)

## Separation of concern

* the core data structure is the *internal representation*. This representation is close to the `.svg` structure, focuses on the geometric aspects but still carries enough information to generate a valid `.svg` file that renders the same picture as the original input file.
* the **parser** converts an `.svg` file into this *internal representation*. 
   * For the `<path>` tag, this representation uses **absolute** coordinates and only the basic path element type (i.e. the same `LineTo` object is used to represent a `L`, `H` or `V` path element). The original element representation letter is stored along the geometric data. This allows to use (and convert the coordinates accordingly) when writing back that representation to an `.svg` file.
* a **semantic** function interprets that *internal representation* and builds the global bounding box by combining all bounding boxes of the individual elements.
* the **writer** creates an `.svg` file from the *internal representation*. There are two degrees of freedom that that change only the `.svg` representation, but not the rendered image. These can be specified via parameters:
   * the representation of geometric affine **transformations** in the `.svg` file. See [transform_writer](/src/svgtools/writer/transform_writer.py) for details.
   * the representation of the contents of the `d` attribute in a **path** tag. See [path_writer](/src/svgtools/writer/path_writer.py) for details.

## Internal geometric representation

The representation is split in two parts:

* The **geometry** part of the model represents the mathematical geometry. Its objects have a geometric extent and can participate in geometric computations.
* The **svg** part of the model represents the hierarchical composition. Its objects organize, reference or group geometry and are mostly linked to svg tags. One notable exception: Drawable objects are modelled as `Shape` objects where their `geometry` only defines whether it is e.g. a circle or rect.

Note that packages (i.e. directories) group types by responsibility, not by inheritance.

### Geometry

* Supported geometry objects
   * Drawables: Circle, Ellipse, Line, Path, Polygon, Polyline, Rect 
   * Transformations: Matrix3, TRHxSDecomposition
   * Helpers: BoundingBox, Point
* Numeric value objects provide exact equality (`==`) and approximate comparison via `isclose()`. Approximate comparison follows the semantics of `math.isclose()`. The tolerances for `isclose` are defined "globally", see below.
* Use [3x3 matrices](https://en.wikipedia.org/wiki/Homogeneous_coordinates) to describe transformations like *scale* or *rotate* so that applying multiple transformations is equivalent to (non-commutative) matrix multiplication.
* The 3x3 matrix is interpreted to be row-major, a point is therefore a column vector.
* The library uses column vectors and **left matrix multiplication**. Therefore, the product A * B represents the composition *first apply B, then apply A*, **(A * B) * p == A * (B * p)**. This follows the standard convention from linear algebra.
* Drawable objects inherit from an abstract base class `Geometry` that enforces that each drawable object has a function `points_for_bounding_box`. Drawable objects whose bounding box is fully defined by some discrete points (like a *Rect* or a *Polyline*), return just those points. "Smooth" objects like a *Circle* or a path *Bezier*-Element, are sampled. The number of points per sampled object (or path element) is defined by `GEOMETRY_NUMBER_OF_SAMPLES` in [tolerance.py](/src/svgtools/geometry/tolerance.py). The more samples, the more exact the bounding box is calculated, but the more cpu time is used for computing the bounding box. The other two constants in this file are `GEOMETRY_REL_TOL` and `GEOMETRY_ABS_TOL`. The latter is important when float numbers are near zero, see the python doc of [math.isclose](https://docs.python.org/3/library/math.html#math.isclose) for more details.
* The initial motivation for this project was to rearrange an existing `.svg` picture so that the *bounding box* of the object is horizontally and vertically *centered* and the *minimal distance* from the bounding box to the edges of the canvas can be parametrized. This is demonstrated in [adjust_viewbox.py](/examples/adjust_viewbox.py).

### Svg

Svg objects do **not** introduce new geometry by themselves; instead, they describe how geometry is specified (e.g. a circle is defined by its center and a radius) and organized (e.g. a circle can be defined and then redrawn using the definition label) more or less in the same way a `.svg` file does.

The toplevel element is a `Document` that lies outside of the `.svg` content. The one and only child object is `Svg`.  Currently, `Svg` is only considered legal as the outmost Element of an `.svg` file (i.e. nested `svg` tags are not supported yet). An `Svg` object has 0 to n children and these can be:

* nestable (i.e. can have children too): `Defs`, `Group`
* terminal (i.e. does not have children): `Shape`, `Use`

`Shape` elements have a `geometry`, only this geometry actually identifies the geometric (a.k.a. "drawable") object, see above.

## SVG parsing and writing

The objects defined above allow to support only very basic `.svg` files. Especially,

* only the standard namespace `http://www.w3.org/2000/svg` at the toplevel is supported, no changing namespaces within the `.svg`.
* only a very limited set of svg tags is supported:
   * `svg` (at the toplevel only), 
   * `defs`, `g`, `use` (organizational)
   * `circle`, `ellipse`, `line`, `path`, `polygon`, `polyline ` and `rect` (drawable)
* all geometric transformations (on all tags above except `defs`) are supported: `translate`, `scale`, `rotate`, `skewX`, `skewY`, `matrix`

## Preserving structure

The parser/writer combo preserve document structure as far as possible. The following changes are applied when writing unconditionally:
* the indendetation is "fixed" to reflect the structural depth
* number lists are written space separated (and not comma separated)
* the attributes (not the children) of an xml tag are (re-) ordered as follows:
   * `xmlns` (only on `svg` element)
   * `id`
   * `href`
   * geometry of drawable objects, e.g. `x`, `y`, `width`, `heigth`, `r`
   * coordinate system, e.g. `width`, `height` and `viewBox` (on toplevel `svg` element)
   * transformations like  `scale` and `translate`
   * "unknown attributes" like `fill`, `stroke`
* the way that elements in a `<path>` are compacted is not stored in the internal model, but you can control the output. The internal model does not make a distinction between `L 10 100 20 200` and `L 10 100 L 20 200`, it stores the latter representation only.

## Optimizing transformations

The writer has 6 modes to optimize the transformations
* `KEEP`: transformations are written exactly as read by the parser
* `AGGREGATE`: if a certain transformation is followed by the same type, the two adjacent ones are merged into one, as long as this is possible in an exact way from the `.svg` parameters.
   * Translations can be merged by addition
   * Scales can be merged by multiplication
   * Rotates can be merged as long as they have the same rotation center
   * SkewX and SkewY **cannot** be merged in an exact way, as this would involve `tan` and `atan`
   * Affine matrices can be merged via matrix multiplication
* `DECOMPOSE_MATRIX`: Any `matrix` occurred is decomposed into **TRHxS**, i.e. a Translate, Rotate (around 0), SkewX and Scale. This allows to have a more visual idea of an arbitrary transformation matrix in the original `.svg`
* `DECOMPOSE_MATRIX_AND_AGGREGATE`: Do first a decompose and then an aggregation.
* `CANONICAL_CONSERVATIVE and CANONICAL_AGGRESSIVE`: The canonical representation of an arbitrary sequence of transformations is considered to be (reading from right to left) a Scaling, followed by a SkewX, followed by Rotation and finally a Translation. The first option first attempts an AGGREGATE and if this already produces an TRHxS order, it is left like this and if not, all transformations are first multiplied and then the resulting matrix is decomposed. Both should deliver the same list of tranformations, but CONSERVATIVE minimizes the risk of numerical edge cases (e.g. 0.999 instead of 1). After a CONSERVATIVE write, you can ask the writer object for stats: how many transform lists could be handled by aggregation and how many needed a matrix decomposition.

## Optimizing path rendering

There are three independent options to choose from to render a `<path>`:
* **PathCoordinates**: Are all coordinates rendered as `ABSOLUTE` (all uppercase "commands") or `RELATIVE` (all lowercase "commands") coordinates? The option `KEEP` keeps the setting from the input file.
* **PathCommandSet**: Some commands have more than one representation, e.g. a *LineTo* can be represented by an `L`, `H` or `V`. The `BASE` command set does not use `H`/`V`, `T` and `S`, but replaces them by the more basic `L`, `Q` and `S` command respectively.
* **PathCompactness**: The `CANONICAL` rendering has each path command followed by exactly one set of parameters. The `COMPACT` rendering converts e.g. `L 10 20 L 30 40` into `L 10 20 30 40`.
