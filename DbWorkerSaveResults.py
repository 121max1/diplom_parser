import config
import sqlite3

from Entities import Player


def save_player(player_name, player_id):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    sql_expression = """INSERT INTO player (name, player_id) VALUES(?, ?);"""
    data_tuple = (player_name, player_id)
    cursor.execute(sql_expression, data_tuple)
    conn.commit()
    conn.close()


def save_match(player1_site_id,
               player2_site_id,
               match_id,
               first_serve_percentage_first_player,
               first_serve_percentage_second_player,
               percentage_points_won_on_serve_first_player,
               percentage_points_won_on_serve_second_player,
               percentage_points_won_on_receive_first_player,
               percentage_points_won_on_receive_second_player
               ):
    player1_id = get_internal_player_id_by_site_id(player1_site_id)
    player2_id = get_internal_player_id_by_site_id(player2_site_id)
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    sql_expression = """INSERT INTO match (player1_id, player2_id, match_site_id,
                                           first_serve_percentage_first_player, first_serve_percentage_second_player,
                                           percentage_points_won_on_serve_first_player, percentage_points_won_on_serve_second_player,
                                           percentage_points_won_on_receive_first_player,percentage_points_won_on_receive_second_player ) 
                                           VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    data_tuple = (player1_id, player2_id, match_id,
                  first_serve_percentage_first_player, first_serve_percentage_second_player,
                  percentage_points_won_on_serve_first_player, percentage_points_won_on_serve_second_player,
                  percentage_points_won_on_receive_first_player, percentage_points_won_on_receive_second_player)
    cursor.execute(sql_expression, data_tuple)
    last_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return last_id


def save_game(number, set_id, on_serve_player_id, first_player_score, second_player_score):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    on_serve_player_internal_id = get_internal_player_id_by_site_id(on_serve_player_id)
    sql_expression = """INSERT INTO game (number, set_id , on_serve_player_id, first_player_score, second_player_score) VALUES(?, ?, ?, ?, ?);"""
    data_tuple = (number, set_id, on_serve_player_internal_id, first_player_score, second_player_score)
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


def save_set(number,
             match_id,
             won_player_site_id,
             won_player_score,
             lose_player_score,
             first_serve_percentage_first_player,
             first_serve_percentage_second_player,
             percentage_points_won_on_serve_first_player,
             percentage_points_won_on_serve_second_player,
             percentage_points_won_on_receive_first_player,
             percentage_points_won_on_receive_second_player
             ):
    won_player = get_internal_player_id_by_site_id(won_player_site_id)
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    sql_expression = """INSERT INTO [set] (number, match_id, won_player_id, won_player_score, lose_player_score,
                                           first_serve_percentage_first_player, first_serve_percentage_second_player,
                                           percentage_points_won_on_serve_first_player, percentage_points_won_on_serve_second_player,
                                           percentage_points_won_on_receive_first_player, percentage_points_won_on_receive_second_player) 
                                           VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    data_tuple = (number, match_id, won_player,
                  won_player_score, lose_player_score,
                  first_serve_percentage_first_player, first_serve_percentage_second_player,
                  percentage_points_won_on_serve_first_player, percentage_points_won_on_serve_second_player,
                  percentage_points_won_on_receive_first_player, percentage_points_won_on_receive_second_player)
    cursor.execute(sql_expression, data_tuple)
    last_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return last_id


def add_to_bad_matches(match_site_id):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    sql_expression = """INSERT INTO bad_matches (match_site_id) VALUES(?);"""
    data_tuple = (match_site_id,)
    cursor.execute(sql_expression, data_tuple)
    conn.commit()
    conn.close()


def is_match_exists_in_bad_matches(match_site_id):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    sql_expression = """SELECT bad_match_id from bad_matches where match_site_id = ?"""
    data_tuple = (match_site_id, )
    cursor.execute(sql_expression, data_tuple)
    if len(cursor.fetchall()) > 0:
        return True
    return False


def is_match_exists(match_site_id):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    sql_expression = """SELECT id from match where match_site_id = ?"""
    data_tuple = (match_site_id, )
    cursor.execute(sql_expression, data_tuple)
    if len(cursor.fetchall()) > 0:
        return True
    return False


def get_players_name_and_ids():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql_expression = """SELECT name, player_id from player"""
    cursor.execute(sql_expression)
    players = []
    for result in cursor:
        players.append(Player(result["name"], result["player_id"]))
    conn.close()
    return players


def save_match_entity(match_entity):
    id_match = save_match(match_entity.player1, match_entity.player2, match_entity.site_id,
                          match_entity.first_serve_percentage_first_player, match_entity.first_serve_percentage_second_player,
                          match_entity.percentage_points_won_on_serve_first_player, match_entity.percentage_points_won_on_serve_second_player,
                          match_entity.percentage_points_won_on_receive_first_player, match_entity.percentage_points_won_on_receive_second_player)
    for match_set in match_entity.sets:
        set_id = save_set(match_set.number, id_match, match_set.won_player_id, match_set.won_player_score, match_set.lose_player_score,
                          match_set.first_serve_percentage_first_player, match_set.first_serve_percentage_second_player,
                          match_set.percentage_points_won_on_serve_first_player, match_set.percentage_points_won_on_serve_second_player,
                          match_set.percentage_points_won_on_receive_first_player, match_set.percentage_points_won_on_receive_second_player)
        for game in match_set.games:
            game_id = save_game(game.number, set_id, game.on_serve_player_site_id, game.first_player_score, game.second_player_score)
            for game_unit in game.game_units:
                save_game_unit(game_id, game_unit.player1_score, game_unit.player2_score)

