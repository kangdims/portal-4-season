import datetime
from google import genai
from google.genai import types
import streamlit as st

# 1. Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Village of Oakhaven - Dynamic Municipal Portal",
    page_icon="🇨🇦",
    layout="wide",
)


# 2. Inisialisasi Gemini Client
@st.cache_resource
def get_gemini_client():
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


client = get_gemini_client()

# 3. System Instruction Gemini (Canadian English Persona)
SYSTEM_INSTRUCTION = """
You are "Maple", an empathetic AI Public Service Assistant for the Village of Oakhaven, Canada.
Your goal is to assist residents with seasonal municipal services, bylaws, and community support.

COMMUNICATION GUIDELINES:
1. LANGUAGE & SPELLING: Use Canadian English strictly (e.g., 'centre', 'neighbour', 'windrow', 'rec centre').
2. TONE: Warm, polite, practical, and helpful (friendly Canadian manner, ending with polite Canadian phrasing like 'eh' where appropriate).
3. SAFETY PROTOCOL: If an inquiry involves severe freezing, power outages, or emergencies, prioritize emergency contact numbers (911) immediately.
"""


# 4. Logika Penentuan Musim & Tema UI
def get_seasonal_theme(month: int, temp_c: int) -> dict:
    if month in [12, 1, 2]:
        return {
            "season": "Winter",
            "icon": "❄️",
            "bg_color": "#0f2027",
            "card_bg": "#1c313a",
            "accent_color": "#0288d1",
            "text_color": "#e0f7fa",
            "alert": "❄️ WINTER PARKING BAN ACTIVE: Public Works plows are clearing priority routes.",
            "services": [
                "🚜 Live Snowplow Tracker",
                "❄️ Report Driveway Windrow",
                "🔥 Emergency Warming Centres",
            ],
        }
    elif month in [3, 4, 5]:
        return {
            "season": "Spring",
            "icon": "🌱",
            "bg_color": "#112613",
            "card_bg": "#1b3e1d",
            "accent_color": "#388e3c",
            "text_color": "#e8f5e9",
            "alert": "🌧️ SPRING THAW ALERT: Watch for localized flooding and report potholes via 311.",
            "services": [
                "🕳️ Report Pothole (311)",
                "🌊 Creek Water Level Monitor",
                "🌱 Yard Waste & Green Bin Schedule",
            ],
        }
    elif month in [6, 7, 8]:
        return {
            "season": "Summer",
            "icon": "☀️",
            "bg_color": "#2c1d02",
            "card_bg": "#422d05",
            "accent_color": "#f57c00",
            "text_color": "#fff3e0",
            "alert": "🔥 AIR QUALITY ADVISORY: Check burn permit requirements before open fires.",
            "services": [
                "🏕️ Park & Rec Facility Booking",
                "🔥 Open Burn Permit Application",
                "🏊 Community Pool Schedule",
            ],
        }
    else:
        return {
            "season": "Autumn",
            "icon": "🍂",
            "bg_color": "#2a1508",
            "card_bg": "#40220e",
            "accent_color": "#d84315",
            "text_color": "#fbe9e7",
            "alert": "🍁 CURBSIDE LEAF COLLECTION: Keep storm drains clear of fallen leaves.",
            "services": [
                "🍂 Leaf Collection Map",
                "🏠 Senior Winterization Assistance",
                "🏛️ Town Hall Budget Consultation",
            ],
        }


# 5. Sidebar Controls (Simulator)
st.sidebar.header("⚙️ Weather & Season Simulator")
current_month = datetime.datetime.now().month
sim_month = st.sidebar.slider("Pilih Bulan", 1, 12, current_month)
sim_temp = st.sidebar.slider("Suhu Cuaca (°C)", -30, 35, -8)

theme = get_seasonal_theme(sim_month, sim_temp)

# 6. Injeksi Styling CSS Dinamis
custom_css = f"""
<style>
    .stApp {{
        background-color: {theme['bg_color']};
        color: {theme['text_color']};
    }}
    .season-card {{
        background-color: {theme['card_bg']};
        padding: 24px;
        border-radius: 12px;
        border-left: 6px solid {theme['accent_color']};
        margin-bottom: 20px;
    }}
    .alert-banner {{
        background-color: {theme['accent_color']};
        color: #ffffff;
        padding: 16px;
        border-radius: 8px;
        font-weight: bold;
        margin-bottom: 24px;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 7. Header Portal & Alert Banner
st.title(
    f"{theme['icon']} Village of Oakhaven — {theme['season']} Public Services"
)
st.caption(
    "🇨🇦 Municipal Automated Portal (Seasonal Dynamic Governance Framework)"
)

st.markdown(
    f"<div class='alert-banner'>{theme['alert']}</div>",
    unsafe_allow_html=True,
)

# 8. Layout Kartu Layanan Musiman
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div class='season-card'>", unsafe_allow_html=True)
    st.subheader("🌡️️ Environmental Status")
    st.metric(
        label="Current Temperature",
        value=f"{sim_temp} °C",
        delta=f"Active Season: {theme['season']}",
    )
    st.write(f"**Season Mode:** {theme['season']}")
    st.write("**Town Hall Operations:** Open (8:30 AM – 4:30 PM EST)")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='season-card'>", unsafe_allow_html=True)
    st.subheader(f"🛠️ Priority Services ({theme['season']})")
    for service in theme["services"]:
        st.button(service, key=f"btn_{service}")
    st.markdown("</div>", unsafe_allow_html=True)

# 9. Asisten AI Maple (Integrasi Gemini API)
st.divider()
st.subheader("💬 Ask Maple — AI Municipal Assistant")

user_query = st.text_input(
    "Ask a question about municipal services (Canadian English):",
    placeholder="e.g., A plow blocked my driveway with snow, what should I do eh?",
)

if user_query:
    if not client:
        st.error(
            "⚠️ API Key tidak ditemukan! Pastikan `.streamlit/secrets.toml` sudah terisi `GEMINI_API_KEY`."
        )
    else:
        with st.spinner("Maple is typing..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"Active Season Context: {theme['season']} ({sim_temp}°C). User Query: {user_query}",
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7,
                    ),
                )
                st.success("**Maple (AI Assistant):**")
                st.write(response.text)
            except Exception as e:
                st.error(f"Gagal memanggil Gemini API: {e}")