from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass(order=True)
class Node:
    """
    Đại diện cho một Node trong cây tìm kiếm (Search Tree).
    Thuộc tính đầu tiên (f_cost) sẽ được dùng mặc định để so sánh (sorting) 
    khi đưa Node vào PriorityQueue của thuật toán A*.
    """
    # f(n) = g(n) + h(n). Phải đặt lên đầu để PriorityQueue so sánh theo giá trị này.
    f_cost: int = field(init=False) 
    
    # Các thuộc tính dưới đây không dùng để so sánh (compare=False)
    state: Any = field(compare=False)
    parent: Optional['Node'] = field(default=None, compare=False)
    
    # g(n): Chi phí từ node gốc đến node hiện tại (độ sâu của node)
    g_cost: int = field(default=0, compare=False)
    
    # h(n): Chi phí ước lượng từ node hiện tại đến đích
    h_cost: int = field(default=0, compare=False)

    def __post_init__(self):
        """
        Hàm built-in của dataclass trong Python 3.
        Tự động chạy ngay sau khi khởi tạo object để tính f_cost.
        """
        self.f_cost = self.g_cost + self.h_cost