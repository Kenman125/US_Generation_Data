import numpy as np
import altair as alt
from altair import datum
import streamlit as st
import pandas as pd

generation_df = pd.read_csv('annual_generation_state.csv')

st.title('US Energy Generation')

line = alt.Chart(generation_df).mark_line().encode(
    x='YEAR',
    y='GENERATION (Megawatthours)'
).transform_filter(
    (alt.datum.STATE == "AK") & (alt.datum['ENERGY SOURCE'] == "Total")
)
st.altair_chart(line, use_container_width=True)

st.dataframe(generation_df)

st.sidebar.radio('Choose:',["Solar","Wind","Total"])


