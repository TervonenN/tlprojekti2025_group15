# Tietoliikenteen sovellusprojekti 2025 / Ryhmä 15

> IoT-sensoridatan keräys, tallennus ja haku - nRF5340 DK, Raspberry & Linux/MySQL

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained-Yes-brightgreen.svg)](https://github.com/TervonenN/tlprojekti2025_group15)

## 📋 Sisällysluettelo

- [Yleiskatsaus](#yleiskatsaus)
- [Järjestelmäarkkitehtuuri](#järjestelmäarkkitehtuuri)
- [Ominaisuudet](#ominaisuudet)
- [Teknologiat](#teknologiat)
- [Projektivaiheet](#projektivaiheet)
- [Tiimi](#tiimi)

---

## 🎯 Yleiskatsaus

Tämä projekti on toteutettu osana Oulun ammattikorkeakoulun **Tietoliikenteen sovellusprojekti-kurssia** syksyllä 2025. Projekti yhdistää IoT-laitteet, langattoman tiedonsiirron, tietokantahallinnan ja koneoppimisen kokonaisuudeksi, joka havaitsee ja luokittelee laitteen suuntaa kiihtyvysanturidatan perusteella

### 🎯 Projektin Tavoitteet
Projektin päätavoitteena on rakentaa toimiva IoT-järjestelmä, jossa:
- **NRF5340 Development Kit** - mikrokontrolleri mittaa kiihtyvyysanturidataa
- Data välitetään **Bluetooth Low Energy (BLE)** - yhteydellä Raspberry Pi:lle.
- Raspberry Pi tallentaa datan **MYSQL-tietokantaan**
- **K-means-koneoppimisalgoritmi** opetetaan luokittelemaan laitteen suunta
- Opetettu malli siirretään takaisin mikrokontrollerille reaaliaikaiseen päättelyyn (Confusion Matrix)

---

## 🖼️ Projektin Juliste (Posteri)

Juliste tarjoaa tiivistetyn yleiskuvan projektin tavoitteista, menetelmistä ja keskeisistä tuloksista.

![Posteri: Tietoliikenteen sovellusprojekti](docs/posteriTurtinenTervonen.png)

---

## 🏗️ Järjestelmäarkkitehtuuri

![Arkkitehtuurikaavio](docs/arkkitehtuuri2.png)

### Komponentit

## 🔧 Teknologiat ja Työkalut

### Laitteisto
- **nRF5340 Development Kit**: Nordic Semiconductorin kehitysalusta
- **Raspberry Pi v3**: IoT-reititin ja BLE-väylä
- **Ubuntu Linux -palvelin**: Web-palvelin ja sovellusrajapinnat
- **Kiihtyvyysanturi**: 3-akselinen anturi (x, y, z -mittaukset)

### Ohjelmistot ja Protokollat
- **Zephyr RTOS** - Mikrokontrollerin käyttöjärjestelmä
- **Bluetooth Low Energy (BLE)** - Langaton tiedonsiirto
- **Python 3.x** - Datan käsittely ja koneoppiminen
  - `mysql-connector-python` - Tietokantayhteys
  - `numpy` - Matriisioperaatiot ja K-means-algoritmi
  - `matplotlib` - Visualisointi
- **MySQL** - Relaatiotietokannat
- **Apache + PHP** - Web-palvelin ja HTTP-rajapinnat
- **GitHub** - Versionhallinta ja projektin dokumentointi

### Kehitystyökalut
- **Visual Studio Code** - Pääasiallinen kehitysympäristö
- **nRF Connect** - BLE-yhteyksien testaus ja debuggaus
- **Wireshark & tcpdump** - Verkkoliikenteen analysointi
- **Thunder Client** - REST API -testaus
- **WinSCP** - Tiedostojen siirto palvelimille
---

## 📊 Projektin Eteneminen Viikoittain

### Viikko 1: Projektin Perustus ja Työkalut
**Toteutetut toiminnot:**
- GitHun-repositoryn ja projektin luonti
- Kanban-taulun käyttöönotto projektinhallintaan
- Markdown-dokumentaation aloitus
- nRF5340 Development Kit -alustan työkalujen asennus
- Kiihtyvyysanturin testaus ja datan lukeminen
- Git-versionhallinnan perusteet
- Arkkitehtuurikaavion suunnittelu

**Opittua:**
- Scrum-menetelmän perusteet
- Git-työskentely tiimissä
- Markdown-dokumentointi
- Kanban-projektin hallinta

### Viikko 2: BLE-kommunikaatio ja ADC-integraatio

**Toteutetut toiminnot:**
- Raspbery Pi -asetukset ja verkkoliitäntä
- Python-ohjelma BLE-datan vastaanottoon
- MySQL-tietokantayhteys ja datan tallennus
- Apache + PHP -asennus Ubuntu-palvelimelle
- PHP-skripti datan hakemiseen tietokannasta
- Netfilter-palomuurin konfigurointi
- TCP-asiakasohjelma Pythonilla

**Opitut taidot:**
- Bluetooth Low energy -kommunikaatio
- MySQL-tietokantaoperaatiot Pythonilla
- Web-palvelimen konfigurointi
- Verkkoliikenteen kaappaus ja analysointi Wiresharkilla
- SSH-avainpohjainen kirjautuminen (ed25519)

### Viikko 3: Rajapinnat ja Protokollat
**Toteutetut toiminnot:**
- HTTP REST API -rajapintojen testaus
- CSV-muotoisen datan käsittely
- MySQL-yhteyden optimointi
- Thunder Client -testit
- GraphQL-kyselyt
- Socket-pohjainen TCP-client (portti 20000)

**Opitut taidot:**
- REST API -suunnittelu ja testaus
- HTTP-protokollan yksityiskohdat
- CSV -dataformaatti
- Socket-ohjelmointi Pythonilla
- API-testien automatisointi

### Viikko 4: 
**Toteutetut toiminnot**

**Opitut taidot:**

### Viikko 5:
**Toteutetut toiminnot**

**Opitut taidot:**

###  Viikko 6:
**Toteutetut toiminnot**

**Opitut taidot**

### Viikko 7:




---

## 👥 Tiimi

**Group 15**

- **Niko Tervonen** - TervonenN
- **Meri-Tuulia Turtinen** - m351351

**Kurssi:** Tietoliikenteen sovellusprojekti 2025  
**Toteutusaika:** Syksy 2025

---

## 📄 Lisenssi

Tämä projekti on lisensoitu **MIT-lisenssillä**.

Katso [LICENSE](LICENSE) lisätietoja varten.


---

## 🙏 Kiitokset

Kiitos ohjaajille **Teemu Korpela** (t2946282) ja **Kari Jyrkkä** (kajyrkka) erinomaisesta ohjauksesta ja tuesta projektin aikana

Kiitos myös Oulun ammattikorkeakoululle laitteistojen ja infrastruktuurin tarjoamisesta.

---

**Oulun ammattikorkeakoulu** | Tietoliikenteen sovellusprojekti 2025 | Ryhmä 15

*Projekti suoritettu syksyllä 2025 osana 15 opintopisteen kokonaisuutta, joka sisälsi sovellusprojektin, viestinnän ja liiketoimintaosaamisen osa-alueet.

<div align="center">

**Tehty ❤️:llä Group 15:n toimesta**

</div>
