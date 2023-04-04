import os
import datetime
import random
from faker import Faker
from shop.models import Category, Product
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
from django.core.management import call_command
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'bitvoid.settings')
os.environ.setdefault('SEED', '23')




model = Faker(int(os.environ.get('SEED')))

ASSAULT_RIFLES = [
    'M4',
    'TAQ-56',
    'Kastov 762',
    'STB 556',
    'Lachmann-556',
    'M16',
    'Kastov 545',
    'Kastov-74u',
    'M13B',
    'Chimera',
    'ISO Hemlock'
]
BATTLE_RIFLES = [
    'Lachmann-762',
    'SO-14',
    'TAQ-V',
    "FTac Recon"
]
SMGS = [
    'VEL 46',
    'PDSW 528',
    'Fennec 45',
    'MX9',
    "Lachmann Sub",
    'Vaznek-9k',
    'FSS Hurricane',
    'Minibak',
    'BAS-P',
]
SHOTGUNS = [
    'Bryson 800',
    'Expedite 12',
    'Lockwood 300',
    'Bryson 890',
    'KV Broadside',
]
LMGS = [
    'SAKIN MG38',
    "RAAL MG",
    'HCR 56',
    '556 Icarus',
    'RPK',
    'RAPP H'
]
M_RIFLES = [
    'EBR-14',
    'SP-R 208',
    'Lockwood Mk2',
    'LM-S',
    'SA-B 50',
    'TAQ-M',
    'Crossbow',
    'Tempus Torrent'
]
S_RIFLES = [
    'MCPR-300',
    'Signal 50',
    'LA-B 330',
    'SP-X 80',
    'Victus XMR',
    'FJX Imperium'
]
HANDGUNS = [
    'P890',
    '.50 GS',
    'X12',
    'Basilisk',
    'X13 Auto'
]
LAUNCHERS = [
    'PILA',
    'STRELA-P',
    'JOKR',
    "RPG-7"
]
MELEE = [
    'Riot Shield',
    'Combat Knife',
    'Dual Kodachis'
]

LETHAL = [
    'Frag Grenade',
    'Proximity Mine',
    'Drill Charge',
    'Molotov Cocktail',
    "Semtex",
    "C4",
    "Claymore",
    'Thermite',
    "Throwing Knife",
    "Shuriken"
]
TACTICAL = [
    'Flash Grenade',
    'Shock Stick',
    'Spotter Scope',
    'Smoke Grenade',
    'Stun Grenade',
    'Decoy Grenade',
    'Stim',
    'Tear Gas',
    'Heartbeat Sensor',
    'Snapshot Grenade'
]

CATEGORIES = {
    "Assault Rifles": ASSAULT_RIFLES,
    "Battle Rifles": BATTLE_RIFLES,
    "Submachine Guns": SMGS,
    'Light Machine Guns': LMGS,
    'Shotguns': SHOTGUNS,
    'Marksman Rifles': M_RIFLES,
    "Sniper Rifles": S_RIFLES,
    "Melee": MELEE,
    "Handguns": HANDGUNS,
    "Launchers": LAUNCHERS,
    "Lethal Equipment": LETHAL,
    'Tactical Equipment': TACTICAL
}



def category_gen(random=False):
    if not random:
        for name in CATEGORIES:
            kwargs = {}
            kwargs['name'] = name
            kwargs['slug'] = slugify(name)
            yield make_category(**kwargs)
            

def product_gen(category=None):
    if not category:
        category = random.choice(Category.objects.all())
    names = CATEGORIES.get(category.name)
    for name in names:
        kwargs = {}
        kwargs['name'] = name
        kwargs['slug'] = slugify(name)
        
        kwargs['price'] = make_price()
        kwargs['description'] = str(input("Product description >>> ")).strip()
        if not kwargs['description']:
            kwargs['description'] = model.text(max_nb_chars=500)
        kwargs['category'] = category
        yield make_product(**kwargs)


def user_gen(count=1, password='onefullsend'):
    for c in range(count):
        kwargs = {}
        kwargs['password'] = make_password(password)
        kwargs['first_name'] = model.first_name()
        kwargs['last_name'] = model.last_name()
        kwargs['username'] = model.user_name()
        kwargs['email'] = model.email()
        yield make_user(**kwargs)


def make_user(**kwargs):
    return User.objects.create(**kwargs)


def make_category(**kwargs):
    return Category.objects.create(**kwargs)


def make_product(**kwargs):
    return Product.objects.create(**kwargs)


def make_price():
    pricetag = model.pricetag()
    pricetag = pricetag.replace('$', '').replace(',', '')
    pricetag = float(pricetag)
    return pricetag
