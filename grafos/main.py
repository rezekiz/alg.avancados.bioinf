"""
Criação de módulo de grafos
Utilização de graphviz para visualizar
A testagem tem de considerar a adição de nós, vértices e ligações
"""


"""
Autor: Rui Sousa
"""

import graphviz

# Métodos estáticos para usar graphviz para renderizar

def display(graph):
    dot = graphviz.Digraph()
    
    for key in graph.keys():
        dot.node(str(key))
        for dest in graph[key]:
            dot.edge(str(key), str(dest))
    dot.view()
    return dot

class Graph():
  def __init__(self, g = None):
    if g is None:
      self.g = {}
    else:
      self.g = g

  def add_node(self, node):
    if node not in self.g:
      self.g[node] = []

  def add_edges(self, edges : list):
    """
    Método para adicionar edges com notação simples como "Origem -> Destino"

    Pode ser usada uma lista ou uma string simples.

    Tem de ser sempre usado o operador "->"

    """

    # TODO pensar no usecase para bidirecional como C <-> A

    if type(edges) == str:
      edges = [edges]

    for edge in edges:
      edge = edge.replace(' ','')
      origin, destinations = edge.split('->')

      if origin not in self.g.keys():
        self.add_node(origin)
      
      for destination in destinations.split(','):
        if destination not in self.g.keys():
          self.add_node(destination)
        
        if destination not in self.g[origin]:
          self.g[origin].append(destination)

  def show(self, txt = False, gviz = True):

    if txt:  
      for key in self.g.keys():
        print(f'{key} ==> {self.g.get(key)}')

    if gviz:  
      return display(self.g)

  def rm_node(self, node):
    if node not in self.g.keys():
      print('Nó não existe.')
    # Removemos das edges
    for edge in self.g.values():
      if node in edge:
        edge.remove(node)
    del self.g[node]

  def rm_edges(self, edges):
    if type(edges) == str:
      edges = [edges]
    
    for edge in edges:
      edge = edge.replace(' ', '')
      origin, destinations = edge.split('->')
      for destination in destinations.split(','):
        self.g[origin].remove(destination)
      



    



  












