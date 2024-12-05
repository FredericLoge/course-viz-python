# Setup

```bash
# assuming you are in a virtual env or temporary env
# see `poetry` for precise library management
pip install pandas plotnine networkx pyvis shiny faicons shinywidgets plotly
```

# Contents

## Graphs

For most graphs, we will be using `plotnine` todya, which is the equivalent of R's `ggplot2` in python. It follows the grammar of graphics. There are many options available in python regarding data visualization libraries, such as `matplotlib`, `altair`, `bokeh`, `seaborn`, `pygal`, ... but imo `plotnine` hits all the marks in terms of:
- pure aesthetics from scratch
- code readability / review 
- adaptability to the requirements

That being said:
- for interactive plots, we will focus on `plotly` (maps included although `folium` is nice as well)
- for network representation, we will look into the `pyvis` library

## WebApp/Dashboard

In python, many options are available: `streamlit`, `Dash`, `Flask`, `Bokeh`, `Panel`, ... and yet we shall be using `shiny` today :party: 