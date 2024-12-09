# pip install shinywidgets
from pyvis.network import Network

import os
import pandas as pd
# import faicons as fa
import plotly.express as px
from shinywidgets import output_widget, render_plotly
from shiny import App, render, ui  # reactive
from constants import characters, characters_group, characters_edges, filming_locations
# from pathlib import Path
from plotnine import *

DIR = os.path.dirname(os.path.abspath(__file__))
WWW = os.path.join(DIR, "www")
PYVIS_OUTPUT_ID = "pyvis"

path_to_css = 'styles.css'
path_to_data = 'star_wars_characters.csv'
# root_path = "/Users/frederic-loge/Documents/perso/GitHubPerso/course-viz-python/"

# ICONS = {
#    "user": fa.icon_svg("user", "regular"),
#    "wallet": fa.icon_svg("wallet"),
#    "currency-dollar": fa.icon_svg("dollar-sign"),
#    "ellipsis": fa.icon_svg("ellipsis"),
#}

# Input types:
# ui.input_slider()
# ui.input_checkbox_group()
# ui.input_action_button()

# Decorators in server - element in UI - description
# @reactive.calc - None - define a function which outputs a reactive value
# @render_text - ui.output_text - text output
# @render_plotly - output_widget (from shiny widgets) - plot output
# @render.data_frame - ui.output_data_frame - table output
# @render.ui - UI output - any output
# @reactive.effect - None - add reactivity based on input changes
# @reactive.event(input.<>) - None - add trigger event -> e.g. submit button

# Add page title and sidebar
app_ui = ui.page_navbar(  
    ui.nav_spacer(), 
    ui.nav_panel(
        "View Data",
        ui.layout_columns(
            ui.output_image("image"),
            ui.navset_card_tab(  
                ui.nav_panel("Characters", ui.output_data_frame("table_characteristics")),
                ui.nav_panel("Relationships", ui.output_data_frame("table_relationships")),
                ui.nav_panel("Locations", ui.output_data_frame("table_locations"))
            ),
            col_widths={"sm": (3, 9)}
        )
    ),
    ui.nav_panel(
        "EDA",
        ui.layout_columns(
            ui.card(
                ui.card_header("Plot"),
                output_widget("plot"),
                full_screen=False
            ),
            ui.card(
                ui.card_header("Network"),
                ui.output_ui(PYVIS_OUTPUT_ID),
                full_screen=False
            ), 
            ui.card(
                ui.input_select('var1', label='Var X', choices=characters.columns.tolist()),
                ui.input_select('var2', label='Var Y', choices=characters.columns.tolist()),
                ui.input_slider('text_angle', label='Angle of x-axis labels', min=0, max=90, value=45)
            ),
            ui.card(
                ui.output_plot('plot_var12')
            ),
            col_widths={"sm": (6, 6, 3, 9)}
        )
    ),
    ui.nav_panel(
        "Reactive demo"
    ),
    #ui.include_css(path_to_css),
    title="Basic app",
    id="bidule",
    # fillable=True,
)


def server(input, output, session):
    # server part
    @render.data_frame
    def table_characteristics():
        return render.DataGrid(characters)

    @render.data_frame
    def table_relationships():
        return render.DataGrid(characters_edges)

    @render.data_frame
    def table_locations():
        return render.DataGrid(filming_locations)

    @render.image
    def image():
        return {"src": "www/rotj-in-theaters-40th-celebration-onesheet_1e34d642.jpeg", "width": '100%'} 

    @render.plot
    def plot_var12():
        print(input.var1())
        c1 = characters[input.var1()].dtype == 'object'
        c2 = characters[input.var2()].dtype == 'object'
        if c1 & c2:
            return ggplot(characters)+aes(x=input.var1(), y=input.var2())+geom_count()+theme(axis_text_x=element_text(angle=input.text_angle()))
        elif c1 & ~c2:
            return ggplot(characters)+aes(x=input.var1(), y=input.var2())+geom_boxplot()+theme(axis_text_x=element_text(angle=input.text_angle()))
        elif ~c1 & c2:
            return ggplot(characters)+aes(y=input.var1(), x=input.var2())+geom_boxplot()+theme(axis_text_x=element_text(angle=input.text_angle()))
        else:
            return ggplot(characters)+aes(x=input.var1(), y=input.var2())+geom_point()+theme(axis_text_x=element_text(angle=input.text_angle()))

    @render_plotly
    def plot():
        # color = input.scatter_color()
        fig = px.scatter(
            characters,
            x="height",
            y="weight",
            color="gender",
            hover_name="name",
            hover_data=["height", "weight"],
            trendline="lowess",
            labels={
                "gender": "Gender",
                "height": "Height (m)",
                "weight": "Weight (kg)"
            },
            title="Scatterplot of weight against height"
        )
        # fig.update_traces(hovertemplate="%{name}%")
        return fig
    
    @output(id=PYVIS_OUTPUT_ID)
    @render.ui
    def _():
        color_mapping = {
            'taught': "blue", 
            'was in fact': "yellow", 
            'became': "orange", 
            'parent': "red", 
            'killed': "green"
        }

        G = Network(height="750px", width="100%", bgcolor="white", font_color="black")

        G.add_nodes(set(characters_edges.name_1.tolist()+characters_edges.name_2.tolist()))

        for idx, row in characters_edges.iterrows():
            G.add_edge(row['name_1'], row['name_2'], color=color_mapping[row['action']])

        # G.show('e.html', notebook=False)
        G.generate_html(local=False)
        f = os.path.join(WWW, PYVIS_OUTPUT_ID + ".html")
        with open(f, "w") as f:
            f.write(G.html)

        return ui.tags.iframe(
            src=f"{PYVIS_OUTPUT_ID}.html",
            style="height:600px;width:100%;",
            scrolling="no",
            seamless="seamless",
            frameBorder="0",
        )

app = App(app_ui, server, static_assets=WWW)

