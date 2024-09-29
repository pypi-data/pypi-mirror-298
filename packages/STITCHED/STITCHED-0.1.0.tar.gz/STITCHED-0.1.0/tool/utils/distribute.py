import sqlite3


def get_overview(connection, category_field, category_table, count_field, count_table, foreign_key):
    """
        Get an overview of the distribution of one field, e.g. distribution of language on text.

        Parameters:
        - category_field: The category column of interest
        - category_table: The table that the category column belongs to.
        - count_field: The column of interest to be counted.
        - count_table: The table that the count column belongs to.
        - foreign_key: The foreign key connecting two tables.

        Returns:
        - Terminal output: table of distribution.
    """

    cursor = connection.cursor()

    query = f"""
    SELECT 
        {category_table}.{category_field} AS source,
        COUNT({count_table}.{count_field}) AS count,
        ROUND((COUNT({count_table}.{count_field}) * 100.0 / total.total_count),2) AS percentage
    FROM
        {count_table}
    JOIN
        {category_table}
    ON
        {count_table}.{foreign_key} = {category_table}.{foreign_key},
        (SELECT COUNT(*) AS total_count FROM {count_table}) AS total
    GROUP BY 
        {category_table}.{category_field}
    """

    cursor.execute(query)
    results = cursor.fetchall()

    # Print the header with specified widths
    print("{:<10} | {:<10} | {:<10}".format("Category", "Count", "Percentage"))
    print("-" * 42)

    # Print each row with specified widths
    for row in results:
        print("{:<10} | {:<10} | {:<10}%".format(row[0], row[1], row[2]))

    # Close the database connection
    connection.close()


# %%
if __name__ == '__main__':
    db_path = '../../../hate_speech_data.db'
    conn = sqlite3.connect(db_path)
    get_overview(conn, 'language','language', 'text','text', 'language_id')
    # get_overview(db_path, 'source','text_source', 'text','text', 'source_id')