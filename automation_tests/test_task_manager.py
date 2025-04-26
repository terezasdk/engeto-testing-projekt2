import pytest

# ---------- Přidání úkolu ----------
def test_pridat_ukol_pozitivni(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("USE task_manager_test")
    title = "Testovací úkol"
    description = "Popis testovacího úkolu"
    cursor.execute("INSERT INTO Ukoly (title, description) VALUES (%s, %s)", (title, description))
    db_connection.commit()
    cursor.execute("SELECT * FROM Ukoly WHERE title = %s", (title,))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == title
    cursor.close()

def test_pridat_ukol_negativni(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("USE task_manager_test")
    with pytest.raises(Exception):
        cursor.execute("INSERT INTO Ukoly (title, description) VALUES (%s, %s)", (None, None))
        db_connection.commit()
    cursor.close()

# ---------- Aktualizace úkolu ----------
def test_aktualizovat_ukol_pozitivni(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("USE task_manager_test")
    cursor.execute("INSERT INTO Ukoly (title, description) VALUES (%s, %s)", ("Úkol k aktualizaci", "Popis"))
    db_connection.commit()
    cursor.execute("SELECT id FROM Ukoly WHERE title = %s", ("Úkol k aktualizaci",))
    task_id = cursor.fetchone()[0]
    cursor.execute("UPDATE Ukoly SET status = %s WHERE id = %s", ("Hotovo", task_id))
    db_connection.commit()
    cursor.execute("SELECT status FROM Ukoly WHERE id = %s", (task_id,))
    new_status = cursor.fetchone()[0]
    assert new_status == "Hotovo"
    cursor.close()

def test_aktualizovat_ukol_negativni(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("USE task_manager_test")
    non_existing_id = 999999
    cursor.execute("UPDATE Ukoly SET status = %s WHERE id = %s", ("Hotovo", non_existing_id))
    db_connection.commit()
    assert cursor.rowcount == 0
    cursor.close()

# ---------- Odstranění úkolu ----------
def test_odstranit_ukol_pozitivni(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("USE task_manager_test")
    cursor.execute("INSERT INTO Ukoly (title, description) VALUES (%s, %s)", ("Úkol ke smazání", "Popis"))
    db_connection.commit()
    cursor.execute("SELECT id FROM Ukoly WHERE title = %s", ("Úkol ke smazání",))
    task_id = cursor.fetchone()[0]
    cursor.execute("DELETE FROM Ukoly WHERE id = %s", (task_id,))
    db_connection.commit()
    cursor.execute("SELECT * FROM Ukoly WHERE id = %s", (task_id,))
    result = cursor.fetchone()
    assert result is None
    cursor.close()

def test_odstranit_ukol_negativni(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("USE task_manager_test")
    non_existing_id = 123456
    cursor.execute("DELETE FROM Ukoly WHERE id = %s", (non_existing_id,))
    db_connection.commit()
    assert cursor.rowcount == 0
    cursor.close()