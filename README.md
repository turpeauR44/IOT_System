# IOT_System
  Deploy your IIOT network

## Some ressources
- myHelper : This page has been designed to list some cheatsheets, tutorials and FAQs [`here`](myHelper.md)

# Configure your Pi
1. Flash SD Card with Raspbian 

    Lite version might be prefered

2. Initial configuration

    2.1. Localisation

    2.2. Wireless LAN
    
    2.3. Hostname

    2.3. Change user settings
    ```bash
    sudo adduser myUser
    sudo adduser myUser sudo
    ```
    Temporarly allow to run sudo without password
    edit /etc/sudoers last row
    ```bash
    <myUser> ALL=(ALL) NOPASSWD:ALL
    ```
    2.4. Restart as myUser & Delete pi user 
    ```bash
    sudo deluser pi
    ```
3. Execution de l'initialisation
    3.1. Clone du fichier

    3.2 Execution du fichier step by step ou complète


    
