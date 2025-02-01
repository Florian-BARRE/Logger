# Logger
# Logger - Documentation Complète

## 1. Introduction
Le module **Logger** est une implémentation avancée de logging en Python. Il repose sur le module standard `logging` tout en améliorant ses capacités grâce à :

- Un **formatage avancé** avec couleurs personnalisables
- Une **gestion des logs** avec suppression automatique des anciens fichiers
- Un **système de monitoring** de l’espace disque et des fichiers journaux
- Des **décorateurs** pour mesurer le temps d’exécution et suivre les appels de fonctions
- Un **LoggerManager** permettant de gérer facilement et intuitivement plusieurs loggers dans les grands projets qui nécessitent une gestion centralisée des logs.

## 2. Installation
### Prérequis
Ce module utilise **Python 3.x** et dépend des bibliothèques suivantes :
```bash
pip install colorama
```

### Intégration dans un projet
Tu peux directement inclure ce module dans ton projet en important les fichiers nécessaires.

## 3. Fonctionnalités principales
### 3.1. Création et configuration d’un Logger
Un logger peut être initialisé avec des paramètres personnalisés :
```python
from logger.logger import Logger

logger = Logger(identifier="MyLogger", path="logs/")
logger.info("Ceci est un message informatif")
```

### 3.2. Gestion des niveaux de log
Le module propose plusieurs niveaux de log :
- **DEBUG**
- **INFO**
- **WARNING**
- **ERROR**
- **CRITICAL**
- **FATAL**

Exemple d’utilisation :
```python
logger.debug("Ceci est un message de débogage")
logger.fatal("Erreur fatale détectée")
```

### 3.3. Formatage des logs avec couleurs personnalisées
Le format des logs suit la structure :
```
<date(heure:min:s.ms)> -> [<identifiant>] [<fichier>:<ligne>] <niveau> | <message>
```
Il est également possible d’activer un formatage coloré.

### 3.4. Décorateurs de logging
Deux décorateurs sont disponibles pour suivre l’exécution des fonctions :

#### Décorateur `@log`
Permet de tracer automatiquement les appels de fonctions :
```python
from logger.decorators import log

@log()
def ma_fonction():
    print("Exécution...")
```

#### Décorateur `@time_tracker`
Mesure le temps d’exécution d’une fonction :
```python
from logger.decorators import time_tracker

@time_tracker()
def calcul():
    return sum(range(10000))
```

### 3.5. Configuration avancée
Le **LoggerConfig** permet d’ajuster le comportement du logger :
```python
from logger.logger_configs import LoggerConfig

config = LoggerConfig(identifier="AppLogger", path="/var/logs")
logger = Logger(config=config)
```

#### Options de configuration principales :
- **log_levels_config** : niveaux de log autorisés
- **placement_config** : mise en forme des logs
- **monitor_config** : activation du monitoring des fichiers

## 4. Gestion des fichiers de log et monitoring
Le module intègre un **DiskMonitor** pour surveiller l’espace disque et nettoyer les logs automatiquement.
```python
logger.disk_monitor.display_monitoring()
logger.disk_monitor.clean_logs()
```

## 5. Gestion centralisée avec LoggerManager
Le **LoggerManager** permet de gérer plusieurs instances de loggers :
```python
from logger.logger_manager import LoggerManager
LoggerManager.enable_unique_logger_identifier = True
```

## 6. Exemples d’utilisation
### 6.1. Logger simple avec couleur
```python
logger = Logger(identifier="App", colors=True)
logger.info("Lancement de l’application")
```

### 6.2. Logger avec sauvegarde dans un fichier
```python
logger = Logger(identifier="App", path="logs/app.log")
logger.warning("Problème détecté")
```

### 6.3. Logger avec décorateur
```python
@log()
def fonction_a_suivre():
    return "Donnée importante"
```

## 7. Conclusion
Le module **Logger** est un outil puissant pour structurer les logs d’une application Python en assurant leur lisibilité, stockage optimisé et supervision efficace.

N’hésitez pas à contribuer ou proposer des améliorations ! 🚀

