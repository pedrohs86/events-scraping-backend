from src.feiras import search_feiras
from src.sympla import search_sympla

if __name__ == '__main__':
    # print('Programa de Scrapping nos sites http://www.feirasdobrasil.com.br/feirasdasemana.asp e https://www.sympla.com.br/')
    # search = input("Informe o Segmento do Evento: ")
    # print('...Pesquisando no site http://www.feirasdobrasil.com.br/feirasdasemana.asp\n')
    # search_feiras(search)

    search = input("Informe a categoria do Evento: ")
    # print('...Pesquisando no site https://www.sympla.com.br/\n')
    paginas = set()
    event_sympla = search_sympla('https://www.sympla.com.br/categorias', search, paginas)
    # print('Foi encontrado no site https://www.sympla.com.br/ o(s) seguinte(s) evento(s): ')
    # print(event_sympla)
