# -*- coding: utf-8 -*-

'''
Dummy Objekt fuer Datenhaltung. Es sind eigentlich nur zwei verschachtelte Listen.
Update der Daten zurueck erfolgt nicht automatisch.
'''
class MyData():
    def __init__(self, no_tables, no_views):
        self.data = []
        tables = []
        for i in range(no_tables-1):
            tables.append(["Tabelle {0}".format(i), r"\pfad\unterpfad\Tabelle_{0}".format(i)])
        tables.append(["Tabelle {0}".format(no_tables-1), r"\pfad\weiterererpfad\Tabelle_{0}".format(no_tables-1)])

        views = []
        for i in range(no_views-1):
            views.append(["View {0}".format(i), r"\pfad\unterpfad\View_{0}".format(i)])
        views.append(["View {0}".format(no_views-1), r"\pfad\weiterererpfad\View_{0}".format(no_views-1)])

        self.data.append(["Tabelle", "Pfad", tables])
        self.data.append(["View", "Pfad", views])

