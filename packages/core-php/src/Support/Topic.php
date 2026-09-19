<?php

declare(strict_types=1);

namespace NeetCode\Core\Support;

/** The eighteen NeetCode 150 topics, in roadmap order. */
enum Topic: string
{
    case ArraysAndHashing = 'arrays-and-hashing';
    case TwoPointers = 'two-pointers';
    case SlidingWindow = 'sliding-window';
    case Stack = 'stack';
    case BinarySearch = 'binary-search';
    case LinkedList = 'linked-list';
    case Trees = 'trees';
    case Tries = 'tries';
    case HeapPriorityQueue = 'heap-priority-queue';
    case Backtracking = 'backtracking';
    case Graphs = 'graphs';
    case AdvancedGraphs = 'advanced-graphs';
    case DynamicProgramming1D = '1d-dynamic-programming';
    case DynamicProgramming2D = '2d-dynamic-programming';
    case Greedy = 'greedy';
    case Intervals = 'intervals';
    case MathAndGeometry = 'math-and-geometry';
    case BitManipulation = 'bit-manipulation';
}
