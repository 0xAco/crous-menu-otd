#!/usr/bin/env python3
from datetime import datetime
from bs4 import (BeautifulSoup, Tag)
import requests
import pyperclip

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

def get_today_str() -> str:
  split = datetime.today().strftime('%A %-d %B %Y').split(' ')
  split[0] = days[split[0]] # translate day
  split[2] = months[split[2]] # translate month
  return ' '.join(split)

def parse(url: str) -> Tag | None:
  response = requests.get(url)
  soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
  all_menus: list[Tag] = soup.find_all('div', { 'class': 'menu'})
  today_str = get_today_str()
  # menus day by day
  for menu in all_menus:
    # check the date
    menu_date: str = menu.find('time').get_text()
    if today_str in menu_date:
      return menu.find('ul', { 'class': 'meal_foodies'})
  return None

def format_menu(menu_element: Tag) -> str:
  menu_str: str = ""
  for section in menu_element.children:
    menu_str += section.encode().decode()
    menu_str = menu_str[4:] # remove <li> prefix
    menu_str = menu_str.replace('</li></ul></li>', '\n') # section separator
    menu_str = menu_str.replace('<ul>', '\n') # title <> first entry separator
    menu_str = menu_str.replace('<li>', '\t') # sub-entry indent (actual food)
    menu_str = menu_str.replace('</li>', '\n') # sub-entries separator
  return menu_str

lamazone: str = 'https://www.crous-bordeaux.fr/restaurant/resto-u-n1-ferme-pour-travaux-2/'
today_menu: Tag | None = parse(lamazone)
if today_menu is None:
  exit("uhoh couldn't find the menu - check it's a weekday, or maybe you got firewalled")
menu_str: str = format_menu(today_menu)

pyperclip.copy(menu_str) # copy to clipboard
print(menu_str) # print for feedback