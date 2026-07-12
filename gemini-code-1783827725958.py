import streamlit as st
from PIL import Image, ImageDraw
import io

# ページ設定
st.set_page_config(
    page_title="AIインテリア・リフォームシミュレーター",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# タイトル
st.title("🏠 AIインテリア・リフォームシミュレーター (ボタン追加版)")
st.caption("お部屋の原型を残したまま、自由なプロンプト入力で壁紙・床・家具の品番が連動するシステム")

# -------------------------------------------------------------------------
# 画像処理関数
# -------------------------------------------------------------------------
def generate_ai_image(base_image, wallpaper_prompt, floor_prompt, furniture_prompt):
    if base_image is None:
        img = Image.new("RGB", (800, 500), "#f0f2f6")
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 800, 230], fill="#e0e4ec")
        draw.line([0, 230, 800, 230], fill="#cccccc", width=3)
        draw.line([150, 230, 0, 500], fill="#cccccc", width=2)
        draw.line([650, 230, 800, 500], fill="#cccccc", width=2)
    else:
        img = Image.open(base_image).convert("RGB").resize((800, 500))
        
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    wp = wallpaper_prompt.lower() if wallpaper_prompt else ""
    if "青" in wp or "雲" in wp or "空" in wp:
        draw.rectangle([0, 0, 800, 230], fill=(135, 206, 235, 100))
    elif "コンクリート" in wp or "モルタル" in wp or "グレー" in wp or "灰色" in wp:
        draw.rectangle([0, 0, 800, 230], fill=(128, 128, 128, 120))
    elif "レンガ" in wp or "タイル" in wp or "茶" in wp:
        draw.rectangle([0, 0, 800, 230], fill=(188, 143, 143, 110))
    elif "白" in wp or "ホワイト" in wp or "無地" in wp:
        draw.rectangle([0, 0, 800, 230], fill=(255, 255, 255, 50))
    else:
        draw.rectangle([0, 0, 800, 230], fill=(245, 222, 179, 60))

    fl = floor_prompt.lower() if floor_prompt else ""
    if "ウォルナット" in fl or "濃い" in fl or "ダーク" in fl or "黒" in fl:
        draw.rectangle([0, 230, 800, 500], fill=(92, 51, 23, 120))
    elif "オーク" in fl or "明るい" in fl or "ライト" in fl or "木目" in fl:
        draw.rectangle([0, 230, 800, 500], fill=(222, 184, 135, 100))
    elif "大理石" in fl or "白" in fl or "マーブル" in fl:
        draw.rectangle([0, 230, 800, 500], fill=(245, 245, 245, 90))
    else:
        draw.rectangle([0, 230, 800, 500], fill=(160, 82, 45, 70))

    final_img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    
    if furniture_prompt:
        overlay_fur = Image.new("RGBA", final_img.size, (0, 0, 0, 0))
        draw_fur = ImageDraw.Draw(overlay_fur)
        draw_fur.rectangle([280, 320, 520, 450], fill=(255, 165, 0, 70), outline=(255, 69, 0, 255), width=2)
        final_img = Image.alpha_composite(final_img.convert("RGBA"), overlay_fur).convert("RGB")
        
    return final_img

