# 🚀 Automatisation de Configuration et Déploiement Réseau Multi-Sites (Cisco DevNet)

Ce projet a été réalisé dans le cadre du module **Cisco DevNet - Python**. Il vise à automatiser le déploiement des configurations réseau, la gestion des sauvegardes pré-déploiement et la vérification de l'infrastructure sur une architecture logique composée de 2 sites distants (Dakar et Abidjan).

---

## 📐 Architecture Réseau (2 Sites)

L'infrastructure s'articule autour d'une interconnexion WAN reliant les deux sites :

* **Site 1 (Dakar - `R1-DKR`) :** 
  * LAN : `10.10.10.0/24` (VLAN 10)
  * Interface passerelle : `10.10.10.1`
* **Site 2 (Abidjan - `R2-ABJ`) :** 
  * LAN : `10.20.10.0/24` (VLAN 20)
  * Interface passerelle : `10.20.10.1`
* **Lien WAN Inter-sites :** `192.168.20.0/30`
* **Routage Dynamique :** EIGRP AS 100 (avec la commande `no auto-summary` activée pour le routage des sous-réseaux spécifiques).

---

## 🛠️ Fonctionnalités du Script (`main.py`)

Le script d'automatisation Python s'appuie sur la bibliothèque **Netmiko** et exécute les tâches suivantes :

1. **Auto-détection de l'OS (`SSHDetect`) :** Identification automatique du type d'équipement Cisco avant d'établir la connexion SSH.
2. **Identification dynamique du rôle :** Lecture du prompt CLI pour déduire le rôle de l'équipement (Routeur, Switch Cœur, Switch Accès).
3. **Sauvegarde pré-déploiement (*Pre-check Backup*) :** Extraction et sauvegarde horodatée du `running-config` dans le dossier `backups/` (`HOSTNAME_YYYYMMDD_HHMMSS.cfg`).
4. **Injection de configuration propre :** Chargement des fichiers textes issus du dossier `configs/`, filtrage automatique des commentaires (`!`, `#`) et des commandes de mode (`configure terminal`, `end`).
5. **Persistance et Journalisation :** Sauvegarde des configurations en NVRAM (`copy running-config startup-config`) et enregistrement détaillé des événements dans `logs/deployment.log`.

---

## 📁 Structure du Dépôt

```text
.
├── configs/                # Fichiers de configuration par équipement (.txt)
│   ├── R1-DKR.txt
│   ├── R2-ABJ.txt
│   ├── SW1-CORE.txt
│   ├── SW2-CORE.txt
│   ├── SW1-ACC.txt
│   └── SW2-ACC.txt
├── backups/                # Sauvegardes pré-déploiement générées automatiquement
├── logs/                   # Fichiers de log d'exécution
│   └── deployment.log
├── inventory.yaml          # Fichier d'inventaire des équipements réseau
├── src/
│   └── main.py             # Script principal d'automatisation Netmiko
└── README.md               # Documentation du projet
