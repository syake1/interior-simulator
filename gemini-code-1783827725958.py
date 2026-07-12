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

st.title("🏠 AIインテリア・リフォームシミュレーター")
st.caption("写真をアップロードし、天井・壁・クロス（床）を個別に指定してAI画像生成・品番連動するシステム")

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
    st.header("🛠️ コントロールパネル")
    
    # 1. 画像アップロード場所を一番上に配置
    uploaded_file = st.file_uploader("📂 1. お部屋の写真をアップロード", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.success("写真を読み込みました！")
        
    st.write("---")
    st.subheader("🎨 2. 部位別リフォームプロンプト入力")
    
    # 天井・壁・クロスの入力欄
    selected_ceiling = st.text_input("① 天井への指示", value="白い無地の天井クロス")
    selected_wall = st.text_input("② 壁への指示", value="コンクリート調のモダンな壁紙")
    selected_floor = st.text_input("③ 床・クロスへの指示", value="大理石風の白い床")
    
    st.write("---")
    run_button = st.button("🚀 このプロンプトでAI画像生成", type="primary")

# メイン画面
col_img, col_info = st.columns([3, 2])

with col_img:
    st.subheader("🖼️ AI生成プレビュー")
    
    if run_button:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("Streamlitの管理画面でAPIキー（GEMINI_API_KEY）が設定されていません。右下の「Manage app」から設定してください。")
        else:
            with st.spinner("Google AIが指定された部位に合わせて画像を生成中...（約10〜15秒）"):
                try:
                    api_key = st.secrets["GEMINI_API_KEY"]
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:generateImages?key={api_key}"
                    
                    # 天井、壁、床の指定を1つの指示書（英語）に組み立てる
                    prompt_text = f"A realistic and high-quality interior photo of a residential room. The ceiling is {selected_ceiling}. The walls are {selected_wall}. The flooring is {selected_floor}. Bright natural lighting, professional architectural photography style."
                    
                    payload = {
                        "prompt": prompt_text,
                        "numberOfImages": 1,
                        "outputMimeType": "image/jpeg",
                        "aspectRatio": "1:1"
                    }
                    
                    response = requests.post(url, json=payload)
                    res_data = response.json()
                    
                    if response.status_code == 200:
                        img_b64 = res_data["generatedImages"][0]["image"]["imageBytes"]
                        img_bytes = base64.b64decode(img_b64)
                        st.session_state.preview_img = Image.open(BytesIO(img_bytes))
                    else:
                        st.error(f"APIエラー: {res_data.get('error', {}).get('message', '不明なエラー')}")
                    
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
                    
    if "preview_img" in st.session_state:
        st.image(st.session_state.preview_img, caption="AIが生成したリフォーム後のイメージ", use_container_width=True)
    elif uploaded_file is not None:
        st.image(uploaded_file, caption="アップロードされた現状の写真（まだAI生成していません）", use_container_width=True)
    else:
        st.info("💡 左側でお部屋の写真をアップロードし、天井・壁・クロスのイメージを言葉で入力して「AI画像生成」ボタンを押してください。")

with col_info:
    st.subheader("📋 自動検出されたメーカー品番")
    
    st.markdown("### 🧱 壁紙クロス候補（壁の指示から連動）")
    wp_prompt = selected_wall.lower()
    wp_key = "標準"
    if "青" in wp_prompt or "雲" in wp_prompt or "空" in wp_prompt: wp_key = "青空"
    elif "コンクリート" in wp_prompt or "モルタル" in wp_prompt or "グレー" in wp_prompt: wp_key = "コンクリート"
    elif "レンガ" in wp_prompt or "タイル" in wp_prompt: wp_key = "レンガ"
    
    for item in catalog_data["wallpaper"][wp_key]:
        st.markdown(f"**・[{item['maker']}] 品番: {item['code']}**")
        st.caption(f" 商品名: {item['name']}")
        
    st.write("")
    st.markdown("### 🪵 床材・クッションフロア候補（床の指示から連動）")
    fl_prompt = selected_floor.lower()
    fl_key = "標準"
    if "ウォルナット" in fl_prompt or "濃い" in fl_prompt or "ダーク" in fl_prompt: fl_key = "ウォルナット"
    elif "オーク" in fl_prompt or "明るい" in fl_prompt or "木目" in fl_prompt: fl_key = "オーク"
    elif "大理石" in fl_prompt or "白" in fl_prompt: fl_key = "大理石"
    
    for item in catalog_data["floor"][fl_key]:
        st.markdown(f"**・[{item['maker']}] 品番: {item['code']}**")
        st.caption(f" 商品名: {item['name']}")
