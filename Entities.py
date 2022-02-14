class Player:
    def __init__(self, name, site_id, player_id =None):
        self.id = player_id
        self.name = name
        self.site_id = site_id


class Match:
    def __init__(self, player1, player2, site_id, sets=None, id=None):
        if sets is None:
            sets = []
        self.id = id
        self.player1 = player1
        self.player2 = player2
        self.sets = sets
        self.site_id = site_id
        self.first_serve_percentage_first_player = None
        self.first_serve_percentage_second_player = None
        self.percentage_points_won_on_serve_first_player = None
        self.percentage_points_won_on_serve_second_player = None
        self.percentage_points_won_on_receive_first_player = None
        self.percentage_points_won_on_receive_second_player = None


class Game:
    def __init__(self, number, player_won_site_id, first_player_score, second_player_score, on_serve_player_site_id, game_id=None, game_unit_list=None):
        if game_unit_list is None:
            game_unit_list = []
        self.id = game_id
        self.player_won_id = player_won_site_id
        self.game_units = game_unit_list
        self.number = number
        self.first_player_score = first_player_score
        self.second_player_score = second_player_score
        self.on_serve_player_site_id = on_serve_player_site_id


class GameUnit:
    def __init__(self, player1_score, player2_score, game_unit_id=None):
        self.game_unit_id = game_unit_id
        self.player1_score = player1_score
        self.player2_score = player2_score


class Set:
    def __init__(self, number, won_player_id, won_player_score, lose_player_score, games=None, id=None, match_id=None):
        if games is None:
            games = []
        self.number = number
        self.match_id = match_id
        self.won_player_id = won_player_id
        self.won_player_score = won_player_score
        self.lose_player_score = lose_player_score
        self.games = games
        self.id = id
        self.first_serve_percentage_first_player = None
        self.first_serve_percentage_second_player = None
        self.percentage_points_won_on_serve_first_player = None
        self.percentage_points_won_on_serve_second_player = None
        self.percentage_points_won_on_receive_first_player = None
        self.percentage_points_won_on_receive_second_player = None


class Stat:
    def __init__(self, first_serve_percentage_first_player,
                 first_serve_percentage_second_player,
                 percentage_points_won_on_serve_first_player,
                 percentage_points_won_on_serve_second_player,
                 percentage_points_won_on_receive_first_player,
                 percentage_points_won_on_receive_second_player):
        self.first_serve_percentage_first_player = first_serve_percentage_first_player
        self.first_serve_percentage_second_player = first_serve_percentage_second_player
        self.percentage_points_won_on_serve_first_player = percentage_points_won_on_serve_first_player
        self.percentage_points_won_on_serve_second_player = percentage_points_won_on_serve_second_player
        self.percentage_points_won_on_receive_first_player = percentage_points_won_on_receive_first_player
        self.percentage_points_won_on_receive_second_player = percentage_points_won_on_receive_second_player
