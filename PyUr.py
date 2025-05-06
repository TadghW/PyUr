import random
from typing import Optional
from graphics import compose_screen

pieces = {}
pieces[1]["A"]["position"] = 0
pieces[1]["B"]["position"] = 0
pieces[1]["C"]["position"] = 0
pieces[1]["D"]["position"] = 0
pieces[1]["E"]["position"] = 0
pieces[1]["F"]["position"] = 0
pieces[1]["G"]["position"] = 0
pieces[2]["a"]["position"] = 0
pieces[2]["b"]["position"] = 0
pieces[2]["c"]["position"] = 0
pieces[2]["d"]["position"] = 0
pieces[2]["e"]["position"] = 0
pieces[2]["f"]["position"] = 0
pieces[2]["g"]["position"] = 0

private_path_1_default = ["", "", "", "*"]
private_path_2_default = ["", "*"]
shared_path_default = ["", "", "", "*", "", "", "", ""]
rosette_positions = [4, 8, 14]

board = {}
board["p1_sideline"] = []
board["p1_private_1"] = private_path_1_default
board["p1_private_2"] = private_path_2_default
board["p2_sideline"] = []
board["p2_private_1"] = private_path_1_default
board["p2_private_2"] = private_path_2_default
board["shared"] = shared_path_default

game_state = {}
game_state["pieces"] = pieces
game_state["board"] = board
game_state["round"] = 1
game_state["active_player"] = 1
game_state["consecutive_turn_count"] = 1
game_state["turn_repeat_flag"] = False
game_state["status"] = ""
game_state["last_roll"] = []
game_state["movement_points"] = 0
game_state["p1_turn_count"] = 0
game_state["p2_turn_count"] = 0


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
    if all(roll == result[0] for roll in result):
        game_state["turn_repeat_flag"] = True


def find_piece_at_position(position_to_check) -> Optional[dict]:
    for player, player_pieces in pieces.items():
        for piece_id, piece_pos in player_pieces.items():
            if piece_id.get("position") == position_to_check:
                return {
                    "player": player,
                    "piece": piece_id,
                    "position": piece_pos
                }
    return None


def request_move() -> None:
    
    selected_piece = input('What piece would you like to move: ')
    
    # Does piece belong to player?
    if selected_piece not in pieces[game_state["active_player"]]:
        game_state["status"] = "You can't move a piece you don't own."
        render_screenspace()
        request_move()
    
    target_square = selected_piece["position"] + game_state["movement_points"]
    space_occupant = find_piece_at_position(target_square)
    
    # Is target square occupied by player?
    if space_occupant and space_occupant["player"] == game_state["active_player"]:
        game_state["status"] = "Another one of your pieces occupies this space."
        render_screenspace()
        request_move()
    
    # Is target occupied as by an entrenched piece?
    if space_occupant and space_occupant["player"] != game_state["active_player"] and target_square == 8:
        game_state["status"] = "You can't capture a piece on a rosette."
        render_screenspace()
        request_move()

    # Would target move piece off the board with unused movement points?
    if target_square > 15:
        game_state["status"] = "You must roll the exact number of spaces required to move a piece off the board."
        render_screenspace()
        request_move()

    

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



