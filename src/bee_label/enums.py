from enum import Enum


class JarSize(Enum):
    SMALL = "280g"
    MEDIUM = "500g"
    LARGE = "1kg"

class HoneyColor(str, Enum):
    PRUNELIER = "#DDA95D"
    MONTAGNE_BOURDAINE = "#DDA95D"
    BRUYERE_BLANCHE = "#B47131"
    BRUYERE_CENDREE = "#B47131"
    LAVANDE = "#FCE697"
    LAVANDE_STOECHAS = "#B47131"
    MONTAGNE = "#D49348"
    MAQUIS = "#B47131"
    ARBOUSIER = "#DDBE6D"
    RONCE = "#F0D36F"
    TILLEUL = "#DFD189"
    CHATAIGNIER = "#996A34"
    PISSENLIT = "#F4F477"
    BOURDAINE = "#DDA95D"

COLORS = {
    "Prunelier" : "#DDA95D",
    "Montagne bourdaine" : "#DDA95D",
    "Bruyere Blanche" : "#B47131",
    "Bruyere Cendrée" : "#B47131",
    "Lavande" : "#FCE697",
    "Lavande Stoechas" : "#B47131",
    "Montagne" : "#D49348",
    "Maquis" : "#B47131",
    "Arbousier" : "#DDBE6D",
    "Ronce" : "#F0D36F",
    "Tilleul" : "#DFD189",
    "Châtaignier" : "#996A34",
    "Pissenlit" : "#F4F477",
    "Bourdaine" : "#DDA95D",
}
