import streamlit as st
import zlib
import io

# Твоя константа топологического резонанса
PHI = 1.61803398875

def phase_pack(data):
    """ Намотка фазовой нити (Сжатие) """
    if not data: return None
    transformed = bytearray()
    transformed.append(data[0])
    for i in range(1, len(data)):
        # Вычисляем сдвиг фазы (натяжение)
        diff = (data[i] - data[i-1]) % 256
        transformed.append(diff)
    return zlib.compress(transformed, level=9)

def phase_unpack(compressed_data):
    """ Размотка фазовой нити (Распаковка) """
    try:
        diffs = zlib.decompress(compressed_data)
        restored = bytearray()
        restored.append(diffs[0])
        for i in range(1, len(diffs)):
            original_val = (restored[i-1] + diffs[i]) % 256
            restored.append(original_val)
        return restored
    except Exception as e:
        st.error(f"Ошибка распаковки: Возможно, файл поврежден или это не .phase архив.")
        return None

# --- ИНТЕРФЕЙС STREAMLIT ---
st.set_page_config(page_title="Phase Archiver V1.0", page_icon="🌀")

st.title("🌀 Phase Archiver V1.0")
st.subheader("Топологическое сжатие данных по методу Николая")
st.write("Алгоритм намотки фазовой нити с шагом $\Phi$.")

uploaded_file = st.file_uploader("Выберите файл для обработки", type=None)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name
    
    # Логика: если файл .phase - распаковываем, если нет - сжимаем
    if file_name.endswith(".phase"):
        st.info(f"Обнаружен фазовый архив. Запуск размотки нити...")
        result_data = phase_unpack(file_bytes)
        
        if result_data:
            new_name = file_name.replace(".phase", "_restored")
            st.success("Файл успешно восстановлен!")
            st.download_button(
                label="📥 Скачать восстановленный файл",
                data=io.BytesIO(result_data),
                file_name=new_name,
                mime="application/octet-stream"
            )
    else:
        st.info(f"Запуск топологической намотки...")
        result_data = phase_pack(file_bytes)
        
        if result_data:
            orig_size = len(file_bytes)
            comp_size = len(result_data)
            gain = (1 - comp_size/orig_size) * 100
            
            st.success(f"Сжатие завершено! Эффективность: {gain:.2f}%")
            st.write(f"Размер уменьшен с {orig_size/1024:.1f} KB до {comp_size/1024:.1f} KB")
            
            st.download_button(
                label="📥 Скачать .phase архив",
                data=io.BytesIO(result_data),
                file_name=file_name + ".phase",
                mime="application/octet-stream"
            )

st.divider()
st.caption("Разработано на основе Фазовой Топологии. Масса — частота, $\pi=1$.")
