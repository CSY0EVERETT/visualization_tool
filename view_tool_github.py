import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd


def convert_null_to_label(values, label='无数据'):
    return [{'label': label if pd.isna(value) else str(value), 'value': 'null' if pd.isna(value) else str(value)} for value in values]
def get_color(severity):
    if pd.isna(severity):
        return 'black'
    if severity < 0.2:
        return 'green'
    elif severity < 0.6 and severity >= 0.2:
        return 'blue'
    elif severity < 0.85 and severity >= 0.6:
        return 'yellow'
    else:
        return 'red'
# 加载数据
data = pd.read_csv( encoding='gbk',
                   dtype={'station_code': str, 'sunrise_time': str, 'sunset_time': str, 'daily_avg_power_deviation_relative_rate': float})

data['daily_output_loss'] = data['daily_output_loss'].replace('#NAME?', 0).astype(float)


# print(f'{station_code}, {regions}, {cold_wave_cycles}')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("交互式散点图"),
    html.Div([
        html.Label("选择气象量"),
        dcc.RadioItems(
            id='weather_source',
            options=[
                {'label': 'EC', 'value': 'ec'},
                {'label': 'ERA5', 'value': 'era5'}
            ],
            value='era5'
        )
    ], style={'margin-right': '20px'}),
    html.Div([
        html.Label("选择横坐标类别"),
        dcc.RadioItems(
            id='xlabel_type',
            options=[
                {'label': '降雪量', 'value': 'sf'},
                {'label': '雪深', 'value': 'sd'}
            ],
            value='sf'
        )
    ], style={'margin-right': '20px', 'margin-top': '20px'}),
    html.Div([
        html.Label("选择差值类别"),
        dcc.RadioItems(
            id='deviation_type',
            options=[
                {'label': '实测功率与预测功率', 'value': 'rt_and_yb'},
                {'label': '实测功率与辐照度', 'value': 'rt_and_fzd'}
            ],
            value='sf'
        )
    ], style={'margin-right': '20px', 'margin-top': '20px'}),
    html.Div([
        html.Div([
            html.Label(f"降雪权重 day{i + 1}"),
            dcc.Input(id=f'precip_weight_{i + 1}', type='number', value=1)
        ]) for i in range(3)
    ], style={'display': 'inline-block', 'margin-right': '20px', 'margin-top': '20px'}),
    html.Div([
        html.Label("选择区域"),
        dcc.Dropdown(id='region_dropdown', options=regions_options, multi=True)
    ], style={'width': '30%', 'display': 'inline-block', 'margin-right': '20px'}),
    html.Div([
        html.Label("选择寒潮轮次"),
        dcc.Dropdown(id='cold_wave_dropdown', options=cold_wave_cycles_options, multi=True)
    ], style={'width': '30%', 'display': 'inline-block', 'margin-right': '20px'}),
    html.Div([
        html.Label("选择场站"),
        dcc.Dropdown(id='station_dropdown', options=stations_options, multi=True)
    ], style={'width': '30%', 'display': 'inline-block', 'margin-right': '20px'}),
    html.Button('查询', id='submit_button', style={'font-size': '20px', 'padding': '10px 20px'}),
    dcc.Graph(id='scatter_plot'),
    html.Button('下载图表', id='download_button', style={'font-size': '20px', 'padding': '10px 20px'}),
    dcc.Download(id='download')
])

@app.callback(
    [Output('region_dropdown', 'options'),
     Output('cold_wave_dropdown', 'options'),
     Output('station_dropdown', 'options')],
    [Input('region_dropdown', 'value'),
     Input('cold_wave_dropdown', 'value'),
     Input('station_dropdown', 'value')]
)
def update_dropdowns(selected_regions, selected_cold_waves, selected_stations):
    filtered_df = gf_data

    # 根据选定区域过滤数据
    if selected_regions:


    # 根据选定寒潮轮次过滤数据
    if selected_cold_waves:

    # 根据选定场站过滤数据
    if selected_stations:


    # 获取更新后的选项


    return regions_options, cold_wave_cycles_options, stations_options

@app.callback(
    Output('scatter_plot', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('weather_source', 'value')],

    [State('region_dropdown', 'value'),
     State('cold_wave_dropdown', 'value'),
     State('station_dropdown', 'value'),
     State('xlabel_type', 'value')],
    [State(f'precip_weight_{i+1}', 'value') for i in range(3)]
)
def update_scatter_plot(n_clicks, weather_source, regions, cold_waves, stations, xlabel, *weight):
    precip_weights = weight
    selected_regions = regions
    selected_cold_waves = cold_waves
    selected_stations = stations


    filtered_df = gf_data
    # 根据选定区域过滤数据
    if selected_regions:

    # 根据选定寒潮轮次过滤数据
    if selected_cold_waves:

    # 根据选定场站过滤数据
    if selected_stations:

    # 如果没有数据，返回一个空的散点图
    if filtered_df.empty:
        return px.scatter()

    # 根据气象量和能源类型选择合适的列
    if weather_source == 'era5':
        if xlabel == 'sf':

        elif xlabel == 'sd':

    elif weather_source == 'ec':
        if xlabel == 'sf':

        elif xlabel == 'sd':


    # 填充NaN值为0
    filtered_df = filtered_df.fillna(0)
    filtered_df['加权累积降雪量'] = (

    )
    if xlabel == 'sf':
        X = '加权累积降雪量'
    elif xlabel == 'sd':
        X = '加权累积降雪量'
    filtered_df['颜色'] = filtered_df['daily_output_loss'].apply(get_color)

    fig = px.scatter(
        filtered_df,
        x=X,
        y=temp_col,
        color='颜色',
        color_discrete_map={'green': 'green', 'blue': 'blue', 'yellow': 'yellow', 'red': 'red'},
        hover_data=['cluster_region', 'station_code', 'cold_wave_period', 'date', 'daily_output_loss'],
        size_max=10,
        opacity=0.8,
        width=1800,
        height=1000
    )

    fig.update_traces(
        marker=dict(line=dict(width=0.5, color='DarkSlateGrey')),
        selector=dict(mode='markers'),
        marker_size=10
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8035)
