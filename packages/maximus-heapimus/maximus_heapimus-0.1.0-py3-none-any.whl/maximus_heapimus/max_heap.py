from typing import List

def heapify(heap) -> List[int]:
    for i in reversed(range(0, len(heap) // 2)):
        _bubble_down(heap, i)
    

def heappush(heap, value) -> None:
    heap.append(value)
    _bubble_up(heap, len(heap) - 1)
    
def heappop(heap) -> int:
    if len(heap) == 1:
        return heap.pop()
    
    to_return = heap[0]
    heap[0] = heap.pop()
    _bubble_down(heap, 0)
    return to_return
        

def heaptop(heap) -> int:
    return heap[0] if heap else -1
    
def _bubble_up(heap, index):
    while index > 0 and heap[index] > heap[(index - 1) // 2]:
        heap[index], heap[(index - 1) // 2] = heap[(index - 1) // 2], heap[index]
        index = (index - 1) // 2

def _bubble_down(heap, index):
    while index * 2 + 1 < len(heap):
        left = index * 2 + 1
        right = index * 2 + 2
        
        if right >= len(heap):
            child = left
        else:
            child = left if heap[left] >= heap[right] else right
        
        if heap[index] < heap[child]:
            heap[index], heap[child] = heap[child], heap[index]
            index = child
        else:
            break


#parent at (i-1 // 2)
#child left at i * 2 + 1
#child right at i * 2 + 2
#HEAP OPERATIONS ARE DONE IN PLACE
# class MaxHeap:
#     def __init__(self):
#         self.heap = []
        
#     def heapify(self, arr) -> List[int]:
#         self.heap = arr
#         for i in reversed(range(0, len(self.heap) // 2)):
#             self._bubble_down(i)
        
#     def access(self):
#         return self.heap
    
#     def push(self, value) -> None:
#         self.heap.append(value)
#         self._bubble_up(len(self.heap) - 1)
        
#     def pop(self) -> int:
#         if len(self.heap) == 1:
#             return self.heap.pop()
        
#         to_return = self.heap[0]
#         self.heap[0] = self.heap.pop()
#         self._bubble_down(0)
#         return to_return
            
    
#     def top(self) -> int:
#         return self.heap[0] if self.heap else -1
        
#     def _bubble_up(self, index):
#         while index > 0 and self.heap[index] > self.heap[(index - 1) // 2]:
#             self.heap[index], self.heap[(index - 1) // 2] = self.heap[(index - 1) // 2], self.heap[index]
#             index = (index - 1) // 2
    
#     def _bubble_down(self, index):
#         while index * 2 + 1 < len(self.heap):
#             left = index * 2 + 1
#             right = index * 2 + 2
            
#             if right >= len(self.heap):
#                 child = left
#             else:
#                 child = left if self.heap[left] >= self.heap[right] else right
            
#             if self.heap[index] < self.heap[child]:
#                 self.heap[index], self.heap[child] = self.heap[child], self.heap[index]
#                 index = child
#             else:
#                 break