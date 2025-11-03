import pandas as pd
import streamlit as st


def gps_state_plots(df: pd.DataFrame):
    if "distance_meters" in df.columns:
        df["cumulative_distance_meters"] = df["distance_meters"].cumsum()
    st.write("Data")
    st.dataframe(
        df.reindex(index=df.index[::-1]),
        hide_index=True,
        use_container_width=True,
        height=10,
    )

    st.write("Location")
    st.map(
        df,
        latitude="latitude",
        longitude="longitude",
        use_container_width=True,
        zoom=13,
    )

    st.write("Distance")
    st.line_chart(
        df,
        x="timestamp",
        y="cumulative_distance_meters",
        use_container_width=True,
    )

    st.write("Speed")
    st.line_chart(
        df,
        x="timestamp",
        y="speed_meters_per_second",
        use_container_width=True,
    )

    st.write("Elevation")
    st.line_chart(
        df,
        x="timestamp",
        y="elevation",
        use_container_width=True,
    )
