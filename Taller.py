import logging
import threading
import time
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-2s) %(message)s')
class Taller(object):
    def __init__(self, start=0):
        self.condicionMangasMAX = threading.Condition()
        self.condicionMangasMIN = threading.Condition()
        self.mangas = 0
        #prenda
        self.condicionCuerposMAX=threading.Condition()
        self.condicionCuerposMIN=threading.Condition()
        self.cuerpos = 0


    def incrementarManga(self):
        with self.condicionMangasMAX:
            if self.mangas >= 10:
                logging.debug("No hay espacio para mangas")
                self.condicionMangasMAX.wait()
            else:
                self.mangas += 1
                logging.debug("Manga creada, mangas=%s", self.mangas)
        with self.condicionMangasMIN:
            if self.mangas >= 2:
                logging.debug("Existen suficientes mangas")
                self.condicionMangasMIN.notify()

    def decrementarManga(self):
        with self.condicionMangasMIN:
            while not self.mangas >= 2:
                logging.debug("Esperando mangas")
                self.condicionMangasMIN.wait()
            self.mangas -= 2
            logging.debug("Mangas tomadas, mangas restantes=%s", self.mangas)
        with self.condicionMangasMAX:
            logging.debug("Hay espacio para mangas")
            self.condicionMangasMAX.notify()

    def getMangas(self):
        return (self.mangas)

    def incrementarCuerpo(self):
        with self.condicionCuerposMAX:
            if self.cuerpos >= 5:
                logging.debug("No hay espacio para cuerpos")
                self.condicionCuerposMAX.wait()
            else:
                self.cuerpos += 1
                logging.debug("Cuerpo Creado, cuerpos=%s", self.cuerpos)
        with self.condicionCuerposMIN:
            if self.cuerpos >= 1:
                logging.debug("Existen suficientes cuerpos")
                self.condicionCuerposMIN.notify()

    def decrementarCuerpo(self):
            with self.condicionCuerposMIN:
                while not self.cuerpos >0:
                    logging.debug("Esperando cuerpos")
                    self.condicionCuerposMIN.wait()
                self.cuerpos -= 1
                logging.debug("Cuerpo tomado, cuerpos restantes=%s", self.cuerpos)
            with self.condicionCuerposMAX:
                logging.debug("Hay espacio para cuerpos")
                self.condicionCuerposMAX.notify()

    def getCuerpos(self):
            return (self.cuerpos)


def crearManga(Taller):
    while (Taller.getMangas() <= 10):
        Taller.incrementarManga()
        time.sleep(2)


def crearCuerpo(Taller):
    while (Taller.getCuerpos() <=5):
        Taller.incrementarCuerpo()
        time.sleep(5)

def ensamblaPrenda(Taller):
    while (Taller.getMangas() >= 0 and Taller.getCuerpos() >= 0):
        Taller.decrementarManga()
        Taller.decrementarCuerpo()
        logging.debug('Ensamblando todo')
        time.sleep(3)

taller = Taller()
Lupita = threading.Thread(name='Lupita(mangas)', target=crearManga, args=(taller,))
Sofia = threading.Thread(name='Sofía(cuerpos)', target=crearCuerpo, args=(taller,))
Ana = threading.Thread(name='Ana (ensamble)', target=ensamblaPrenda, args=(taller,))
Lupita.start()
Sofia.start()
Ana.start()
Lupita.join()
Sofia.join()
Ana.join()