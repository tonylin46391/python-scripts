import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd

# 題庫
words = [
    "新學", "希望", "坐下", "位子", "課本", "淡淡的", "書香", "老師",
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
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "last_played_index" not in st.session_state:
    st.session_state.last_played_index = -1
if "feedback_msg" not in st.session_state:
    st.session_state.feedback_msg = ""

st.markdown("<h3>🎧 聽音辨字練習 App</h3>", unsafe_allow_html=True)

# 播放文字音訊
def play_word(word):
    tts = gTTS(word, lang="zh-TW")
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp.read(), format="audio/mp3")

# 取得下一題
def get_next_word():
    now = datetime.datetime.now()
    for w, t in list(st.session_state.retry_time.items()):
        if now >= t:
            return w
    if all(v is True for v in st.session_state.answered.values()):
        st.session_state.answered = {w: None for w in words}
        st.success("🎉 恭喜完成一輪！開始第二輪複習！")
    return words[st.session_state.index]

current_word = get_next_word()

# 顯示提示文字，不顯示答案
st.markdown("<h4>請聽發音並輸入正確的中文字：</h4>", unsafe_allow_html=True)

# 顯示答題提示訊息（答錯紅字 / 答對綠字）
if st.session_state.feedback_msg:
    st.markdown(st.session_state.feedback_msg, unsafe_allow_html=True)

# 答題提交 + 移到下一題
def submit_and_next():
    user_input = st.session_state.user_input.strip()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    feedback_html = ""
    # 判斷正確與否
    if user_input == current_word:
        result = "正確"
        st.session_state.answered[current_word] = True
        st.session_state.stats[current_word]["正確"] += 1
        feedback_html = f"<span style='color:green; font-weight:bold'>✅ 答對！</span>"
    else:
        result = "錯誤"
        st.session_state.answered[current_word] = False
        st.session_state.stats[current_word]["錯誤"] += 1
        st.session_state.retry_time[current_word] = datetime.datetime.now() + datetime.timedelta(minutes=1)
        # 不顯示答案，只提示錯誤
        feedback_html = f"<span style='color:red; font-weight:bold'>❌ 答錯！</span>"
    
    st.session_state.feedback_msg = feedback_html
    
    # 紀錄歷史：只在答錯時紀錄「錯誤答案」
    history_entry = {
        "題目": current_word,
        "結果": result,
        "時間": now_str
    }
    if result == "錯誤":
        history_entry["錯誤答案"] = user_input
    st.session_state.history.append(history_entry)
    
    # 移到下一題
    st.session_state.index = (st.session_state.index + 1) % len(words)
    st.session_state.user_input = ""  # 清空輸入框

# 輸入框，按 Enter 提交
st.text_input(
    "輸入你聽到的中文字：",
    key="user_input",
    on_change=submit_and_next
)

# 自動播放當前題目發音（避免重複播放）
if st.session_state.last_played_index != st.session_state.index:
    play_word(current_word)
    st.session_state.last_played_index = st.session_state.index

# 側邊欄：學習進度
st.sidebar.header("📊 學習進度")
done = sum(1 for v in st.session_state.answered.values() if v is True)
st.sidebar.write(f"✅ 已正確答對：{done} / {len(words)}")

# 側邊欄：答題歷史
st.sidebar.header("📝 答題歷史")
if st.session_state.history:
    df_hist = pd.DataFrame(st.session_state.history)
    # 交換「時間」與「錯誤答案」欄位位置：顯示為 題目、結果、錯誤答案、時間
    desired = ["題目", "結果"]
    if "錯誤答案" in df_hist.columns:
        desired.append("錯誤答案")
    if "時間" in df_hist.columns:
        desired.append("時間")
    df_hist = df_hist.reindex(columns=desired)
    st.sidebar.dataframe(df_hist, use_container_width=True)

# 側邊欄：單字正確率統計
st.sidebar.header("📊 單字正確率統計")
stats_list = []
for w, s in st.session_state.stats.items():
    total = s["正確"] + s["錯誤"]
    rate = f"{s['正確']}/{total}" if total > 0 else "0/0"
    stats_list.append({"單字": w, "正確/總次數": rate})
df_stats = pd.DataFrame(stats_list)
st.sidebar.dataframe(df_stats, use_container_width=True)
