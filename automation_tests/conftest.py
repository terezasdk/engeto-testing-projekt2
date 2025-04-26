import pytest
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456"
}

@pytest.fixture(scope="session")
def db_connection():
    # Připojení k MySQL
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Vytvoření nové DB
    cursor.execute("DROP DATABASE IF EXISTS task_manager_test")
    cursor.execute("CREATE DATABASE task_manager_test")
    cursor.execute("USE task_manager_test")

    # Vytvoření tabulky
    cursor.execute("""
        CREATE TABLE Ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            status ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    yield conn

    # Úklid po testech
    cursor.execute("DROP DATABASE IF EXISTS task_manager_test")
    conn.close()