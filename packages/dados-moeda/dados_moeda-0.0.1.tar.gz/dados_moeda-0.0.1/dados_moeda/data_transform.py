def aumentar(val, p=10, formato=True):
    """
    --> Função que aumenta o valor digitado pelo usuário
    :param val: valor digitado pelo usuário
    :param p: valor de aumento em porcentagem (10% é o valor default)
    :param formato: Verifica o formato do separador decimal de ponto para vírgula (True = substitui "," por ".")
    :return: retorna o valor final
    """
    up = val + (val * p/100)
    if not formato:
        return up
    else:
        return moeda(up)


def diminuir(val, d=10, formato=True):
    """
    --> Função que diminui o valor digitado pelo usuário
    :param val: valor digitado pelo usuário
    :param d: valor de redução em porcentagem (10% é o valor default)
    :param formato: Verifica o formato do separador decimal de ponto para vírgula (True = substitui "," por ".")
    :return: retorna o valor final
    """
    menos = val - (val * (d/100))
    if not formato:
        return menos
    else:
        return moeda(menos)


def dobro(val, formato=True):
    """
    --> Função que dobra o valor digitado pelo usuário
    :param val: valor digitado pelo usuário
    :param formato: Verifica o formato do separador decimal de ponto para vírgula (True = substitui "," por ".")
    :return: retorna o valor final
    """
    n = val * 2
    if not formato:
        return n
    else:
        return moeda(n)


def metade(val, formato=True):
    """
    --> Função que divide o valor digitado pelo usuário pela metade
    :param val: valor digitado pelo usuário
    :param formato: Verifica o formato do separador decimal de ponto para vírgula (True = substitui "," por ".")
    :return: retorna o valor final
    """
    m = val / 2
    if not formato:
        return m
    else:
        return moeda(m)
    # print(f'A metade de R$ {val:.2f} é R$ {m:.2f}.')


def moeda(val, moeda='R$'):
    """
    --> Função que formata o separador decimal de ponto para vírgula
    :param val: valor que será formatado
    :return: retorno do valor formatado
    """
    return f'{moeda} {val:.2f}'.replace('.', ',')


def resumo(val, d=10, p=10):
    """
    --> Função que retorna um resumo de todas as outras funções anteriores
    :param val: valor digitado pelo usuário
    :param d: porcentagem de redução do valor (padrão é 10%)
    :param p: porcentagem de aumento do valor (padrão é 10%)
    """
    print('-' * 30)
    print('RESUMO DOS VALORES'.center(30))
    print('-' * 30)
    print(f'Preço Analisado: \t{moeda(val)}')
    print(f'Dobro do preço: \t{dobro(val)}')
    print(f'Metade do preço: \t{metade(val)}')
    print(f'{p}% de aumento: \t{aumentar(val)}')
    print(f'{d}% de redução: \t{diminuir(val)}')
    print('-' * 30)