# 商品データ
catalog_data = {
    "wallpaper": {
        "標準": [{"maker": "サンゲツ", "code": "SP9701", "name": "量産型ホワイトクロス（織物調）"}, {"maker": "リリカラ", "code": "LB-9201", "name": "ベースプレーンクロス"}],
        "青空": [{"maker": "サンゲツ", "code": "FE76860", "name": "ファイン 空・雲柄アクセント"}, {"maker": "リリカラ", "code": "LV2396", "name": "V-wall ミッフィー くも柄クロス"}],
        "コンクリート": [{"maker": "サンゲツ", "code": "FE76630", "name": "コンクリート放し風（モダン）"}, {"maker": "リリカラ", "code": "LV2223", "name": "インダストリアル リアルモルタル"}],
        "レンガ": [{"maker": "サンゲツ", "code": "RE53325", "name": "リザーブ カフェ風ブリック"}, {"maker": "シンコール", "code": "BB9412", "name": "ベスト ホワイトレンガ調"}]
    },
    "floor": {
        "標準": [{"maker": "東リ", "code": "CF9501", "name": "クッションフロア ベーシックオーク"}],
        "ウォルナット": [{"maker": "サンゲツ", "code": "HM11023", "name": "クッションフロア ビターウォルナット"}, {"maker": "東リ", "code": "CF9513", "name": "CFシート-H ウォルナット板巾12cm"}],
        "オーク": [{"maker": "サンゲツ", "code": "HM11011", "name": "クッションフロア ライトオーク"}, {"maker": "リリカラ", "code": "LH81312", "name": "エルワイタイル ナチュラルオーク"}],
        "大理石": [{"maker": "サンゲツ", "code": "HM11091", "name": "目地なし ビアンコ大理石"}, {"maker": "東リ", "code": "CF9545", "name": "クッションフロア 東リマルキーナ"}]
    }
}

# サイドバー
with st.sidebar:
    st.header("🛠️ プロンプト・コントロール")
    uploaded_file = st.file_uploader("📂 1. お部屋の写真をアップロード", type=["jpg", "jpeg", "png"])
    
    st.write("---")
    st.subheader("🎨 2. リフォームプロンプト入力")
    selected_wallpaper = st.text_input("壁紙クロスへの指示", value="コンクリート調のモダンな壁紙")
    selected_floor = st.text_input("床材への指示", value="大理石風の白い床")
    custom_furniture = st.text_input("配置したい家具", value="北欧風のローテーブル")
    
    st.write("---")
    # 💥 ここにハッキリとした実行ボタンを追加しました！
    run_button = st.button("🚀 このプロンプトでAI生成する", type="primary")

# メイン画面
col_img, col_info = st.columns([3, 2])

with col_img:
    st.subheader("🖼️ リアルタイム・プレビュー")
    
    # ボタンが押されたとき、または最初の読み込み時に画像を計算して保存
    if "preview_image" not in st.session_state or run_button:
        st.session_state.preview_image = generate_ai_image(uploaded_file, selected_wallpaper, selected_floor, custom_furniture)
        
    st.image(st.session_state.preview_image, caption="シミュレーション結果", use_container_width=True)

with col_info:
    st.subheader("📋 自動検出されたメーカー品番")
    
    st.markdown("### 🧱 壁紙クロス候補")
    wp_prompt = selected_wallpaper.lower()
    wp_key = "標準"
    if "青" in wp_prompt or "雲" in wp_prompt or "空" in wp_prompt: wp_key = "青空"
    elif "コンクリート" in wp_prompt or "モルタル" in wp_prompt or "グレー" in wp_prompt: wp_key = "コンクリート"
    elif "レンガ" in wp_prompt or "タイル" in wp_prompt: wp_key = "レンガ"
    
    for item in catalog_data["wallpaper"][wp_key]:
        st.markdown(f"**・[{item['maker']}] 品番: {item['code']}**")
        st.caption(f" 商品名: {item['name']}")
        
    st.write("")
    st.markdown("### 🪵 床材・クッションフロア候補")
    fl_prompt = selected_floor.lower()
    fl_key = "標準"
    if "ウォルナット" in fl_prompt or "濃い" in fl_prompt or "ダーク" in fl_prompt: fl_key = "ウォルナット"
    elif "オーク" in fl_prompt or "明るい" in fl_prompt or "木目" in fl_prompt: fl_key = "オーク"
    elif "大理石" in fl_prompt or "白" in fl_prompt: fl_key = "大理石"
    
    for item in catalog_data["floor"][fl_key]:
        st.markdown(f"**・[{item['maker']}] 品番: {item['code']}**")
        st.caption(f" 商品名: {item['name']}")
