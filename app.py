import streamlit as st
import zlib
import io
import numpy as np

PHI = 1.61803398875

def phase_transform_v2(data):
    """ 
    Версия 2.0: Золотой Резонанс.
    Мы не просто вычитаем байты, мы ищем 'замок' через PHI.
    """
    if not data: return None
    arr = np.frombuffer(data, dtype=np.uint8).astype(np.int16)
    transformed = np.zeros_like(arr, dtype=np.uint8)
    
    transformed[0] = arr[0]
    for i in range(1, len(arr)):
        # Золотой прогноз: следующий байт должен быть в резонансе с прошлым
        # Используем PHI как оператор поворота фазы
        prediction = int(arr[i-1] * (PHI - 1)) % 256
        # Сохраняем только отклонение от резонанса
        transformed[i] = (arr[i] - prediction) % 256
        
    return zlib.compress(transformed.tobytes(), level=9)

def phase_restore_v2(compressed_data):
    """ Обратное восстановление резонанса """
    diffs = np.frombuffer(zlib.decompress(compressed_data), dtype=np.uint8).astype(np.int16)
    restored = np.zeros_like(diffs, dtype=np.uint8)
    
    restored[0] = diffs[0]
    for i in range(1, len(diffs)):
        prediction = int(restored[i-1] * (PHI - 1)) % 256
        restored[i] = (diffs[i] + prediction) % 256
        
    return restored.tobytes()

# --- Остальной интерфейс Streamlit оставляем таким же, 
# просто меняем вызовы функций на phase_transform_v2 ---
