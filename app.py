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
        # Exclude specified energy sources
        excluded_sources = ["Total","Other", "Other Biomass", "Other Gases"]
        energy_mix_df = df[(df["STATE"] == selected_state) & (~df["ENERGY SOURCE"].isin(excluded_sources))]

        # Apply the constant filter for "TYPE OF PRODUCER"
        energy_mix_df = energy_mix_df[
            energy_mix_df["TYPE OF PRODUCER"] == "Total Electric Power Industry"
        ]

        # Check if the filtered DataFrame is not empty
        if not energy_mix_df.empty:
            # Create Altair chart for the horizontal stacked bar chart
            bar_chart = alt.Chart(energy_mix_df).mark_bar().encode(
                x=alt.X("YEAR:O", title="Year"),
                y=alt.Y(
                    "GENERATION (Megawatthours):Q",
                    stack="normalize",
                    title="Generation (MWh)",
                ),
                color="ENERGY SOURCE:N",
                tooltip=["ENERGY SOURCE:N", "GENERATION (Megawatthours):Q"],
            ).properties(
                width=600,
                height=400,
                title=f"Energy Mix Over Time - {selected_state}",
            )

            # Display the Altair chart
            st.altair_chart(bar_chart, use_container_width=True)
        else:
            st.info(f"No data available for {selected_state}.")

    else:
        st.info("Please select a state.")

def renewable_vs_dirty_over_time():
    # Sidebar with unique states select box
    sorted_states = ['Select'] + sorted(df["STATE"].unique())
    selected_state = st.sidebar.selectbox("Choose a State", sorted_states)

    # Filter the DataFrame based on the selected state
    if selected_state != 'Select':
        # Group sources into renewable and dirty energy
        renewable_sources = ["Wind", "Solar Thermal and Photovoltaic", "Hydroelectric Conventional","Nuclear", "Geothermal", "Other Biomass","Wood and Wood Derived Fuels"]
        dirty_sources = ["Coal", "Natural Gas", "Petroleum"]

        # Exclude specified energy sources and "Total"
        energy_mix_df = df[(df["STATE"] == selected_state) & (~df["ENERGY SOURCE"].isin(["Total"]))]

        # Apply the constant filter for "TYPE OF PRODUCER"
        energy_mix_df = energy_mix_df[
            energy_mix_df["TYPE OF PRODUCER"] == "Total Electric Power Industry"
        ]

        # Check if the filtered DataFrame is not empty
        if not energy_mix_df.empty:
            # Create a new column to group sources into renewable and dirty
            energy_mix_df['Energy Type'] = energy_mix_df['ENERGY SOURCE'].apply(lambda x: 'Renewable' if x in renewable_sources else 'Dirty')

            # Create Altair chart for the horizontal stacked bar chart
            bar_chart = alt.Chart(energy_mix_df).mark_bar().encode(
                x=alt.X("YEAR:O", title="Year"),
                y=alt.Y(
                    "GENERATION (Megawatthours):Q",
                    stack="normalize",
                    title="Generation (MWh)",
                ),
                color=alt.Color("Energy Type:N", scale=alt.Scale(domain=['Renewable', 'Dirty'], range=['green', 'black'])),
                tooltip=["ENERGY SOURCE:N", "GENERATION (Megawatthours):Q"],
            ).properties(
                width=600,
                height=400,
                title=f"Renewable vs Dirty Over Time - {selected_state}",
            )

            # Display the Altair chart
            st.altair_chart(bar_chart, use_container_width=True)
        else:
            st.info(f"No data available for {selected_state}.")

    else:
        st.info("Please select a state.")

def main():
    # Tabs
    tabs = st.radio("Select Tab", ["Generation Over Time", "Energy Mix Over Time", "Renewable vs Dirty Over Time"])

    # Display content based on the selected tab
    if tabs == "Generation Over Time":
        generation_over_time()
    elif tabs == "Energy Mix Over Time":
        energy_mix_over_time()
    elif tabs == "Renewable vs Dirty Over Time":
        renewable_vs_dirty_over_time()

if __name__ == "__main__":
    main()