import random

round = 1
player = 1
turn = 1
turn_repeat_flag = False

p1_pieces = {}
p1_pieces["A"]["position"] = 0
p1_pieces["B"]["position"] = 0
p1_pieces["C"]["position"] = 0
p1_pieces["D"]["position"] = 0
p1_pieces["E"]["position"] = 0
p1_pieces["F"]["position"] = 0
p1_pieces["G"]["position"] = 0
p1_turn_number = 0

p2_pieces = {}
p2_pieces["a"]["position"] = 0
p2_pieces["b"]["position"] = 0
p2_pieces["c"]["position"] = 0
p2_pieces["d"]["position"] = 0
p2_pieces["e"]["position"] = 0
p2_pieces["f"]["position"] = 0
p2_pieces["g"]["position"] = 0
p2_turn_number = 0
p2_private_1 = ["", "", "", "*"]
p2_private_2 = ["", "*"]

shared_path = ["", "", "", "*", "", "", "", ""]
status = ""
last_roll = []
movement_points = 0


def compose_sideline(sideline: list[str]) -> str:
    sideline_str = ""
    for sideline_content in sideline:
        sideline_str += f"{sideline_content} "
    return sideline_str


def compose_row(row: list[str]) -> str:
    row_str = ""
    for space_content in row:
        if space_content == "*":
            row_str += "[ * ]"
        elif space_content == "":
            row_str += "[   ]"
        else:
            row_str += f" [ {space_content} ] "
    return row_str


def compose_private(private_1: list[str], private_2: list[str]) -> str:
    # Pieces move right to left on private rows
    # We're representing those two segments at lists
    # So we're going to reverse them
    reversed_private_1 = compose_row(list(reversed(private_1)))
    reversed_private_2 = compose_row(list(reversed(private_2)))
    
    return f"{reversed_private_1}          {reversed_private_2}"


def distribute_pieces(pieces, sideline, private_1, private_2, shared) -> list[list]:
    
    for piece in pieces:
        pos = piece["position"]
        if pos == 0:
            sideline.append(piece)
        elif 1 <= pos <= 4:
            private_1[pos - 1] = piece
        elif 5 <= pos <= 12:
            shared[pos - 5] = piece
        elif 13 <= pos <= 14:
            private_2[pos - 13] = piece


def compose_screen() -> str:

    space_line = ""
    title = "*** PyUr ***"

    p1_sideline = []
    p1_private_1 = ["", "", "", "*"]
    p1_private_2 = ["", "*"]
    p2_sideline = []
    p2_private_1 = ["", "", "", "*"]
    p2_private_2 = ["", "*"]
    shared = ["", "", "", "*", "", "", "", ""]

    distribute_pieces(p1_pieces, p1_sideline, p1_private_1, p1_private_2, shared)
    distribute_pieces(p2_pieces, p2_sideline, p2_private_1, p2_private_2, shared)
                        
    for piece in p2_pieces:
        if piece["position"] == 0:
            p1_sideline.append(piece)

    sidelines_1 = compose_sideline(p1_sideline)
    private_1 = compose_private(p1_private_1, p1_private_2)
    shared = compose_row(shared_path)
    private_2 = compose_private(p2_private_1, p2_private_2)
    sidelines_2 = compose_sideline(p2_sideline)
    turn_count = f"Player {player} turn {turn}"
    roll = f"Rolled {last_roll[0]}, {last_roll[1]}, and {last_roll[2]}. You move {movement_points} spaces"
    lines = [space_line, title, space_line, sidelines_1, private_1, shared, private_2, sidelines_2, space_line, turn_count, roll, status]
    return "\n".join(lines)


def draw_screen() -> None:
    print(compose_screen())


def roll_dice() -> None:
    sides = [1, 0]
    num_rolls = 3
    result = []
    for roll in range(num_rolls):
        throw = random.choice(sides)
        result.append(throw)
    last_roll = result


def request_move() -> None:
    
    status = "What piece would you like to move?"
    selected_piece = input('Piece: ')
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



