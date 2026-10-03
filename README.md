# 🍁 Village of Oakhaven — 4-Season Dynamic Municipal Portal

An AI-powered, season-aware public service portal designed for small-town Canadian municipal governance. Built using **Python**, **Streamlit**, and **Google Gemini API** (*Canadian English Persona*).

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4.svg)
![Governance](https://img.shields.io/badge/GovTech-Municipal-green.svg)

---

## 🌟 Key Features

- **🎨 Dynamic Seasonal UI:** Automatically switches theme colors, ambient styling, and priority public services based on 4-season weather contexts (Winter, Spring, Summer, Autumn).
- **💬 "Maple" AI Municipal Assistant:** Powered by Gemini 3.6 Flash API with hard-prompted *Canadian English* persona and local municipal knowledge (311 ticketing, bylaws, safety protocols).
- **🚨 Priority Seasonal Services:**
  - **Winter:** Live Snowplow Tracker, Driveway Windrow Logging, Warming Centres.
  - **Spring:** Pothole 311 Reporting, Flood Creek Level Monitor, Green Bin Schedule.
  - **Summer:** Park & Rec Booking, Open Burn Permits, Pool Schedule.
  - **Autumn:** Curbside Leaf Collection Map, Senior Winterization, Town Hall Budgeting.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** Streamlit
- **AI Engine:** Google GenAI SDK (`gemini-2.5-flash`) via Google AI Studio
- **Styling:** Dynamic CSS Injection based on environmental temperature parameters
- **Environment Management:** Streamlit Secrets & `secrets.toml`

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/kangdims/portal-4-season.git](https://github.com/kangdims/portal-4-season.git)
   cd portal-4-season
