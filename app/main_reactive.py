import json

import pandas as pd
import redis
import streamlit as st
from fastapi.encoders import jsonable_encoder

from app.widgets import gps_state_plots
from gps_replay.config import RedisConfig
from gps_replay.models import GPS


cfg = RedisConfig()

st.markdown("# GPS Reactive Replayer")

placeholder = st.empty()

if "gps_samples" not in st.session_state:
    st.session_state["gps_samples"] = []


def subscriber(topic: str, redis: redis.Redis):
    pubsub = redis.pubsub()
    pubsub.subscribe(topic)
    while True:
        msg = pubsub.get_message()
        if msg is not None and isinstance(msg, dict):
            gps = msg.get("data")
            if isinstance(gps, str):
                st.session_state.gps_samples.append(GPS(**json.loads(gps)))
                df = pd.DataFrame(jsonable_encoder(st.session_state.gps_samples))
                with placeholder.container():
                    gps_state_plots(df)


db = redis.Redis(host=cfg.redis_host, port=cfg.redis_port, decode_responses=True)
subscriber(topic="gps_state_topic", redis=db)
