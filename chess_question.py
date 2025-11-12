def main():
    
    # Main function to handle user input, manage the board, and output capturable pieces.
    allowed_white = {"pawn", "rook"}
    board: dict[str, str] = {}

    # White piece input
    while True:
        raw = input("Enter WHITE piece and position (pawn/rook), e.g., 'pawn e4': ").strip()
        parsed = parse_piece_input(raw) 
        if not parsed:
            print("Invalid format. Please use: '<piece> <square>', e.g., 'pawn e4'.")
            continue
        white_piece, white_pos = parsed

        if white_piece not in allowed_white:
            print(f"White piece must be one of {sorted(allowed_white)}.")
            continue

        if not add_piece(board, white_piece, white_pos):
            print("Failed to add white piece (invalid square). Try again.")
            continue

        print(f"Added WHITE {white_piece} on {white_pos}.")
        break

    # Get 1-16 black pieces
    print("Now add BLACK pieces one by one (any valid chess piece).")
    print("Format: 'bishop d6'. Add at least 1 and max 16 pieces. Type 'done' when finished\n")

    black_count = 0
    while True:
        if black_count >= 16:
            print("Reached the maximum of 16 black pieces.")
            break

        raw = input("Add BLACK piece (or 'done'): ").strip()
        if raw.lower() == "done":
            if black_count == 0:
                print("You must add at least one black piece.")
                continue
            break

        parsed = parse_piece_input(raw)
        if not parsed:
            print("Invalid format. Please use: 'piece square', e.g., 'rook d6'.")
            continue
        piece, pos = parsed

        # Checking if not occupied
        if pos in board:
            print("That square is already occupied. Pick another square.")
            continue

        # Checking if valid name and square
        if not add_piece(board, piece, pos):
            print("Failed to add black piece (invalid name or out-of-bounds square). Try again.")
            continue

        black_count += 1
        print(f"Added BLACK {piece} on {pos}.")

    capturable = get_capturable_pieces(board, white_piece, white_pos)

    # Print results
    print("\n=== Result ===")
    if not capturable:
        print(f"No black pieces can be captured by the white {white_piece} on {white_pos}.")
    else:
        print(f"The white {white_piece} on {white_pos} can capture these squares:")
        for sq in sorted(capturable):
            print(f" - {sq} {board.get(sq)}")

valid_pieces = {"pawn", "knight", "bishop", "rook", "queen", "king"}
columns = "abcdefgh"
rows = "12345678"

def is_valid_piece(piece: str) -> bool:

    # Checks if valid chess piece, accepts VALID_PIECES (case-insensitive)
    if not isinstance(piece, str):
        return False
    return piece.strip().lower() in valid_pieces

def is_valid_position(pos: str) -> bool:

    # Validates if given position is valid on a chessboard
    if not isinstance(pos, str):
        return False
    s = pos.strip().lower()
    if len(s) != 2:
        return False
    column_char, row_char = s[0], s[1]
    return (column_char in columns) and (row_char in rows)

def parse_piece_input(text: str):

    # Parses input strings like "knight a5" into piece and position
    if not isinstance(text, str):
        return None
    parts = text.strip().lower().split()
    if len(parts) != 2:
        return None
    piece, pos = parts
    if not (is_valid_piece(piece) and is_valid_position(pos)):
        return None
    return piece, pos

def add_piece(board: dict, piece: str, pos: str) -> bool:
    
    # Adds a piece to the board, piece and pos are already validated and normalized
    if pos in board:
        return False
    board[pos] = piece
    return True

def get_pawn_captures(position: str, board: dict[str, str]) -> list[str]:

    # Convert "e4" -> into columns (c) and rows (r)
    c = columns.index(position[0])
    r = rows.index(position[1])

    capture_squares: list[str] = []

    # Left-diagonal
    if c - 1 >= 0 and r + 1 < 8:
        capture_squares.append(columns[c - 1] + rows[r + 1])

    # Right-diagonal
    if c + 1 < 8 and r + 1 < 8:
        capture_squares.append(columns[c + 1] + rows[r + 1])

    # Keep only those diagonal squares that are actually occupied on the board
    return [sq for sq in capture_squares if sq in board]

def get_rook_captures(position: str, board: dict[str, str]) -> list[str]:

    # Convert "e4" -> into columns (c) and rows (r)
    c = columns.index(position[0])
    r = rows.index(position[1])

    capture_squares: list[str] = []

    # 4 directions
    directions = [
        (0, 1),   # up 
        (0, -1),  # down
        (1, 0),   # right
        (-1, 0),  # left
    ]

    for dc, dr in directions:
        cc, cr = c, r
        # Walk square-by-square until we hit board edge or a piece
        while True:
            cc += dc
            cr += dr
            # board bounds
            if not (0 <= cc < 8 and 0 <= cr < 8):
                break
            sq = columns[cc] + rows[cr]
            if sq in board:
                # only first encounter can be captured (no jumps) 
                capture_squares.append(sq)
                break

    return capture_squares

