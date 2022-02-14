import sqlite3
import numpy as np
import pandas as pd

cnx = sqlite3.connect('dbTennisScores.db')

sql_select_match = """ SELECT id AS match_id
                             ,player1_id
                             ,player2_id
                             ,first_serve_percentage_first_player AS match_first_serve_percentage_first_player
                             ,first_serve_percentage_second_player AS match_first_serve_percentage_second_player
                             ,percentage_points_won_on_serve_first_player AS match_percentage_points_won_on_serve_first_player
                             ,percentage_points_won_on_serve_second_player AS match_percentage_points_won_on_serve_second_player
                             ,percentage_points_won_on_receive_first_player AS match_percentage_points_won_on_receive_first_player
                             ,percentage_points_won_on_receive_second_player AS match_percentage_points_won_on_receive_second_player
                       FROM [match];
"""
sql_select_set = """ SELECT id AS set_id
                           ,number AS set_number
                           ,match_id
                           ,won_player_id AS set_won_player_id
                           ,won_player_score AS set_won_player_score
                           ,lose_player_score AS set_lose_player_score
                           ,first_serve_percentage_first_player AS set_first_serve_percentage_first_player
                           ,first_serve_percentage_second_player AS set_first_serve_percentage_second_player
                           ,percentage_points_won_on_serve_first_player AS set_percentage_points_won_on_serve_first_player
                           ,percentage_points_won_on_serve_second_player AS set_percentage_points_won_on_serve_second_player
                           ,percentage_points_won_on_receive_first_player AS set_percentage_points_won_on_receive_first_player
                           ,percentage_points_won_on_receive_second_player AS set_percentage_points_won_on_receive_second_player
                     FROM [set];
"""
sql_select_game = """ SELECT id AS game_id
                            ,number AS game_number
                            ,set_id
                            ,on_serve_player_id AS game_on_serve_player_id
                            ,first_player_score AS game_first_player_score
                            ,second_player_score AS game_second_player_score
                      FROM [game];
"""
sql_select_game_unit = """ SELECT id AS game_unit_id
                                 ,game_id
                                 ,player1_score AS game_unit_player1_score
                                 ,player2_score AS game_unit_player2_score
                            FROM [game_unit]
"""

df_match = pd.read_sql_query(sql_select_match, cnx)
df_set = pd.read_sql_query(sql_select_set, cnx)
df_game = pd.read_sql_query(sql_select_game, cnx)
df_game_unit = pd.read_sql_query(sql_select_game_unit, cnx)
#df_player = pd.read_sql_query("SELECT * FROM [player]", cnx)

df_match_set = pd.merge(df_match, df_set, on='match_id')
df_match_set_game = pd.merge(df_match_set, df_game, on='set_id')
df_match_set_game_game_unit = pd.merge(df_match_set_game, df_game_unit,on='game_id')

print(df_match_set_game_game_unit)