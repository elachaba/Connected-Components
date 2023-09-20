#!/usr/bin/env python3

"""
This module takes a file that contains
a set of points with a minimum threshold
as input and returns the number of the connected
components between these points.
"""

from sys import argv
from geo.point import Point


def load_instance(filename):
    """
    Retrieves the data from the file 'filename'
    """
    with open(filename, "r", encoding='UTF-8') as instance_file:
        lines = iter(instance_file)
        distance = float(next(lines))
        points = [Point([float(f) for f in l.split(",")]) for l in lines]
    return distance, points


def coord_cell(point, distance):
    """
    Given a point and distance,
    calculates the coordinates of the cell that the point belongs to in the grid.
    """
    abscisse = int(point.coordinates[0] // distance)
    ordonnee = int(point.coordinates[1] // distance)
    return abscisse, ordonnee


def build_grid(distance, points):
    """
    Constructs the grid data structure
    by putting points into their corresponding cells.
    """
    grid = {}
    for idx, point in enumerate(points):
        cell = coord_cell(point, distance)
        if cell not in grid:
            grid[cell] = set()
        grid[cell].add(idx)
    return grid


def find(parents, point):
    """
    Given a point and the list of parents,
    returns the parent of the point.
    This is an implematation of the find method in the 
    union-find structure.
    """
    if parents[point] != point:
        parents[point] = find(parents, parents[point])
    return parents[point]


def union(parents, ranks, point_1, point_2):
    """
    Given two points and the parents list, merges the connected
    components of the two points.
    This implelements the union method of tyhe union-find structure.
    """
    parent_point_1 = find(parents, point_1)
    parent_point_2 = find(parents, point_2)

    if parent_point_1 == parent_point_2:
        return

    if ranks[parent_point_1] < ranks[parent_point_2]:
        parents[parent_point_1] = parent_point_2
    elif ranks[parent_point_1] > ranks[parent_point_2]:
        parents[parent_point_2] = parent_point_1
    else:
        parents[parent_point_2] = parent_point_1
        ranks[parent_point_1] += 1


def implement_union_find(distance, points):
    """
    Given the list of points and the distance threshold,
    constructs and returns the Union-Find data structure
    to efficiently find connected components among the points
    based on the specified distance.
    """
    parents = list(range(len(points)))
    ranks = [0] * len(points)
    grid = build_grid(distance, points)

    for cell, point_indexes in grid.items():
        adj_cells = [
            (cell[0] + dx, cell[1] + dy) for dx in range(-1, 2)
            for dy in range(-1, 2)
        ]

        for idx in point_indexes:
            for adj_cell in adj_cells:
                if adj_cell in grid:
                    for j in grid[adj_cell]:
                        if idx != j and points[idx].distance_to(points[j]) <= distance:
                            union(parents, ranks, idx, j)

    return parents


def print_components_sizes(distance, points):
    """
    Given the list of points and the distance threshold,
    returns the list of the size of the connected components.
    """
    parents = implement_union_find(distance, points)
    components = {}

    for idx in range(len(points)):
        root = find(parents, idx)
        if root not in components:
            components[root] = 0
        components[root] += 1

    component_sizes = sorted(components.values(), reverse=True)
    print(component_sizes)

def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)

if __name__ == '__main__':
    main()
