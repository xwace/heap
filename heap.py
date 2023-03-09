#https://zhuanlan.zhihu.com/p/44774786#1%20%E4%BB%80%E4%B9%88%E6%98%AF%E2%80%9C%E5%A0%86%E2%80%9D
from copy import copy
from time import time
import numpy as np


class MaxHeap(object):
    def __init__(self, max_size, fn):
        """MaxHeap class.
        Arguments:
            max_size {int} -- The maximum size of MaxHeap instance.
            fn {function} -- Function to caculate the values of items
            when comparing items.
        Attributes:
            _items {object} -- The items in the MaxHeap instance.
            size {int} -- The size of MaxHeap instance.
        """

        self.max_size = max_size
        self.fn = fn

        self._items = [None] * max_size
        self.size = 0

    def __str__(self):
        item_values = str([self.fn(x) for x in self.items])
        info = (self.size, self.max_size, self.items, item_values)
        return "Size: %d\nMax size: %d\nItems: %s\nItem_values: %s\n" % info

    @property
    def items(self):
        return self._items[:self.size]

    @property
    def full(self):
        """If the heap is full.
        Returns:
            bool
        """

        return self.size == self.max_size

    def value(self, idx):
        """Caculate the value of item.
        Arguments:
            idx {int} -- The index of item.
        Returns:
            float
        """
        item = self._items[idx]
        if item is None:
            ret = -float('inf')
        else:
            ret = self.fn(item)
        return ret

    def add(self, item):

        if self.full:
            if self.fn(item) < self.value(0):
                self._items[0] = item
                self._shift_down(0)
        else:
            self._items[self.size] = item
            self.size += 1
            self._shift_up(self.size - 1)

    def pop(self):
        """Pop the top item out of the heap.
        Returns:
            object -- The item popped.
        """

        assert self.size > 0, "Cannot pop item! The MaxHeap is empty!"
        ret = self._items[0]
        self._items[0], self._items[self.size - 1] = \
            self._items[self.size - 1], self._items[0]
        self.size -= 1
        self._shift_down(0)
        return ret

    def _shift_up(self, idx):

        assert idx < self.size, \
            "The parameter idx must be less than heap's size!"
        parent = (idx - 1) // 2
        while parent >= 0 and self.value(parent) < self.value(idx):
            self._items[parent], self._items[idx] = \
                self._items[idx], self._items[parent]
            idx = parent
            parent = (idx - 1) // 2

    def _shift_down(self, idx):
        """Shift down item until its children are less than the item.
        Arguments:
            idx {int} -- Heap item's index.
        """

        child = (idx + 1) * 2 - 1
        while child < self.size:
            # Compare the left child and the right child and get the index
            # of the larger one.
            if child + 1 < self.size and \
                    self.value(child + 1) > self.value(child):
                child += 1
            # Swap the items, if the value of father is less than child.
            if self.value(idx) < self.value(child):
                self._items[idx], self._items[child] = \
                    self._items[child], self._items[idx]
                idx = child
                child = (idx + 1) * 2 - 1
            else:
                break

    def _is_valid(self):
        """Validate a MaxHeap by comparing all the parents and its children.
        Returns:
            bool
        """

        ret = []
        for i in range(1, self.size):
            parent = (i - 1) // 2
            ret.append(self.value(parent) >= self.value(i))
        return all(ret)



def exhausted_search(nums, k):
    rets = []
    idxs = []
    key = None
    for _ in range(k):
        val = float("inf")
        for i, num in enumerate(nums):
            if num < val and i not in idxs:
                key = i
                val = num
        idxs.append(key)
        rets.append(val)
    return rets

def gen_data(low, high, n_rows, n_cols=None):
    if n_cols is None:
        ret = [np.random.randint(low, high) for _ in range(n_rows)]
    else:
        ret = [[np.random.randint(low, high) for _ in range(n_cols)]
               for _ in range(n_rows)]
    return ret

if __name__ == "__main__":
    print("Testing MaxHeap...")
    test_times = 100
    run_time_1 = run_time_2 = 0
    for _ in range(test_times):
        # Generate dataset randomly
        low = 0
        high = 1000
        n_rows = 10000
        k = 100
        nums = gen_data(low, high, n_rows)

        # Build Max Heap
        heap = MaxHeap(k, lambda x: x)
        start = time()
        for num in nums:
            heap.add(num)
        ret1 = copy(heap.items)
        run_time_1 += time() - start

        # Exhausted search
        start = time()
        ret2 = exhausted_search(nums, k)
        run_time_2 += time() - start

        # Compare result
        ret1.sort()
        assert ret1 == ret2, "target:%s\nk:%d\nrestult1:%s\nrestult2:%s\n" % (
            str(nums), k, str(ret1), str(ret2))
    print("%d tests passed!" % test_times)
    print("Max Heap Search %.2f s" % run_time_1)
    print("Exhausted search %.2f s" % run_time_2)
