import json
import sqlite3

# Classe Singleton pour gérer une instance unique de la base de données de la bibliothèque
class LibraryDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialisation de la base de données SQLite
            cls._instance.connection = sqlite3.connect('library.db')
            cls._instance.cursor = cls._instance.connection.cursor()
            # Création des tables si elles n'existent pas
            cls._instance.cursor.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, category TEXT, available INTEGER)')
            cls._instance.cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
            cls._instance.connection.commit()
        return cls._instance
    
    def close(self):
        self.connection.close()
    
    # Méthodes pour ajouter et retirer des livres de la bibliothèque
    def add_book(self, title, author, category):
        self.cursor.execute('INSERT INTO books (title, author, category, available) VALUES (?, ?, ?, 1)', (title, author, category))
        self.connection.commit()

    def remove_book(self, book_title):
        self.cursor.execute('DELETE FROM books WHERE title = ?', (book_title,))
        self.connection.commit()

    # Méthodes pour emprunter et retourner des livres
    def borrow_book(self, book_id, user_id):
        self.cursor.execute('UPDATE books SET available = 0 WHERE id = ?', (book_id,))
        self.cursor.execute('INSERT INTO borrowed_books (book_id, user_id) VALUES (?, ?)', (book_id, user_id))
        self.connection.commit()

    def return_book(self, book_id, user_id):
        self.cursor.execute('UPDATE books SET available = 1 WHERE id = ?', (book_id,))
        self.cursor.execute('DELETE FROM borrowed_books WHERE book_id = ? AND user_id = ?', (book_id, user_id))
        self.connection.commit()

    # Méthode pour savoir qui détient un livre
    def get_book_holder(self, book_id):
        self.cursor.execute('SELECT users.name FROM users JOIN borrowed_books ON users.id = borrowed_books.user_id WHERE borrowed_books.book_id = ?', (book_id,))
        return self.cursor.fetchone()

    # Méthodes pour rechercher des livres par titre, auteur ou catégorie
    def search_books_by_title(self, title):
        self.cursor.execute('SELECT * FROM books WHERE title LIKE ?', ('%' + title + '%',))
        return self.cursor.fetchall()

    def search_books_by_author(self, author):
        self.cursor.execute('SELECT * FROM books WHERE author LIKE ?', ('%' + author + '%',))
        return self.cursor.fetchall()

    def search_books_by_category(self, category):
        self.cursor.execute('SELECT * FROM books WHERE category LIKE ?', ('%' + category + '%',))
        return self.cursor.fetchall()
    
    # Méthodes pour afficher les livres et les utilisateurs
    def display_books(self):
        self.cursor.execute('SELECT * FROM books')
        books = self.cursor.fetchall()
        print('/-----------------------------------------/')
        for book in books:
            print(book)
        print('/-----------------------------------------/')
    
    def display_users(self):
        self.cursor.execute('SELECT * FROM users')
        users = self.cursor.fetchall()
        print('/-----------------------------------------/')
        for user in users:
            print(user)
        print('/-----------------------------------------/')
    
    # Méthode pour sauvegarder l'état de la bibliothèque dans un fichier JSON
    def save_state(self, file_path):
        self.cursor.execute('SELECT * FROM books')
        books = self.cursor.fetchall()
        self.cursor.execute('SELECT * FROM users')
        users = self.cursor.fetchall()
        data = {'books': books, 'users': users}
        with open(file_path, 'w') as file:
            json.dump(data, file)

# Classe Factory pour créer des objets Livre
class BookFactory:
    @staticmethod
    def create_book(title, author, category):
        return Book(title, author, category)

# Classe Factory pour créer des objets Utilisateur
class UserFactory:
    @staticmethod
    def create_user(name):
        return User(name)

# Classe Livre
class Book:
    def __init__(self, title, author, category):
        self.title = title
        self.author = author
        self.category = category

# Classe Strategy pour différentes stratégies de recherche de livres
class BookSearchStrategy:
    def search(self, library, query):
        pass

# Recherche par titre
class TitleSearchStrategy(BookSearchStrategy):
    def search(self, library, query):
        return library.search_books_by_title(query)

