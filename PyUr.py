round = 1
player = 1
turn = 1
p1_turn_number = 0
p1_sideline = ["A", "B", "C", "D", "E", "F", "G"]
p1_private_1 = ["", "", "", ""]
p1_private_2 = ["", "*"]
p2_turn_number = 0
p2_sideline = ["A", "B", "C", "D", "E", "F", "G"]
p2_private_1 = ["", "", "", "*"]
p2_private_2 = ["", "*"]
shared = ["", "", "", "*", "", "", "", ""]
status_bar = ""
dice_1_value = 0
dice_2_value = 0

def compose_row(row: list[str]) -> str:
    row_str = ""
    for space_content in row:
        if space_content == "*":
            row_str.join([row_str, " [ * ] "])
        elif space_content == "":
            row_str.join([row_str, " [   ] "])
        else:
            row_str.join([row_str, " [ ", space_content, " ] "])
    return row_str

#need to reverse composition!
def compose_private(private_1: list[str], private_2: list[str]) -> str:
    private_str = ""
    compose_row(private_1)
    private_str.join([" [  ] [  ] "])
    compose_row(private_2)
    return private_str

def compose_screen() -> list:
    
    sidelines_1 = compose_row(p1_sideline)
    private_1 = compose_private(p1_private_1, p1_private_2)
    shared = compose_row(shared)
    private_2 = compose_private(p2_private_1, p2_private_2)
    sidelines_2 = compose_row(p2_sideline)
    turn_count = f"Player {player} turn {turn}"
    roll = ""
    status = ""

def visualise_screen() -> None:
