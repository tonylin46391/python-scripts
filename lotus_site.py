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

# 訂購者資訊
st.header("📋 訂購者資訊")
name = st.text_input("請輸入姓名")
phone = st.text_input("請輸入電話")
address = st.text_input("請輸入地址 (若選宅配填寫)")

# 產品展示
st.header("📷 新鮮蓮藕展示")
st.image(
    "picture/oosay_01.jpg",
    caption="新鮮現採蓮藕",
    use_container_width=True
)

# 價目表
st.header("💰 價目表")
st.table({"產品": list(products.keys()), "價格 (NTD)": list(products.values())})

# 購物區
st.header("🛒 新增商品到購物車")
product = st.selectbox("選擇產品", list(products.keys()))
quantity = st.number_input("數量", min_value=1, step=1)

if st.button("加入購物車"):
    st.session_state.cart.append({
        "product": product,
        "price": products[product],
        "qty": quantity
    })
    st.success(f"已加入購物車：{product} × {quantity}")

# 顯示購物車
st.header("🛍️ 我的購物車")
if st.session_state.cart:
    cart_items = []
    total = 0
    for item in st.session_state.cart:
        subtotal = item["price"] * item["qty"]
        total += subtotal
        cart_items.append({
            "產品": item["product"],
            "數量": item["qty"],
            "單價 (NTD)": item["price"],
            "小計 (NTD)": subtotal
        })

    st.table(cart_items)
    st.markdown(f"### 💵 總金額：NTD {total}")

    # 選擇配送方式
    st.header("🚚 選擇配送方式")
    delivery = st.radio(
        "配送方式",
        ("超商取貨 (7-ELEVEN / 全家冷凍)", "宅配到家")
    )

    # 選擇支付方式
    st.header("💳 選擇支付方式")
    payment = st.radio(
        "支付方式",
        ("信用卡", "銀行轉帳", "LINE Pay / 行動支付", "超商付款")
    )

    # 提交訂單按鈕
    if st.button("提交訂單"):
        if not (name.strip() and phone.strip()):
            st.warning("⚠ 請填寫完整的姓名與電話才能下單。")
        elif delivery == "宅配到家" and not address.strip():
            st.warning("⚠ 請填寫完整地址以便宅配。")
        else:
            st.success(f"✅ 感謝 {name} 的訂購！")
            st.write(f"電話：{phone}")
            if delivery == "宅配到家":
                st.write(f"配送地址：{address}")
            st.write(f"配送方式：{delivery}")
            st.write(f"支付方式：{payment}")
            st.write("訂購商品如下：")
            for item in st.session_state.cart:
                st.write(f"- {item['product']} × {item['qty']}")
            st.markdown(f"### 💵 總金額：NTD {total}")
            st.info("我們將盡快與您聯繫，完成付款與配送。")
            st.session_state.cart = []  # 清空購物車

else:
    st.info("購物車目前是空的，請先加入商品。")
