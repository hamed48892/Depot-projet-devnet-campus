import os

import yaml

import logging

from datetime import datetime

from netmiko import ConnectHandler, SSHDetect

from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException



logging.basicConfig(

    filename='logs/deployment.log',

    level=logging.INFO,

    format='%(asctime)s - %(levelname)s - %(message)s'

)



def load_inventory(filepath="inventory.yaml"):

    with open(filepath, "r") as f:

        return yaml.safe_load(f)["devices"]



def get_role_from_prompt(prompt):

    hostname = prompt.rstrip("#>").strip()

    if hostname.startswith("R"):

        return "routeur", hostname

    elif "CORE" in hostname:

        return "core", hostname

    elif "ACC" in hostname:

        return "acces", hostname

    return "inconnu", hostname



def load_config_commands(hostname):

    path = f"configs/{hostname}.txt"

    if not os.path.exists(path):

        raise FileNotFoundError(f"Fichier de configuration introuvable : {path}")

    with open(path, "r", encoding="utf-8") as f:

        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]



def deploy():

    os.makedirs("backups", exist_ok=True)

    os.makedirs("logs", exist_ok=True)

    devices = load_inventory()



    for dev in devices:

        ip = dev["host"]

        print(f"\n Connexion vers {ip}...")

        try:

            # 1. Autodétection du type OS avec SSHDetect

            guesser = SSHDetect(**dev)

            dev["device_type"] = guesser.autodetect()

            print(f"   OS détecté : {dev['device_type']}")



            with ConnectHandler(**dev) as net:

                net.enable()

                

                # 2. Identification dynamique via le prompt

                prompt = net.find_prompt()

                role, hostname = get_role_from_prompt(prompt)

                print(f"   Équipement : {hostname} | Rôle : {role}")



                # 3. Sauvegarde pré-déploiement

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                backup_filename = f"backups/{hostname}_{timestamp}.cfg"

                running_config = net.send_command("show running-config")

                with open(backup_filename, "w") as bf:

                    bf.write(running_config)

                print(f"   Backup sauvegardé : {backup_filename}")



                # 4. Application des configurations

                commands = load_config_commands(hostname)

                output = net.send_config_set(commands)

                print(f"   Configuration appliquée avec succès sur {hostname}.")

                

                # 5. Écriture en NVRAM

                net.save_config()

                logging.info(f"Déploiement réussi sur {hostname} ({ip})")



        except NetmikoAuthenticationException:

            err = f"Échec d'authentification sur {ip}"

            print(f"   {err}")

            logging.error(err)

        except NetmikoTimeoutException:

            err = f"Timeout / Équipement injoignable : {ip}"

            print(f"   {err}")

            logging.error(err)

        except Exception as e:

            err = f"Erreur sur {ip} : {str(e)}"

            print(f"   {err}")

            logging.error(err)



if __name__ == "__main__":

    deploy() 

