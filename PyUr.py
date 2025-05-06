import random
from graphics import compose_screen

turn_info = {}
turn_info["round"] = 1
turn_info["active_player"] = 1
turn_info["consecutive_turn_count"] = 1
turn_info["turn_repeat_flag"] = False
turn_info["status"] = ""
turn_info["last_roll"] = []
turn_info["movement_points"] = 0
turn_info["p1_turn_count"] = 0
turn_info["p2_turn_count"] = 0

pieces = {}
pieces["p1_pieces"]["A"]["position"] = 0
pieces["p1_pieces"]["B"]["position"] = 0
pieces["p1_pieces"]["C"]["position"] = 0
pieces["p1_pieces"]["D"]["position"] = 0
pieces["p1_pieces"]["E"]["position"] = 0
pieces["p1_pieces"]["F"]["position"] = 0
pieces["p1_pieces"]["G"]["position"] = 0
pieces["p2_pieces"]["a"]["position"] = 0
pieces["p2_pieces"]["b"]["position"] = 0
pieces["p2_pieces"]["c"]["position"] = 0
pieces["p2_pieces"]["d"]["position"] = 0
pieces["p2_pieces"]["e"]["position"] = 0
pieces["p2_pieces"]["f"]["position"] = 0
pieces["p2_pieces"]["g"]["position"] = 0

private_path_1_default = ["", "", "", "*"]
private_path_2_default = ["", "*"]
shared_path_default = ["", "", "", "*", "", "", "", ""]

board = {}
board["p1_sideline"] = []
board["p1_private_1"] = private_path_1_default
board["p1_private_2"] = private_path_2_default
board["p2_sideline"] = []
board["p2_private_1"] = private_path_1_default
board["p2_private_2"] = private_path_2_default
board["shared"] = shared_path_default

game_state = {}
game_state["turn_info"] = turn_info
game_state["pieces"] = pieces
game_state["board"] = board


def render_screenspace() -> None:
    print(compose_screen(game_state))


def roll_dice() -> None:
    sides = [1, 0]
    num_rolls = 3
    result = []
    for roll in range(num_rolls):
        throw = random.choice(sides)
        result.append(throw)
    game_state["last_roll"] = result
    game_state["movement_points"] = list(sum(result))

def request_move() -> None:
    
    selected_piece = input('What piece would you like to move: ')
    # All move logic will now take place with the player pieces dicts
    # Drawing the board is decoupled
    # Must check the validity of moves and piece positions during moves
    # Implement move checking
    # Implement move making


def next_turn(player: int) -> None:
    
    roll_dice()
    draw_screen()
    request_move()
    draw_screen()

    if turn_repeat_flag: 
        turn_repeat_flag = False
        return
    elif player is 1:
        player = 2
        return
    elif player is 2:
        player = 1 
        return

if __name__ == "__main__":
    while p1_sideline and p2_sideline:
        next_turn()



