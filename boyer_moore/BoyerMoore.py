"""
Código base retirado dos powerpoints das aulas (da autoria de Rui Mendes) com pequenas alterações.
Utilização do stack overflow e de LLMs (GPT 3.5 e Gemini 1.5) para algumas correções
"""

class BoyerMoore:
    """
    Implementação do algoritmo Boyer-Moore para busca de padrões em texto.

    Atributos:
        alphabet (str): O alfabeto permitido nos padrões e sequências.
        pattern (str): O padrão que será procurado na sequência.
        occ (dict): Dicionário que mapeia caracteres do alfabeto para a última posição onde ocorrem no padrão.
        f (list): Lista que guarda informações para o pré-processamento do bom sufixo.
        s (list): Lista que guarda informações para o pré-processamento do bom sufixo.
    """
    
    def __init__(self, alphabet : str, pattern : str) -> None:

        """
        Inicia a classe BoyerMoore com o alfabeto e o padrão fornecidos.

        Parâmetros:
            alphabet (str): O alfabeto permitido nos padrões e sequências.
            pattern (str): O padrão que será procurado na sequência.
        
        Retorna:
            None
        """

        self.alphabet = alphabet
        self.pattern = pattern
        self.preprocess()

    def preprocess(self) -> None:

        """
        Realiza o pré-processamento do padrão para construir as tabelas de mau caractere e bom sufixo.

        Parâmetros:
            None
        
        Retorna:
            None
        """

        self.process_bcr()
        self.process_gsr()
        
    def process_bcr(self) -> None:

        """
        Implementação do pre-processamento do bad caracter rule

        Parâmetros:
            None
        
        Retorna:
            None
        """

        self.occ = {}
        for s in self.alphabet:
            self.occ[s] = -1
        for i in range(len(self.pattern)):
            self.occ[self.pattern[i]] = i
            #ou
            # c = self.pattern
            #self.occ[c] = i

            
    def process_gsr(self) -> None:

        """
        Implementação do pre-processamento do good suffix rule

        Parâmetros:
            None
        
        Retorna:
            None
        """

        self.f = [0] * (len(self.pattern) + 1)
        self.s = [0] * (len(self.pattern) + 1)
        i = len(self.pattern)
        j = len(self.pattern) + 1
        self.f[i] = j
        while i > 0:
            while j <= len(self.pattern) and self.pattern[i -1] != self.pattern[j - 1]:
                if self.s[j] == 0:
                    self.s[j] = j - i
                j = self.f[j]
            i = i - 1
            j = j - 1
            self.f[i] = j

        j = self.f[0]

        for i in range(0, len(self.pattern)):
            if self.s[i] == 0:
                self.s[i] = j
            if i == j:
                j = self.f[j]

        
    def search_pattern(self, text : str) -> list:

        """
        Procura o padrão na sequência fornecida .

        Parâmetros:
            text (str): A sequência na qual o padrão será procurado.

        Retorna:
            list: Lista de índices onde o padrão foi encontrado na sequência.
        """

        res = []
        i = 0
        while i <= (len(text) - len(self.pattern)):
            j = (len(self.pattern) - 1) #posicao no padrao
            while j >= 0 and self.pattern[j] == text[j + i]:
                j -= 1
            if j < 0:
                res.append(i)
                i = i +self.s[0]
            else:
                c = text[i + j]
                i += max(self.s[j + 1], j - self.occ[c])
        return res

def test():

    """
    Função de teste para o algoritmo Boyer-Moore.
    """

    bm = BoyerMoore("ACTG", "ACCA")
    print (bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"))

if __name__ == "__main__":
    test()



            
