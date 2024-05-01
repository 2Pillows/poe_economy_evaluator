import plotly.graph_objects as go
import plotly.graph_objects as px


def create_graph(gems_info, GEM_TYPES_LIST):

    categories = list(gems_info.keys())
    average_values = [gems_info[category]["Total_Expected_Profit"]
                      for category in categories]

    min_values = []
    max_values = []

    for sub_dict in gems_info.values():
        profit_keys = {key: value for key,
                       value in sub_dict.items() if "Profit_" in key}

        min_profit_value = min(profit_keys.values())

        max_profit_value = max(profit_keys.values())

        min_values.append(min_profit_value)
        max_values.append(max_profit_value)

    # Create a list of box traces for each category
    box_traces = []

    for i in range(len(categories)):
        box_trace = go.Box(
            y=[min_values[i], average_values[i], max_values[i]],
            name=categories[i],
            boxpoints='outliers',  # Show individual data points as outliers
            jitter=0.3,           # Add jitter to the points for better visibility
            pointpos=-1.8         # Adjust the position of the data points relative to the boxes
        )
        box_traces.append(box_trace)

    # Create the layout for the plot
    layout = go.Layout(
        title='Box Plot',
        xaxis=dict(title='Categories'),
        yaxis=dict(title='Values'),
    )

    # Create the figure and plot
    fig = go.Figure(data=box_traces, layout=layout)

    fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='Black')
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='Black')

    fig.show()
