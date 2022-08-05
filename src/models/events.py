import json


class Event:
    def __init__(self, date, local, name, categoria):
        self.date = date
        self.local = local
        self.name = name
        self.categoria = categoria

    def setName(self, name):
        self.name = name

    def setLocal(self, local):
        self.local = local

    def setDate(self, date):
        self.date = date

    def __repr__(self):
        return "\n\nNome do evento: %s;\n%s;\n%s;\n%s" % (self.name, self.date, self.local, self.categoria)

    def __str__(self):
        return "%s; %s; %s" % (self.date, self.name, self.local)

    def toJSON(self):
        return {
            "date": self.date,
            "local": self.local,
            "name": self.name,
            "categoria": self.categoria,
        }