# Recherche par auteur
class AuthorSearchStrategy(BookSearchStrategy):
    def search(self, library, query):
        return library.search_books_by_author(query)

# Recherche par catégorie
class CategorySearchStrategy(BookSearchStrategy):
    def search(self, library, query):
        return library.search_books_by_category(query)

# Classe Utilisateur
class User:
    def __init__(self, name):
        self.name = name

    # Méthodes pour enregistrer de nouveaux utilisateurs de la bibliothèque
    def add_user(self, name):
        self.cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
        self.connection.commit()

    # Méthode pour supprimer des utilisateurs de la bibliothèque
    def remove_user(self, user_name):
        self.cursor.execute('DELETE FROM users WHERE name = ?', (user_name,))
        self.connection.commit()

# Classe Observer pour notifier les utilisateurs lorsqu'un livre recherché devient disponible
class BookAvailabilityObserver:
    def __init__(self, library):
        self.library = library

    def notify(self, book_id):
        book_holder = self.library.get_book_holder(book_id)
        if book_holder is None:
            print('Le livre est maintenant disponible !')
        else:
            print(f'Le livre est détenu par {book_holder[0]}.')

if __name__ == '__main__':
    
    def display_menu():
        print('Menu:')
        print('1. Ajouter un livre')
        print('2. Retirer un livre')
        print('3. Rechercher un livre')
        print('4. Enregistrer un utilisateur')
        print('5. Supprimer un utilisateur')
        print('6. Emprunter un livre')
        print('7. Retourner un livre')
        print('8. Afficher les livres')
        print('9. Afficher les utilisateurs')
        print('10. Quitter')

    def execute_menu():
        while True:
            display_menu()
            choix = input("Choisissez une option: ")
            if choix == "1":
                title = input("Entrez le titre du livre: ")
                author = input("Entrez l'auteur du livre: ")
                category = input("Entrez la catégorie du livre: ")
                book = BookFactory.create_book(title, author, category)
                library.add_book(book.title, book.author, book.category)
                print(f"{title} a été ajouté à la bibliothèque")
            elif choix == "2":
                book_title = input("Entrez le titre du livre à retirer: ")
                library.remove_book(book_title)
                print(f"{title} a été retiré de la bibliothèque.")
            elif choix == "3":
                search_strategy = None
                print('Choisissez une stratégie de recherche:')
                print('1. Par titre')
                print('2. Par auteur')
                print('3. Par catégorie')
                search_strategy_choice = input('Choisissez une option: ')
                if search_strategy_choice == '1':
                    search_strategy = TitleSearchStrategy()
                elif search_strategy_choice == '2':
                    search_strategy = AuthorSearchStrategy()
                elif search_strategy_choice == '3':
                    search_strategy = CategorySearchStrategy()
                else:
                    print('Option invalide. Veuillez réessayer.')
                    continue
                search_query = input('Entrez votre recherche: ')
                results = search_strategy.search(library, search_query)
                print('Voici les résultats de la recherche :')
                print('/-----------------------------------------/')
                for result in results:
                    print(result)
                print('/-----------------------------------------/')
            elif choix == "4":
                name = input("Entrez le nom de l'utilisateur: ")
                user = UserFactory.create_user(name)
                library.add_user(user.name)
            elif choix == "5":
                user_name = input("Entrez le nom de l'utilisateur à supprimer: ")
                library.remove_user(user_name)
            elif choix == "6":
                book_id = input("Entrez l'ID du livre à emprunter: ")
                user_id = input("Entrez l'ID de l'utilisateur: ")
                if library.get_book_holder(book_id) is not None:
                    print('Le livre est déjà détenu par quelqu\'un.')
                else:
                    library.borrow_book(book_id, user_id)
            elif choix == "7":
                book_id = input("Entrez l'ID du livre à retourner: ")
                user_id = input("Entrez l'ID de l'utilisateur: ")
                library.return_book(book_id, user_id)
            elif choix == "8":
                library.display_books()
            elif choix == "9":
                library.display_users()
            elif choix == "10":
                break
            else:
                print("Option invalide. Veuillez réessayer.")

    library = LibraryDatabase()
    execute_menu()
    library.save_state('library.json')
    library.close()

display_menu()

