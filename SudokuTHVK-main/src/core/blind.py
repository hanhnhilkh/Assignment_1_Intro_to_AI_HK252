from collections import deque
from typing import Optional, Tuple, Set
from .node import Node
from src.sudoku.state import SudokuState, select_first_unassigned_cell

def bfs(initial_state: SudokuState) -> Tuple[Optional[Node], int, int]:
    root = Node(state=initial_state)
    if root.state.is_goal():
        return root, 1, 1

    frontier = deque([root])
    # TỐI ƯU HÓA: Dùng thêm set để kiểm tra node có trong frontier hay không với tốc độ O(1)
    frontier_states: Set[SudokuState] = {root.state} 
    explored: Set[SudokuState] = set()
    
    nodes_generated = 1
    max_memory_nodes = 1

    while frontier:
        current_memory = len(frontier) + len(explored)
        if current_memory > max_memory_nodes:
            max_memory_nodes = current_memory

        node = frontier.popleft()
        frontier_states.remove(node.state)
        explored.add(node.state)

        for child_state in node.state.get_successors(select_first_unassigned_cell):
            # Tra cứu siêu tốc nhờ Hash Set thay vì duyệt mảng
            if child_state not in explored and child_state not in frontier_states:
                child_node = Node(state=child_state, parent=node, g_cost=node.g_cost + 1)
                nodes_generated += 1
                
                if child_state.is_goal():
                    return child_node, nodes_generated, max_memory_nodes
                
                frontier.append(child_node)
                frontier_states.add(child_state)

    return None, nodes_generated, max_memory_nodes