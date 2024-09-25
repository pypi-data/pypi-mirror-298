def valida(val):
    """
    --> Função que valida a entrada de dados no formato da moeda local (R$)
    :param val: valor inserido pelo usuário
    :return: caso o valor não seja uma string, ele é armazenado como float
    """
    while True:
        n = str(input(val)).strip().replace(',', '.')
        if n.isalpha() or n.strip() == '':
            print(f'\033[0;31mErro! {n} é um valor inválido!\033[m')
        else:
            return float(n)
            break
