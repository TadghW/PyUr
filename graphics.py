from types import Tuple

private_path_1_default = ["", "", "", "*"]
private_path_2_default = ["", "*"]
shared_path_default = ["", "", "", "*", "", "", "", ""]


def distribute_pieces(board: dict, pieces: dict) -> dict:
    
    # This function does no state checking, it just distributes pieces

    for piece in pieces[1]:
        pos = piece["position"]
        if pos == 0:
            board["p1_sideline"].append(piece)
        elif 1 <= pos <= 4:
            board["p1_private_1"][pos - 1] = piece
        elif 5 <= pos <= 12:
            board["shared"][pos - 5] = piece
        elif 13 <= pos <= 14:
            board["p1_private_2"][pos - 13] = piece

    for piece in pieces[2]:
        pos = piece["position"]
        if pos == 0:
            board["p2_sideline"].append(piece)
        elif 1 <= pos <= 4:
            board["p2_private_1"][pos - 1] = piece
        elif 5 <= pos <= 12:
            board["shared"][pos - 5] = piece
        elif 13 <= pos <= 14:
            board["p2_private_2"][pos - 13] = piece

    return board


def draw_sideline(sideline: list[str]) -> str:
    sideline_str = ""
    for sideline_content in sideline:
        sideline_str += f"{sideline_content} "
    return sideline_str


def draw_row(row: list[str]) -> str:
    row_str = ""
    for space_content in row:
        if space_content == "*":
            row_str += "[ * ]"
        elif space_content == "":
            row_str += "[   ]"
        else:
            row_str += f" [ {space_content} ] "
    return row_str


def draw_private(private_1: list[str], private_2: list[str]) -> str:
    # Pieces move right to left on private rows
    # We conceptualise them left to right in the code
    # And reverse them on print.
    reversed_private_1 = draw_row(list(reversed(private_path_1_default)))
    reversed_private_2 = draw_row(list(reversed(private_path_2_default)))
    return f"{reversed_private_1}          {reversed_private_2}"


def compose_screen(game_state: dict) -> str:

    space = ""
    title = "*** PyUr ***"

    game_state["board"] = distribute_pieces(game_state["pieces"],
                                            game_state["board"])
    
    sidelines_1 = draw_sideline(game_state["board"]["p1_sideline"])
    private_1 = draw_private(game_state["board"]["p1_private_1"],
                             game_state["board"]["p1_private_2"])
    
    shared = draw_row(game_state["board"]["shared_path"])
    
    private_2 = draw_private(game_state["board"]["p2_private_1"],
                             game_state["board"]["p2_private_2"])
    sidelines_2 = draw_sideline(game_state["board"]["p2_sideline"])
    
    round = f"Round {game_state["round"]}"
    turn_count = f"Player {game_state["active_player"]}, turn {game_state["consecutive_turn_count"]}"
    
    roll = f"You rolled {game_state["last_roll"][0]}, {game_state["last_roll"][1]}, and {game_state["last_roll"][2]}. You net {game_state["movement_points"]} movement points."
    
    status = game_state["board"]["status"]

    lines = [space, title, space, sidelines_1, private_1, shared, private_2,
             sidelines_2, space, round, turn_count, roll, status]
    
    return "\n".join(lines)
