# This file is automatically generated by pyo3_stub_gen
# ruff: noqa: E501, F401

import typing
import pathlib

class Anchor:
    r"""
    An `Anchor` is a reference point for a given [`Curve`].
    It can be a milestone, a bridge…
    """
    name: str
    position: typing.Optional[Point]
    curve_position: float
    scale_position: float

class AnchorOnLrm:
    r"""
    The linear position of an anchor doesn’t always match the measured distance
    For example if a road was transformed into a bypass, resulting in a longer road,
    but measurements are kept the same
    The start of the curve might also be different from the `0` of the LRM
    """
    anchor_index:int
    distance_along_lrm:float
    def __new__(cls,anchor_index:int, distance_along_lrm:float): ...
    ...

class Builder:
    def __new__(cls,): ...
    def add_node(self, id:str, coord:Point, properties:typing.Mapping[str, str]) -> int:
        r"""
        Add a new topological node (e.g. a railway switch)
        """
        ...

    def add_anchor(self, id:str, coord:Point, properties:typing.Mapping[str, str], name:typing.Optional[str]) -> int:
        r"""
        Add a new anchor by its cooordinates
        """
        ...

    def add_projected_anchor(self, id:str, position_on_curve:float, properties:typing.Mapping[str, str], name:typing.Optional[str]) -> int:
        r"""
        Add a new anchor by its position along the curve
        """
        ...

    def add_segment(self, id:str, geometry:typing.Sequence[Point], start_node_index:int, end_node_index:int) -> int:
        r"""
        Add a new segment
        
        The geometry represents the curve
        start_node_index and end_node_index are the topological extremeties returned by `add_node`
        """
        ...

    def add_traversal(self, traversal_id:str, segments:typing.Sequence[SegmentOfTraversal]) -> None:
        r"""
        Add a traversal
        
        segments represent the curve of the traversal
        """
        ...

    def add_lrm(self, id:str, traversal_index:int, anchors:typing.Sequence[AnchorOnLrm], properties:typing.Mapping[str, str]) -> None:
        r"""
        Add a linear referencing model
        
        It is composed by the traversal identified by traversa_index (that represents the curve)
        and the anchors (that represent the milestones)
        """
        ...

    def get_traversal_indexes(self) -> dict[str, int]:
        r"""
        List all the traversals by their id and index
        """
        ...

    def read_from_osm(self, input_osm_file:pathlib.Path, lrm_tag:str, required:typing.Sequence[tuple[str, str]], to_reject:typing.Sequence[tuple[str, str]]) -> None:
        r"""
        Read the topology from an OpenStreetMap source
        
        It reads the nodes, segments and traversals.
        """
        ...

    def save(self, out_file:pathlib.Path, properties:typing.Mapping[str, str]) -> None:
        r"""
        Save the lrs to a file
        """
        ...

    def euclidean_distance(self, lrm_index_a:int, lrm_index_b:int) -> float:
        r"""
        Compute the euclidean distance between two lrms
        """
        ...

    def get_nodes_of_traversal(self, lrm_index:int) -> list[int]:
        r"""
        List all the node indices of a traversal
        """
        ...

    def get_node_coord(self, node_index:int) -> Point:
        r"""
        Get the coordinates of a node identified by its index
        """
        ...

    def project(self, lrm_index:int, point:Point) -> typing.Optional[float]:
        r"""
        Project a point on a the curve of an lrm
        
        Return a value between 0 and 1, both included
        Return None if the curve of the traversal is not defined
        """
        ...

    def reverse(self, lrm_index:int) -> None:
        r"""
        Reverse the orientation of the lrm
        
        If it is composed by the segments (a, b)-(b, c) it will be (c, b)-(b, a)
        """
        ...


class LrmScaleMeasure:
    r"""
    Represent a position on an [`LrmScale`] relative as an `offset` to an [`Anchor`].
    """
    anchor_name: str
    scale_offset: float
    def __new__(cls,anchor_name:str, scale_offset:float): ...

class Lrs:
    r"""
    Holds the whole Linear Referencing System.
    """
    def __new__(cls,data:bytes): ...
    def lrm_len(self) -> int:
        r"""
        How many LRMs compose the LRS.
        """
        ...

    def get_lrm_geom(self, index:int) -> list[Point]:
        r"""
        Return the geometry of the LRM.
        """
        ...

    def get_lrm_scale_id(self, index:int) -> str:
        r"""
         `id` of the [`LrmScale`].
        """
        ...

    def get_anchors(self, lrm_index:int) -> list[Anchor]:
        r"""
        All the [`Anchor`]s of a LRM.
        """
        ...

    def resolve(self, lrm_index:int, measure:LrmScaleMeasure) -> Point:
        r"""
        Get the position given a [`LrmScaleMeasure`].
        """
        ...

    def locate_point(self, lrm_index:int, measure:LrmScaleMeasure) -> float:
        r"""
        Get the positon along the curve given a [`LrmScaleMeasure`]
        The value will be between 0.0 and 1.0, both included
        """
        ...

    def resolve_range(self, lrm_index:int, from:LrmScaleMeasure, to:LrmScaleMeasure) -> list[Point]:
        r"""
        Given two [`LrmScaleMeasure`]s, return a range of [`Point`] that represent a line string.
        """
        ...

    def find_lrm(self, lrm_id:str) -> typing.Optional[int]:
        r"""
        Given a ID returns the corresponding lrs index (or None if not found)
        """
        ...


class Point:
    r"""
    A geographical [`Point`], it can be either a projected or spherical coordinates.
    """
    x: float
    y: float
    def __new__(cls,x:float, y:float): ...

class SegmentOfTraversal:
    r"""
    A traversal is composed by segments
    """
    segment_index:int
    reversed:bool
    def __new__(cls,segment_index:int, reversed:bool): ...
    ...

