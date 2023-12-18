# Bibliothèque Python
Ce projet est une implémentation d'une bibliothèque en Python. Il permet de gérer des livres et des utilisateurs, ainsi que de rechercher des livres par titre, auteur ou catégorie.

## Fonctionnalités
Ajouter et supprimer des utilisateurs de la bibliothèque
Créer de nouveaux livres avec un titre, un auteur et une catégorie
Rechercher des livres par titre, auteur ou catégorie
Afficher la liste des livres et des utilisateurs de la bibliothèque
Notifier les utilisateurs lorsque les livres recherchés deviennent disponibles

## Structure du code

Le code est organisé en plusieurs classes :

- LibraryDatabase : 
Classe principale représentant la bibliothèque. Elle contient des méthodes pour gérer les utilisateurs, les livres et effectuer des recherches.

- BookFactory : 
Classe pour créer des objets Livre.

- UserFactory : 
Classe pour créer des objets Utilisateur.

- Book : 
Classe représentant un livre avec un titre, un auteur et une catégorie.

- BookSearchStrategy : 
Classe abstraite pour différentes stratégies de recherche de livres.

- TitleSearchStrategy, AuthorSearchStrategy, CategorySearchStrategy :
Classes pour effectuer des recherches par titre, auteur ou catégorie.

- User : 
Classe représentant un utilisateur de la bibliothèque.

- BookAvailabilityObserver : 
Classe pour notifier les utilisateurs lorsque les livres recherchés deviennent disponibles.

## Utilisation
Pour utiliser la bibliothèque, exécutez le fichier evaluation.py. Vous serez présenté avec un menu d'options pour interagir avec la bibliothèque. Les données de la bibliothèque sont sauvegardées dans un fichier JSON.

## Auteur
Ce projet a été développé par Claire Nguyen.
