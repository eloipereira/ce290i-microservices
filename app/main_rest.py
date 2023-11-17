import time

import pandas as pd
import requests
import streamlit as st
from fastapi.encoders import jsonable_encoder

from app.config import Config
from app.widgets import gps_state_plots
from gps_replay.models import GPS


def fetch_gps(session, url) -> GPS:
    try:
        result = session.get(url)
        return GPS(**result.json())
    except Exception:
        return {}


cfg = Config()

session = requests.Session()

st.markdown("# GPS REST Replayer")

request_period_sec = st.number_input(
    "Data request period / seconds", min_value=1, max_value=60, value=5
)

placeholder = st.empty()

if "gps_samples" not in st.session_state:
    st.session_state["gps_samples"] = []


while True:
    with placeholder.container():
        gps = fetch_gps(
            session=session, url=f"http://{cfg.api_host}:{cfg.api_port}/gps_state"
        )
        st.session_state.gps_samples.append(gps)
        df = pd.DataFrame(jsonable_encoder(st.session_state.gps_samples))
        gps_state_plots(df)
        time.sleep(request_period_sec)
