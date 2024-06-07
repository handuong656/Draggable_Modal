import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server= app.server

app.layout = html.Div([
    html.Button('Open Modal', id='open_modal_button'),
    dbc.Modal([
        dbc.ModalHeader("Draggable Modal"),
        dbc.ModalBody("This is a draggable modal."),
        dbc.ModalFooter(
            dbc.Button("Close", id="close_modal_button", className="ml-auto")
        ),
    ],
    id="modal",
    ),
    dcc.Store(id='modal-position', data={'x': 0, 'y': 0})
])

app.clientside_callback(
    """
    function dragElement(elmnt) {
        var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        if (document.getElementById(elmnt.id + "-header")) {
            // if present, the header is where you move the DIV from:
            document.getElementById(elmnt.id + "-header").onmousedown = dragMouseDown;
        } else {
            // otherwise, move the DIV from anywhere inside the DIV:
            elmnt.onmousedown = dragMouseDown;
        }

        function dragMouseDown(e) {
            e = e || window.event;
            e.preventDefault();
            // get the mouse cursor position at startup:
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            // call a function whenever the cursor moves:
            document.onmousemove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            // calculate the new cursor position:
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            // set the element's new position:
            elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
            elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";

            // Store modal position
            var modalPosition = { 'x': elmnt.offsetLeft, 'y': elmnt.offsetTop };
            const modalPositionJson = JSON.stringify(modalPosition);
            document.getElementById('modal-position').setAttribute('data', modalPositionJson);
        }

        function closeDragElement() {
            // stop moving when mouse button is released:
            document.onmouseup = null;
            document.onmousemove = null;
        }
    }

    var modal = document.getElementById('modal');
    dragElement(modal);
    """,
    Output('modal', 'children'),
    [Input('modal', 'n_clicks')]
)

app.clientside_callback(
    """
    document.getElementById('modal').style.top = modalPosition.y + 'px';
    document.getElementById('modal').style.left = modalPosition.x + 'px';
    """,
    Output('modal', 'style'),
    [Input('modal-position', 'data')]
)

@app.callback(
    Output("modal", "is_open"),
    [Input("open_modal_button", "n_clicks"),
     Input("close_modal_button", "n_clicks")],
    [dash.dependencies.State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(port=8056)
