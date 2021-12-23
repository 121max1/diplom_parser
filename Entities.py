class Player:
    def __init__(self, name, player_id, site_id =None):
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


class Game:
    def __init__(self, number, match, game_id=None, game_init_list=None):
        if game_init_list is None:
            game_init_list = []
        self.id = game_id
        self.match = match
        self.game_units = game_init_list
        self.number = number


class GameUnit:
    def __init__(self, player1_score, player2_score, game, game_unit_id=None):
        self.game_unit_id = game_unit_id
        self.game = game
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
