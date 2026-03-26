class BinaryHeap:
    
    def __init__(self):
        self._data = []
    
    def _parent(self, j):
        return (j - 1) // 2
    
    def _left(self, j):
        return 2 * j + 1
    
    def _right(self, j):
        return 2 * j + 2
    
    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]
    
    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j][0] < self._data[parent][0]:
            self._swap(j, parent)
            self._upheap(parent)
    
    def _downheap(self, j):
        if self._left(j) < len(self._data):
            left_child = self._left(j)
            small_child = left_child
            right_child = self._right(j)
            if right_child < len(self._data) and self._data[right_child][0] < self._data[left_child][0]:
                small_child = right_child
            if self._data[small_child][0] < self._data[j][0]:
                self._swap(j, small_child)
                self._downheap(small_child)
    
    def add(self, key, value):
        self._data.append((key, value))
        self._upheap(len(self._data) - 1)
    
    def min(self):
        if len(self._data) == 0:
            return None
        return self._data[0]
    
    def remove_min(self):
        if len(self._data) == 0:
            return None
        min_val = self._data[0]
        self._data[0] = self._data[-1]
        self._data.pop()
        if len(self._data) > 0:
            self._downheap(0)
        return min_val
    
    def is_empty(self):
        return len(self._data) == 0
    
    def __len__(self):
        return len(self._data)


class AdaptablePriorityQueue:
    
    def __init__(self):
        self._heap = BinaryHeap()
        self._entry_map = {}
        self._counter = 0
    
    def add(self, key, value):
        if value in self._entry_map:
            return
        entry = [key, self._counter, value]
        self._counter += 1
        self._entry_map[value] = entry
        self._heap.add((key, entry), entry)
    
    def min(self):
        while not self._heap.is_empty():
            key, entry = self._heap.min()
            if entry[2] in self._entry_map and self._entry_map[entry[2]] == entry:
                return entry[0], entry[2]
            else:
                self._heap.remove_min()
        return None
    
    def remove_min(self):
        while not self._heap.is_empty():
            key, entry = self._heap.remove_min()
            if entry[2] in self._entry_map and self._entry_map[entry[2]] == entry:
                del self._entry_map[entry[2]]
                return entry[0], entry[2]
        return None
    
    def update(self, value, new_key):
        if value in self._entry_map:
            entry = self._entry_map[value]
            if new_key < entry[0]:
                entry[0] = new_key
                self._heap.add((new_key, entry), entry)
    
    def is_empty(self):
        return len(self._entry_map) == 0
    
    def __len__(self):
        return len(self._entry_map)


class UnsortedListAPQ:

    def __init__(self):
        self._data = []
        self._map  = {}

    def add(self, key, value):
        if value in self._map:
            return
        entry = [key, value]
        self._map[value] = entry
        self._data.append(entry)

    def min(self):
        if not self._data:
            return None
        m = min(self._data, key=lambda e: e[0])
        return m[0], m[1]

    def remove_min(self):
        if not self._data:
            return None
        min_idx = 0
        for i in range(1, len(self._data)):
            if self._data[i][0] < self._data[min_idx][0]:
                min_idx = i
        entry = self._data[min_idx]
        self._data[min_idx] = self._data[-1]
        self._data.pop()
        del self._map[entry[1]]
        return entry[0], entry[1]

    def update(self, value, new_key):
        if value in self._map:
            entry = self._map[value]
            if new_key < entry[0]:
                entry[0] = new_key

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)