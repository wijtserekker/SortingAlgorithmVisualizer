from list import List
import math


# =====================================================
# =============== SORTING ALGORITHMS ==================
# =====================================================

def bubble_sort(l: List):
    changed = True
    while changed:
        changed = False
        for i in range(0, len(l) - 1):
            if l[i] > l[i+1]:
                l.swap(i, i+1)
                changed = True


# =====================================================

def insertion_sort(l: List):
    for i in range(1, len(l)):
        j = i
        while j > 0 and l[j] < l[j-1]:
            l.swap(j, j-1)
            j -= 1


# =====================================================

def selection_sort(l: List):
    for i in range(0, len(l)):
        small_sub = i
        for j in range(i+1, len(l)):
            if l[j] < l[small_sub]:
                small_sub = j
        l.swap(i, small_sub)


# =====================================================

def quick_sort(l: List, lo=0, hi=-1):
    if hi == -1:
        hi = len(l) - 1
    if lo < hi:
        p = partition(l, lo, hi)
        quick_sort(l, lo, p - 1)
        quick_sort(l, p + 1, hi)


def partition(l, lo, hi):  # Quick sort helper function
    pivot = l[hi]
    i = lo - 1
    for j in range(lo, hi):
        if l[j] < pivot:
            i += 1
            l.swap(i, j)
    l.swap(i + 1, hi)
    return i + 1


# =====================================================

def shell_sort(l: List):
    interval = 0
    while interval < len(l)/3:
        interval = interval*3 + 1

    while interval > 0:
        for outer in range(interval, len(l)):
            inner = outer
            while inner > interval - 1 and l[inner - interval] > l[inner]:
                l.swap(inner - interval, inner)
                inner = inner - interval
        interval = int((interval-1) / 3)


# =====================================================

def heap_sort(l: List):
    n = len(l)

    for i in range(n, -1, -1):
        heapify(l, n, i)

    for i in range(n - 1, 0, -1):
        l.swap(0, i)
        heapify(l, i, 0)


def heapify(l: List, n, i):  # Heap sort helper function
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and l[i] < l[left]:
        largest = left

    if right < n and l[largest] < l[right]:
        largest = right

    if largest != i:
        l.swap(largest, i)
        heapify(l, n, largest)


# =====================================================

def cocktail_shaker_sort(l: List):
    swapped = True
    while swapped:
        swapped = False
        for i in range(0, len(l)-1):
            if l[i] > l[i+1]:
                l.swap(i, i+1)
                swapped = True
        if not swapped:
            break
        for i in range(len(l)-2, -1, -1):
            if l[i] > l[i+1]:
                l.swap(i, i+1)
                swapped = True


# =====================================================

def bitonic_sort(l: List, up=True, lo=0, hi=-1):
    if hi == -1:
        hi = len(l) - 1
    l_size = hi - lo + 1
    if l_size < 2:
        return
    else:
        bitonic_sort(l, True, int(lo + math.floor(l_size / 2)), hi)
        bitonic_sort(l, False, lo, int(hi - math.ceil(l_size / 2)))
        bitonic_merge(l, up, lo, hi)


def bitonic_merge(l: List, up: bool, lo: int, hi: int):  # Bitonic sort helper function
    l_size = hi - lo + 1
    if l_size < 2:
        return
    else:
        bitonic_compare(l, up, lo, hi)
        bitonic_merge(l, up, int(lo + math.floor(l_size / 2)), hi)
        bitonic_merge(l, up, lo, int(hi - math.ceil(l_size / 2)))


def bitonic_compare(l: List, up: bool, lo: int, hi: int):  # Bitonic sort helper function
    l_size = hi - lo + 1
    dist = l_size // 2
    for i in range(lo, lo + dist):
        if (l[i] > l[i + dist]) == up:
            l.swap(i, i + dist)


# =====================================================

def merge_sort(l: List, lo=0, hi=-1):
    if hi == -1:
        hi = len(l) - 1
    l_size = hi - lo + 1
    if l_size < 2:
        return
    merge_sort(l, lo, int(hi - math.ceil(l_size / 2)))
    merge_sort(l, int(lo + math.floor(l_size / 2)), hi)
    merge(l, lo, int(hi - math.ceil(l_size / 2)), int(lo + math.floor(l_size / 2)), hi)


def merge(l: List, lo1: int, hi1: int, lo2: int, hi2: int):  # Merge sort helper function
    while lo1 <= hi1 and lo2 <= hi2:
        if l[lo1] < l[lo2]:
            lo1 += 1
        else:
            left_size = hi1 - lo1 + 1
            for i in range(0, left_size):
                l.swap(lo1+i, lo2)
            lo2 += 1
            lo1 += 1
            hi1 += 1

# =====================================================
