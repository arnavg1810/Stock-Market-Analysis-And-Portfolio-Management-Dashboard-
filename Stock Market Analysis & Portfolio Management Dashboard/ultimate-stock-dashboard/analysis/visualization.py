"""
Charts: price/MA with golden cross, correlation/covariance heatmaps,
drawdown curve, risk–return scatter, efficient frontier, rolling Sharpe.
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def _golden_death_cross_dates(price_series, ma_short, ma_long):
    """Find dates where short MA crosses long MA (golden = above, death = below)."""
    cross = (ma_short - ma_long).dropna()
    sign = np.sign(cross)
    # crossover: sign change
    crossover = sign.diff().fillna(0) != 0
    crossover = crossover & (cross != 0)
    cross_dates = cross[crossover].index.tolist()
    golden = []
    death = []
    for d in cross_dates:
        if ma_short.loc[d] > ma_long.loc[d]:
            golden.append(d)
        else:
            death.append(d)
    return golden, death


def price_ma_chart_with_crossovers(prices_series, ma_50, ma_200, ticker_name="Price"):
    """Price + 50/200 MA with markers at golden cross (green) and death cross (red)."""
    golden, death = _golden_death_cross_dates(prices_series, ma_50, ma_200)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prices_series.index, y=prices_series, name=ticker_name, line=dict(width=2)))
    fig.add_trace(go.Scatter(x=ma_50.index, y=ma_50, name="50-Day MA", line=dict(dash="dash")))
    fig.add_trace(go.Scatter(x=ma_200.index, y=ma_200, name="200-Day MA", line=dict(dash="dot")))
    if golden:
        fig.add_trace(
            go.Scatter(
                x=golden,
                y=[prices_series.loc[d] for d in golden],
                mode="markers",
                marker=dict(symbol="triangle-up", size=14, color="green", line=dict(width=1, color="darkgreen")),
                name="Golden Cross",
            )
        )
    if death:
        fig.add_trace(
            go.Scatter(
                x=death,
                y=[prices_series.loc[d] for d in death],
                mode="markers",
                marker=dict(symbol="triangle-down", size=14, color="red", line=dict(width=1, color="darkred")),
                name="Death Cross",
            )
        )
    fig.update_layout(height=400, xaxis_title="Date", yaxis_title="Price", legend=dict(orientation="h"))
    return fig


def correlation_heatmap(corr_matrix, title="Correlation of Daily Returns"):
    """Plotly heatmap for correlation matrix."""
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale="RdYlGn",
            zmin=-1,
            zmax=1,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            textfont={"size": 12},
        )
    )
    fig.update_layout(height=400, title=title)
    return fig


def covariance_heatmap(cov_matrix, title="Covariance Matrix (Annualized)"):
    """Plotly heatmap for covariance matrix."""
    fig = go.Figure(
        data=go.Heatmap(
            z=cov_matrix.values,
            x=cov_matrix.columns,
            y=cov_matrix.index,
            colorscale="Blues",
            text=np.round(cov_matrix.values, 4),
            texttemplate="%{text}",
            textfont={"size": 10},
        )
    )
    fig.update_layout(height=400, title=title)
    return fig


def drawdown_curve_chart(drawdown_df, title="Drawdown Over Time"):
    """Drawdown curve; optionally highlight crisis (e.g. drawdown < -0.15)."""
    fig = go.Figure()
    for col in drawdown_df.columns:
        fig.add_trace(go.Scatter(x=drawdown_df.index, y=drawdown_df[col], name=col, fill="tozeroy"))
    fig.update_layout(height=350, xaxis_title="Date", yaxis_title="Drawdown", title=title)
    fig.update_yaxes(tickformat=".0%")
    return fig


def risk_return_scatter(annual_returns, annual_vol, tickers, title="Risk vs Return"):
    """Scatter: x=volatility, y=annual return, one point per ticker."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=annual_vol,
            y=annual_returns,
            mode="markers+text",
            text=tickers,
            textposition="top center",
            marker=dict(size=14, color=annual_returns, colorscale="Viridis", showscale=True, colorbar=dict(title="Return")),
            name="Stocks",
        )
    )
    fig.update_layout(
        height=400,
        xaxis_title="Volatility (Annualized)",
        yaxis_title="Annual Return",
        title=title,
        showlegend=False,
    )
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    return fig


def efficient_frontier_chart(portfolios_df, max_sharpe_port, min_vol_port, opt_tickers):
    """Efficient frontier scatter with max Sharpe and min vol highlighted."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=portfolios_df["Volatility"],
            y=portfolios_df["Return"],
            mode="markers",
            marker=dict(
                size=4,
                color=portfolios_df["Sharpe"],
                colorscale="Viridis",
                showscale=True,
                # Place colorbar just to the right of the plot area
                colorbar=dict(title="Sharpe", x=1.05, len=0.7, thickness=15, xpad=10),
            ),
            name="Portfolios",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[max_sharpe_port["Volatility"]],
            y=[max_sharpe_port["Return"]],
            mode="markers",
            marker=dict(size=16, symbol="star", color="red"),
            name="Max Sharpe",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[min_vol_port["Volatility"]],
            y=[min_vol_port["Return"]],
            mode="markers",
            marker=dict(size=16, symbol="star", color="blue"),
            name="Min Volatility",
        )
    )
    fig.update_layout(
        xaxis_title="Volatility",
        yaxis_title="Expected Return",
        height=400,
        showlegend=True,
        # Keep legend fully outside the chart, to the right of the colorbar
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="left",
            x=1.25,
            bgcolor="rgba(22, 27, 34, 0.8)",
            bordercolor="rgba(48, 54, 61, 0.8)",
            borderwidth=1,
        ),
        # Extra right margin to accommodate colorbar + legend
        margin=dict(r=220),
    )
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    return fig


def rolling_sharpe_chart(rolling_sharpe_df, title="Rolling Sharpe Ratio"):
    """Line chart of rolling Sharpe per ticker."""
    fig = go.Figure()
    for col in rolling_sharpe_df.columns:
        fig.add_trace(go.Scatter(x=rolling_sharpe_df.index, y=rolling_sharpe_df[col], name=col, mode="lines"))
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(height=350, xaxis_title="Date", yaxis_title="Sharpe", title=title)
    return fig
