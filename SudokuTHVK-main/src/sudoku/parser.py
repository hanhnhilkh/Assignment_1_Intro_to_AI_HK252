from typing import List, Tuple

def parse_puzzle(text: str) -> Tuple[int, ...]:
    # Tách thành các dòng, loại bỏ dòng trống
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    digits: List[int] = []
    
    if len(lines) == 9:
        for line in lines:
            # Loại bỏ mọi khoảng trắng lỡ tay copy dính vào
            clean_line = line.replace(" ", "")
            if len(clean_line) != 9:
                raise ValueError(f"Dòng không hợp lệ (đang có {len(clean_line)} ký tự): {clean_line}")
            
            # ĐÃ SỬA LỖI BUG: 'for ch in clean_line' thay vì 'for ch in lines'
            for ch in clean_line:
                digits.append(_char_to_int(ch))
    else:
        # Gộp tất cả lại nếu input không phải định dạng 9 dòng
        flat = "".join(lines).replace(" ", "")
        if len(flat) != 81:
            raise ValueError(f"Input có {len(flat)} ký tự. Sudoku yêu cầu chính xác 81 ký tự.")
        for ch in flat:
            digits.append(_char_to_int(ch))
            
    return tuple(digits)

def load_puzzle(path: str) -> Tuple[int, ...]:
    # Dùng utf-8-sig để tự động loại bỏ ký tự ẩn BOM (Byte Order Mark) của Windows Notepad
    with open(path, 'r', encoding='utf-8-sig') as f:
        return parse_puzzle(f.read())

def _char_to_int(ch: str) -> int:
    if ch in ('0', '.', '_'): 
        return 0
    if ch in '123456789': 
        return int(ch)
    raise ValueError(f"Ký tự không hợp lệ trong input: '{ch}'")