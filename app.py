import streamlit as st
import requests
import json
from datetime import datetime

# Page Configuration - Premium Look Ke Liye
st.set_page_config(page_title="Bharat Express - Premium News Portal", page_icon="📰", layout="wide")

# ================= SECURE CONFIGURATION =================
# Ab koi bhi key code me nahi hai. Ye sab Streamlit Dashboard se aayega.
GNEWS_API_KEY = st.secrets["GNEWS_API_KEY"] 
ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]

# Local Database Simulation
if "custom_articles" not in st.session_state:
    st.session_state["custom_articles"] = []

# ================= HELPER FUNCTIONS =================
def fetch_global_news(category):
    category_map = {
        "Desh-Videsh": "world",
        "Politics": "nation",
        "Entertainment": "entertainment",
        "Games": "sports"
    }
    gnews_category = category_map.get(category, "general")
    url = f"https://gnews.io{gnews_category}&lang=hi&country=in&apikey={GNEWS_API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("articles", [])
        else:
            return []
    except:
        return []

# ================= PREMIUM BRANDING & HEADER =================
st.markdown("""
    <style>
    .main-title { font-size:45px !important; font-weight: bold; color: #E50914; text-align: center; margin-bottom: 0px;}
    .sub-title { font-size:18px !important; text-align: center; color: #555; margin-bottom: 20px;}
    .news-card { padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 15px; background-color: #f9f9f9; }
    .news-title { font-size: 20px; font-weight: bold; color: #111; text-decoration: none; }
    .news-title:hover { color: #E50914; }
    .badge { background-color: #E50914; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    </style>
""", unsafe_with_html=True)

st.markdown('<p class="main-title">📰 BHARAT EXPRESS</p>', unsafe_with_html=True)
st.markdown('<p class="sub-title">Sabse Tez, Sabse Nishpaksh | Desh Videsh Ki Har Khabar</p>', unsafe_with_html=True)
st.write("---")

# ================= MULTI-PAGE NAVIGATION PANEL =================
st.sidebar.title("📌 Navigation Panel")
page = st.sidebar.radio("Go to Section:", ["Desh-Videsh", "Politics", "Entertainment", "Games", "⚙️ Admin Portal"])

# ================= DISPLAY LOGIC =================
if page != "⚙️ Admin Portal":
    st.header(f"🔥 Latest {page} Headlines")
    
    # 1. Custom Articles
    section_custom_posts = [post for post in st.session_state["custom_articles"] if post["category"] == page]
    if section_custom_posts:
        st.subheader("📌 Breaking Exclusive")
        for post in section_custom_posts:
            with st.container():
                st.markdown(f'<div class="news-card">', unsafe_with_html=True)
                col1, col2 = st.columns()
                with col1:
                    if post["image"]:
                        st.image(post["image"], use_container_width=True)
                    else:
                        st.image("https://placeholder.com", use_container_width=True)
                with col2:
                    st.markdown(f'<span class="badge">EXCLUSIVE</span>', unsafe_with_html=True)
                    st.markdown(f'<p class="news-title">{post["title"]}</p>', unsafe_with_html=True)
                    st.caption(f"Published on: {post['date']} | By: Editor In Chief")
                    st.write(post["content"])
                st.markdown('</div>', unsafe_with_html=True)
        st.write("---")

    # 2. Automatic GNews API News
    with st.spinner("Fetching latest news from internet..."):
        api_articles = fetch_global_news(page)
        
    if api_articles:
        for art in api_articles:
            with st.container():
                st.markdown(f'<div class="news-card">', unsafe_with_html=True)
                col1, col2 = st.columns()
                with col1:
                    if art.get("image"):
                        st.image(art["image"], use_container_width=True)
                    else:
                        st.image("https://placeholder.com", use_container_width=True)
                with col2:
                    st.markdown(f'<a class="news-title" href="{art["url"]}" target="_blank">{art["title"]}</a>', unsafe_with_html=True)
                    st.caption(f"Source: {art['source']['name']} | Published at: {art['publishedAt'][:10]}")
                    st.write(art.get("description", "No description available."))
                    st.markdown(f'[Read full story on {art["source"]["name"]}]({art["url"]})')
                st.markdown('</div>', unsafe_with_html=True)
    else:
        st.info("Iss section ke liye automatic news load nahi ho payi. Kirpya thodi der baad check karein.")

# ================= WORKFLOW FOR ADMIN PORTAL =================
else:
    st.header("⚙️ News Admin Control Room")
    password_input = st.text_input("Enter Admin Security Password:", type="password")
    
    if password_input == ADMIN_PASSWORD:
        st.success("Access Granted! Welcome Back, Editor.")
        st.write("---")
        
        st.subheader("✍️ Publish a New Article")
        post_title = st.text_input("Article Headline (Mukhya Samachar):")
        post_category = st.selectbox("Select News Section (Category):", ["Desh-Videsh", "Politics", "Entertainment", "Games"])
        post_image_url = st.text_input("Image Web URL (Optional):")
        post_content = st.text_area("Write Detailed News Content:", height=200)
        
        if st.button("Publish News Live 🚀"):
            if post_title and post_content:
                new_article = {
                    "title": post_title,
                    "category": post_category,
                    "image": post_image_url if post_image_url else None,
                    "content": post_content,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state["custom_articles"].insert(0, new_article)
                st.balloons()
                st.success(f"Mubarak ho! Aapka article live ho gaya hai.")
            else:
                st.error("Headline aur Content likhna zaroori hai!")
    elif password_input != "":
        st.error("Galat Password!")
              
