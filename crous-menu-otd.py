#!/usr/bin/env python3
from datetime import datetime
from bs4 import BeautifulSoup
import requests

days: dict[str, str] = {
  'Monday': 'lundi',
  'Tuesday': 'mardi',
  'Wednesday': 'mercredi',
  'Thursday': 'jeudi',
  'Friday': 'vendredi',
  'Saturday': 'samedi',
  'Sunday': 'dimanche'
}

months: dict[str, str] = {
  'January': 'janvier',
  'February': 'février',
  'March': 'mars',
  'April': 'avril',
  'May': 'mai',
  'June': 'juin',
  'July': 'juillet',
  'August': 'août',
  'September': 'septembre',
  'October': 'octobre',
  'November': 'novembre',
  'December': 'décembre'
}

def get_today_str():
  split = datetime.today().strftime('%A %-d %B %Y').split(' ')
  split[0] = days[split[0]] # translate day
  split[2] = months[split[2]] # translate month
  return ' '.join(split)

def parse(url: str):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  all_menus = soup.find_all('div', { 'class': 'menu'})
  today_str = get_today_str()
  for menu in all_menus:
    menu_date = menu.find('time').get_text()
    if today_str in menu_date:
      print("FOUND THE MENU!!")
      return menu.find('ul', { 'class': 'meal_foodies'})
    
def print_menu(menu_element):
  for section in menu_element.children:
    section_str = section.encode().decode()
    section_str = section_str[4:] # remove <li> prefix
    section_str = section_str.replace('</li></ul></li>', '\n') # section separator
    section_str = section_str.replace('<ul>', '\n') # title <> first entry separator
    section_str = section_str.replace('<li>', '\t') # sub-entry indent (actual food)
    section_str = section_str.replace('</li>', '\n') # sub-entries separator
    print(section_str)

# DEBUG 
def print_menu_str(menu_str):
  for section_str in menu_str:
    section_str = section_str[4:]
    section_str = section_str.replace('</li></ul></li>', '\n')
    section_str = section_str.replace('<ul>', '\n')
    section_str = section_str.replace('<li>', '\t')
    section_str = section_str.replace('</li>', '\n')
    print(section_str)

lamazone = 'https://www.crous-bordeaux.fr/restaurant/resto-u-n1-ferme-pour-travaux-2/'
today_menu = parse(lamazone)
# DEBUG
# today_menu = [
#   "<li>ENTREES<ul><li>menu non communiqué</li></ul></li>",
#   "<li>PLAT DU JOUR - STAND 1<ul><li>Sauté de dinde à la vanille</li><li>Boulgour aux amandes</li><li>Poêlée de poivrons</li></ul></li>",
#   "<li>PLAT DU JOUR - STAND 3<ul><li>Sauté de dinde à la vanille</li><li>Boulgour aux amandes</li><li>Poêlée de poivrons  Ou</li><li>Alternative sans viande :</li><li>Flan courgettes parmesan</li></ul></li>",
#   "<li>DESSERT<ul><li>Dessert lacté ou Fruit ou Compote BIO</li><li>Fromage blanc BIO</li><li>Tarte noix de coco</li><li>( Dessert supplément )</li><li>Pain BIO</li></ul></li>"
# ]
# print_menu_str(today_menu)
print_menu(today_menu)