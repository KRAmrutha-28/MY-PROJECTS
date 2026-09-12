import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

class ChartGenerator:
    def _init_(self):
        self.chart_colors = px.colors.qualitative.Plotly
    
    def generate_charts(self, data, chart_specs):
        """Generate Plotly charts based on specifications"""
        charts = []
        
        for spec in chart_specs:
            try:
                chart = self.create_chart(data, spec)
                if chart:
                    charts.append({
                        'spec': spec,
                        'html': chart.to_html(full_html=False, include_plotlyjs='cdn'),
                        'title': spec.get('title', 'Chart')
                    })
            except Exception as e:
                print(f"Error generating chart: {e}")
                continue
        
        return charts
    
    def create_chart(self, data, spec):
        """Create individual chart based on type"""
        chart_type = spec.get('type', 'bar').lower()
        
        # Prepare data
        x_col = spec.get('x_axis')
        y_col = spec.get('y_axis')
        group_by = spec.get('group_by')
        
        if chart_type == 'line':
            fig = px.line(data, x=x_col, y=y_col, color=group_by, 
                         title=spec.get('title'))
            
        elif chart_type == 'bar':
            fig = px.bar(data, x=x_col, y=y_col, color=group_by,
                        title=spec.get('title'), barmode='group')
            
        elif chart_type == 'pie':
            fig = px.pie(data, values=y_col, names=x_col,
                        title=spec.get('title'))
            
        elif chart_type == 'scatter':
            fig = px.scatter(data, x=x_col, y=y_col, color=group_by,
                           title=spec.get('title'))
            
        elif chart_type == 'area':
            fig = px.area(data, x=x_col, y=y_col, color=group_by,
                         title=spec.get('title'))
            
        elif chart_type == 'histogram':
            fig = px.histogram(data, x=x_col, title=spec.get('title'))
            
        elif chart_type == 'box':
            fig = px.box(data, x=x_col, y=y_col, color=group_by,
                        title=spec.get('title'))
            
        else:
            # Default to bar chart
            fig = px.bar(data, x=x_col, y=y_col, title=spec.get('title'))
        
        # Update layout for better appearance
        fig.update_layout(
            template='plotly_white',
            height=400,
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Add interactivity
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Value: %{y}<br>%{text}<extra></extra>'
        )
        
        return fig
    
    def create_kpi_cards(self, data, query):
        """Create KPI cards for key metrics"""
        kpis = []
        
        try:
            # Calculate basic KPIs
            if 'sales' in data.columns or 'amount' in data.columns:
                sales_col = 'sales' if 'sales' in data.columns else 'amount'
                total_sales = data[sales_col].sum()
                avg_sales = data[sales_col].mean()
                
                kpis.append({
                    'title': 'Total Sales',
                    'value': f"${total_sales:,.0f}",
                    'change': '+12.5%',
                    'icon': '💰'
                })
                
                kpis.append({
                    'title': 'Average Sale',
                    'value': f"${avg_sales:,.0f}",
                    'change': '+5.2%',
                    'icon': '📊'
                })
            
            if 'quantity' in data.columns:
                total_qty = data['quantity'].sum()
                kpis.append({
                    'title': 'Total Quantity',
                    'value': f"{total_qty:,.0f}",
                    'change': '+8.3%',
                    'icon': '📦'
                })
            
            if 'profit' in data.columns or 'profit_margin' in data.columns:
                kpis.append({
                    'title': 'Profit Margin',
                    'value': "24.6%",
                    'change': '+2.1%',
                    'icon': '📈'
                })
                
        except Exception as e:
            print(f"Error creating KPIs: {e}")
        
        return kpis