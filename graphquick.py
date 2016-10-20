from graphviz import Digraph
import re
import unittest

NODE_REGEXP = '(-+)>\s*(.*)'

class Node:
    def __init__(self, i, level, label):
        self.id = i
        self.level = level
        self.label = label

    def add_to_dot(self, dot):
        dot.node(str(self.id), self.label)

class Parser:
    def __init__(self, source_or_path, from_file=False):
        if from_file:
            with open(source_or_path, 'r') as f:
                self.source = f.read()
        else:
            self.source = source
        self.dot = Digraph()

    def set_graph_attrs(self, **kwargs):
        self.dot.attr('graph', kwargs)

    def set_node_attrs(self, **kwargs):
        self.dot.attr('node', kwargs)

    def convert_to_dot(self):
        i = 0
        currents = {}
        
        for line in self.source.split('\n'):
            match = re.match(NODE_REGEXP, line)
            if match:
                level = len(match.group(1))-1
                label = match.group(2).rstrip()
                if level != 0 and not level-1 in currents:
                    continue
                current = Node(i, level, label)
                i += 1
                current.add_to_dot(self.dot)
                currents[level] = current

                if level > 0:
                    parent = currents[level-1]
                    self.dot.edge(str(parent.id), str(current.id))

        return self.dot

    def convert_to_source(self):
        return self.convert_to_dot().source

    def render_to_file(self, filename=None, out_format='png'):
        dot = self.convert_to_dot()
        dot.format = out_format
        dot.render(filename, cleanup=True)
        

if __name__ == '__main__':
    source = """
-> Aristote
--> La Nature
--> La Raison
"""
    dot = parse(source)
    dot.format = 'png'
    dot.render(cleanup=True)
