import streamlit as st

# 網站標題
st.title("🌸 蓮藕直送 ─ 新鮮健康好滋味")

# 簡介
st.markdown("""
歡迎來到 **蓮藕直送**！  
我們提供產地直送的優質蓮藕，無農藥、純天然。  
無論是煮湯、炒菜、涼拌，都能吃得健康又安心。
""")

# 產品圖片展示
st.header("📷 新鮮蓮藕展示")
st.image("https://i.imgur.com/0h5bV6s.jpeg", caption="新鮮現採蓮藕", use_column_width=True)

# 價目表
st.header("💰 價目表")
st.table({
    "產品": ["蓮藕 (1公斤裝)", "蓮藕粉 (500g)", "蓮藕禮盒 (3公斤)"],
    "價格 (NTD)": ["150", "200", "600"]
})

# 訂購表單
st.header("🛒 線上訂購")
name = st.text_input("姓名")
phone = st.text_input("電話")
product = st.selectbox("選擇產品", ["蓮藕 (1公斤裝)", "蓮藕粉 (500g)", "蓮藕禮盒 (3公斤)"])
quantity = st.number_input("數量", min_value=1, step=1)

if st.button("提交訂單"):
    if name and phone:
        st.success(f"✅ 感謝 {name} 的訂購！我們會盡快與您聯繫（電話：{phone}）。\n\n"
                   f"您訂購了 {product} × {quantity}。")
    else:
        st.warning("⚠ 請填寫完整的姓名與電話才能下單。")
