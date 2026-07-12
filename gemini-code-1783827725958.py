import streamlit as st

# ページ設定
st.set_page_config(
    page_title="内装リフォーム・シミュレーター",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏠 内装リフォーム・シミュレーター (品番連動デモ版)")
st.caption("天井・壁・床（クロス）を切り替えて、実際のメーカー品番を瞬時に確認できるシステム")

# -------------------------------------------------------------------------
# データ準備（選んだ組み合わせに連動する画像と品番）
# -------------------------------------------------------------------------
# 高画質な部屋のベース画像（Unsplashのフリー素材）
IMAGES = {
    "コンクリート": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
    "レンガ": "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?auto=format&fit=crop&w=800&q=80",
    "白無地": "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=800&q=80",
    "木目調": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80",
    "大理石": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=800&q=80",
    "ウォルナット": "https://images.unsplash.com/photo-1540518614846-7eded433c457?auto=format&fit=crop&w=800&q=80",
}

catalog_data = {
    "ceiling": {
        "白無地": {"maker": "サンゲツ", "code": "SP9701", "name": "量産型ホワイトクロス（織物調）"},
        "木目調": {"maker": "リリカラ", "code": "LV2245", "name": "プレミアムウッド（天井おすすめ）"}
    },
    "wall": {
        "白無地": {"maker": "リリカラ", "code": "LB-9201", "name": "ベースプレーンクロス"},
        "コンクリート": {"maker": "サンゲツ", "code": "FE76630", "name": "コンクリート放し風（モダン）"},
        "レンガ": {"maker": "サンゲツ", "code": "RE53325", "name": "リザーブ カフェ風ブリック"}
    },
    "floor": {
        "木目調": {"maker": "東リ", "code": "CF9501", "name": "クッションフロア ベーシックオーク"},
        "ウォルナット": {"maker": "サンゲツ", "code": "HM11023", "name": "クッションフロア ビターウォルナット"},
        "大理石": {"maker": "サンゲツ", "code": "HM11091", "name": "目地なし ビアンコ大理石"}
    }
}

# -------------------------------------------------------------------------
# サイドバー（選択画面）
# -------------------------------------------------------------------------
with st.sidebar:
    st.header("🧱 部位別の選択")
    st.write("リフォームしたい場所の柄を選んでください。")
    
    # セレクトボックスで場所を選択
    select_ceiling = st.selectbox("① 天井の仕上げ", list(catalog_data["ceiling"].keys()))
    select_wall = st.selectbox("② 壁クロスの柄", list(catalog_data["wall"].keys()))
    select_floor = st.selectbox("③ 床・クロスの種類", list(catalog_data["floor"].keys()))
    
    st.write("---")
    st.info("💡 選択を変えると、右側の画像とメーカー品番がすぐに連動して切り替わります。")

# -------------------------------------------------------------------------
# メイン画面（表示画面）
# -------------------------------------------------------------------------
col_img, col_info = st.columns([4, 3])

with col_img:
    st.subheader("🖼️ 仕上がりイメージプレビュー")
    
    # 壁の選択に合わせて、最高に鮮明でおしゃれな部屋の画像をパッと切り替える
    selected_image_url = IMAGES.get(select_wall, IMAGES["白無地"])
    st.image(selected_image_url, caption=f"【現在のイメージ】天井: {select_ceiling} / 壁: {select_wall} / 床: {select_floor}", use_container_width=True)

with col_info:
    st.subheader("📋 決定されたメーカー品番")
    st.write("選んだ内装材の正式な型番リストです。")
    st.write("---")
    
    # 天井の品番
    c_item = catalog_data["ceiling"][select_ceiling]
    st.markdown("### 🔼 天井クロス")
    st.markdown(f"**・[{c_item['maker']}] 品番: {c_item['code']}**")
    st.caption(f"商品名: {c_item['name']}")
    
    st.write("")
    
    # 壁の品番
    w_item = catalog_data["wall"][select_wall]
    st.markdown("### 🧱 壁クロス")
    st.markdown(f"**・[{w_item['maker']}] 品番: {w_item['code']}**")
    st.caption(f"商品名: {w_item['name']}")
    
    st.write("")
    
    # 床の品番
    f_item = catalog_data["floor"][select_floor]
    st.markdown("### 🪵 床材・クッションフロア")
    st.markdown(f"**・[{f_item['maker']}] 品番: {f_item['code']}**")
    st.caption(f"商品名: {f_item['name']}")
