import pandas as pd
from pymongo import MongoClient
import streamlit as st
import plotly.express as px

# 1. Usanidi wa Ukurasa wa Streamlit
st.set_page_config(
    page_title="Duka Analytics Dashboard", page_icon="📊", layout="wide"
)

st.title("📊 Duka Analytics Dashboard - Tableau Style")
st.markdown("Dashibodi ya uchambuzi wa mauzo na bidhaa kutoka MongoDB Atlas.")


# 2. Kuunganisha na MongoDB Atlas kwa kutumia st.secrets
@st.cache_resource
def init_connection():
  # Inasoma connection string kutoka kwenye Streamlit secrets au local .streamlit/secrets.toml
  uri = st.secrets["mongo"]["uri"]
  client = MongoClient(uri)
  return client


try:
  client = init_connection()
  # Chagua database na makusanyo (collections) yako
  db = client["duka_db"]

  # Mfano wa kuchota data kutoka makusanyo ya mauzo (mauzo)
  # Unaweza kurekebisha majina ya makusanyo kulingana na ulivyoweka kwenye MongoDB Compass
  if "mauzo" in db.list_collection_names():
    mauzo_data = list(db.mauzo.find())
    df_mauzo = pd.DataFrame(mauzo_data)

    # Kuondoa _id ya MongoDB isilete shida kwenye Pandas
    if "_id" in df_mauzo.columns:
      df_mauzo = df_mauzo.drop(columns=["_id"])
  else:
    # Data ya mfano kama mkusanyo haujapatikana bado
    df_mauzo = pd.DataFrame()

except Exception:
  st.error("Imeshindwa kuunganisha na MongoDB Atlas. Hakiki Streamlit Secrets na ruhusa za mtandao za Atlas.")
  df_mauzo = pd.DataFrame()

# 3. Muundo wa Dashibodi (Dashboard Layout)
if not df_mauzo.empty:
  st.sidebar.header("Chuja Taarifa (Filters)")

  # Onyesha jedwali fupi la data
  st.subheader("📋 Taarifa za Hivi Punde za Mauzo")
  st.dataframe(df_mauzo, width="stretch")

  # Mfano wa michoro ya Plotly ikitumia 'width="stretch"' badala ya 'use_container_width'
  col1, col2 = st.columns(2)

  with col1:
    st.subheader("📈 Mauzo Kulingana na Bidhaa")
    if (
        "bidhaa" in df_mauzo.columns
        and "jumla" in df_mauzo.columns
        or "bei" in df_mauzo.columns
    ):
      # Hapa unaweza kubadilisha nguzo kulingana na data zako halisi za wateja/mauzo
      fig_bar = px.bar(
          df_mauzo,
          x=df_mauzo.columns[0],
          y=df_mauzo.columns[1] if len(df_mauzo.columns) > 1 else None,
          title="Uchambuzi wa Bar Chart",
      )
      st.plotly_chart(fig_bar, width="stretch")
    else:
      st.info("Tafadhali weka nguzo za bidhaa na bei kwenye MongoDB.")

  with col2:
    st.subheader("🔄 Muhtasari wa Uwiano")
    fig_donut = px.pie(
        df_mauzo,
        names=df_mauzo.columns[0] if not df_mauzo.empty else [],
        hole=0.4,
        title="Uwiano wa Takwimu",
    )
    st.plotly_chart(fig_donut, width="stretch")

  # Mchoro wa mstari (Line chart) chini
  st.subheader("📉 Mwenendo wa Miamala")
  fig_line = px.line(df_mauzo, title="Mwenendo kwa Ujumla")
  st.plotly_chart(fig_line, width="stretch")

else:
  st.warning(
      "Hakuna data iliyopatikana kwenye mkusanyo wa 'mauzo' au bado"
      " inaunganishwa."
  )
  st.info(
      "Hakikisha una data ndani ya MongoDB Atlas na jina la database yako"
      " limekaa sawa."
  )


