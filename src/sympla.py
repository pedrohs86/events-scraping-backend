import unicodedata
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re

from src.models.events import Event

paginas_invalidas = set()
category_card_patern = 'collection-card'

onDemand_info_patern = 'OndemandCardstyle__OndemandCardContainer.*'
onDemand_name_patern = 'OndemandCardstyle__EventTitle.*'

events_info_patern = 'EventCardstyle__EventCardContainer.*'
events_local_patern = 'EventCardstyle__EventLocation.*'
events_name_patern = 'EventCardstyle__EventTitle.*'
events_date_patern = 'sc-1sp59be-0.*'

events_name_list = []
events_local_list = []
events_date_list = []
events_list = set()
nova_pagina = ""


def search_sympla(url, filtro, paginas, events_list_filter):
    global nova_pagina
    try:

        events_info = []
        onDemand_info = []
        r = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(r)
        bs_obj = BeautifulSoup(html.read(), "html.parser")
        events_info = bs_obj.findAll("div", {'class': re.compile(events_info_patern)})
        onDemand_info = bs_obj.findAll("div", {'class': re.compile(onDemand_info_patern)})
        categoria = 'Indeterminado'

        if len(url.split('/')) > 4:
            categoria = url.split('/')[4].split('?')[0]

        if categoria != 'Indeterminado':
            for event in onDemand_info:
                name = event.find("h3", {'class': re.compile(onDemand_name_patern)})
                events_local_list.append('Evento Online')
                events_date_list.append('On demand')
                if name:
                    events_name_list.append(name.text)
                else:
                    events_name_list.append('Sem Titulo')

            for event in events_info:
                local = event.find("div", {'class': re.compile(events_local_patern)})
                name = event.find("h3", {'class': re.compile(events_name_patern)})
                date = event.find("div", {'class': re.compile(events_date_patern)})
                if date or name or local:
                    if local:
                        events_local_list.append(local.text)
                    else:
                        events_local_list.append('Evento Online')
                    if name:
                        events_name_list.append(name.text)
                    else:
                        events_name_list.append('Sem Titulo')
                    if date:
                        if len(date.text) == 12:
                            text = date.text[:6] + ' ' + date.text[6:]
                        else:
                            text = date.text
                        events_date_list.append(text)
                    else:
                        events_date_list.append('On demand')

        for i in range(len(events_date_list) - 1):
            events_list.add(Event(events_date_list[i], events_local_list[i], events_name_list[i], categoria.title()))
        # print(events_list)

        if filtro:
            filtro_normalize = unicodedata.normalize("NFD", filtro.lower())
            filtro_normalize = filtro_normalize.encode("ascii", "ignore")
            filtro_normalize = filtro_normalize.decode("utf-8")
            for event in events_list:
                evento_normalize = unicodedata.normalize("NFD", event.name.lower())
                evento_normalize = evento_normalize.encode("ascii", "ignore")
                evento_normalize = evento_normalize.decode("utf-8")

                evento_normalize_categoria = unicodedata.normalize("NFD", event.categoria.lower())
                evento_normalize_categoria = evento_normalize_categoria.encode("ascii", "ignore")
                evento_normalize_categoria = evento_normalize_categoria.decode("utf-8")

                if filtro_normalize in evento_normalize or filtro_normalize in evento_normalize_categoria:
                    if event.name != 'Sem Titulo':
                        events_list_filter.add(event)
        else:
            events_list_filter = events_list

        # events_type = ('eventos\/(tecnologia|gratis)')
        events_type = ('eventos\/(online|tecnologia|gratis|curso-workshop)')
        # events_type = ('(eventos\/(online|gratis|curso-workshop|congresso-palestra|tecnologia|teatro-espetaculo))')
        if categoria == 'Indeterminado':
            for link in bs_obj.findAll("a", href=re.compile(events_type)):
                if "href" in link.attrs:
                    nova_pagina = link.attrs['href']
                    if nova_pagina not in paginas and nova_pagina not in paginas_invalidas:
                        paginas.add(nova_pagina)
                        new_events_list = set()
                        conjunto_nova_pagina = search_sympla('https://www.sympla.com.br' + nova_pagina, filtro, paginas,
                                                             new_events_list)
                        events_list_filter = events_list_filter.union(conjunto_nova_pagina)
                        list_aux = set()
                        list_aux_name = []
                        for event in events_list_filter:
                            if event.name not in list_aux_name:
                                list_aux.add(event)
                                list_aux_name.append(event.name)

                        events_list_filter = list_aux
                        # print(events_list_filter)
        return events_list_filter
    except Exception as e:
        # print('sympla: ', e)
        # print('sympla: ', nova_pagina)
        paginas_invalidas.add(nova_pagina)
        return events_list_filter
