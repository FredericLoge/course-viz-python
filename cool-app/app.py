# search for information on a character
import os
import pandas as pd
import numpy as np 
from pyvis.network import Network
from shiny import App, render, ui, reactive
from shiny.types import ImgData
from constants import characters, characters_edges

DIR = os.path.dirname(os.path.abspath(__file__))
WWW = os.path.join(DIR, "www")
PYVIS_OUTPUT_ID = "pyvis"

picture_links = pd.read_csv('assets/links.csv')
LIST_OF_CHARACTERS = picture_links.name.tolist()

app_ui = ui.page_fluid(
    ui.panel_title("Star Wars"),
    ui.layout_columns(
        (
            ui.input_select("selected_character", "Select your character:", choices=LIST_OF_CHARACTERS),
            ui.output_image("picture", click=True)
        ),
        (
            ui.output_text("character_description"),
            ui.output_ui("character_profile"),
            ui.output_ui(PYVIS_OUTPUT_ID),
        ), 
        col_widths=[5, 7]
    )
)


def server(input, output, session):

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

        G = Network(height="400px", width="100%", bgcolor="#FFFFFF", font_color="black")

        set_chars = list(set(characters_edges.name_1.tolist()+characters_edges.name_2.tolist()))
        set_colors = ['black' if s == input.selected_character() else 'blue' for s in set_chars]
        print(set_chars)
        print(set_colors)
        G.add_nodes(set_chars, color=set_colors)

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


    @reactive.effect # @reactive.event(input.picture_click())
    def show_notification():
        if input.picture_click():
            sel = input.selected_character()
            phrase = picture_links.query("name==@sel").phrase.iloc[0]
            phrases = phrase.split('|')
            ui.notification_show(
                np.random.choice(phrases),
                type="warning",
                duration=2,
            )

    @render.image
    def picture():
        sel = input.selected_character()
        url = picture_links.query("name==@sel").url.iloc[0]
        img: ImgData = {"src": os.path.join("assets", url), "width": "300px"}
        return img

    @render.text
    def character_description():
        sel = input.selected_character()
        return characters.query('name == @sel').description.iloc[0]
    
    @render.ui
    def character_profile():
        sel = input.selected_character()
        tmp = characters.query('name == @sel')
        var = ['species', 'gender', 'height', 'weight']
        sca = ['', '', 'm', 'Kg']
        md_text = "" 
        for v, s in zip(var, sca):
            md_text += "**" + v.capitalize() + "**: " + str(tmp[v].iloc[0]) + s + '<br>'
        return ui.markdown(md_text)


app = App(app_ui, server, static_assets=WWW)
