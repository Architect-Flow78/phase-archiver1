import streamlit as st
import zlib
import io

PHI = 1.61803398875

def phase_logic_v3(data, mode="pack"):
    if mode == "pack":
        res = bytearray()
        res.append(data[0])
        for i in range(1, len(data)):
            if i == 1:
                prediction = int(data[i-1] * (PHI - 1)) % 256
            else:
                # Второе зацепление (память нити)
                prediction = int((data[i-1] * PHI + data[i-2] * (1-PHI))) % 256
            diff = (data[i] - prediction) % 256
            res.append(diff)
        return zlib.compress(res, level=9)
    else:
        raw = zlib.decompress(data)
        res = bytearray()
        res.append(raw[0])
        for i in range(1, len(raw)):
            if i == 1:
                prediction = int(res[i-1] * (PHI - 1)) % 256
            else:
                prediction = int((res[i-1] * PHI + res[i-2] * (1-PHI))) % 256
            val = (raw[i] + prediction) % 256
            res.append(val)
        return res

# --- ИНТЕРФЕЙС ---
st.set_page_config(page_title="Phase vs ZIP Detector")
st.title("🌀 Phase vs ZIP: Битва за байты")
st.write(f"Параметры: $\pi=1, \Phi={PHI}$")

file = st.file_uploader("Загрузите файл для честного сравнения")

if file:
    raw = file.read()
    orig_size = len(raw)
    
    # 1. Сжатие обычным ZIP
    std_zip_data = zlib.compress(raw, level=9)
    std_size = len(std_zip_data)
    
    # 2. Сжатие твоим методом
    phase_data = phase_logic_v3(raw, mode="pack")
    phase_size = len(phase_data)
    
    # Расчеты
    st.subheader("Результаты сравнения")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Оригинал", f"{orig_size/1024:.1f} KB")
    col2.metric("Стандарт ZIP", f"{std_size/1024:.1f} KB")
    col3.metric("Метод Николая", f"{phase_size/1024:.1f} KB")

    # Считаем чистую выгоду над ЗИПом
    net_gain = (1 - phase_size/std_size) * 100
    
    if phase_size < std_size:
        st.success(f"🔥 ПОБЕДА! Мы обошли ZIP еще на {net_gain:.2f}%")
        st.write(f"Ты сэкономил дополнительные {(std_size - phase_size)/1024:.1f} KB, которые ZIP не смог увидеть.")
    else:
        st.warning(f"ZIP оказался сильнее на {abs(net_gain):.2f}%. Нить перетянута, нужна подстройка.")

    st.download_button("📥 Скачать .phase архив", io.BytesIO(phase_data), file_name=file.name + ".phase")

st.divider()
st.info("💡 Если ты видишь победу даже в 1-2% на PDF — это КРУТО. PDF уже сжат. Побеждать сжатое — это высший пилотаж.")
