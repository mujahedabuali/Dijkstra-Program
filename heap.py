class Heap:
    def __init__(self):
        self.heap = []

    def push(self, node, distance):
        self.heap.append((node, distance))
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None

        node, distance = self.heap[0]
        last_node, last_distance = self.heap.pop()
        if self.heap:
            self.heap[0] = (last_node, last_distance)
            self._heapify_down(0)
        return node

    def peek(self):
        return self.heap[0][0] if self.heap else None

    def is_empty(self):
        return not bool(self.heap)

    def size(self):
        return len(self.heap)

    def _heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index][1] < self.heap[parent_index][1]:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def _heapify_down(self, index):
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            smallest = index

            if left_child_index < len(self.heap) and self.heap[left_child_index][1] < self.heap[smallest][1]:
                smallest = left_child_index

            if right_child_index < len(self.heap) and self.heap[right_child_index][1] < self.heap[smallest][1]:
                smallest = right_child_index

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

