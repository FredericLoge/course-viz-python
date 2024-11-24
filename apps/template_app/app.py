import pandas as pd
import faicons as fa
import plotly.express as px
from shinywidgets import output_widget, render_plotly
from shiny import App, reactive, render, ui

# bill_rng = (min(tips.total_bill), max(tips.total_bill))

df = pd.read_csv('../../data/star_wars_characters.csv')

ICONS = {
    "user": fa.icon_svg("user", "regular"),
    "wallet": fa.icon_svg("wallet"),
    "currency-dollar": fa.icon_svg("dollar-sign"),
    "ellipsis": fa.icon_svg("ellipsis"),
}

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
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_slider('slider_birth_year', 'Minimum Birth Year', min=-1000, max=+1000, value=0, post='A.Y.'),
        # ui.input_checkbox_group(),
        # ui.input_action_button(),
        open="desktop",
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("General information"), 
            ui.output_data_frame("table"), 
            full_screen=True
        )
    ),
    ui.include_css("styles.css"),
    title="Bare app",
    fillable=True,
)

    
def server(input, output, session):
    # server part
    @render.data_frame
    def table():
      return render.DataGrid(df)

app = App(app_ui, server)
