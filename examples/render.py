import sys
sys.path.append('..')

import graphquick

parser = graphquick.Parser('source', from_file=True)
parser.set_node_attrs(shape='box')
parser.render_to_file('out')