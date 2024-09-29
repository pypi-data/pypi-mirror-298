import sqlite3
#create all tables
def setupSchema(conn):
    try:
        c = conn.cursor()
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("BEGIN")
        #%%
        c.execute('''
        CREATE TABLE IF NOT EXISTS dataset (
        dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_original_name TEXT NOT NULL UNIQUE,
        dataset_name TEXT NOT NULL UNIQUE,
        original_paper TEXT)
        ''')
        #%%
        c.execute('''
        CREATE TABLE IF NOT EXISTS schema (
            dataset_id INTEGER,
            label_name TEXT,
            PRIMARY KEY (dataset_id, label_name),
            FOREIGN KEY(dataset_id) REFERENCES dataset(dataset_id)
        )
        ''')
        #%%
        c.execute('''
        CREATE TABLE IF NOT EXISTS text_source (
            source_id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT UNIQUE
        )
        ''')
        #%%
        c.execute('''
        CREATE TABLE IF NOT EXISTS "language" (
            language_id INTEGER PRIMARY KEY AUTOINCREMENT,
            "language" TEXT UNIQUE
        )
        ''')
        #%%
        c.execute('''
        CREATE TABLE IF NOT EXISTS text (
            dataset_id INTEGER,
            text_id INTEGER,
            source_id INTEGER,
            language_id INTEGER,
            text TEXT,
            PRIMARY KEY (dataset_id, text_id),
            FOREIGN KEY(dataset_id) REFERENCES dataset(dataset_id),
            FOREIGN KEY(source_id) REFERENCES text_source(source_id),
            FOREIGN KEY(language_id) REFERENCES language(language_id)
        )
        ''')
        #%%
        c.execute('''
        CREATE TABLE IF NOT EXISTS label (
            dataset_id INTEGER,
            text_id INTEGER,
            label_name TEXT,
            label_value TEXT,
            label_definition TEXT,
            PRIMARY KEY (dataset_id, text_id, label_name),
            FOREIGN KEY(dataset_id, text_id) REFERENCES text(dataset_id, text_id)
        )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        c.close()
#  label_value NOT NULL


#clear all content in all tables, keep the schema
def resetDatabase(conn):
    try:
        c = conn.cursor()
        conn.execute("BEGIN")

        conn.execute("PRAGMA foreign_keys = OFF")

        c.execute('DELETE FROM label')
        c.execute('DELETE FROM text')
        c.execute('DELETE FROM language')
        c.execute('DELETE FROM text_source')
        c.execute('DELETE FROM schema')
        c.execute('DELETE FROM dataset')

        conn.execute("PRAGMA foreign_keys = ON")
        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        c.close()