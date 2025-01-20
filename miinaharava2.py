import random
import math
import datetime
import haravasto

tila = {
    "kentta": [],
    "kentta_kulku":[],
    "pelaa": False
}

hiiren_painike = {
        1: "vasen",
        2: "keski",
        4: "oikea"
        }

klikkaukset = []
klikkausmaara = []
        
def luo_kentta(rivit, sarakkeet, miinamaara):
    """
    Luo kentän, asettaa miinat kutsumalla miinoita funktiota ja laskee montako miinaa
    ruudun ympärillä on kutsumalla laske miinat funktiota. Palauttaa luodun kentän,
    sekä saman kokoisen tyhjän kentän.
    """
    kentta = []
    kentta_kulku = []
    ruudut = []
    rivi_lkm = -1
    for rivi in range(rivit):
        kentta.append([])
        kentta_kulku.append([])
        rivi_lkm += 1
        sarake_lkm = -1
        for sarake in range(sarakkeet):
            sarake_lkm += 1
            kentta[-1].append("0")
            kentta_kulku[-1].append(" ")
            ruudut.append((sarake_lkm, rivi_lkm))
              
    miinoita(kentta, ruudut, miinamaara)
    
    for koordinaatti in ruudut:
        x_kd, y_kd = koordinaatti
        miinat_vieressa = str(laske_miinat(x_kd, y_kd, kentta))
        kentta[y_kd][x_kd] = miinat_vieressa
    return kentta, kentta_kulku
    
def miinoita(mkentta, vpruudut, miinam):
    """
    Asettaa kentälle N kpl miinoja satunnaisiin paikkoihin.
    """
    for i in range(miinam):
        miinanaatit = random.choice(vpruudut)
        vpruudut.remove(miinanaatit)
        miinax, miinay = miinanaatit
        mkentta[miinay][miinax] = "x"

def laske_miinat(x_kd, y_kd, miinakentta):
    """
    Laskee annetussa kentässä yhden ruudun ympärillä olevat miinat ja palauttaa
    niiden lukumäärän. Funktio toimii sillä oletuksella, että valitussa ruudussa ei
    ole miinaa.
    """
    miinat_ymp = 0
    y_etaisyys = -1
    for sarake in miinakentta:
        y_etaisyys += 1
        x_etaisyys = -1
        for miina in sarake:
            x_etaisyys += 1
            if miina == "x" and x_kd -1 <= x_etaisyys <= x_kd + 1 and\
            y_kd -1 <= y_etaisyys <= y_kd + 1:
                miinat_ymp += 1
    return miinat_ymp

def tulvataytto(pelikentta, kentan_kulku, ruutux, ruutuy):
    """
    Tutkii annetun ruudun vieressä olevien ruutujen tilaa. Jos viereinen ruutu on tyhjä, 
    ruutu lisätään tutkittavien listaan. Sijoittaa tutkittujen ruutujen arvot piirrettävään
    kenttään.
    """
    ruudut = [(ruutux, ruutuy)]
    while ruudut:
        xkd, ykd = ruudut.pop()
        xmin = xkd - 1
        xmin = max(xmin, 0)
        xmax = xkd + 1
        if xmax > leveys - 1:
            xmax = xkd
        ymin = ykd - 1
        ymin = max(ymin, 0)
        ymax = ykd + 1
        if ymax > korkeus - 1:
            ymax = ykd
        for rivi in range(ymin, ymax + 1):
            for arvo in range(xmin, xmax + 1): 
                if kentan_kulku[rivi][arvo] == " ":
                    kentan_kulku[rivi][arvo] = pelikentta[rivi][arvo]
                    if pelikentta[rivi][arvo] == "0":
                        ruudut.append((arvo, rivi))
                    
def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    if tila["pelaa"] is True:
        haravasto.tyhjaa_ikkuna()
        haravasto.aloita_ruutujen_piirto()
        kentan_paivitys()
        yarvo = -1
        for yrivi in tila["kentta_kulku"]:
            yarvo += 1
            xarvo = -1
            for xrivi in yrivi:
                xarvo += 1
                haravasto.lisaa_piirrettava_ruutu(tila["kentta_kulku"][yarvo][xarvo],\
                xarvo * 40,yarvo * 40)
        haravasto.piirra_ruudut()

