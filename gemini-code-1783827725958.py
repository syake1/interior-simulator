import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ページ設定
st.set_page_config(
    page_title="AIインテリア・リフォームシミュレーター",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# タイトル
st.title("🏠 AIインテリア・リフォームシミュレーター (開発用プロトタイプ)")
st.caption("壁紙や床をカチカチ切り替えて、実際のメーカー品番がリアルタイムに連動するシステム")

# -------------------------------------------------------------------------
# 将来のAPI連携用の関数（プレースホルダー）
# -------------------------------------------------------------------------
def generate_ai_image(base_image, wallpaper, floor, furniture):
    """
    【将来の拡張用】
    ここにGoogle CloudのVertex AIやStable DiffusionのAPIを接続します。
    現在は手元で100%動くように、選択したデザインに応じてプレビュー画像を自動生成します。
    """
    # ベース画像がない場合はダミーを生成
    if base_image is None:
        img = Image.new("RGB", (800, 500), "#f0f2f6")
    else:
        img = Image.open(base_image).convert("RGB").resize((800, 500))
        
    draw = ImageDraw.Draw(img)
    
    # 壁紙のデザインに応じたオーバーレイ表現（簡易デモ用）
    if wallpaper == "青空・雲柄":
        # 上半分（壁・天井イメージ）を水色に
        draw.rectangle([0, 0, 800, 250], fill="#87CEEB")
        draw.ellipse([150, 50, 250, 100], fill="white")
        draw.ellipse([180, 70, 300, 120], fill="white")
        draw.ellipse([450, 80, 550, 130], fill="white")
    elif wallpaper == "コンクリート調":
        draw.rectangle([0, 0, 800, 250], fill="#808080")
        # コンクリートのセパ穴風の模様
        for x in [100, 300, 500, 700]:
            for y in [50, 180]:
                draw.ellipse([x, y, x+10, y+10], fill="#505050")
    elif wallpaper == "モダン北欧（レンガ調）":
        draw.rectangle([0, 0, 800, 250], fill="#D2B48C")
        for y in range(20, 240, 30):
            draw.line([0, y, 800, y], fill="#FFFFFF", width=2)
            
    # 床のデザインに応じたオーバーレイ表現
    if floor == "ウォルナット（濃い木目）":
        draw.rectangle([0, 250, 800, 500], fill="#4A2711")
        for x in range(0, 800, 40):
            draw.line([x, 250, x, 500], fill="#2E1708", width=1)
    elif floor == "オーク（明るい木目）":
        draw.rectangle([0, 250, 800, 500], fill="#DEB887")
        for x in range(0, 800, 40):
            draw.line([x, 250, x, 500], fill="#CD853F", width=1)
    elif floor == "大理石風（ホワイト）":
        draw.rectangle([0, 250, 800, 500], fill="#F5F5F5")
        # 大理石の模様風の線
        draw.line([50, 250, 200, 500], fill="#D3D3D3", width=2)
        draw.line([400, 250, 300, 500], fill="#D3D3D3", width=2)
        draw.line([600, 250, 750, 500], fill="#E0E0E0", width=3)

    # 家具のテキストプロンプトがある場合、画面にバッジを表示
    if furniture:
        draw.rectangle([50, 350, 350, 430], fill="#FFFAF0", outline="#D2691E", width=3)
        try:
            draw.text((70, 380), f"[AI配置]: {furniture}", fill="#8B4513")
        except:
            pass
            
    return img

# -------------------------------------------------------------------------
# 商品データベース（モックデータ：選択したデザインに完全に連動）
# -------------------------------------------------------------------------
catalog_data = {
    "wallpaper": {
        "標準の壁紙": [
            {"maker": "サンゲツ", "code": "SP9701", "name": "量産型ホワイトクロス（織物調）", "url": "https://www.sangetsu.co.jp/"},
            {"maker": "リリカラ", "code": "LB-9201", "name": "ベースプレーンクロス", "url": "https://www.lineame.top/"}
        ],
        "青空・雲柄": [
            {"maker": "サンゲツ", "code": "FE76860", "name": "ファイン 空・雲柄アクセント", "url": "https://www.sangetsu.co.jp/"},
            {"maker": "サンゲツ", "code": "SGM1349", "name": "エクセレクト ORI（高級織物・雲柄）", "url": "https://www.sangetsu.co.jp/"},
            {"maker": "リリカラ", "code": "LV2396", "name": "V-wall ミッフィー くも柄クロス", "url": "https://www.lineame.top/"}
        ],
        "コンクリート調": [
            {"maker": "サンゲツ", "code": "FE76630", "name": "コンクリート放し風（モダン）", "url": "https://www.sangetsu.co.jp/"},
            {"maker": "リリカラ", "code": "LV2223", "name": "インダストリアル リアルモルタル", "url": "https://www.lineame.top/"},
            {"maker": "東リ", "code": "WVP4132", "name": "パワー1000 打ちっぱなし風", "url": "https://www.toli.co.jp/"}
        ],
        "モダン北欧（レンガ調）": [
            {"maker": "サンゲツ", "code": "RE53325", "name": "リザーブ カフェ風ブリック", "url": "https://www.sangetsu.co.jp/"},
            {"maker": "シンコール", "code": "BB9412", "name": "ベスト ホワイトレンガ調", "url": "https://www.sincol-group.jp/"}
        ]
    },
    "floor": {
        "標準の床": [
            {"maker": "東リ", "code": "CF9501", "name": "クッションフロア ベーシックオーク", "url": "https://www.toli.co.jp/"}
        ],
        "ウォルナット（濃い木目）": [
            {"maker": "サンゲツ", "code": "HM11023", "name": "クッションフロア ビターウォルナット", "url": "https://www.sangetsu.co.jp/"},
            {"maker": "東リ", "code": "CF9513", "name": "CFシート-H ウォルナット板巾12cm", "url": "https://www.toli.co.jp/"}
        ],
        "オーク（明るい木目）": [
            {"maker": "サンゲツ", "code": "HM11011", "name": "クッションフロア ライトオーク", "url": "https://www.sangetsu.co.jp/"},
            {"maker": "リリカラ", "code": "LH81312", "name": "エルワイタイル ナチュラルオーク", "url": "https://www.lineame.top/"}
        ],
        "大理石風（ホワイト）": [
            {"maker": "サンゲツ", "code": "HM11091", "name": "目地なし ビアンコ大理石", "url": "https://www.sangetsu.co.jp/"},
            {"maker": "東リ", "code": "CF9545", "name": "クッションフロア 東リマルキーナ", "url": "https://www.toli.co.jp/"}
        ]
    }
}

# -------------------------------------------------------------------------
# UI構成
# -------------------------------------------------------------------------

# サイドバー：操作・設定パネル
with st.sidebar:
    st.header("🛠️ コントロールパネル")
    st.write("画面を見ながらここでデザインを切り替えます。")
    
    # 1. 画像アップロード
    uploaded_file = st.file_uploader("📂 1. お部屋の写真をアップロード", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.success("写真を読み込みました！")
    else:
        st.info("※未アップロード時はサンプル部屋でシミュレートします")
        
    st.write("---")
    
    # 2. デザイン追加・変更の選択（カチカチ切り替え）
    st.subheader("🎨 2. デザインの追加・変更")
    
    selected_wallpaper = st.selectbox(
        "壁紙（クロス）のデザイン変更",
        options=["標準の壁紙", "青空・雲柄", "コンクリート調", "モダン北欧（レンガ調）"]
    )
    
    selected_floor = st.selectbox(
        "床（クッションフロア・タイル）の変更",
        options=["標準の床", "ウォルナット（濃い木目）", "オーク（明るい木目）", "大理石風（ホワイト）"]
    )
    
    # 自由入力欄
    custom_furniture = st.text_input("追加したい家具プロンプト (例: カウチソファ、ローテーブル)", value="")
    
    st.write("---")
    # 将来の有料決済デモ用スイッチ
    st.subheader("💰 将来のマネタイズ機能")
    pay_mode = st.checkbox("【テスト】1回100円の決済画面を挟む", value=False)
    if pay_mode:
        st.warning("⚠️ 現在プレビューモードです。本番環境ではStripe決済完了後に画像が生成されます。")

# -------------------------------------------------------------------------
# メインコンテンツエリア
# -------------------------------------------------------------------------
col_img, col_info = st.columns([3, 2])

with col_img:
    st.subheader("🖼️ リアルタイム・プレビュー")
    
    # 画像生成処理の呼び出し
    preview_image = generate_ai_image(uploaded_file, selected_wallpaper, selected_floor, custom_furniture)
    
    # 画面に画像を表示
    st.image(preview_image, caption=f"現在のシミュレーション: 【壁紙: {selected_wallpaper}】×【床: {selected_floor}】", use_container_width=True)
    
    st.info("💡 左側のコントロールパネルを切り替えると、上の部屋の画像がリアルタイムに変化し、隣の品番リストも連動して切り替わります。")

with col_info:
    st.subheader("📋 連動する実際のメーカー品番・商品名")
    st.write("選択されたデザインに適合する、日本の主要メーカーの型番データです。")
    
    # 壁紙の品番リスト表示
    st.markdown("### 🧱 壁紙クロス候補")
    wp_items = catalog_data["wallpaper"].get(selected_wallpaper, [])
    for item in wp_items:
        st.markdown(f"**・[{item['maker']}] 品番: {item['code']}**")
        st.caption(f" 商品名: {item['name']}")
        
    st.write("")
    
    # 床材の品番リスト表示
    st.markdown("### 🪵 床材・クッションフロア候補")
    fl_items = catalog_data["floor"].get(selected_floor, [])
    for item in fl_items:
        st.markdown(f"**・[{item['maker']}] 品番: {item['code']}**")
        st.caption(f" 商品名: {item['name']}")

    st.write("")
    
    # 家具の自動検索モック
    if custom_furniture:
        st.markdown(f"### 🛋️ 家具のネット検索連動結果")
        st.success(f"「{custom_furniture}」に類似する売れ筋商品を検出しました")
        st.markdown(f"1. **[LOWYA]** モダンデザイン {custom_furniture} (参考価格: ¥24,990)")
        st.markdown(f"2. **[無印良品]** オーク材使用テイスト商品 (参考価格: ¥19,800)")
        st.caption("※本番環境では、ここからAmazon・楽天等のアフィリエイトリンクへ繋ぎ、紹介報酬（数％）を獲得できます。")