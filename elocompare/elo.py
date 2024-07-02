def calculate_elo(item1, item2, winner, mysql):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT elo_rating FROM items WHERE name = %s', [item1])
    item1_rating = cursor.fetchone()['elo_rating']
    cursor.execute('SELECT elo_rating FROM items WHERE name = %s', [item2])
    item2_rating = cursor.fetchone()['elo_rating']

    K = 32
    expected_score_item1 = 1 / (1 + 10 ** ((item2_rating - item1_rating) / 400))
    expected_score_item2 = 1 / (1 + 10 ** ((item1_rating - item2_rating) / 400))

    if winner == item1:
        new_rating_item1 = item1_rating + K * (1 - expected_score_item1)
        new_rating_item2 = item2_rating + K * (0 - expected_score_item2)
    else:
        new_rating_item1 = item1_rating + K * (0 - expected_score_item1)
        new_rating_item2 = item2_rating + K * (1 - expected_score_item2)

    cursor.execute('UPDATE items SET elo_rating = %s WHERE name = %s', (new_rating_item1, item1))
    cursor.execute('UPDATE items SET elo_rating = %s WHERE name = %s', (new_rating_item2, item2))
    mysql.connection.commit()
