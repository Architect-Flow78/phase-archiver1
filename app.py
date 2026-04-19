import streamlit as st
import zlib
import io

# Твоя константа (Золотое сечение)
PHI = 1.61803398875

def phase_logic(data, mode="pack"):
    """ Чистая топологическая намотка без внешних библиотек """
    if mode == "pack":
        # Сжатие
        res = bytearray()
        res.append(data[0])
        for i in range(1, len(data)):
            # Золотой прогноз: (предыдущий байт * 0.618)
            prediction = int(data[i-1] * (PHI - 1)) % 256
            diff = (data[i] - prediction) % 256
            res.append(diff)
        return zlib.compress(res, level=9)
    else:
        # Распаковка
        raw = zlib.decompress(data)
        res = bytearray()
        res.append(raw[0])
        for i in range(1, len(raw)):
            prediction = int(res[i-1] * (PHI - 1)) % 256
            original_val = (raw[i] + prediction) % 256
            res.append(original_val)
        return res

# --- ИНТЕРФЕЙС ---
st.title("🌀 Phase Archiver V2.1")
st.write(f"Инструмент Николая. Метрика: $\pi=1, \Phi=1.618$")

uploaded_file = st.file_uploader("Загрузите любой файл", type=None)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    name = uploaded_file.name
    
    if name.endswith(".phase"):
        st.info("🔄 Восстановление из архива...")
        try:
            out = phase_logic(file_bytes, mode="unpack")
            st.success("Файл восстановлен!")
            st.download_button("📥 Скачать результат", io.BytesIO(out), file_name=name.replace(".phase", ""))
        except:
            st.error("Ошибка! Возможно, файл не является фазовым архивом.")
    else:
        st.info("🌀 Сжатие по фазе...")
        out = phase_logic(file_bytes, mode="pack")
        gain = (1 - len(out)/len(file_bytes)) * 100
        st.success(f"Готово! Эффективность: {gain:.2f}%")
        st.download_button("📥 Скачать .phase", io.BytesIO(out), file_name=name + ".phase")

st.divider()
st.caption("Если экран темный — обновите страницу через минуту.")
