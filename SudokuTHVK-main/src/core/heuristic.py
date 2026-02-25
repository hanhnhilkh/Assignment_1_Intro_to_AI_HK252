import heapq
from typing import Optional, Tuple, Set, Dict
from .node import Node
from src.sudoku.state import SudokuState
from src.sudoku.rules import select_unassigned_cell_mrv
from src.sudoku.heuristic_rule import heuristic_empty_cells

def a_star(initial_state: SudokuState) -> Tuple[Optional[Node], int, int]:
    """
    A* Search Algorithm
    Trả về: (Goal_Node, số_node_đã_tạo, số_node_lưu_trữ_tối_đa_trong_RAM)
    """
    # Tính h(n) cho state gốc
    root_h = heuristic_empty_cells(initial_state.board)
    root = Node(state=initial_state, g_cost=0, h_cost=root_h)
    
    # Priority Queue (Min-Heap) cho frontier
    frontier = []
    heapq.heappush(frontier, root)
    
    # Dùng dictionary để tra cứu nhanh chi phí g(n) hiện tại của các state trong frontier
    frontier_states: Dict[SudokuState, int] = {initial_state: root.g_cost}
    explored: Set[SudokuState] = set()
    
    nodes_generated = 1
    max_memory_nodes = 1

    while frontier:
        # Cập nhật thông số bộ nhớ (đo lường RAM)
        current_memory = len(frontier) + len(explored)
        if current_memory > max_memory_nodes:
            max_memory_nodes = current_memory

        # Lấy Node có f_cost nhỏ nhất
        node = heapq.heappop(frontier)
        
        # Nếu node này đã được pop, gỡ khỏi dict tra cứu
        if node.state in frontier_states:
            del frontier_states[node.state]
            
        # A* kiểm tra đích KHI POP Node ra khỏi frontier
        if node.state.is_goal():
            return node, nodes_generated, max_memory_nodes
            
        explored.add(node.state)

        # Mở rộng (Expand) node hiện tại. Dùng MRV để tối ưu hóa việc chọn ô (Variable Ordering).
        for child_state in node.state.get_successors(select_unassigned_cell_mrv):
            if child_state in explored:
                continue
                
            child_g = node.g_cost + 1
            child_h = heuristic_empty_cells(child_state.board)
            child_node = Node(state=child_state, parent=node, g_cost=child_g, h_cost=child_h)
            
            # Nếu child_state chưa có trong frontier, hoặc tìm được đường đi tốt hơn (g_cost nhỏ hơn)
            if child_state not in frontier_states or child_g < frontier_states[child_state]:
                heapq.heappush(frontier, child_node)
                frontier_states[child_state] = child_g
                nodes_generated += 1

    return None, nodes_generated, max_memory_nodes