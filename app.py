import numpy as np
import altair as alt
from altair import datum
import streamlit as st
import pandas as pd

df = pd.read_csv('annual_generation_state.csv')

st.title('US Energy Generation')

df['STATE'] = df['STATE'].astype(str)
df['GENERATION (Megawatthours)'] = df['GENERATION (Megawatthours)'].astype(str)
df['ENERGY SOURCE'] = df['ENERGY SOURCE'].astype(str)

df['GENERATION (Megawatthours)'] = pd.to_numeric(df['GENERATION (Megawatthours)'].str.replace(',', ''), errors='coerce')

df['GENERATION (Megawatthours)'] = df['GENERATION (Megawatthours)'].astype(int)

tab1, tab2, tab3 = st.tabs(["Total Generation Over Time", "Renewable", "Dirty"])

def main():

    # Sidebar with unique states select box
    sorted_states = ['Select'] + sorted(df["STATE"].unique())
    selected_state = st.sidebar.selectbox("Choose a State", sorted_states)

    # Sidebar with additional filter for energy source
    selected_source = st.sidebar.selectbox("Choose an Energy Source", ['Select'] + sorted(df["ENERGY SOURCE"].unique()))

    # Filter the DataFrame based on the selected state
    if selected_state != 'Select':
        filtered_df = df[df["STATE"] == selected_state]

        # Apply the constant filter for "TYPE OF PRODUCER"
        filtered_df = filtered_df[filtered_df["TYPE OF PRODUCER"] == "Total Electric Power Industry"]

        if selected_source != 'Select':
            filtered_df = filtered_df[filtered_df["ENERGY SOURCE"] == selected_source]

        # Compute the total production for the selected state
        total_production = filtered_df["GENERATION (Megawatthours)"].max()

        # Create Altair chart
        line_chart = alt.Chart(filtered_df).mark_line().encode(
            x='YEAR:O',
            y=alt.Y('GENERATION (Megawatthours):Q', title='Generation (MWh)', axis=alt.Axis(format=',d'), scale=alt.Scale(domain=[0, total_production])),
            tooltip=['YEAR:O', 'GENERATION (Megawatthours):Q'],
        ).properties(
            width=600,
            height=400,
            title=f'Generation Over Time - {selected_state}'
        )

        # Display the Altair chart
        st.altair_chart(line_chart, use_container_width=True)
    else:
        st.info("Please select a state from the sidebar.")

if __name__ == "__main__":
    main()
