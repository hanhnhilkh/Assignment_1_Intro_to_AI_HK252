import time
import tracemalloc
from typing import Callable, Any, Tuple

def measure_performance(func: Callable, *args, **kwargs) -> Tuple[Any, float, float]:
    """
    Đo lường thời gian thực thi (Runtime) và bộ nhớ (Memory).
    Trả về: (Kết_quả_của_hàm, Thời_gian_chạy_giây, Dung_lượng_RAM_đỉnh_MB)
    """
    tracemalloc.start()
    start_time = time.perf_counter()
    
    # Thực thi thuật toán tìm kiếm (BFS hoặc A*)
    result = func(*args, **kwargs)
    
    end_time = time.perf_counter()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    execution_time = end_time - start_time
    peak_memory_mb = peak_memory / (1024 * 1024) # Chuyển đổi từ Byte sang Megabyte
    
    return result, execution_time, peak_memory_mb