import plotly.graph_objects as go
import pandas as pd

def ranking_vis(tab_rank: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    pull_list = [0] * len(tab_rank)
    pull_list[tab_rank["Rank"].idxmax()] = 0.2 

    fig.add_trace(
        go.Pie(
        labels= tab_rank["Symbol"],
        values = tab_rank["Rank"],
        pull= pull_list,
        textinfo="label+percent"
        )
    )
    fig.update_traces(
        hoverinfo = "label+percent",
        textfont = dict(size=15),
        textposition = "inside",
        marker=dict(colors=colors, line=dict(color='#000000', width=2))
    )
    fig.update_layout(
        title = "Ranking de Instrumentos"
    )
    return fig

def drawdwn_vis(mad_hist: pd.DataFrame, mad_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
        x=mad_hist.index,
        y=mad_hist['profit_acm_d'],
        mode='lines+markers',
        line=dict(color='black', width=4),
        name='Capital Acumulado Diario'        
        )
    )
    fig.add_trace(
        go.Scatter(
        x = [mad_df.loc[2,'valor'],mad_df.loc[3,'valor']],
        y = [mad_hist.loc[mad_df.loc[2,'valor'],'profit_acm_d'],
             mad_hist.loc[mad_df.loc[3,'valor'],'profit_acm_d']],
        line=dict(color='red', width=2, dash='dot'),
        name = 'Capital Perdido en Drawdown' 
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[mad_df.loc[5,'valor'], mad_df.loc[6,'valor']],
            y=[mad_hist.loc[mad_df.loc[5,'valor'],'profit_acm_d'], 
            mad_hist.loc[mad_df.loc[6,'valor'],'profit_acm_d']],
            mode='lines',
            line=dict(color='green', width=2, dash='dot'),
            name='Capital Recuperado en Drawup'
        )
    )

    fig.update_layout(
        title='Evolución del Capital Acumulado ($USD)',
        xaxis_title='timestamp',
        yaxis_title='Valor en $USD'
    )

    return fig
def de_vis(de_df: pd.DataFrame,contador_global: int) -> go.Figure:
    fig = go.Figure()    
    fig.add_trace(go.Bar(
        x=['Status Quo', 'Aversión Perdida', 'Sensibilidad Decreciente'],
        y=[de_df['status_quo'][0],de_df['aversion_perdida'][0],contador_global]
    ))
    return fig


