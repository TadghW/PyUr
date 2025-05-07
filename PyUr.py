import random
from typing import Optional, Tuple
from graphics import render_screenspace

pieces = {
    1: {ch: {"position": 0} for ch in "ABCDEFG"},
    2: {ch: {"position": 0} for ch in "abcdefg"},
}

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
game_state["round"] = 0
game_state["active_player"] = 0
game_state["consecutive_turn_count"] = 1
game_state["turn_repeat_flag"] = False
game_state["status"] = ""
game_state["last_roll"] = []
game_state["movement_points"] = 0
game_state["p1_turn_count"] = 0
game_state["p2_turn_count"] = 0


def roll_dice() -> None:
    sides = [1, 0]
    num_rolls = 3
    result = []
    for roll in range(num_rolls):
        throw = random.choice(sides)
        result.append(throw)
    game_state["last_roll"] = result
    game_state["movement_points"] = sum(result)
    if result == [1, 1, 1]:
        game_state["turn_repeat_flag"] = True
        game_state["status"] = (
            f"Player {game_state["active_player"]} rolls an extra turn!"
        )
    render_screenspace(game_state)


def find_piece_at_position(position_to_check) -> Optional[dict]:
    for player, player_pieces in pieces.items():
        for piece_id, piece_data in player_pieces.items():
            if piece_data["position"] == position_to_check:
                return {"player": player, "piece": piece_id}
    return None


def can_player_move() -> bool:

    if game_state["movement_points"] == 0:
        input("Bad luck. Hit enter to skip.")
        return False

    possible_destinations = []

    for piece, piece_data in pieces[game_state["active_player"]].items():
        possible_destinations.append(
            piece_data["position"] + game_state["movement_points"]
        )

    possible_open_spaces = []

    for destination in possible_destinations:
        space_occupant = find_piece_at_position(destination)
        if (
            destination <= 15
            and (
                space_occupant
                and space_occupant["player"] != game_state["active_player"]
                and not destination == 8
            )
            or not space_occupant
        ):
            possible_open_spaces.append(destination)

    if possible_open_spaces:
        return True
    else:
        input("No possible moves. Hit enter to skip.")
        return False


def request_move() -> Tuple[str, int, dict]:

    active_player = game_state["active_player"]
    selected_piece = input("What piece would you like to move: ")

    # Does piece belong to player?
    if selected_piece not in pieces[game_state["active_player"]]:
        game_state["status"] = "You can't move a piece you don't own."
        render_screenspace(game_state)
        return request_move()

    target_square = (
        pieces[active_player][selected_piece]["position"]
        + game_state["movement_points"]
    )
    space_occupant = find_piece_at_position(target_square)

    # Is target square occupied by player?
    if space_occupant and space_occupant["player"] == game_state["active_player"]:
        game_state["status"] = "Another one of your pieces occupies this space."
        render_screenspace(game_state)
        return request_move()

    # Is target occupied as by an entrenched piece?
    if (
        space_occupant
        and space_occupant["player"] != game_state["active_player"]
        and target_square == 8
    ):
        game_state["status"] = "You can't capture a piece on a rosette."
        render_screenspace(game_state)
        return request_move()

    # Would target move piece off the board with unused movement points?
    if target_square > 15:
        game_state["status"] = (
            "You must roll the exact number of spaces required to move a piece off the board."
        )
        render_screenspace(game_state)
        return request_move()

    # If you've made it this far - it's a valid move!
    return selected_piece, target_square, space_occupant


def make_move(
    selected_piece: str, target_square: int, space_occupant: Optional[dict]
) -> None:

    if target_square in rosette_positions:
        game_state["turn_repeat_flag"] = True
        game_state["status"] = (
            f"Player {game_state["active_player"]} gets an extra roll for landing on a rosette."
        )

    if space_occupant:
        pieces[space_occupant["player"]][space_occupant["piece"]]["position"] = 0
        pieces[game_state["active_player"]][selected_piece]["position"] = target_square
    elif target_square == 15:
        del pieces[game_state["active_player"]][selected_piece]
    else:
        pieces[game_state["active_player"]][selected_piece]["position"] = target_square


def do_turn() -> None:

    roll_dice()
    if not can_player_move():
        return
    selected_piece, target_square, space_occupant = request_move()
    make_move(selected_piece, target_square, space_occupant)
    return


def next_turn() -> None:

    # turn repeat
    if game_state["turn_repeat_flag"]:
        game_state["consecutive_turn_count"] += 1
        game_state["turn_repeat_flag"] = False
        do_turn()
        return

    # player 1 to 2
    # init
    # player 2 to 1
    if game_state["active_player"] == 1:
        game_state["round"] += 1
        game_state["active_player"] = 2
        do_turn()
        return
    elif game_state["active_player"] == 0:
        game_state["round"] += 1
        game_state["active_player"] = 1
        do_turn()
        return
    else:
        game_state["round"] += 1
        game_state["active_player"] = 1
        do_turn()
        return


if __name__ == "__main__":
    while pieces[1].items() and pieces[2].items():
        next_turn()
