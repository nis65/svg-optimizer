# svgtools

A lightweight library for geometric svg processing

## Motivation

Initially, I just wanted to optimize a simple `.svg` logo so that the object (geometrically: the bounding box of the object) is nicely centered and "just right" in size, i.e. there is some space between the bounding box and the edge of the canvas, but not too much, not too little.

It turned out that this is a very nice python exercise. As I am not experienced python coder (yet), I used AI to train myself. I did not use an agent, so every line of code has been written by myself. How should I learn when an agent does the work?

## Design Goals

* SVG parser to build an internal python representation from an svg file
* SVG writer to output the internal representation to an svg file
* Immutable geometry objects
* Exact bounding box computation
* Minimal dependencies
* Modern python
* Test driven development

## Other documentation

* see the [architecture](docs/architecture.md) and the [style-guide](docs/style-guide.md) documents to understand **how** we wanto develop
* see the [roadmap](docs/roadmap.md) to see **when** we want to develop **what**.

## Current status

This project is under active development. The API is not considered stable.
