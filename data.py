'''Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License. '''
import json  #json imp
import os  #os imp
from cryptography.fernet import Fernet  #fernet imp

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  #projekta saknes cels
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')  #datu mapes cels
KEY_FILE = os.path.join(DATA_DIR, 'key.key')  #atslegas faila cels
ENC_FILE = os.path.join(DATA_DIR, 'products.json.enc')  #sifreta json faila cels
PLAIN_FILE = os.path.join(DATA_DIR, 'products.json')  #plain json faila cels

os.makedirs(DATA_DIR, exist_ok=True)  #izveido data mapi ja nav

initial_products = [  #saraksts ar produktiem
    {"id": "1", "name": "Kafija", "price": 3.50, "stock": 20},
    {"id": "2", "name": "Tēja", "price": 2.00, "stock": 30},
    {"id": "3", "name": "Šokolāde", "price": 1.50, "stock": 50},
    {"id": "4", "name": "Cepumi", "price": 2.20, "stock": 40},
    {"id": "5", "name": "Enerģ. dzēriens Monster", "price": 1.49, "stock": 50},
    {"id": "6", "name": "Enerģ. dzēriens Lucky punch", "price": 1.10, "stock": 15},
    {"id": "7", "name": "Enerģ. dzēriens Dynamite", "price": 1.59, "stock": 40},
    {"id": "8", "name": "Siers", "price": 4.50, "stock": 100},
    {"id": "9", "name": "Kūpināta makrele", "price": 4.20, "stock": 50000}
]

def create_key_if_missing():  #izveidot atslēgu ja trukst
    if not os.path.exists(KEY_FILE):  #ja atslēgas fails neeksiste
        key = Fernet.generate_key()  #veido jaunu fernet atslēgu
        with open(KEY_FILE, 'wb') as f:  #atver atslēgas failu rakstisanai
            f.write(key)  #ieraksta atslēgu faila
        print("atslega uztaisita", KEY_FILE)  #izvada zinu
    else:  #ja fails jau eksiste
        print("ir jau atslega", KEY_FILE)  #izvada ziņu ka atslega jau ir

def create_plain_json():  #funkcija izveidot plain json ja trukst
    if not os.path.exists(PLAIN_FILE):  #ja plain fails neeksiste
        with open(PLAIN_FILE, 'w', encoding='utf-8') as f:  #atver plain failu rakstīšanai ar utf-8
            json.dump(initial_products, f, ensure_ascii=False, indent=2)  #ieraksta inicialos produktus json formata
        print("Izveidots", PLAIN_FILE)  #izvada ziņu par izveidi
    else:  #ja fails jau eksiste
        print("eksiste jau", PLAIN_FILE)  #izvada ziņu ka fails jau eksiste

def encrypt_plain_to_enc():  #funkcija sifret plain json uz enc failu
    with open(KEY_FILE, 'rb') as f:  #atver atslegas failu
        key = f.read()  #nolasa atslegu
    fernet = Fernet(key)  #izveido fernet objektu ar atslegu
    if os.path.exists(PLAIN_FILE):  #ja plain fails eksiste
        with open(PLAIN_FILE, 'rb') as f:  #atver plain failu lasisanai
            raw = f.read()  #nolasa plain failu
    else:  #ja plain fails neeksiste
        raw = json.dumps(initial_products, ensure_ascii=False, indent=2).encode('utf-8')  #inicialos produktus uz utf-8

    encrypted = fernet.encrypt(raw)  #sifree raw ar fernet
    with open(ENC_FILE, 'wb') as f:  #atver enc failu rakstisanai
        f.write(encrypted)  #ieraksta sifretos faila
    print("!SIFRETS!", ENC_FILE)  #izvada pazinojumu par sifresanu

def main():  #galvena funkcija
    create_key_if_missing()  #izsauc atslēgas izveidi ja vajag
    create_plain_json()  #izsauc plain json izveidi ja vajag
    encrypt_plain_to_enc()  #izsauc sifresanu uz enc failu
    print("var laist programmu")  #izvada ka var palaist programmu

if __name__ == "__main__":  #ja skripts tiek palaists tiesi
    main()  #izsauc main funkciju