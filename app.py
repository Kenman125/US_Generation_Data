import altair as alt
import streamlit as st
import pandas as pd

df = pd.read_csv('annual_generation_state.csv')

st.title('US Energy Generation')

df['STATE'] = df['STATE'].astype(str)
df['GENERATION (Megawatthours)'] = df['GENERATION (Megawatthours)'].astype(str)
df['ENERGY SOURCE'] = df['ENERGY SOURCE'].astype(str)

df['GENERATION (Megawatthours)'] = pd.to_numeric(df['GENERATION (Megawatthours)'].str.replace(',', ''), errors='coerce')

df['GENERATION (Megawatthours)'] = df['GENERATION (Megawatthours)'].astype(int)


def generation_over_time():
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

        # Check if the filtered DataFrame is not empty
        if not filtered_df.empty:
            # Compute the total production for the selected state using the maximum value
            total_production = filtered_df["GENERATION (Megawatthours)"].max()

            # Create Altair chart
            line_chart = alt.Chart(filtered_df).mark_line().encode(
                x='YEAR:O',
                y=alt.Y('GENERATION (Megawatthours):Q', title='Generation (MWh)', axis=alt.Axis(format=',d'), scale=alt.Scale(domain=[0, total_production])),
                tooltip=['YEAR:O', 'GENERATION (Megawatthours):Q']
            ).properties(
                width=600,
                height=400,
                title=f'Generation Over Time - {selected_state}'
            )

            # Display the Altair chart
            st.altair_chart(line_chart, use_container_width=True)
        else:
            st.info(f"No data available for {selected_state} and {selected_source}.")

    else:
        st.info("Please select a state.")

def energy_mix_over_time():
    # Sidebar with unique states select box
    sorted_states = ['Select'] + sorted(df["STATE"].unique())
    selected_state = st.sidebar.selectbox("Choose a State", sorted_states)

    # Filter the DataFrame based on the selected state
    if selected_state != 'Select':
        # Exclude "Total" energy source
        energy_mix_df = df[(df["STATE"] == selected_state) & (df["ENERGY SOURCE"] != "Total")]

        # Apply the constant filter for "TYPE OF PRODUCER"
        energy_mix_df = energy_mix_df[energy_mix_df["TYPE OF PRODUCER"] == "Total Electric Power Industry"]

        # Create Altair chart for the horizontal stacked bar chart
        bar_chart = alt.Chart(energy_mix_df).mark_bar().encode(
            x=alt.X('YEAR:O', title='Year'),
            y=alt.Y('GENERATION (Megawatthours):Q', stack='normalize', title='Generation (MWh)'),
            color='ENERGY SOURCE:N',
            tooltip=['ENERGY SOURCE:N', 'GENERATION (Megawatthours):Q']
        ).properties(
            width=600,
            height=400,
            title=f'Energy Mix Over Time - {selected_state}'
        )

        # Display the Altair chart
        st.altair_chart(bar_chart, use_container_width=True)
    else:
        st.info("Please select a state.")

def main():
    # Tabs
    tabs = st.radio("Select Tab", ["Generation Over Time", "Energy Mix Over Time"])

    # Display content based on the selected tab
    if tabs == "Generation Over Time":
        generation_over_time()
    elif tabs == "Energy Mix Over Time":
        energy_mix_over_time()

if __name__ == "__main__":
    main()