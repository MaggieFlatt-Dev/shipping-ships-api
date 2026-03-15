import sqlite3
import json

def create_ship(ship_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Ship
                (name, hauler_id)
                VALUES (?, ?)
            """,
            (ship_data['name'], ship_data['hauler_id']),
        )

        new_ship_id = db_cursor.lastrowid

    return new_ship_id

def update_ship(id, ship_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Ship
                SET
                    name = ?,
                    hauler_id = ?
            WHERE id = ?
            """,
            (ship_data['name'], ship_data['hauler_id'], id)
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False

def delete_ship(pk):
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        DELETE FROM Ship WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def list_ships(url):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if "_expand" in url["query_params"]:
        # Write the SQL query to get the information you want
            db_cursor.execute("""
                SELECT
                    s.id,
                    s.name,
                    s.hauler_id,
                    h.id hauler_id,
                    h.name hauler_name,
                    h.dock_id hauler_dock_id
                FROM Ship s
                JOIN Hauler h ON h.id = s.hauler_id
            """)
        else: 
            db_cursor.execute("""
                SELECT
                    s.id,
                    s.name,
                    s.hauler_id 
                FROM Ship s
            """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        if "_expand" in url["query_params"]:
            ships = []
            for row in query_results:
                hauler = {
                    "id": row['hauler_id'],
                    "name": row['hauler_name'],
                    "dock_id": row["hauler_dock_id"]
                 }
                ship = {
                    "id": row['id'],
                    "name": row['name'],
                    "hauler_id": row["hauler_id"],
                    "hauler": hauler
                 }
                ships.append(ship)
        
        else:
            ships=[]
            for row in query_results:
                ships.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_ships = json.dumps(ships)

    return serialized_ships

def retrieve_ship(url, pk):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if "_expand" in url["query_params"]:
        # Write the SQL query to get the information you want
           db_cursor.execute("""
                SELECT
                    s.id,
                    s.name,
                    s.hauler_id,
                    h.id hauler_id,
                    h.name hauler_name,
                    h.dock_id hauler_dock_id
                FROM Ship s
                JOIN Hauler h ON h.id = s.hauler_id
                WHERE s.id = ?
            """, (pk,))
        else: 
            db_cursor.execute("""
                SELECT
                    s.id,
                    s.name,
                    s.hauler_id 
                FROM Ship s
                WHERE s.id = ?
            """, (pk,))
        query_results = db_cursor.fetchone()

        if "_expand" in url["query_params"]:
            row = query_results
            ship = {
                "id": row['id'],
                "name": row['name'],
                "hauler_id": row["hauler_id"],
                "hauler": {
                    "id": row['hauler_id'],
                    "name": row['hauler_name'],
                    "dock_id": row["hauler_dock_id"]
                }
            }
            serialized_ship = json.dumps(ship)
        
        else:
            serialized_ship = json.dumps(dict(query_results))

        # # Serialize Python list to JSON encoded string
        # dictionary_version_of_object = dict(query_results)
        # serialized_ship = json.dumps(dictionary_version_of_object)

    return serialized_ship