def kasittele_hiiri(hiiri_x, hiiri_y, painike, mknappain):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Funktio lisää klikatun ruudun ja hiiren painikken klikkaukset listaan.
    """
    painettu_ruutu = (math.floor(hiiri_x / 40), math.floor(hiiri_y / 40), hiiren_painike[painike])
    klikkaukset.append(painettu_ruutu)
    
def kentan_paivitys():
    """
    Tutkii klikkauksen lähettämät arvot ja muokkaa kenttää sen mukaan.
    Päättää pelin, kun miinaa klikataan tai kun kaikki vapaat ruudut
    on avattu. Funktio määritää pelin etenemisen.
    """
    while klikkaukset:
        klikattux, klikattuy, painike = klikkaukset.pop()
        if painike == "vasen" and tila["kentta_kulku"][klikattuy][klikattux] == " ":
            klikkausmaara.append("k")
            tila["kentta_kulku"][klikattuy][klikattux] = tila["kentta"][klikattuy][klikattux]
            if tila["kentta"][klikattuy][klikattux] == "0":
                tulvataytto(tila["kentta"], tila["kentta_kulku"], klikattux, klikattuy)
            elif tila["kentta"][klikattuy][klikattux] == "x":
                print("Hävisit pelin :(")
                tila["pelaa"] = False
                haravasto.lopeta()
                tulos = "Häviö"
                tallenna_peli(tulos)
        elif painike == "oikea" and tila["kentta_kulku"][klikattuy][klikattux] == " ":
            klikkausmaara.append("k")
            tila["kentta_kulku"][klikattuy][klikattux] = "f"    
        elif painike == "oikea" and tila["kentta_kulku"][klikattuy][klikattux] == "f":
            klikkausmaara.append("k")
            tila["kentta_kulku"][klikattuy][klikattux] = " "
        ruudut_jaljella = 0
        for i in tila["kentta_kulku"]:
            for j in i:
                if j in (" ", "f"):
                    ruudut_jaljella += 1
        if ruudut_jaljella == miinat and tila["pelaa"] is True:
            tila["pelaa"] = False
            print("Voitit pelin :)")
            haravasto.lopeta()
            tulos = "Voitto"
            tallenna_peli(tulos)
            
def tallenna_peli(lopputulos):
    """
    Tallentaa pelin tulokset tiedostoon. Tallentaa päivämäärän, pelin päättymisajan, 
    keston, lopputuloksen, kentän koon ja miinamäärän sekä klikkausmäärän.
    """
    aikatiedot = datetime.datetime.now()
    pvm = aikatiedot.strftime("%d/%m/%Y")
    aika = aikatiedot.strftime("%H:%M:%S")
    kesto = aikatiedot - aloitusaika
    kestomin = round(kesto.total_seconds() / 60, 2)
    klm = len(klikkausmaara)
    with open("miinatulokset.txt", "a") as tulokset:
        tulokset.write(
                f" {nimi}: {pvm}, {aika} Pelin kesto: {kestomin} minuuttia."\
                f" {lopputulos} kentällä {leveys}x{korkeus} ja {miinat} miinalla. "\
                f"{klm} klikkausta. \n")
        
    
def main():
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    """
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(leveys * 40, korkeus * 40)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aloita()
    

if __name__ == "__main__":
    print("Tervetuloa pelaamaan miinaharavaa!")
    nimi = input("Anna nimesi: ")
    while True:
        print("Valitse jokin alla olevista vaihtoehdoista:"
                "\n Pelaa(P) \n Tilastot(T) \n Lopeta(L)")
        valinta = input("Anna valintasi: ").lower().strip()
    
        if valinta == "p":
            klikkaukset = []
            while True:
                try:
                    leveys = int(input("Anna kentän leveys: "))
                    korkeus = int(input("Anna kentän korkeus: "))
                    miinat = int(input("Anna miinojen lukumäärä: "))
                    if leveys == 1 and korkeus == 1:
                        print("kentän tulee olla suurempi kuin 1x1")
                        break
                    if miinat > leveys * korkeus:
                        print("Tälle kentälle ei mahdu näin monta miinaa")
                        break
                except ValueError:
                    print("Anna kokonaisluku")
                else:
                    tila["kentta"], tila["kentta_kulku"] = luo_kentta(korkeus, leveys, miinat)
                    tila["pelaa"] = True
                    aloitusaika = datetime.datetime.now()
                    klikkausmaara.clear()
                    main()
                    break
           
        elif valinta == "t":
            with open("miinatulokset.txt", "r") as miinatulokset:
                tulosteet = miinatulokset.read()
                print(tulosteet)
        elif valinta == "l":
            break
        else:
            print("Tämä ei ole vaihtoehto!")
    