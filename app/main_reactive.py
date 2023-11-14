import json

import pandas as pd
import redis
import streamlit as st
from fastapi.encoders import jsonable_encoder

from gps_replay.config import RedisConfig
from gps_replay.models import GPS


cfg = RedisConfig()

st.markdown("GPS Reactive Replayer")

placeholder = st.empty()


def subscriber(topic: str, redis: redis.Redis):
    pubsub = redis.pubsub()
    pubsub.subscribe(topic)
    gps_samples = []
    while True:
        msg = pubsub.get_message()
        if msg is not None and isinstance(msg, dict):
            gps = msg.get("data")
            if isinstance(gps, str):
                gps_samples.append(GPS(**json.loads(gps)))
                df = pd.DataFrame(jsonable_encoder(gps_samples))
                with placeholder.container():
                    st.dataframe(df)
                    st.map(df, latitude="latitude", longitude="longitude")


db = redis.Redis(host=cfg.redis_host, port=cfg.redis_port, decode_responses=True)
subscriber(topic="gps_state_topic", redis=db)
