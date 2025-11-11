#!/bin/bash

echo "Asetetaan perussäännöt..."

# Tyhjennetään vanhat säännöt
iptables -F

# Oletuspolitiikka: kaikki estetään paitsi lähtevät yhteydet
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Sallitaan olemassa olevat ja liittyvät yhteydet
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Sallitaan SSH (portti 22)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Sallitaan HTTP (portti 80)
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Sallitaan "takaovi" osoitteesta 193.167.100.97
iptables -A INPUT -p tcp -s 193.167.100.97 -j ACCEPT

# Sallitaan ICMP (ping)
iptables -A INPUT -p icmp -j ACCEPT

# Hylätään kaikki muu
iptables -A INPUT -j DROP

echo "Palomuuri asetettu"
