import config
import sqlite3


def save_player(player_name, player_id):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    sql_expression = """INSERT INTO player (name, player_id) VALUES(?, ?);"""
    data_tuple = (player_name, player_id)
    cursor.execute(sql_expression, data_tuple)
    conn.commit()
    conn.close()


def save_match(player1_site_id, player2_site_id, match_id):
    player1_id = get_internal_player_id_by_site_id(player1_site_id)
    player2_id = get_internal_player_id_by_site_id(player2_site_id)
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    sql_expression = """INSERT INTO match (player1_id, player2_id,match_site_id) VALUES(?, ?, ?);"""
    data_tuple = (player1_id, player2_id, match_id)
    cursor.execute(sql_expression, data_tuple)
    last_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return last_id


def save_game(number, match_id, set_number):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    sql_expression = """INSERT INTO game (number, match_id ,set_number) VALUES(?, ?, ?);"""
    data_tuple = (number, match_id, set_number)
    cursor.execute(sql_expression, data_tuple)
    last_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return last_id


def save_game_unit(game_id, player1_score, player2_score):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    sql_expression = """INSERT INTO game_unit (game_id, player1_score ,player2_score) VALUES(?, ?, ?);"""
    data_tuple = (game_id, player1_score, player2_score)
    cursor.execute(sql_expression, data_tuple)
    conn.commit()
    conn.close()


def get_internal_player_id_by_site_id(site_id):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    sql_expression = """SELECT id from player where player_id = ?"""
    data_tuple = (site_id, )
    cursor.execute(sql_expression, data_tuple)
    return cursor.fetchall()[0][0]


def save_set(number, match_id, won_player_site_id, won_player_score, lose_player_score):
    won_player = get_internal_player_id_by_site_id(won_player_site_id)
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    sql_expression = """INSERT INTO set (number, match_id, won_player_id, won_player_score, lose_player_score) VALUES(?, ?, ?);"""
    data_tuple = (number, match_id, won_player, won_player_score, lose_player_score)
    cursor.execute(sql_expression, data_tuple)
    last_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return last_id


def is_match_exists(match_site_id):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    sql_expression = """SELECT id from match where match_site_id = ?"""
    data_tuple = (match_site_id, )
    cursor.execute(sql_expression, data_tuple)
    if len(cursor.fetchall()) > 0:
        return True
    return False
