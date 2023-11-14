import time

import pandas as pd
import requests
import streamlit as st
from fastapi.encoders import jsonable_encoder

from app.config import Config
from gps_replay.models import GPS


def fetch_gps(session, url) -> GPS:
    try:
        result = session.get(url)
        return GPS(**result.json())
    except Exception:
        return {}


cfg = Config()

session = requests.Session()

st.markdown("GPS REST Replayer")

placeholder = st.empty()
df = pd.DataFrame()

gps_samples = []
while True:
    with placeholder.container():
        gps = fetch_gps(
            session=session, url=f"http://{cfg.api_host}:{cfg.api_port}/gps_state"
        )
        gps_samples.append(gps)
        df = pd.DataFrame(jsonable_encoder(gps_samples))
        st.dataframe(df)
        st.map(df, latitude="latitude", longitude="longitude")
        time.sleep(5)
