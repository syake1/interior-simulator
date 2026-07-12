import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# ページ設定
st.set_page_config(
    page_title="AIインテリア・リフォームシミュレーター",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏠 AIインテリア・リフォームシミュレーター (Google Gemini版)")
st.caption("Googleの画像生成AI（Imagen 3）を接続し、プロンプト通りに鮮明なリフォーム画像を生成するシステム")

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
    selected_wallpaper = st.text_input("壁紙クロスへの指示", value="コンクリート調のモダンな壁紙")
    selected_floor = st.text_input("床材への指示", value="大理石風の白い床")
    custom_furniture = st.text_input("配置したい家具", value="北欧風のローテーブル")
    
    st.write("---")
    run_button = st.button("🚀 このプロンプトでAI画像生成", type="primary")

# メイン画面
col_img, col_info = st.columns([3, 2])

with col_img:
    st.subheader("🖼️ AI生成プレビュー")
    
    if run_button:
        # 安全な暗号庫（Secrets）からGoogleのAPIキーを読み込む
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("Streamlitの管理画面でAPIキー（GEMINI_API_KEY）が設定されていません。右下の「Manage app」から設定してください。")
        else:
            with st.spinner("Google AIが鮮明なリフォーム画像を生成中...（約10〜15秒）"):
                try:
                    api_key = st.secrets["GEMINI_API_KEY"]
                    
                    # Google Imagen 3 の画像生成エンドポイント
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:generateImages?key={api_key}"
                    
                    prompt_text = f"A realistic and high-quality interior photo of a Japanese residential room. The wallpaper is {selected_wallpaper}. The flooring is {selected_floor}. The room is furnished with {custom_furniture}. Bright natural lighting, professional architectural photography style."
                    
                    payload = {
                        "prompt": prompt_text,
                        "numberOfImages": 1,
                        "outputMimeType": "image/jpeg",
                        "aspectRatio": "1:1"
                    }
                    
                    # AIへのリクエスト送信
                    response = requests.post(url, json=payload)
                    res_data = response.json()
                    
                    if response.status_code == 200:
                        # 特殊な画像データを画面に表示できる形に復元
                        img_b64 = res_data["generatedImages"][0]["image"]["imageBytes"]
                        img_bytes = base64.b64decode(img_b64)
                        st.session_state.preview_img = Image.open(BytesIO(img_bytes))
                    else:
                        st.error(f"APIエラー: {res_data.get('error', {}).get('message', '不明なエラー')}")
                    
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
                    
    if "preview_img" in st.session_state:
        st.image(st.session_state.preview_img, caption="Google AIが生成したリフォーム後のイメージ", use_container_width=True)
    else:
        st.info("💡 左側にプロンプトを入力し、「AI画像生成」ボタンを押すと、ここに最高画質の部屋画像が現れます。")

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
