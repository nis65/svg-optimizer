# Architecture

See also the [Style Guide](./style-guide.md)

## Separation of concern

* simple internal representation of a vector image consisting of multiple potentially reused and transformed objects. Basic geometric forms supported are currently rectangles and circles only.
* the task of the svg parsing and writer functions is to convert between the internal svg representation and the svg file format.

## Internal geometric representation

The representation is split in two parts:

* The **geometry** part of the model represents the mathematical geometry. Its objects have a geometric extent and can participate in geometric computations.
* The **svg** part of the model represents the hierarchical composition. Its objects organize, reference or group geometry and are mostly linked to svg tags. One notable exception: Drawable shapes are `Shape` objects where the geometry only defines whether it is a circle or rect.

Note that packages (i.e. directories) group types by responsibility, not by inheritance.

### Geometry

* Examples for Geometry objects
   * Drawable objects: Circle, Rect
   * Transformations: Matrix3, TRHxSDecomposition
   * Helpers: Point, BoundingBox
* A point is the same as a vector.
* Numeric value objects provide exact equality (==) and approximate comparison via `isclose()`. Approximate comparison following the semantics of math.isclose().
* Use [3x3 matrices](https://en.wikipedia.org/wiki/Homogeneous_coordinates) to describe transformations like *scale* or *rotate* so that applying multiple transformations is equivalent to (non-commutative) matrix multiplication.
* The 3x3 matrix is interpreted to be row-major, a point is therefore a column vector.
* The library uses column vectors and **left matrix multiplication**. Therefore, the product A * B represents the composition *first apply B, then apply A*, **(A * B) * p == A * (B * p)**. This follows the standard convention from linear algebra.
* Drawable objects inherit from an abstract base class `Geometry` that enforces that each drawable Object has a function `points_for_bounding_box`. This function returns a set of `n` points that are part of the object when drawn. These can be used to determine the bounding box. A `Rect` ignores the parameter `n` and delivers always just the four points that determine the rect fully (under any affine transformation), the circle is currently requested to return 128 points for bounding box computation. This approach allows to apply the current transformation to each point and identify the most top, most bottom, most left and most right coordinate in a generic way.

* Currently, the ultimate goal is to rearrange an existing `.svg` picture so that the *bounding box* of the object is horizontally and vertically *centered* and the *minimal distance* from the bounding box to the edges of the canvas can be parametrized. Therefore, every geometric object needs to have `.bounding_box`.


### Svg

Svg objects do **not** introduce new geometry by themselves; instead, they describe how geometry is organized more or less in the same way a `.svg` file does.

The toplevel element is a `Document` that lies outside of the `.svg` content. The one and only child object is `Svg`.  Currently, `Svg` is only considered legal as the outmost Element of an `.svg` file (i.e. nested `svg` tags are not supported yet). An `Svg` object has 0 to n children and these can be:

* nestable (i.e. can have children too): `Defs`, `Group`
* terminal (i.e. does not have children): `Shape`, `Use`

`Shape` elements have a `geometry` that identifies them as `Circle` or `Rect` (see above).

## SVG parsing and writing

The Objects defined above allow to support only very basic `.svg` files. Especially,

* only the standard namespace `http://www.w3.org/2000/svg` at the toplevel is supported, no changing namespaces within the `.svg`.
* only the following svg tags are supported: `svg` (at the toplevel only), `defs`, `g`, `use`, `circle` and `rect`.
* all geometric transformations (on all tags above except `defs`) are supported: `translate`, `scale`, `rotate`, `skewX`, `skewY`, `matrix`

## Preserving structure

The parser/writer preserve document structure. The following changes are applied in any case:
* the indendetation is "fixed" to reflect the structural depth
* number lists are always written space separated (and not comma separated)
* the attributes (not the children) of an xml tag are ordered as follows:
   * `xmlns` (only on `svg` element)
   * `id`
   * `href`
   * geometry of drawable objects, e.g. `x`, `y`, `width`, `heigth`, `r`
   * coordinate system, e.g. `width`, `height` and `viewBox` (on toplevel `svg` element)
   * transformations like  `scale` and `translate`
   * "unknown attributes" like `fill`, `stroke`

## Optimizing transformations

The writer has 6 modes to optimize the transformations
* `KEEP`: transformations are written exactly as read with the parser
* `AGGREGATE`: if a certain transformation is followed by the same type, the two adjacent ones are merged into one, as long as this is possible in an exact way from the `.svg` parameters.
   * Translations can be merged by addition
   * Scales can be merged by multiplication
   * Rotates can be merged as long as they have the same rotation center
   * SkewX and SkewY **cannot** be merged in an exact way, as this would involve `tan` and `atan`
   * Affine matrix can be merged via matrix multiplication
* `DECOMPOSE_MATRIX`: Any `matrix` occurred is decomposed into **TRHxS**, i.e. a Translate, Rotate (around 0), SkewX and Scale. This allows to have a more visual idea of an arbitrary transformation matrix in the original `.svg`
* `DECOMPOSE_MATRIX_AND_AGGREGATE`: Do first a decompose and then an aggregation.
* `CANONICAL_CONSERVATIVE and CANONICAL_AGGRESSIVE`: The canonical representation of an arbitrary sequence of transformations is considered to be (reading from right to left) a Scaling, followed by a SkewX, followed by Rotation and finall a Translation. The first option first attempts an AGGREGATE and if this already produces an TRHxS order, it is left like this and if not, all transformations are first multiplied and then the resulting matrix is decomposed. Both should deliver the same list of tranformations, but CONSERVATIVE minimizes the risk of numerical edge cases (e.g. 0.999 instead of 1). After a CONSERVATIVE write, you can ask the writer object for stats: how many transform lists could be handled by aggregation and how many needed a matrix decomposition.
