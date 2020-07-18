import dash
import pandas as pd
import pathlib
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from helpers import (make_dash_table, create_plot,
                     extract_text_from_url, gen_sound_from_text)



app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server

DATA_PATH = pathlib.Path(__file__).parent.joinpath("data").resolve()

# read from datasheet
df = pd.read_csv(DATA_PATH.joinpath("small_molecule_drugbank.csv")).drop(
    ["Unnamed: 0"], axis=1
)

DATA_FILE = DATA_PATH.joinpath("test.txt")
AUDIO_FILE = DATA_PATH.joinpath("test.mp3")

# read from datasheet
df = pd.read_csv(DATA_PATH.joinpath("small_molecule_drugbank.csv")).drop(
    ["Unnamed: 0"], axis=1
)



STARTING_DRUG = "Levobupivacaine"
DRUG_DESCRIPTION = df.loc[df["NAME"] == STARTING_DRUG]["DESC"].iloc[0]
DRUG_IMG = df.loc[df["NAME"] == STARTING_DRUG]["IMG_URL"].iloc[0]
FIGURE = create_plot(
    x=df["PKA"],
    y=df["LOGP"],
    z=df["SOL"],
    size=df["MW"],
    color=df["MW"],
    name=df["NAME"],
)

app.layout = html.Div(
    [
        # html.Div(
        #    [html.Img(src=app.get_asset_url("dash-logo.png"))], className="app__banner"
        # ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Text Toolkit",
                                    className="uppercase title",
                                ),
                                html.Span(
                                    "Enter URL ", className="uppercase bold"),
                                html.Span(
                                    "to extract text content or, "
                                ),
                                html.Br(),
                                html.Span(
                                    "Copy text ", className="uppercase bold"),
                                html.Span(
                                    "directly into the text area box."
                                ),
                            ]
                        )
                    ],
                    className="app__header",
                ),
                html.Div([
                    dcc.Textarea(
                        id='textarea-url',
                        value='https://en.wikipedia.org/wiki/Kubernetes',
                        style={'width': '50%', 'height': 100},
                    ),
                    html.Button('Extract Text', id='textarea-url-button', n_clicks=0),
                    #html.Div(id='textarea-url-output', style={'whiteSpace': 'pre-line'})
                ],
                    className="app__url_enter_box",
                ),

                html.Br(),

                html.Div([
                    html.Span("Text to be analyzed: "),
                    ],
                    className="app__subheader",
                ),

                html.Br(),
                html.Div(
                    [
                        html.Div(id='text-output'),
                    ],
                    className="app__text_output_box",
                ),

                html.Br(),
                html.Div([
                    html.Span("Click to listen to the text: "),
                    ],
                    className="app__subheader",
                ),

                #html.Button('Click to conver to sound', id='convert-sound-button', n_clicks=0),

                html.Br(),
                html.Div(
                    [
                        html.Audio(id="player", src=AUDIO_FILE,
                        controls=True, style={"width": "50%"}),
                    ],
                    className="app__audio_output",
                ),

                # html.Div(
                #    [
                #        dcc.Dropdown(
                #            id="chem_dropdown",
                #            multi=True,
                #            value=[STARTING_DRUG],
                #            options=[{"label": i, "value": i}
                #                     for i in df["NAME"]],
                #        )
                #    ],
                #    className="app__dropdown",
                # ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.RadioItems(
                                    id="charts_radio",
                                    options=[
                                        {"label": "3D Scatter",
                                            "value": "scatter3d"},
                                        {"label": "2D Scatter",
                                            "value": "scatter"},
                                        {
                                            "label": "2D Histogram",
                                            "value": "histogram2d",
                                        },
                                    ],
                                    labelClassName="radio__labels",
                                    inputClassName="radio__input",
                                    value="scatter3d",
                                    className="radio__group",
                                ),
                                dcc.Graph(
                                    id="clickable-graph",
                                    hoverData={"points": [{"pointNumber": 0}]},
                                    figure=FIGURE,
                                ),
                            ],
                            className="two-thirds column",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Img(
                                            id="chem_img",
                                            src=DRUG_IMG,
                                            className="chem__img",
                                        )
                                    ],
                                    className="chem__img__container",
                                ),
                                html.Div(
                                    [
                                        html.A(
                                            STARTING_DRUG,
                                            id="chem_name",
                                            href="https://www.drugbank.ca/drugs/DB01002",
                                            target="_blank",
                                        ),
                                        html.P(DRUG_DESCRIPTION,
                                               id="chem_desc"),
                                    ],
                                    className="chem__desc__container",
                                ),
                            ],
                            className="one-third column",
                        ),
                    ],
                    className="container card app__content bg-white",
                ),
                # html.Div(
                #    [
                #        html.Table(
                #            make_dash_table([STARTING_DRUG], df),
                #            id="table-element",
                #            className="table__container",
                #        )
                #    ],
                #    className="container bg-white p-0",
                # ),
            ],
            className="app__container",
        ),
    ]
)


def df_row_from_hover(hoverData):
    """ Returns row for hover point as a Pandas Series. """

    try:
        point_number = hoverData["points"][0]["pointNumber"]
        molecule_name = str(FIGURE["data"][0]["text"][point_number]).strip()
        return df.loc[df["NAME"] == molecule_name]
    except KeyError as error:
        print(error)
        return pd.Series()


@app.callback(
    Output("text-output", "children"),
    [Input("textarea-url-button", "n_clicks")],
    [State('textarea-url', 'value')]
)
def process_input_box(n_clicks, url_values):
    """
    :params textarea-url: url link
    """
    if n_clicks > 0:
        text = extract_text_from_url(url_values)

        file = open(DATA_FILE, "w")
        file.write(text)
        #t2s = gen_sound_from_text(text)
        #t2s.text2sound()
        #t2s.save_sound_2_mp3()

        return text
    else:
        return "Imagination is more important than knowledge."


@app.callback(
    Output("player", "children"),
    [Input("convert-sound-button", "n_clicks")]
)
def convert_text_to_sound(n_clicks):
    """
    :params textarea-url: url link
    """
    if n_clicks > 0:
        with open(DATA_FILE, 'r') as file:
            text = file.read().replace('\n', ' ')

        t2s = gen_sound_from_text(text, outputfile=AUDIO_FILE)
        t2s.text2sound()
        t2s.save_sound_2_mp3()


'''
@app.callback(Output("table-element", "children"),
[Input("chem_dropdown", "value")])
def update_table(chem_dropdown_value):
    """
    Update the table rows.

    :params chem_dropdown_values: selected dropdown values
    """

    return make_dash_table(chem_dropdown_value, df)
'''


@app.callback(
    [
        Output("chem_name", "children"),
        Output("chem_name", "href"),
        Output("chem_img", "src"),
        Output("chem_desc", "children"),
    ],
    [Input("clickable-graph", "hoverData")],
)
def chem_info_on_hover(hoverData):
    """
    Display chemical information on graph hover.
    Update the image, link, description.

    :params hoverData: data on graph hover
    """

    if hoverData is None:
        raise PreventUpdate

    try:
        row = df_row_from_hover(hoverData)
        if row.empty:
            raise Exception
        return (
            row["NAME"].iloc[0],
            row["PAGE"].iloc[0],
            row["IMG_URL"].iloc[0],
            row["DESC"].iloc[0],
        )

    except Exception as error:
        print(error)
        raise PreventUpdate


if __name__ == "__main__":

    import os
    app.run_server(debug=True, host='0.0.0.0', port=os.getenv('PORT', 8500))
