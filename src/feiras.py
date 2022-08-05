import unicodedata
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re

from src.models.events import Event

date_patern = "\d{2} .+ \d{4}"
local_patern = ":[a-z]+([A-Z][^0-9]+\/[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]{2})"
categoria_patern = ":[a-z]+([\D]+)[a-z]\nDa"


def search_feiras(filtro):
    try:
        all_events_name = []
        date_match = []
        events_list = []
        local_match = []
        categoria_match = []

        url = 'http://www.feirasdobrasil.com.br/feirasdasemana.asp'
        r = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(r)
        bs_obj = BeautifulSoup(html.read(), "html.parser")
        td_all = bs_obj.find_all("td", {"class": "verdana20_cinza"})
        for td in td_all:
            b = td.find("b")
            if b is not None:
                name = b.text.strip().strip('\n').strip('\t').strip('\r')
                all_events_name.append(name)
        del all_events_name[0]
        # print(all_events_name)

        date_type = re.compile(date_patern)
        local_type = re.compile(local_patern)
        categoria_type = re.compile(categoria_patern)
        date_local_td = bs_obj.find_all("td", {"class": "verdana15_cinza"})
        for td in date_local_td:
            if td is not None:
                date_aux = date_type.findall(td.text)[0]
                date_match.append(date_aux)

                local_aux = local_type.findall(td.text)[0]
                local_match.append(local_aux)

                categoria_aux = categoria_type.findall(td.text)[0]
                categoria_match.append(categoria_aux)

        # print(date_match)
        # print(local_match)
        # print(categoria_match)
        # print(len(categoria_match), len(date_match), len(all_events_name), len(local_match))

        for i in range(len(all_events_name)):
            events_list.append(Event(date_match[i], local_match[i], all_events_name[i], categoria_match[i]))
        # print(events_list)
        events_list_filter = []
        if filtro:
            filtro_normalize = unicodedata.normalize("NFD", filtro.lower())
            filtro_normalize = filtro_normalize.encode("ascii", "ignore")
            filtro_normalize = filtro_normalize.decode("utf-8")
            for i in range(len(all_events_name)):
                evento_normalize = unicodedata.normalize("NFD", events_list[i].categoria.lower())
                evento_normalize = evento_normalize.encode("ascii", "ignore")
                evento_normalize = evento_normalize.decode("utf-8")
                if filtro_normalize in evento_normalize:
                    # print(events_list_filter)
                    events_list_filter.append(events_list[i].toJSON())
            return events_list_filter
        else:
            for i in range(len(all_events_name)):
                events_list_filter.append(events_list[i].toJSON())
            return events_list_filter
        # print('Foi encontrado no site http://www.feirasdobrasil.com.br/feirasdasemana.asp o(s) seguinte(s) evento(s): ')
        # print(events_list_filter)
    except Exception as e:
        print('feiras: ', e)
        return 'except' + e.__str__()
        # print('Pagina com erro')
