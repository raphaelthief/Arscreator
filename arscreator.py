import os, sys

# colorama
from colorama import init, Fore, Style

init() # Init colorama


BANNER = f'''{Fore.GREEN}
{Fore.CYAN}   ##     #####     ####   {Fore.WHITE}  ####    #####    ######     ##    {Fore.RED} ######    ####    #####
{Fore.CYAN}  ####    ##  ##   ##  ##  {Fore.WHITE} ##  ##   ##  ##   ##        ####   {Fore.RED}   ##     ##  ##   ##  ##
{Fore.CYAN} ##  ##   ##  ##   ##      {Fore.WHITE} ##       ##  ##   ##       ##  ##  {Fore.RED}   ##     ##  ##   ##  ##
{Fore.CYAN} ######   #####     ####   {Fore.WHITE} ##       #####    ####     ######  {Fore.RED}   ##     ##  ##   #####
{Fore.CYAN} ##  ##   ####         ##  {Fore.WHITE} ##       ####     ##       ##  ##  {Fore.RED}   ##     ##  ##   ####
{Fore.CYAN} ##  ##   ## ##    ##  ##  {Fore.WHITE} ##  ##   ## ##    ##       ##  ##  {Fore.RED}   ##     ##  ##   ## ##
{Fore.CYAN} ##  ##   ##  ##    ####   {Fore.WHITE}  ####    ##  ##   ######   ##  ##  {Fore.RED}   ##      ####    ##  ##
                                                                           {Fore.YELLOW}<{Fore.CYAN}raph{Fore.WHITE}aelt{Fore.RED}hief{Fore.YELLOW}>
{Fore.YELLOW}--- {Fore.BLUE}Cheat sheet generator for arsenal tool {Fore.YELLOW}---
{Fore.YELLOW}https://github.com/Orange-Cyberdefense/arsenal
'''



def charger_chemins(fichier_conf):
    if not os.path.exists(fichier_conf):
        with open(fichier_conf, 'w') as f:
            f.write('# Access Paths\n')
        return []

    with open(fichier_conf, 'r') as f:
        chemins = [ligne.strip() for ligne in f.readlines() if ligne.strip() and not ligne.startswith('#')]
    
    return chemins  

def sauvegarder_chemins(fichier_conf, chemins):
    with open(fichier_conf, 'w') as f:
        f.write('# Access Paths\n')
        for chemin in chemins:
            f.write(f'{chemin}\n')

def ajouter_fichier_md(chemin, chemins):
    nom_fichier = input(f"{Fore.CYAN}Enter the name of the .md file (without the extension) : {Fore.GREEN}") + '.md'
    titre = input(f"{Fore.CYAN}Enter the title : {Fore.GREEN}")

    tags_input = input(f"{Fore.CYAN}Enter the tags (separated by spaces) : {Fore.GREEN}")
    tags = ' '.join(f'#{tag.strip()}' for tag in tags_input.split() if tag.strip())  

    contenu = f"# {titre}\n\n{tags}\n\n"
    
    if not os.path.exists(chemin):
        os.makedirs(chemin)

    while True:
        titre_commande = input(f"{Fore.CYAN}Enter the title of the command (or type 'exit' to finish) : {Fore.GREEN}")
        if titre_commande.lower() == 'exit':
            break  

        commande = input(f"{Fore.CYAN}Enter the command : {Fore.GREEN}")
        contenu += f"## {titre_commande}\n```\n{commande}\n```\n\n"

    chemin_fichier = os.path.join(chemin, nom_fichier)
    with open(chemin_fichier, 'w') as f:
        f.write(contenu)

    print(f"{Fore.YELLOW}[!] {Fore.GREEN}File  '{nom_fichier}' successfully added in '{chemin}'")
    
    if chemin not in chemins:
        chemins.append(chemin)
        sauvegarder_chemins('config.conf', chemins)

