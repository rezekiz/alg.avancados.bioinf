"""
Código base retirado dos powerpoints das aulas (da autoria de Rui Mendes) com pequenas alterações.
Utilização do stack overflow e de LLMs (GPT 3.5/Gemini 1.5/ blackboxAI) para algumas correções
"""

from typing import Dict, List
import graphviz

class MetabolicNetworkGraph:
    def __init__(self, g: Dict[str, List[str]] = None):
        """
        Inicializa o grafo da rede metabólica.

        Args:
            g (dict, opcional): Um dicionário representando a estrutura do grafo.
        """
        if g is None:
            self.g = {}
        else:
            self.g = g

    def add_reaction(self, reaction: str, substrates: List[str], products: List[str]) -> None:
        """
        Adiciona uma reação metabólica ao grafo.

        Args:
            reaction (str): O nome da reação.
            substrates (lista de str): Lista de substratos participantes na reação.
            products (lista de str): Lista de produtos produzidos pela reação.
        """
        assert isinstance(reaction, str),
        assert isinstance(substrates, list),
        assert isinstance(products, list),
        assert all(isinstance(sub, str) for sub in substrates),
        assert all(isinstance(prod, str) for prod in products),
        
        self.g[reaction] = {'substrates': substrates, 'products': products}

    def show(self, txt: bool = False, gviz: bool = True) -> graphviz.Digraph:
        """
        Grafo da rede metabólica.

        Args:
            txt (bool, opcional): Se True, imprime a estrutura do grafo em formato de texto. Padrão é False.
            gviz (bool, opcional): Se True, exibe o grafo usando o Graphviz. Padrão é True.

        Returns:
            graphviz.Digraph: O objeto Graphviz representando o grafo.
        """
        if txt:
            for reaction, data in self.g.items():
                substrates = ', '.join(data['substrates'])
                products = ', '.join(data['products'])
                print(f"Reação: {reaction} | Substratos: {substrates} | Produtos: {products}")
        if gviz:
            return self._display()

    def _display(self) -> graphviz.Digraph:
        """
        Método auxiliar para exibir o grafo usando o Graphviz.

        Returns:
            graphviz.Digraph: O objeto Graphviz representando o grafo.
        """
        dot = graphviz.Digraph()
        for reaction, data in self.g.items():
            substrates = ', '.join(data['substrates'])
            products = ', '.join(data['products'])
            label = f"{reaction}\nSubstratos: {substrates}\nProdutos: {products}"
            dot.node(reaction, label=label)
        return dot

    def remove_reaction(self, reaction: str) -> None:
        """
        Remove uma reação do grafo.

        Args:
            reaction (str): A reação a ser removida.
        """
        assert isinstance(reaction, str), 
        if reaction not in self.g.keys():
            raise ValueError("A reação não existe")
        del self.g[reaction]
