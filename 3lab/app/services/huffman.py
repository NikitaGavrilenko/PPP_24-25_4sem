import heapq
from collections import defaultdict


class HuffmanCoder:
    def __init__(self):
        self.codes = {}

    class Node:
        def __init__(self, char=None, freq=0, left=None, right=None):
            self.char = char
            self.freq = freq
            self.left = left
            self.right = right

        def __lt__(self, other):
            return self.freq < other.freq

    def build_frequency_dict(self, data):
        frequency = defaultdict(int)
        for char in data:
            frequency[char] += 1
        return frequency

    def build_huffman_tree(self, frequency):
        priority_queue = []
        for char, freq in frequency.items():
            heapq.heappush(priority_queue, self.Node(char=char, freq=freq))

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            merged = self.Node(freq=left.freq + right.freq, left=left, right=right)
            heapq.heappush(priority_queue, merged)

        return priority_queue[0] if priority_queue else None

    def build_codes(self, node, current_code=""):
        if node is None:
            return

        if node.char is not None:
            self.codes[node.char] = current_code
            return

        self.build_codes(node.left, current_code + "0")
        self.build_codes(node.right, current_code + "1")

    def encode_data(self, data):
        frequency = self.build_frequency_dict(data)
        root = self.build_huffman_tree(frequency)
        self.build_codes(root)

        encoded_text = ''.join([self.codes[char] for char in data])

        # Вычисляем padding (дополнение до целого числа байтов)
        padding = (8 - len(encoded_text) % 8)
        if padding != 0:
            encoded_text += '0' * padding

        return encoded_text, padding

    def get_codes(self):
        return self.codes