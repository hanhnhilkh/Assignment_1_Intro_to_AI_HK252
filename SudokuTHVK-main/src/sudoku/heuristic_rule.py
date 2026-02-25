from typing import Tuple
from .rules import EMPTY

def heuristic_empty_cells(board: Tuple[int, ...]) -> int:
    """
    Heuristic h(n): Đếm số lượng ô trống còn lại trên bảng.
    
    Giải thích:
    Mỗi bước (action) ta chỉ điền được đúng 1 ô. 
    Để hoàn thành game, ta bắt buộc phải thực hiện số bước bằng đúng số ô trống.
    Vì vậy h(n) luôn bằng chi phí thực tế h*(n). 
    Điều này đảm bảo tính Admissible tuyệt đối cho thuật toán A*.
    """
    return board.count(EMPTY)