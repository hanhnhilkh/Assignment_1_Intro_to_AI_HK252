from typing import List, Tuple, Set, Optional

BOARD_SIZE = 9
BOX_SIZE = 3
EMPTY = 0
DIGITS = list(range(1,10))

def idx_to_rc(idx: int) -> Tuple[int, int]:
    row = idx // BOARD_SIZE
    col = idx % BOARD_SIZE
    return row, col

def rc_to_idx(row: int, col: int) -> int:
    return row * BOARD_SIZE + col

def box_start(x: int) -> int:
    return (x // BOX_SIZE) * BOX_SIZE

def row_values(board: Tuple[int, ...], row: int) -> Set[int]:
    values: Set[int] = set()
    start = row * BOARD_SIZE
    for c in range(BOARD_SIZE):
        v = board[start + c]
        if v != EMPTY:
            values.add(v)
    return values

def col_values(board: Tuple[int, ...], col: int) -> Set[int]:
    values: Set[int] = set()
    for r in range(BOARD_SIZE):
        v = board[r * BOARD_SIZE + col]
        if v != EMPTY:
            values.add(v)
    return values

def box_values(board: Tuple[int, ...], row: int, col: int) -> Set[int]:
    values: Set[int] = set()
    r0 = box_start(row)
    c0 = box_start(col)
    for r in range(r0, r0 + BOX_SIZE):
        for c in range(c0, c0 + BOX_SIZE):
            v = board[r * BOARD_SIZE + c]
            if v != EMPTY:
                values.add(v)
    return values

def is_valid_assignment(board: Tuple[int, ...], idx: int, val: int) -> bool:
    if val not in DIGITS:
        return False
    row, col = idx_to_rc(idx)
    
    for c in range(BOARD_SIZE):
        j = rc_to_idx(row, c)
        if j != idx and board[j] == val:
            return False
            
    for r in range(BOARD_SIZE):
        j = rc_to_idx(r, col)
        if j != idx and board[j] == val:
            return False
            
    r0 = box_start(row)
    c0 = box_start(col)
    for r in range(r0, r0 + BOX_SIZE):
        for c in range(c0, c0 + BOX_SIZE):
            j = rc_to_idx(r, c)
            if j != idx and board[j] == val:
                return False
    return True

def get_candidates(board: Tuple[int, ...], idx: int) -> List[int]:
    if board[idx] != EMPTY:
        return []
    row, col = idx_to_rc(idx)
    used = set()
    used |= row_values(board, row)
    used |= col_values(board, col)
    used |= box_values(board, row, col)
    return [d for d in DIGITS if d not in used]

def find_empty_cells(board: Tuple[int, ...]) -> List[int]:
    empties: List[int] = []
    for i, v in enumerate(board):
        if v == EMPTY:
            empties.append(i)
    return empties

def select_unassigned_cell_mrv(board: Tuple[int, ...]) -> Optional[int]:
    empties = find_empty_cells(board)
    if not empties:
        return None
    best_idx: Optional[int] = None
    best_count = 10
    
    for idx in empties:
        cand = get_candidates(board, idx)
        cnt = len(cand)
        if cnt < best_count:
            best_count = cnt
            best_idx = idx
            if best_count == 1:
                break
    return best_idx

def is_board_consistent(board: Tuple[int, ...]) -> bool:
    for idx, v in enumerate(board):
        if v == EMPTY:
            continue
        if not is_valid_assignment(board, idx, v):
            return False
    return True