def get_capturable_pieces(board: dict[str, str], white_piece: str, white_position: str) -> list[str]:
    
    
    if white_piece == "pawn":
        captures = get_pawn_captures(white_position, board)
        return [sq for sq in captures if board.get(sq) != "king"]

    if white_piece == "rook":
        captures = get_rook_captures(white_position, board)
        return [sq for sq in captures if board.get(sq) != "king"]

    return []

if __name__ == "__main__":

 # comment main() and uncomment next block to run assert tests
    """
    # Assert tests for is_valid_position
    assert is_valid_position("a1") == True
    assert is_valid_position("h8") == True
    assert is_valid_position("A1") == True
    assert is_valid_position("H8") == True
    assert is_valid_position("i1") == False    # column out of range
    assert is_valid_position("a0") == False    # row out of range
    assert is_valid_position("1a") == False    # wrong order
    assert is_valid_position("a10") == False   # too long
    assert is_valid_position("aa") == False    # row not a digit 1..8
    assert is_valid_position("") == False      # empty
    assert is_valid_position("  a1  ") == True # spaces trimmed
    assert is_valid_position(None) == False    # non-string

    print("All positions are valid")

    # Assert test for is_valid_piece
    assert is_valid_piece("pawn") == True
    assert is_valid_piece("knight") == True
    assert is_valid_piece("knight") == True  # duplicate is fine
    assert is_valid_piece("bishop") == True
    assert is_valid_piece("queen") == True
    assert is_valid_piece("king") == True
    assert is_valid_piece("dragon") == False
    assert is_valid_piece("elephant") == False
    assert is_valid_piece("ROOK") == True
    assert is_valid_piece("  bishop  ") == True
    assert is_valid_piece(None) == False  # non-string should be invalid

    print("All pieces are valid")
    
    # Assert tests for parse_piece_input
    assert parse_piece_input("knight a5") == ("knight", "a5")
    assert parse_piece_input("ROOK H8") == ("rook", "h8")            # case-insensitive
    assert parse_piece_input("pawn  a2") == ("pawn", "a2")           # extra spaces
    assert parse_piece_input("  bishop    c4  ") == ("bishop", "c4") # messy spacing
    assert parse_piece_input("bad a2") is None         # unknown piece
    assert parse_piece_input("rook z9") is None        # invalid position
    assert parse_piece_input("knight a9") is None      # invalid position
    assert parse_piece_input("rook") is None           # missing part
    assert parse_piece_input("") is None               # empty
    assert parse_piece_input(None) is None             # non-string
    assert parse_piece_input("queen c4 extra") is None # too many tokens
    print("All inputs are succesfully parsed")

    # Assert tests for add_piece
    # add_piece now assumes inputs are already normalized and validated

    board = {}

    # Already validated and normalized inputs
    assert add_piece(board, "rook", "e4") == True
    assert board["e4"] == "rook"

    # Cannot place on occupied square
    assert add_piece(board, "queen", "e4") == False

    # Add more valid pieces
    assert add_piece(board, "queen", "h8") == True
    assert board["h8"] == "queen"

    assert add_piece(board, "bishop", "a1") == True
    assert board["a1"] == "bishop"

    # Try to add to occupied squares
    assert add_piece(board, "pawn", "a1") == False
    assert add_piece(board, "knight", "h8") == False

    print("All add_piece tests passed!")
        
    # assert test for get_pawn_captures
    # get_pawn_captures now assumes inputs are already normalized and validated

    test_board = {
        "e4": "pawn",      # Our test pawn
        "d5": "bishop",    # Capturable piece diagonally left
        "f5": "knight",    # Capturable piece diagonally right
        "e5": "rook",      # Piece directly in front (not capturable)
        "a2": "pawn",      # Pawn on edge (can only capture one direction)
        "h2": "pawn",      # Pawn on other edge (can only capture one direction)
        "b3": "queen",     # Target for edge pawn
        "g3": "king",      # Target for other edge pawn
        "c7": "pawn",      # Pawn at top of board (can't move further)
        "b8": "rook",      # Target for pawn on c7
    }

    # Test case 1: Standard pawn with two possible captures
    assert sorted(get_pawn_captures("e4", test_board)) == sorted(["d5", "f5"])

    # Test case 2: Pawn with piece directly in front (not capturable)
    assert "e5" not in get_pawn_captures("e4", test_board)

    # Test case 3: Pawn on left edge (can only capture right)
    assert get_pawn_captures("a2", test_board) == ["b3"]

    # Test case 4: Pawn on right edge (can only capture left)
    assert get_pawn_captures("h2", test_board) == ["g3"]

    # Test case 5: Pawn would capture a piece at top rank
    assert get_pawn_captures("c7", test_board) == ["b8"]

    # Test case 6: Valid position but no pieces to capture
    empty_board = {"e4": "pawn"}
    assert get_pawn_captures("e4", empty_board) == []

    print("All get_pawn_captures tests passed!")
        
    # Assert tests for get_rook_captures
    # get_rook_captures now assumes inputs are already normalized and validated

    test_board = {
        "e4": "rook",      # Our test rook in the middle of the board
        "e6": "pawn",      # Capturable up (blocks e8)
        "e8": "queen",     # Not capturable (blocked by e6)
        "e2": "bishop",    # Capturable down
        "g4": "knight",    # Capturable right
        "c4": "pawn",      # Capturable left
        "a4": "king",      # Not capturable (blocked by c4)
        "a1": "rook",      # Rook in the corner
        "a3": "pawn",      # Capturable by corner rook
        "d1": "bishop",    # Capturable by corner rook
        "h8": "rook",      # Rook in opposite corner
        "h3": "knight",    # Capturable by corner rook
        "f8": "queen",     # Capturable by corner rook
    }

    # Test case 1: Rook in the middle with piece interference
    assert sorted(get_rook_captures("e4", test_board)) == sorted(["e6", "e2", "g4", "c4"])

    # Test case 2: Rook in bottom-left corner
    assert sorted(get_rook_captures("a1", test_board)) == sorted(["a3", "d1"])

    # Test case 3: Rook in top-right corner
    assert sorted(get_rook_captures("h8", test_board)) == sorted(["h3", "f8"])

    # Test case 4: Valid position but no pieces to capture
    empty_board = {"e4": "rook"}
    assert get_rook_captures("e4", empty_board) == []

    # Test case 5: Specific interference test
    interference_board = {
        "e4": "rook",
        "e6": "pawn",
        "e8": "queen"
    }
    assert get_rook_captures("e4", interference_board) == ["e6"]
    assert "e8" not in get_rook_captures("e4", interference_board)

    print("All get_rook_captures tests passed!")

    # assert tests for get_capturable_pieces
    # get_capturable_pieces now assumes inputs are already normalized and validated
    test_board = {
    # White pieces
        "e4": "pawn",      # White pawn in middle
        "a1": "rook",      # White rook in corner
        "c1": "bishop",    # White bishop
        "g1": "knight",    # White knight
        "d1": "queen",     # White queen
        "e1": "king",      # White king

    # Black pieces (potential captures)
        "d5": "bishop",    # Capturable by pawn diagonally
        "f5": "knight",    # Capturable by pawn diagonally
        "e5": "rook",      # Not capturable by pawn (directly in front)

        "a3": "pawn",      # Capturable by rook vertically
        "a8": "queen",     # Capturable by rook vertically
        "h1": "bishop",    # Capturable by rook horizontally

        "a3": "knight",    # Capturable by bishop diagonally (overwrites previous a3)
        "h6": "rook",      # Capturable by bishop diagonally

        "e3": "pawn",      # Capturable by knight L-move
        "f3": "bishop",    # Capturable by knight L-move

        "b1": "pawn",      # Capturable by queen horizontally
        "d3": "rook",      # Capturable by queen diagonally
        "h4": "knight",    # Capturable by queen diagonally

        "e2": "bishop",    # Capturable by king adjacent
        "f2": "pawn",      # Capturable by king adjacent
    }


    # Test case 1: White pawn captures
    pawn_captures = get_capturable_pieces(test_board, "pawn", "e4")
    assert sorted(pawn_captures) == sorted(["d5", "f5"])
    assert "e5" not in pawn_captures  # Pawn can't capture directly in front

    # Test case 2: White rook captures
    rook_captures = get_capturable_pieces(test_board, "rook", "a1")
    assert sorted(rook_captures) == sorted(["a3", "b1"])

    # Test case 3: Empty board
    empty_board = {}
    assert get_capturable_pieces(empty_board, "pawn", "e4") == []
    assert get_capturable_pieces(empty_board, "rook", "a1") == []

    # Test case 4: No capturable pieces
    no_capture_board = {"e4": "pawn"}
    assert get_capturable_pieces(no_capture_board, "pawn", "e4") == []

    # Test case 5: King should not be capturable
    king_test_board = {
        "e4": "pawn",
        "d5": "king",      # King on diagonal - should NOT be capturable
        "f5": "bishop",    # Regular piece - should be capturable
    }
    captures = get_capturable_pieces(king_test_board, "pawn", "e4")
    assert "d5" not in captures  # King not capturable
    assert "f5" in captures      # Bishop is capturable

    king_rook_test = {
        "a1": "rook",
        "a3": "king",      # King in line - should NOT be capturable
        "b1": "pawn",      # Regular piece - should be capturable
    }
    captures = get_capturable_pieces(king_rook_test, "rook", "a1")
    assert "a3" not in captures  # King not capturable
    assert "b1" in captures      # Pawn is capturable

    # Test case 6: Unknown piece type returns empty list
    assert get_capturable_pieces(test_board, "bishop", "c1") == []
    assert get_capturable_pieces(test_board, "knight", "g1") == []

    print("All get_capturable_pieces tests passed!")   
    """

    main()