# Django-sovellusten ajaminen Kapsissa

Tämä ohje kuvaa yhden tavan ajaa [Django](https://www.djangoproject.com/)-sovelluksia 
[Kapsissa](https://www.kapsi.fi/). Ohjeessa on huomioitu 
[vuoden 2017 verkkosivu-uudistuksen](https://www.kapsi.fi/ohjeet/web2.html) tuomat muutokset.

Tässä ohjeessa pystytetään [django-wiki](https://github.com/django-wiki/django-wiki) julkiseen osoitteeseen
`http://<tunnus>.kapsi.fi/kapsi-django-ohje`. Sovelluspalvelimena toimii [gunicorn](https://gunicorn.org/).

Pythonin, Djangon ja muiden kirjastojen versiot on valittu niin, että ne toimivat Kapsissa. Huolehdi itse, 
että "tuotantokäytössä" kirjastot ovat ajan tasalla niin vältyt tietoturvaongelmilta.


## Kirjaudu webapp1-palvelimelle

Aja kaikki komennot webapp1-palvelimella, ellei muuta mainita.
```
ssh <tunnus>@webapp1.kapsi.fi
```


## Ympäristön pystytys

Kloonaa tämä repo sites-hakemistoosi:
```
cd ~/sites/<tunnus>.kapsi.fi/
git clone https://github.com/suniala/kapsi-django-ohje.git
```

Luo paikallinen Python-ympäristö:
```
cd kapsi-django-ohje
virtualenv -p python3.4 env
```

Asenna paikalliseen ympäristöön Django ja django-wiki:
```
env/bin/pip install -r requirements.txt
```

## Kokeile sovellusta

Laita sovelluksen asetukset kuntoon. Kopioi mallista oma asetustiedostosi:
```
cd ~/sites/<tunnus>.kapsi.fi/kapsi-django-ohje/
cp kirja/settings.py.tmpl kirja/settings.py
```

Täytä puuttuvat kohdat `kirja/settings.py` -tiedostoon. Löydät ne hakemalla sanaa "TODO".

Pystytä sitten tietokanta (mallikonfiguraatiossa käytetään paikkallista sqlite-kantaa). Huomaa,
että kätevyyden vuoksi `manage.py` viittaa paikallisen ympäristömme python-komentoon, eikä
sitä tarvitse erikseen sanoa tässä:
```
cd ~/sites/<tunnus>.kapsi.fi/kapsi-django-ohje/
./manage.py migrate
```

Käynnistä sitten sovelluspalvelin. Tässä vaiheessa voit arpoa porttinumeron itse 30000 ja 40000 väliltä:
```
env/bin/gunicorn \
    --bind webapp1.n.kapsi.fi:<portti> \
    --chdir /home/users/<tunnus>/sites/<tunnus>.kapsi.fi/kapsi-django-ohje/kirja wsgi
```

Jos gunicorn käynnistyy ilman virheitä, pitäisi sovellukseen päästä kiinni Kapsin sisältä,
esimerkiksi lakka-palvelimelta:
```
lynx http://webapp1.n.kapsi.fi:<portti>/kapsi-django-ohje/
```

Voit nyt sammuttaa gunicornin niin jatketaan säätämistä.


## Pääsy sovellukseen internetistä

Internetistä ei pääse webapp1-palvelimella pyörivään sovellukseen suoraan käsiksi.

> Yhteyksiä yhdistyksen palvelimille muualta internetistä on rajoitettu palomuurilla. Tämä estää 
palvelinohjelmien ajamisen ja IRC:n DCC-yhteydet. Jäsenet voivat kuitenkin pyytää ylläpidolta 
portteja käyttöönsä.
https://www.kapsi.fi/palvelut/portit.html

Pyydä siis itsellesi [porttia](https://www.kapsi.fi/palvelut/portit.html) lähettämällä sähköpostiä 
[ylläpidolle](https://www.kapsi.fi/tukipalvelut.html). Vastauksessa voi mennä pari päivää.

Kun ylläpito kertoo sinulle portin numeron, voit tehdä tarvittavan Apache-konfiguraation. Apache toimii
siis [proxynä](https://www.kapsi.fi/ohjeet/mod_rewrite.html#proxy), joka välittää internetistä tulevat
pyynnöt sisäverkossa sovelusspalvelimellemme. Lisää tiedostoon `sites/<tunnus>.kapsi.fi/www/.htaccess`:
```
RewriteEngine On
RewriteCond %{REQUEST_URI} ^/kapsi-django-ohje(.*)$
RewriteRule ^(.*)$ http://webapp1.n.kapsi.fi:<portti>/$1 [P]
```

Käynnistä gunicorn käyttäen saamaasi porttinumeroa ja mene selaimella osoitteeseen:
`http://<tunnus>.kapsi.fi/kapsi-django-ohje`

Tässä kohti kuvat ja tyylit vielä puuttuvat sivulta. Jos näyttää muuten toimivalta, niin tehdään
vielä viimeiset silaukset.


## Viimeistely

Luo hakemistot tiedostojen jakamista varten. Nämä voi nimetä miten vaan mutta tässä on ollut
ajatuksena, että static ja media-hakemistojen alla voisi olla useammankin sovelluksen tiedostoja:
```
mkdir -p /home/users/<tunnus>/sites/<tunnus>.kapsi.fi/www/static/kapsi-django-ohje/
mkdir -p /home/users/<tunnus>/sites/<tunnus>.kapsi.fi/www/media/kapsi-django-ohje/
```

Julkaise Django-sovelluksen tarvitsemat staattiset tiedostot:
```
cd ~/sites/<tunnus>.kapsi.fi/kapsi-django-ohje/
./manage.py collectstatic
```

Pääkäyttäjän tunnuksen voi luoda komentoriviltä. Tällä tunnuksella voi myös kirjautua
django-wikiin. Luo tunnus: 
```
./manage.py createsuperuser --username=<jokutunnus> --email=<jokusähköpostiosoite>
```

Tässä kohtaa kannattaa kokeilla gunicornin käynnistämistä uudestaan ja varmistaa, että sivustolla
näkyy tyylit ja kuvat oikein. Kirjaudu sisään, luo uusi sivu, lataa sinne kuvatiedosto ja
tarkista, että kuva näkyy tallennetulla sivulla. Näin varmistat, että myös media-hakemisto toimii.

Kokeile myös, että ylläpitosivusto toimii: `http://<tunnus>.kapsi.fi/kirja/yllapito`


## Sovelluspalvelimen ajaminen taustalla

TODO


## Palaute

Palaute on tervetullutta vaikkapa Githubin kautta (issues, pull requests).