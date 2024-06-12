from Tries import Trie
from Tries import TrieNode

if __name__ == "__main__":

    trie = Trie()

    # Inserção de algumas palavras na Trie
    palavras = ["casa", "casaco", "casinha", "carro", "camisa", "computador"]
    for palavra in palavras:
        trie.insert(palavra)

    # Impressão da estrutura da Trie
    print("Estrutura da Trie:")
    trie.pprint()

    # Função de procura
    testes = ["casa", "casaco", "camisola", "car", "computador", "c"]
    print("\nA testar a função de procura:")
    for palavra in testes:
        if trie.procura(palavra):
            print(f"A palavra '{palavra}' está na Trie.")
        else:
            print(f"A palavra '{palavra}' não está na Trie.")

    # Função de prefixo
    prefixos = ["ca", "cas", "co", "cai", "cam"]
    print("\nTestando a função de prefixo:")
    for prefixo in prefixos:
        if trie.comeca(prefixo):
            print(f"Alguma palavra na Trie começa com '{prefixo}'.")
        else:
            print(f"Nenhuma palavra na Trie começa com '{prefixo}'.")



