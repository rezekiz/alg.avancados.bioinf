def sobreposicao(s1, s2):
    """
    Retorna o comprimento do maior prefixo comum entre duas strings.

    Parâmetros:
        s1 (str): A primeira string.
        s2 (str): A segunda string.

    Retorna:
        int: O comprimento do maior prefixo comum.
    """

    max_ov = min(len(s1), len(s2))
    for i in range(max_ov, 0, -1):
        if s1[-i:] == s2[:i]:
            return i
    return 0