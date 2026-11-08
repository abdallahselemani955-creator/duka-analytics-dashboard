import pandas as pd
from pymongo import MongoClient
import streamlit as st
import plotly.express as px
import os

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
  uri = None
  try:
    uri = st.secrets["mongo"]["uri"]
  except Exception:
    try:
      uri = st.secrets["MONGODB_URI"]
    except Exception:
      uri = os.environ.get("MONGODB_URI")
  if not uri:
    raise RuntimeError("MISSING_MONGODB_URI")
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

except Exception as e:
  if isinstance(e, RuntimeError) and str(e) == "MISSING_MONGODB_URI":
    st.error("Weka URI kwenye Streamlit Secrets kama [mongo] uri = \"...\" au MONGODB_URI = \"...\".")
  else:
    st.error("Imeshindwa kuunganisha na MongoDB Atlas. Hakiki URI/credentials na ruhusa za mtandao za Atlas.")
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
    bidhaa_col = "bidhaa_iliyouzwa" if "bidhaa_iliyouzwa" in df_mauzo.columns else "bidhaa" if "bidhaa" in df_mauzo.columns else None
    mapato_col = "jumla_bei" if "jumla_bei" in df_mauzo.columns else "jumla" if "jumla" in df_mauzo.columns else "bei" if "bei" in df_mauzo.columns else None
    if bidhaa_col and mapato_col:
      df_bidhaa = df_mauzo.groupby(bidhaa_col, as_index=False)[mapato_col].sum()
      fig_bar = px.bar(
          df_bidhaa,
          x=bidhaa_col,
          y=mapato_col,
          title="Mapato kwa Bidhaa",
      )
      st.plotly_chart(fig_bar, width="stretch")
    else:
      st.info("Tafadhali weka nguzo za bidhaa na mapato kwenye MongoDB.")

  with col2:
    st.subheader("🔄 Muhtasari wa Uwiano")
    bidhaa_col = "bidhaa_iliyouzwa" if "bidhaa_iliyouzwa" in df_mauzo.columns else df_mauzo.columns[0]
    fig_donut = px.pie(
        df_mauzo,
        names=bidhaa_col,
        values="idadi" if "idadi" in df_mauzo.columns else None,
        hole=0.4,
        title="Uwiano wa Takwimu",
    )
    st.plotly_chart(fig_donut, width="stretch")

  # Mchoro wa mstari (Line chart) chini
  st.subheader("📉 Mwenendo wa Miamala")
  tarehe_col = "tarehe_ya_mauzo" if "tarehe_ya_mauzo" in df_mauzo.columns else None
  mapato_col = "jumla_bei" if "jumla_bei" in df_mauzo.columns else "jumla" if "jumla" in df_mauzo.columns else "bei" if "bei" in df_mauzo.columns else None
  if tarehe_col and mapato_col:
    df_trend = df_mauzo.groupby(tarehe_col, as_index=False)[mapato_col].sum()
    fig_line = px.line(df_trend, x=tarehe_col, y=mapato_col, title="Mapato kwa Tarehe")
  else:
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


