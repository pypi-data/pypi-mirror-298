import sqlite3
from collections import defaultdict

def search_and_count_labels(connection, keyword):
    # Connect to the SQLite database
    cursor = connection.cursor()
    
    # Perform a fuzzy search for rows where label_name and label_definition contain the keyword
    query = """
    SELECT dataset_id, label_name, label_definition FROM label
    WHERE label_name LIKE ? OR label_definition LIKE ?;
    """
    keyword = f"%{keyword}%"
    cursor.execute(query, (keyword, keyword))
    results = cursor.fetchall()
    
    # Count the number of rows for each dataset_id and collect related label_names and label_definitions
    dataset_info = defaultdict(lambda: {"count": 0, "label_names": set(), "label_definitions": set()})
    for row in results:
        dataset_id = row[0]
        label_name = row[1]
        label_definition = row[2]
        dataset_info[dataset_id]["count"] += 1
        dataset_info[dataset_id]["label_names"].add(label_name)
        dataset_info[dataset_id]["label_definitions"].add(label_definition)
    
    # Print the statistics
    print("dataset_id | count | label_names | label_definitions")
    for dataset_id, info in dataset_info.items():
        label_names = ", ".join(info["label_names"])
        label_definitions = ", ".join([ld for ld in info["label_definitions"] if ld is not None])
        print(f"{dataset_id} | {info['count']} | {label_names} | {label_definitions}")
    
    # Close the database connection
    conn.close()
#%%
if __name__ == "__main__":
    db_path = '../../../../hate_speech_data.db'
    conn = sqlite3.connect(db_path)
    keyword = input("Please enter the keyword: ")
    search_and_count_labels(conn, keyword)
