#!/usr/bin/env python3
"""
Advanced Visualization System for Socrates AI
Creates interactive charts and visualizations for market analysis
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
import base64
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedVisualizer:
    """Advanced visualization system for Socrates AI"""
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        
        # Set up matplotlib style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Configure plotly default template
        self.plotly_template = "plotly_white"
    
    def create_market_price_chart(self, symbol: str, days: int = 252) -> Dict[str, Any]:
        """Create interactive price chart with technical indicators"""
        try:
            # Get market data
            data = self._get_market_data(symbol, days)
            if data.empty:
                return {'error': f'No data available for {symbol}'}
            
            # Create subplot figure
            fig = make_subplots(
                rows=3, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                subplot_titles=(f'{symbol} Price Chart', 'Volume', 'Technical Indicators'),
                row_heights=[0.6, 0.2, 0.2]
            )
            
            # Price chart with candlesticks
            fig.add_trace(
                go.Candlestick(
                    x=data['date'],
                    open=data['open_price'],
                    high=data['high_price'],
                    low=data['low_price'],
                    close=data['close_price'],
                    name='Price',
                    increasing_line_color='green',
                    decreasing_line_color='red'
                ),
                row=1, col=1
            )
            
            # Moving averages
            if len(data) >= 20:
                data['ma20'] = data['close_price'].rolling(window=20).mean()
                data['ma50'] = data['close_price'].rolling(window=50).mean()
                
                fig.add_trace(
                    go.Scatter(
                        x=data['date'],
                        y=data['ma20'],
                        mode='lines',
                        name='MA20',
                        line=dict(color='blue', width=1)
                    ),
                    row=1, col=1
                )
                
                if len(data) >= 50:
                    fig.add_trace(
                        go.Scatter(
                            x=data['date'],
                            y=data['ma50'],
                            mode='lines',
                            name='MA50',
                            line=dict(color='orange', width=1)
                        ),
                        row=1, col=1
                    )
            
            # Volume chart
            colors = ['green' if close >= open else 'red' 
                     for close, open in zip(data['close_price'], data['open_price'])]
            
            fig.add_trace(
                go.Bar(
                    x=data['date'],
                    y=data['volume'],
                    name='Volume',
                    marker_color=colors,
                    opacity=0.7
                ),
                row=2, col=1
            )
            
            # RSI indicator
            rsi = self._calculate_rsi(data['close_price'])
            fig.add_trace(
                go.Scatter(
                    x=data['date'],
                    y=rsi,
                    mode='lines',
                    name='RSI',
                    line=dict(color='purple')
                ),
                row=3, col=1
            )
            
            # RSI overbought/oversold lines
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
            
            # Update layout
            fig.update_layout(
                title=f'{symbol} Advanced Price Analysis',
                template=self.plotly_template,
                height=800,
                showlegend=True,
                xaxis_rangeslider_visible=False
            )
            
            # Update y-axis labels
            fig.update_yaxes(title_text="Price ($)", row=1, col=1)
            fig.update_yaxes(title_text="Volume", row=2, col=1)
            fig.update_yaxes(title_text="RSI", row=3, col=1, range=[0, 100])
            
            return {
                'chart_html': fig.to_html(include_plotlyjs='cdn'),
                'chart_json': fig.to_json(),
                'data_points': len(data),
                'symbol': symbol,
                'chart_type': 'price_analysis'
            }
            
        except Exception as e:
            logger.error(f"Error creating price chart for {symbol}: {e}")
            return {'error': str(e)}
    
    def create_ecm_cycle_chart(self, symbol: str = None) -> Dict[str, Any]:
        """Create ECM cycle visualization"""
        try:
            # ECM cycle parameters
            base_cycle_days = 3141  # π × 1000
            reference_date = datetime(2007, 2, 27)
            current_date = datetime.now()
            
            # Calculate cycle position
            days_since_reference = (current_date - reference_date).days
            cycle_position = (days_since_reference % base_cycle_days) / base_cycle_days
            
            # Create cycle visualization
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'ECM Cycle Position', 
                    'Historical Turning Points',
                    'Cycle Phases', 
                    'Confidence Level'
                ),
                specs=[[{"type": "polar"}, {"type": "scatter"}],
                       [{"type": "bar"}, {"type": "indicator"}]]
            )
            
            # Polar chart for cycle position
            theta = np.linspace(0, 2*np.pi, 100)
            r = np.ones(100)
            
            fig.add_trace(
                go.Scatterpolar(
                    r=r,
                    theta=theta * 180/np.pi,
                    mode='lines',
                    name='Cycle',
                    line=dict(color='blue', width=2)
                ),
                row=1, col=1
            )
            
            # Current position marker
            current_theta = cycle_position * 360
            fig.add_trace(
                go.Scatterpolar(
                    r=[1],
                    theta=[current_theta],
                    mode='markers',
                    name='Current Position',
                    marker=dict(size=15, color='red')
                ),
                row=1, col=1
            )
            
            # Historical turning points
            turning_points = [
                {'year': 1929, 'event': 'Stock Market Crash'},
                {'year': 1981, 'event': 'Interest Rate Peak'},
                {'year': 2007.15, 'event': 'Financial Crisis'},
                {'year': 2015.75, 'event': 'ECM Turning Point'},
                {'year': 2024.3, 'event': 'Projected Turn'}
            ]
            
            years = [tp['year'] for tp in turning_points]
            events = [tp['event'] for tp in turning_points]
            
            fig.add_trace(
                go.Scatter(
                    x=years,
                    y=list(range(len(years))),
                    mode='markers+text',
                    text=events,
                    textposition="middle right",
                    name='Turning Points',
                    marker=dict(size=10, color='red')
                ),
                row=1, col=2
            )
            
            # Cycle phases
            phases = ['Early Expansion', 'Late Expansion', 'Early Contraction', 'Late Contraction']
            phase_values = [25, 35, 25, 15]  # Example distribution
            
            fig.add_trace(
                go.Bar(
                    x=phases,
                    y=phase_values,
                    name='Phase Distribution',
                    marker_color=['green', 'lightgreen', 'red', 'lightcoral']
                ),
                row=2, col=1
            )
            
            # Confidence gauge
            confidence_level = 0.75  # Example confidence
            
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=confidence_level * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "ECM Confidence %"},
                    delta={'reference': 50},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "gray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ),
                row=2, col=2
            )
            
            # Update layout
            fig.update_layout(
                title='Economic Confidence Model (ECM) Analysis',
                template=self.plotly_template,
                height=800,
                showlegend=True
            )
            
            return {
                'chart_html': fig.to_html(include_plotlyjs='cdn'),
                'chart_json': fig.to_json(),
                'cycle_position': cycle_position,
                'days_into_cycle': days_since_reference % base_cycle_days,
                'chart_type': 'ecm_cycle'
            }
            
        except Exception as e:
            logger.error(f"Error creating ECM cycle chart: {e}")
            return {'error': str(e)}
    
    def create_correlation_heatmap(self, symbols: List[str] = None) -> Dict[str, Any]:
        """Create correlation heatmap for multiple markets"""
        try:
            if not symbols:
                symbols = ['AAPL', 'GOOGL', 'MSFT', 'SPY', 'GLD', 'EURUSD=X']
            
            # Get correlation data
            correlation_matrix = self._calculate_correlation_matrix(symbols)
            
            if correlation_matrix is None:
                return {'error': 'Insufficient data for correlation analysis'}
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns,
                y=correlation_matrix.index,
                colorscale='RdBu',
                zmid=0,
                text=correlation_matrix.round(3).values,
                texttemplate="%{text}",
                textfont={"size": 10},
                hoverongaps=False
            ))
            
            fig.update_layout(
                title='Market Correlation Heatmap',
                template=self.plotly_template,
                height=600,
                width=800
            )
            
            return {
                'chart_html': fig.to_html(include_plotlyjs='cdn'),
                'chart_json': fig.to_json(),
                'correlation_matrix': correlation_matrix.to_dict(),
                'symbols': symbols,
                'chart_type': 'correlation_heatmap'
            }
            
        except Exception as e:
            logger.error(f"Error creating correlation heatmap: {e}")
            return {'error': str(e)}
    
    def create_capital_flow_chart(self, symbols: List[str] = None) -> Dict[str, Any]:
        """Create capital flow visualization"""
        try:
            if not symbols:
                symbols = ['SPY', 'GLD', 'TLT', 'VIX', 'DXY']
            
            # Get recent data for capital flow analysis
            flow_data = self._analyze_capital_flows(symbols)
            
            # Create sankey diagram for capital flows
            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=flow_data['labels'],
                    color=flow_data['colors']
                ),
                link=dict(
                    source=flow_data['source'],
                    target=flow_data['target'],
                    value=flow_data['values']
                )
            )])
            
            fig.update_layout(
                title_text="Capital Flow Analysis",
                font_size=10,
                template=self.plotly_template,
                height=600
            )
            
            return {
                'chart_html': fig.to_html(include_plotlyjs='cdn'),
                'chart_json': fig.to_json(),
                'flow_data': flow_data,
                'chart_type': 'capital_flow'
            }
            
        except Exception as e:
            logger.error(f"Error creating capital flow chart: {e}")
            return {'error': str(e)}
    
    def create_forecast_chart(self, symbol: str, forecast_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create forecast visualization with confidence intervals"""
        try:
            # Get historical data
            historical_data = self._get_market_data(symbol, 60)
            
            if historical_data.empty:
                return {'error': f'No historical data for {symbol}'}
            
            # Create forecast chart
            fig = go.Figure()
            
            # Historical prices
            fig.add_trace(go.Scatter(
                x=historical_data['date'],
                y=historical_data['close_price'],
                mode='lines',
                name='Historical Price',
                line=dict(color='blue')
            ))
            
            # Forecast data (simulated for demonstration)
            forecast_dates = pd.date_range(
                start=historical_data['date'].iloc[-1] + timedelta(days=1),
                periods=30,
                freq='D'
            )
            
            # Generate forecast values (this would come from actual forecast model)
            last_price = historical_data['close_price'].iloc[-1]
            forecast_trend = forecast_data.get('trend', 0.001)  # Daily trend
            forecast_volatility = forecast_data.get('volatility', 0.02)
            
            forecast_prices = []
            upper_bound = []
            lower_bound = []
            
            for i, date in enumerate(forecast_dates):
                base_price = last_price * (1 + forecast_trend) ** i
                volatility_factor = forecast_volatility * np.sqrt(i + 1)
                
                forecast_prices.append(base_price)
                upper_bound.append(base_price * (1 + 1.96 * volatility_factor))
                lower_bound.append(base_price * (1 - 1.96 * volatility_factor))
            
            # Forecast line
            fig.add_trace(go.Scatter(
                x=forecast_dates,
                y=forecast_prices,
                mode='lines',
                name='Forecast',
                line=dict(color='red', dash='dash')
            ))
            
            # Confidence interval
            fig.add_trace(go.Scatter(
                x=forecast_dates,
                y=upper_bound,
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                name='Upper Bound'
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast_dates,
                y=lower_bound,
                mode='lines',
                fill='tonexty',
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(width=0),
                name='95% Confidence Interval'
            ))
            
            fig.update_layout(
                title=f'{symbol} Price Forecast with Confidence Intervals',
                xaxis_title='Date',
                yaxis_title='Price ($)',
                template=self.plotly_template,
                height=600,
                hovermode='x unified'
            )
            
            return {
                'chart_html': fig.to_html(include_plotlyjs='cdn'),
                'chart_json': fig.to_json(),
                'forecast_data': {
                    'dates': forecast_dates.strftime('%Y-%m-%d').tolist(),
                    'prices': forecast_prices,
                    'upper_bound': upper_bound,
                    'lower_bound': lower_bound
                },
                'chart_type': 'forecast'
            }
            
        except Exception as e:
            logger.error(f"Error creating forecast chart for {symbol}: {e}")
            return {'error': str(e)}
    
    def create_dashboard_summary(self, symbols: List[str] = None) -> Dict[str, Any]:
        """Create comprehensive dashboard with multiple visualizations"""
        try:
            if not symbols:
                symbols = ['AAPL', 'SPY', 'GLD', 'EURUSD=X']
            
            # Create subplot dashboard
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Market Performance', 
                    'Volatility Analysis',
                    'Volume Trends', 
                    'Momentum Indicators'
                ),
                specs=[[{"secondary_y": True}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Get data for each symbol
            colors = ['blue', 'red', 'green', 'orange', 'purple']
            
            for i, symbol in enumerate(symbols[:5]):  # Limit to 5 symbols
                data = self._get_market_data(symbol, 30)
                if data.empty:
                    continue
                
                color = colors[i % len(colors)]
                
                # Performance chart (normalized)
                normalized_prices = (data['close_price'] / data['close_price'].iloc[0] - 1) * 100
                fig.add_trace(
                    go.Scatter(
                        x=data['date'],
                        y=normalized_prices,
                        mode='lines',
                        name=f'{symbol} Performance',
                        line=dict(color=color)
                    ),
                    row=1, col=1
                )
                
                # Volatility (rolling standard deviation)
                if len(data) >= 10:
                    volatility = data['close_price'].pct_change().rolling(10).std() * 100
                    fig.add_trace(
                        go.Scatter(
                            x=data['date'],
                            y=volatility,
                            mode='lines',
                            name=f'{symbol} Volatility',
                            line=dict(color=color)
                        ),
                        row=1, col=2
                    )
                
                # Volume trends
                if 'volume' in data.columns:
                    volume_ma = data['volume'].rolling(5).mean()
                    fig.add_trace(
                        go.Scatter(
                            x=data['date'],
                            y=volume_ma,
                            mode='lines',
                            name=f'{symbol} Volume MA',
                            line=dict(color=color)
                        ),
                        row=2, col=1
                    )
                
                # RSI momentum
                rsi = self._calculate_rsi(data['close_price'])
                fig.add_trace(
                    go.Scatter(
                        x=data['date'],
                        y=rsi,
                        mode='lines',
                        name=f'{symbol} RSI',
                        line=dict(color=color)
                    ),
                    row=2, col=2
                )
            
            # Add RSI reference lines
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=2)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=2)
            
            # Update layout
            fig.update_layout(
                title='Socrates AI Market Dashboard',
                template=self.plotly_template,
                height=800,
                showlegend=True
            )
            
            # Update axis labels
            fig.update_yaxes(title_text="Performance (%)", row=1, col=1)
            fig.update_yaxes(title_text="Volatility (%)", row=1, col=2)
            fig.update_yaxes(title_text="Volume", row=2, col=1)
            fig.update_yaxes(title_text="RSI", row=2, col=2, range=[0, 100])
            
            return {
                'chart_html': fig.to_html(include_plotlyjs='cdn'),
                'chart_json': fig.to_json(),
                'symbols': symbols,
                'chart_type': 'dashboard_summary'
            }
            
        except Exception as e:
            logger.error(f"Error creating dashboard summary: {e}")
            return {'error': str(e)}
    
    def _get_market_data(self, symbol: str, days: int = 252) -> pd.DataFrame:
        """Get market data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = '''
                SELECT date, open_price, high_price, low_price, close_price, volume
                FROM market_data 
                WHERE symbol = ? 
                ORDER BY date DESC 
                LIMIT ?
            '''
            
            df = pd.read_sql_query(query, conn, params=(symbol, days))
            conn.close()
            
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                df = df.reset_index(drop=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting market data for {symbol}: {e}")
            return pd.DataFrame()
    
    def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> np.ndarray:
        """Calculate RSI indicator"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi.fillna(50).values
            
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return np.full(len(prices), 50)
    
    def _calculate_correlation_matrix(self, symbols: List[str]) -> Optional[pd.DataFrame]:
        """Calculate correlation matrix for symbols"""
        try:
            price_data = {}
            
            for symbol in symbols:
                data = self._get_market_data(symbol, 60)
                if not data.empty:
                    price_data[symbol] = data.set_index('date')['close_price']
            
            if len(price_data) < 2:
                return None
            
            # Align data and calculate correlations
            df = pd.DataFrame(price_data)
            df = df.dropna()
            
            # Calculate returns correlation
            returns = df.pct_change().dropna()
            correlation_matrix = returns.corr()
            
            return correlation_matrix
            
        except Exception as e:
            logger.error(f"Error calculating correlation matrix: {e}")
            return None
    
    def _analyze_capital_flows(self, symbols: List[str]) -> Dict[str, Any]:
        """Analyze capital flows between asset classes"""
        try:
            # Simplified capital flow analysis
            # In reality, this would use more sophisticated flow analysis
            
            asset_classes = {
                'SPY': 'Equities',
                'GLD': 'Gold',
                'TLT': 'Bonds',
                'VIX': 'Volatility',
                'DXY': 'Dollar'
            }
            
            labels = list(set(asset_classes.values()))
            
            # Simulate flow data (in practice, this would be calculated from actual data)
            flow_data = {
                'labels': labels + ['Inflow', 'Outflow'],
                'colors': ['blue', 'gold', 'green', 'red', 'gray', 'lightblue', 'lightcoral'],
                'source': [0, 1, 2, 3, 4, 5, 5, 5],
                'target': [5, 5, 5, 6, 6, 0, 1, 2],
                'values': [20, 15, 25, 10, 5, 30, 20, 25]
            }
            
            return flow_data
            
        except Exception as e:
            logger.error(f"Error analyzing capital flows: {e}")
            return {
                'labels': ['Error'],
                'colors': ['red'],
                'source': [0],
                'target': [0],
                'values': [1]
            }
    
    def export_chart_as_image(self, chart_data: Dict[str, Any], format: str = 'png') -> str:
        """Export chart as base64 encoded image"""
        try:
            if 'chart_json' not in chart_data:
                return ''
            
            # This would require additional setup for image export
            # For now, return placeholder
            return 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
            
        except Exception as e:
            logger.error(f"Error exporting chart as image: {e}")
            return ''