def ajouter_commande_md(chemin):
    fichiers_md = lister_fichiers_md(chemin)  
    if not fichiers_md:
        return  

    try:
        id_fichier = int(input(f"{Fore.CYAN}Enter the ID of the .md file to which you want to add a command : {Fore.GREEN}"))
        if 0 <= id_fichier < len(fichiers_md):
            chemin_fichier = os.path.join(chemin, fichiers_md[id_fichier])
            
            titre_commande = input(f"{Fore.CYAN}Enter the title of the command :{Fore.GREEN} ")
            commande = input(f"{Fore.CYAN}Enter the command :{Fore.GREEN} ")

            with open(chemin_fichier, 'a') as f:  
                f.write(f"\n## {titre_commande}\n```\n{commande}\n```\n\n")
                
            print(f"{Fore.YELLOW}[!] {Fore.GREEN}Command successfully added to the file '{fichiers_md[id_fichier]}'")
        else:
            print(f"{Fore.RED}[!] Invalid ID")
    except ValueError:
        print(f"{Fore.RED}[!] Please enter a valid number for the ID")

def lister_fichiers_md(chemin):
    fichiers_md = [f for f in os.listdir(chemin) if f.endswith('.md')]
    
    if fichiers_md:
        print(f"{Fore.YELLOW}[!] Present .md files :{Fore.GREEN}")
        for index, fichier in enumerate(fichiers_md):
            print(f" [{index}] {fichier}")
    else:
        print(f"{Fore.RED}[!] No .md files found in this directory")
    
    return fichiers_md

def supprimer_fichier_md(chemin):
    fichiers_md = lister_fichiers_md(chemin)  
    if not fichiers_md:
        return  

    try:
        id_fichier = int(input(f"{Fore.CYAN}Enter the ID of the .md file to delete : {Fore.GREEN}"))
        if 0 <= id_fichier < len(fichiers_md):
            chemin_fichier = os.path.join(chemin, fichiers_md[id_fichier])
            os.remove(chemin_fichier)
            print(f"{Fore.YELLOW}[!] {Fore.GREEN}File '{fichiers_md[id_fichier]}' successfully deleted")
        else:
            print(f"{Fore.RED}[!] Invalid ID")
    except ValueError:
        print(f"{Fore.RED}[!] Please enter a valid number for the ID")

def menu():
    fichier_conf = 'config.conf'
    chemins = charger_chemins(fichier_conf)
    
    print(BANNER)

    try:

        if not chemins:
            chemin_default = input(f"{Fore.RED}[!] The configuration file is empty. Please enter the path to my_cheat arsenal :{Fore.GREEN} ")
            chemins.append(chemin_default)
            sauvegarder_chemins(fichier_conf, chemins)
        
        while True:
            print(f"\n{Fore.YELLOW}Menu :")
            print(f"{Fore.YELLOW}1. {Fore.GREEN}Add a .md file")
            print(f"{Fore.YELLOW}2. {Fore.GREEN}Delete a .md file")
            print(f"{Fore.YELLOW}3. {Fore.GREEN}Add a command to a .md file")
            print(f"{Fore.YELLOW}4. {Fore.GREEN}Quit")

            choix = input(f"{Fore.YELLOW}Choose an option ({Fore.GREEN}1-4{Fore.YELLOW}) : ")
            
            if choix == '1':
                chemin = chemins[0]  
                ajouter_fichier_md(chemin, chemins)  
                
            elif choix == '2':
                chemin = chemins[0]  
                supprimer_fichier_md(chemin)

            elif choix == '3':
                chemin = chemins[0]  
                ajouter_commande_md(chemin)

            elif choix == '4':
                print(f"{Fore.YELLOW}[!] Ending ...")
                break

            else:
                print(f"{Fore.RED}[!] Invalid option. Please choose an option between 1 and 4")

    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] KeyboardInterrupt...\n{Fore.YELLOW}[!] Ending ...")
        sys.exit(0)


if __name__ == "__main__":
    menu()
