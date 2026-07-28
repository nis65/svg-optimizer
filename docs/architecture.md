# Architecture

See also the [Style Guide](./style-guide.md)

## Separation of concern

* simple internal representation of a vector image consisting of multiple potentially reused and transformed objects. Basic geometric forms supported are currently rectangles and circles only.
* the task of the svg parsing and rendering functions is to convert between the internal geometric representation and the svg format.

## Internal geometric representation

The representation is split in two parts: 

* The **geometry** part of the model represents the mathematical geometry. Its objects have a geometric extent and can participate in geometric computations.
* The **scene** part of the model represents the hierarchical composition. Its objects organize, reference or group geometry.

Note that packages (i.e. directories) group types by responsibility, not by inheritance.

### Geometry

* Examples for Geometry objects
   * Point, Circle, Rect
   * Size, Matrix3, BoundingBox
* A point is the same as a vector.
* Use [3x3 matrices](https://en.wikipedia.org/wiki/Homogeneous_coordinates) to describe transformations like *scale* or *rotate* so that applying multiple transformations is equivalent to (non-commutative) matrix multiplication.
* The transformations we need are currently *translate* and *scale* only. Rotation could be added seamlessly later.
* Currently, the ultimate goal is to rearrange an existing `.svg` picture so that the *bounding box* of the object is horizontally and vertically *centered* and the *minimal distance* from the bounding box to the edges of the canvas can be parametrized. Therefore, every geometric object needs to have `.bounding_box`.

### Scene

Scene objects do **not** introduce new geometry by themselves; instead, they describe how geometry is organized. Examples are

* Document, Element
* Group, Defs, Use

Scene objects do **not** introduce new geometry by themselves; instead, they describe how geometry is organized.

## SVG parsing and rendering

To start with, we only support the svg tags that are needed for our example. This implicitly defines what objects geometric objects we need to define in the geometry.
* the generic xml header
* `svg`: the SVG header defining the width and height of the canvas and the viewBox to apply when rendering
* `defs`: used to define objects that can be referred to later
* `g`: grouping multiple objects into one named object
* `use`: referall to an object that is defined
* `circle`: A circle with a center and a radius
* `rect`: A rectangle with a width and a height