def main():
    """Test the advanced visualization system"""
    print("Advanced Visualization System for Socrates AI")
    print("=" * 50)
    
    visualizer = AdvancedVisualizer()
    
    # Test different chart types
    print("1. Creating price chart...")
    price_chart = visualizer.create_market_price_chart('AAPL', 60)
    if 'error' not in price_chart:
        print(f"   ✓ Price chart created with {price_chart['data_points']} data points")
    else:
        print(f"   ✗ Error: {price_chart['error']}")
    
    print("2. Creating ECM cycle chart...")
    ecm_chart = visualizer.create_ecm_cycle_chart()
    if 'error' not in ecm_chart:
        print(f"   ✓ ECM chart created, cycle position: {ecm_chart['cycle_position']:.3f}")
    else:
        print(f"   ✗ Error: {ecm_chart['error']}")
    
    print("3. Creating correlation heatmap...")
    correlation_chart = visualizer.create_correlation_heatmap(['AAPL', 'GOOGL', 'SPY'])
    if 'error' not in correlation_chart:
        print(f"   ✓ Correlation heatmap created for {len(correlation_chart['symbols'])} symbols")
    else:
        print(f"   ✗ Error: {correlation_chart['error']}")
    
    print("4. Creating capital flow chart...")
    flow_chart = visualizer.create_capital_flow_chart()
    if 'error' not in flow_chart:
        print("   ✓ Capital flow chart created")
    else:
        print(f"   ✗ Error: {flow_chart['error']}")
    
    print("5. Creating forecast chart...")
    forecast_data = {'trend': 0.001, 'volatility': 0.02}
    forecast_chart = visualizer.create_forecast_chart('AAPL', forecast_data)
    if 'error' not in forecast_chart:
        print("   ✓ Forecast chart created")
    else:
        print(f"   ✗ Error: {forecast_chart['error']}")
    
    print("6. Creating dashboard summary...")
    dashboard = visualizer.create_dashboard_summary(['AAPL', 'SPY', 'GLD'])
    if 'error' not in dashboard:
        print(f"   ✓ Dashboard created for {len(dashboard['symbols'])} symbols")
    else:
        print(f"   ✗ Error: {dashboard['error']}")
    
    print("\nAdvanced visualization system test completed!")
    print("Charts can be embedded in web applications using the HTML output.")

if __name__ == "__main__":
    main()

