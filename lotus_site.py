import streamlit as st

# 初始化購物車
if "cart" not in st.session_state:
    st.session_state.cart = []

# 商品資料
products = {
    "蓮藕 (1公斤裝)": 150,
    "蓮藕粉 (500g)": 200,
    "蓮藕禮盒 (3公斤)": 600
}

# 網站標題
st.title("🌸 蓮藕直送 ─ 新鮮健康好滋味")

# 簡介
st.markdown("""
歡迎來到 **蓮藕直送**！  
我們提供產地直送的優質蓮藕，無農藥、純天然。  
無論是煮湯、炒菜、涼拌，都能吃得健康又安心。  
""")

# 產品展示
st.header("📷 新鮮蓮藕展示")
st.image("C:/Users/hp/AppData/Local/Programs/Python/Python313/Scripts/picture/oosay_01.jpg", caption="新鮮現採蓮藕", use_container_width=True)

# 價目表
st.header("💰 價目表")
st.table({"產品": list(products.keys()), "價格 (NTD)": list(products.values())})

# 購物區
st.header("🛒 新增商品到購物車")
product = st.selectbox("選擇產品", list(products.keys()))
quantity = st.number_input("數量", min_value=1, step=1)

if st.button("加入購物車"):
    st.session_state.cart.append({"product": product, "price": products[product], "qty": quantity})
    st.success(f"已加入購物車：{product} × {quantity}")

# 顯示購物車
st.header("🛍️ 我的購物車")
if st.session_state.cart:
    cart_items = []
    total = 0
    for item in st.session_state.cart:
        subtotal = item["price"] * item["qty"]
        total += subtotal
        cart_items.append([item["product"], item["qty"], item["price"], subtotal])

    st.table(cart_items)
    st.markdown(f"### 💵 總金額：NTD {total}")

    if st.button("提交訂單"):
        st.success("✅ 感謝您的訂購！我們將盡快與您聯繫。")
        st.session_state.cart = []  # 清空購物車
else:
    st.info("購物車目前是空的，請先加入商品。")
if st.button("提交訂單"):
    if name and phone:
        st.success(f"✅ 感謝 {name} 的訂購！我們會盡快與您聯繫（電話：{phone}）。\n\n"
                   f"您訂購了 {product} × {quantity}。")
    else:
        st.warning("⚠ 請填寫完整的姓名與電話才能下單。")