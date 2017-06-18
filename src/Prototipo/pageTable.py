from tabulate import tabulate

from Prototipo.page import Page


class PageTable:
    def __init__(self, requiredPages):
        self._pages = self.createPages(requiredPages)

    #Proposito:Crea la cantidad de paginas que va a nesesitar segun <requiredPages>
    #Proposito:--
    def createPages(self,requiredPages):
        pageTable=[]
        for i in range(0,requiredPages):
            pageTable.append(Page())
        return pageTable

    #Proposito:retorno la pagina que corresponde al bd enviado por parametro
    #Precondicion:-
    def searchPage(self,bd):
        for page in self._pages:
            if page.getBDPhysicalMemory()==bd:
                return page

    # Proposito:
    # Precondicion:-
    def getPages(self):
        return self._pages

    # Proposito:
    # Precondicion:-
    def getPagesPhysical(self):
        res=[]
        for page in self._pages:
            if page.isInPhysicalMemory():
                res.append(page)
        return res

    # Proposito:
    # Precondicion:-
    def getPagesVirtual(self):
        res=[]
        for page in self._pages:
            if page.inSwap():
                res.append(page)
        return res

    # Proposito:
    # Precondicion:-
    def getPage(self, page):
        return self._pages[page]


    #def __repr__(self):
        #return tabulate(enumerate(self._pages), tablefmt='psql')
        #res = []
        #pageNumber = 0
        #for page in self._pages:
        #    res.append(["Page: " + str(pageNumber) + "  {p}".format(p=page)])
        #    pageNumber += 1
        #return tabulate(res, tablefmt='psql')

