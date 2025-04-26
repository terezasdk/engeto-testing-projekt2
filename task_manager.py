import mysql.connector
from mysql.connector import Error
from datetime import datetime

def vytvoreni_databaze():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456'
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS task_manager")
        print("Databáze 'task_manager' ověřena nebo vytvořena.")
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Chyba při vytváření databáze: {e}")

def pripojeni_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='task_manager'
        )
        return connection
    except Error as e:
        print(f"Chyba při připojení k databázi: {e}")
        return None

def vytvoreni_tabulky():
    connection = pripojeni_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                status ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
                created DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        connection.commit()
        cursor.close()
        connection.close()

def hlavni_menu():
    vytvoreni_databaze()
    vytvoreni_tabulky()
    while True:
        print("\n--- HLAVNÍ MENU ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Konec")
        volba = input("Vyberte možnost 1–5: ")
        if volba == '1':
            pridat_ukol()
        elif volba == '2':
            zobrazit_ukoly()
        elif volba == '3':
            aktualizovat_ukol()
        elif volba == '4':
            odstranit_ukol()
        elif volba == '5':
            print("Program ukončen.")
            break
        else:
            print("Neplatná volba. Zkuste znovu.")

def pridat_ukol():
    title = input("Zadejte název úkolu: ").strip()
    description = input("Zadejte popis úkolu: ").strip()
    if not title or not description:
        print("Název i popis jsou povinné.")
        return
    connection = pripojeni_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO ukoly (title, description) VALUES (%s, %s)", (title, description))
        connection.commit()
        print("Úkol byl přidán.")
        cursor.close()
        connection.close()

def zobrazit_ukoly():
    connection = pripojeni_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ukoly WHERE status IN ('Nezahájeno', 'Probíhá')")
        vysledky = cursor.fetchall()
        if not vysledky:
            print("Žádné aktivní úkoly.")
        else:
            print("\n--- Aktivní úkoly ---")
            for ukol in vysledky:
                print(f"{ukol['id']}: {ukol['title']} - {ukol['description']} | Stav: {ukol['status']}")
        cursor.close()
        connection.close()

def aktualizovat_ukol():
    connection = pripojeni_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, title, status FROM ukoly")
        ukoly = cursor.fetchall()
        if not ukoly:
            print("Žádné úkoly k aktualizaci.")
            return
        print("\n--- Úkoly ---")
        for ukol in ukoly:
            print(f"{ukol['id']}: {ukol['title']} | Stav: {ukol['status']}")
        try:
            id_ukolu = int(input("Zadejte ID úkolu pro změnu stavu: "))
            if not any(u['id'] == id_ukolu for u in ukoly):
                print("Neplatné ID.")
                return
        except ValueError:
            print("Zadejte platné číselné ID.")
            return
        print("1. Probíhá\n2. Hotovo")
        nova_volba = input("Zadejte nový stav (1 nebo 2): ")
        novy_stav = None
        if nova_volba == '1':
            novy_stav = 'Probíhá'
        elif nova_volba == '2':
            novy_stav = 'Hotovo'
        else:
            print("Neplatná volba stavu.")
            return
        cursor.execute("UPDATE ukoly SET status = %s WHERE id = %s", (novy_stav, id_ukolu))
        connection.commit()
        print("Stav úkolu byl aktualizován.")
        cursor.close()
        connection.close()

def odstranit_ukol():
    connection = pripojeni_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, title FROM ukoly")
        ukoly = cursor.fetchall()
        if not ukoly:
            print("Žádné úkoly k odstranění.")
            return
        print("\n--- Úkoly ---")
        for ukol in ukoly:
            print(f"{ukol['id']}: {ukol['title']}")
        try:
            id_ukolu = int(input("Zadejte ID úkolu, který chcete odstranit: "))
            if not any(u['id'] == id_ukolu for u in ukoly):
                print("Neplatné ID.")
                return
        except ValueError:
            print("Zadejte platné číselné ID.")
            return
        cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
        connection.commit()
        print("Úkol byl odstraněn.")
        cursor.close()
        connection.close()

hlavni_menu()