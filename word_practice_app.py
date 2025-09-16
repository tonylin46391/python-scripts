import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd

# 題庫
words = [
    "學年", "希望", "坐下", "位子", "課本", "淡淡的", "書香", "老師",
    "以前", "大聲", "成為", "用力", "只有", "高矮", "現在", "開始", "還要"
]

# 初始化 session state
if "index" not in st.session_state:
    st.session_state.index = 0
if "answered" not in st.session_state:
    st.session_state.answered = {w: None for w in words}
if "retry_time" not in st.session_state:
    st.session_state.retry_time = {}
if "history" not in st.session_state:
    st.session_state.history = []
if "stats" not in st.session_state:
    st.session_state.stats = {w: {"正確": 0, "錯誤": 0} for w in words}

st.title("🎧 聽音辨字練習 App (自動發音 + 正確率統計)")

def generate_tts(word):
    """生成 TTS 並播放"""
    tts = gTTS(word, lang="zh-TW")
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp.read(), format="audio/mp3")

def get_next_word():
    now = datetime.datetime.now()
    # 優先出現答錯且已到時間的題目
    for w, t in list(st.session_state.retry_time.items()):
        if now >= t:
            return w
    # 若全部答對一輪，重新開始
    if all(v == True for v in st.session_state.answered.values()):
        st.session_state.answered = {w: None for w in words}
        st.success("🎉 恭喜完成一輪！開始第二輪複習！")
    return words[st.session_state.index]

# 取得目前題目
current_word = get_next_word()
input_key = f"input_{current_word}_{st.session_state.index}"

st.subheader("👉 請聽發音並輸入正確的中文字：?")

# 自動播放音訊
if "played" not in st.session_state or st.session_state.get("last_word") != current_word:
    generate_tts(current_word)
    st.session_state.played = True
    st.session_state.last_word = current_word

# 使用 form 讓 Enter 自動提交
def submit_answer():
    user_input = st.session_state[input_key]
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if user_input == current_word:
        st.success("✅ 答對了！")
        st.session_state.answered[current_word] = True
        st.session_state.stats[current_word]["正確"] += 1
        st.session_state.history.append({"題目": current_word, "結果": "正確", "時間": now_str})
    else:
        st.error(f"❌ 答錯！正確答案是：{current_word}")
        st.session_state.answered[current_word] = False
        st.session_state.stats[current_word]["錯誤"] += 1
        st.session_state.history.append({"題目": current_word, "結果": "錯誤", "時間": now_str})
        # 1 分鐘後再出現
        st.session_state.retry_time[current_word] = datetime.datetime.now() + datetime.timedelta(minutes=1)
    
    # 自動跳下一題
    st.session_state.index = (st.session_state.index + 1) % len(words)
    # 清空輸入框
    st.session_state[input_key] = ""
    # 設置播放下一題標誌
    st.session_state.played = False
    # 強制刷新頁面播放下一題音訊
    st.experimental_rerun() if hasattr(st, "experimental_rerun") else st.session_state.update({})

with st.form(key=f"form_{current_word}", clear_on_submit=False):
    st.text_input("請輸入你聽到的中文字：", key=input_key)
    st.form_submit_button("提交答案", on_click=submit_answer)

# 顯示學習進度
st.sidebar.header("📊 學習進度")
done = sum(1 for v in st.session_state.answered.values() if v is True)
total = len(words)
st.sidebar.write(f"✅ 已正確答對：{done} / {total}")

# 顯示答題歷史
st.sidebar.header("📝 答題歷史")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.sidebar.dataframe(df, use_container_width=True)

# 顯示每個單字正確率統計
st.sidebar.header("📊 單字正確率統計")
stats_list = []
for w, s in st.session_state.stats.items():
    total_attempts = s["正確"] + s["錯誤"]
    rate = f"{s['正確']}/{total_attempts}" if total_attempts > 0 else "0/0"
    stats_list.append({"單字": w, "正確/總次數": rate})
df_stats = pd.DataFrame(stats_list)
st.sidebar.dataframe(df_stats, use_container_width=True)
