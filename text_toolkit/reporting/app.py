import dash
import pandas as pd
import pathlib
import dash_html_components as html
import dash_core_components as dcc
import dash_dangerously_set_inner_html

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from helpers import (make_dash_table, create_plot,
                     extract_text_from_url, gen_sound_from_text,
                     gen_summary_from_text, gen_summary_from_sentences)


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

server = app.server

DATA_PATH = pathlib.Path(__file__).parent.joinpath("data").resolve()

# read from datasheet
df = pd.read_csv(DATA_PATH.joinpath("small_molecule_drugbank.csv")).drop(
    ["Unnamed: 0"], axis=1
)

DATA_FILE = DATA_PATH.joinpath("test.txt")
AUDIO_FILE = DATA_PATH.joinpath("test.mp3")

#html_audio_code = '<figure> <audio controls src=\"{}\" > Your audio</audio> </figure>'.format(AUDIO_FILE)
#html_audio_code = '<embed src=\"{}\">'.format(AUDIO_FILE)
#print(html_audio_code)

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
        #html.Div(
        #    [html.Img(src=app.get_asset_url("dash-logo.png"))], className="app__banner"
        #),
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

                # Textarea box for entering url for text extraction
                html.Div([
                    dcc.Textarea(
                        id='textarea-url',
                        value='https://en.wikipedia.org/wiki/Kubernetes',
                        style={'width': '50%', 'height': 100},
                    ),

                    #html.Div(id='textarea-url-output', style={'whiteSpace': 'pre-line'})
                ],
                    className="app__url_enter_box",
                ),
                html.Div([
                    html.Button('Extract', id='textarea-url-button',
                            n_clicks=0, style={'width': '12%',
                                                'height': '10%',
                                             }),
                    ],
                        className="app__button",
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
                        html.Div(id='title-output'),
                    ],
                    className="app__subheader",
                ),
                html.Div(
                    [
                        html.Div(id='text-output'),
                    ],
                    className="app__text_output_box",
                ),

                html.Br(),
                html.Div([
                    html.Span("Summary: "),
                    ],
                    className="app__subheader",
                ),
                html.Br(),
                html.Div(
                    [
                        html.Div(id='summary-output'),
                    ],
                    className="app__text_summary_box",
                ),

                html.Br(),
                #html.Div([
                #    dash_dangerously_set_inner_html.DangerouslySetInnerHTML(html_audio_code),
                #    ])


            ],
            className="app__container",

        ),
    ],
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



@app.callback([
    Output("title-output", "children"),
    Output("text-output", "children"),
    Output("summary-output", "children"),
    ],
    [Input("textarea-url-button", "n_clicks")],
    [State('textarea-url', 'value')]
)
def process_input_box(n_clicks, url_values):
    """
    :params textarea-url: url link
    """
    if n_clicks > 0:

        if url_values.startswith('http'):
            # extract text from url
            title, text = extract_text_from_url(url_values)

            file = open(DATA_FILE, "w")
            file.write(text)
            #t2s = gen_sound_from_text(text, outputfile=AUDIO_FILE)
            #t2s.text2sound()
            #t2s.save_sound_2_mp3()

        else:
            text = url_values
            title = "NA"

            file = open(DATA_FILE, "w")
            file.write(text)


        summary = gen_summary_from_text(text)

        #summary_in_html_display = []
        #for ss in list_summary:

        #    line = html.P(ss)
        #    summary_in_html_display.append(line)

        #summary = html.Div([summary_in_html_display])

        return [title, text, summary]
    else:
        return ["title", "Imagination is more important than knowledge.",
                "summary"]





if __name__ == "__main__":
    app.run_server(debug=True)
