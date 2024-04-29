"""
Criação de módulo de grafos
Utilização de graphviz para visualizar
A testagem tem de considerar a adição de nós, vértices e ligações
"""


import graphviz

class Graph(graph):
  def __init__(self):
    if graph is None:
      self.g = {}
    else:
      self.g = g

  def add_node(self, node):
    if node not in self:
      self[node] = []

  def add_branch(self, origin, destination):
    if origin not in self.keys():
      add_node(self, origin)
    elif destination not in self.keys():
      add_node(self, destination)
    elif destination not in self[origin]:
      self[origin].append(destination)
      
    



