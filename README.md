# US_Generation_Data

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://us-electricity-generation.streamlit.app/)

## Summary

This app shows each state's electric power generation statistics and how they have changed over time.  On the first tab, you can filter for the specific state and energy source you would like to see.  
If there is no generation for a specific energy source (ex: Geothermal generation in Alaska) the app will tell you that there is no data for that specific seleciton. The second tab gives you a more 
wholistic view on a state's complete enegry mix generation data.  The data goes back all the way to 1990 so you can visually see how each state's energy mix has changed.

The main story this app is trying to tell is how badly each state needs to improve their renewable energy mix.  When looking at the 'Generation Over Time' tab you can see that generation is much
higher for the dirty energy source such as coal and natural gas for almost every state.  This becomes even more clear when looking at the 'Energy Mix Over Time' tab where you can see each state is
far below where they need to be in order to meet any type of clean energy target.

## Data Source

The data used is from the US Energy Information Agency and can be found here: https://www.eia.gov/electricity/data/state/

## Future Work

As my streamlit skills progress, I would like to add more data sources such as emissions detail also from the EIA and then I can create more interactive graphs that tell a better story of how each
state is doing in terms of climate change progress.  Maybe one state uses more natural gas than another state, but natural gas produces ~50% less carbon emissions than coal so they still might be
doing better than a state that uses minimal coal.  Finally, adding population data into the graphs and charts would be beneficial too so we could have a better comparison acorss the country.



