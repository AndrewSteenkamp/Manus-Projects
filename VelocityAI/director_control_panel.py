"""
Director Control Panel - Executive Oversight System
Provides high-level control and monitoring for the autonomous AI agency
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import json

class DirectorControlPanel:
    def __init__(self):
        self.setup_page_config()
        
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="AI Agency Director Dashboard",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
    def run(self):
        """Run the director control panel"""
        st.title("🚀 AI-Powered UGC Agency - Director Dashboard")
        st.markdown("**Your Autonomous Agency at a Glance**")
        
        # Sidebar for navigation
        self.render_sidebar()
        
        # Main dashboard sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Executive Overview", 
            "🤖 Agent Performance", 
            "💰 Financial Metrics", 
            "👥 Client Management", 
            "⚙️ System Controls"
        ])
        
        with tab1:
            self.render_executive_overview()
            
        with tab2:
            self.render_agent_performance()
            
        with tab3:
            self.render_financial_metrics()
            
        with tab4:
            self.render_client_management()
            
        with tab5:
            self.render_system_controls()
    
    def render_sidebar(self):
        """Render sidebar with key metrics"""
        st.sidebar.header("🎯 Key Metrics")
        
        # Real-time metrics
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            st.metric("MRR", "$125K", "+$25K")
            st.metric("Clients", "25", "+8")
            
        with col2:
            st.metric("Profit", "87%", "+2%")
            st.metric("Satisfaction", "4.9/5", "+0.1")
        
        st.sidebar.markdown("---")
        
        # Agent status
        st.sidebar.header("🤖 Agent Status")
        
        agents = [
            ("Sales Agent", "🟢", "94%"),
            ("Creative Agent", "🟢", "97%"),
            ("Account Manager", "🟢", "95%"),
            ("Operations Agent", "🟢", "96%"),
            ("Finance Agent", "🟢", "98%"),
            ("Marketing Agent", "🟢", "92%")
        ]
        
        for name, status, performance in agents:
            st.sidebar.write(f"{status} {name}: {performance}")
        
        st.sidebar.markdown("---")
        
        # Quick actions
        st.sidebar.header("⚡ Quick Actions")
        
        if st.sidebar.button("📈 Generate Report"):
            st.sidebar.success("Report generated!")
            
        if st.sidebar.button("🎯 Set New Targets"):
            st.sidebar.info("Target setting panel opened")
            
        if st.sidebar.button("🚨 Emergency Stop"):
            st.sidebar.error("Emergency protocols activated")
    
    def render_executive_overview(self):
        """Render executive overview section"""
        st.header("📊 Executive Overview")
        
        # Key performance indicators
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Monthly Recurring Revenue",
                value="$125,000",
                delta="$25,000 (+25%)",
                help="Total monthly recurring revenue from all clients"
            )
            
        with col2:
            st.metric(
                label="Active Clients",
                value="25",
                delta="8 new this month",
                help="Total number of active paying clients"
            )
            
        with col3:
            st.metric(
                label="Videos Produced",
                value="2,500",
                delta="500 above target",
                help="Total UGC videos produced this month"
            )
            
        with col4:
            st.metric(
                label="Profit Margin",
                value="87%",
                delta="2% improvement",
                help="Net profit margin after all expenses"
            )
        
        st.markdown("---")
        
        # Revenue growth chart
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📈 Revenue Growth Trend")
            
            # Sample revenue data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            revenue = [50000, 65000, 80000, 95000, 110000, 125000]
            
            fig = px.line(
                x=months, 
                y=revenue,
                title="Monthly Recurring Revenue Growth",
                labels={'x': 'Month', 'y': 'Revenue ($)'}
            )
            fig.update_traces(line_color='#00CC96', line_width=3)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Performance Summary")
            
            performance_data = {
                "Metric": ["Client Acquisition", "Video Quality", "Client Retention", "System Uptime"],
                "Score": [94, 97, 98, 99.9],
                "Target": [90, 95, 95, 99.5]
            }
            
            df = pd.DataFrame(performance_data)
            
            for _, row in df.iterrows():
                progress = row['Score'] / 100
                st.write(f"**{row['Metric']}**")
                st.progress(progress)
                st.write(f"{row['Score']}% (Target: {row['Target']}%)")
                st.write("")
    
    def render_agent_performance(self):
        """Render agent performance section"""
        st.header("🤖 Agent Performance Dashboard")
        
        # Agent performance overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🎯 Sales Agent")
            st.metric("New Clients", "8", "+3 vs target")
            st.metric("Conversion Rate", "8.5%", "+0.5%")
            st.metric("Response Rate", "12%", "+2%")
            
            # Performance gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = 94,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Performance Score"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎨 Creative Agent")
            st.metric("Videos Created", "2,500", "100% of target")
            st.metric("Quality Score", "96.2%", "+1.2%")
            st.metric("Turnaround Time", "36 hours", "-12 hours")
            
            # Performance gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = 97,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Performance Score"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.subheader("👥 Account Manager")
            st.metric("Client Satisfaction", "4.9/5", "+0.1")
            st.metric("Retention Rate", "98%", "+3%")
            st.metric("Upsell Success", "35%", "+5%")
            
            # Performance gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = 95,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Performance Score"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkorange"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Agent task completion
        st.subheader("📋 Agent Task Completion")
        
        task_data = {
            'Agent': ['Sales', 'Creative', 'Account Mgr', 'Operations', 'Finance', 'Marketing'],
            'Completed': [45, 250, 78, 156, 89, 123],
            'In Progress': [8, 15, 12, 4, 3, 18],
            'Pending': [2, 5, 3, 1, 0, 7]
        }
        
        df_tasks = pd.DataFrame(task_data)
        
        fig = px.bar(
            df_tasks, 
            x='Agent', 
            y=['Completed', 'In Progress', 'Pending'],
            title="Task Status by Agent",
            color_discrete_map={
                'Completed': '#00CC96',
                'In Progress': '#FFA15A',
                'Pending': '#EF553B'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def render_financial_metrics(self):
        """Render financial metrics section"""
        st.header("💰 Financial Performance")
        
        # Financial overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Monthly Revenue", "$125,000", "+$25,000")
        with col2:
            st.metric("Operating Costs", "$16,250", "-$1,750")
        with col3:
            st.metric("Net Profit", "$108,750", "+$26,750")
        with col4:
            st.metric("Profit Margin", "87%", "+2%")
        
        st.markdown("---")
        
        # Revenue breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💵 Revenue by Package Type")
            
            package_data = {
                'Package': ['Standard ($5K)', 'Premium ($10K)', 'Enterprise ($25K)'],
                'Clients': [15, 8, 2],
                'Revenue': [75000, 80000, 50000]
            }
            
            fig = px.pie(
                values=package_data['Revenue'],
                names=package_data['Package'],
                title="Revenue Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Cost Breakdown")
            
            cost_data = {
                'Category': ['AI Tools', 'Infrastructure', 'Marketing', 'Operations'],
                'Amount': [5000, 2000, 7000, 2250]
            }
            
            fig = px.bar(
                x=cost_data['Category'],
                y=cost_data['Amount'],
                title="Monthly Operating Costs"
            )
            fig.update_traces(marker_color='#EF553B')
            st.plotly_chart(fig, use_container_width=True)
        
        # Financial projections
        st.subheader("📈 Financial Projections")
        
        projection_data = {
            'Month': ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            'Projected Revenue': [150000, 180000, 220000, 270000, 330000, 400000],
            'Projected Costs': [19500, 23400, 28600, 35100, 42900, 52000]
        }
        
        df_proj = pd.DataFrame(projection_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_proj['Month'], 
            y=df_proj['Projected Revenue'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#00CC96', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=df_proj['Month'], 
            y=df_proj['Projected Costs'],
            mode='lines+markers',
            name='Costs',
            line=dict(color='#EF553B', width=3)
        ))
        
        fig.update_layout(
            title="6-Month Financial Projection",
            xaxis_title="Month",
            yaxis_title="Amount ($)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_client_management(self):
        """Render client management section"""
        st.header("👥 Client Management")
        
        # Client overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Clients", "25", "+8 this month")
        with col2:
            st.metric("Avg. Satisfaction", "4.9/5", "+0.1")
        with col3:
            st.metric("Retention Rate", "98%", "+3%")
        with col4:
            st.metric("Churn Risk", "0 clients", "0%")
        
        st.markdown("---")
        
        # Client list
        st.subheader("📋 Client Portfolio")
        
        client_data = {
            'Client': [f'Client {i+1}' for i in range(10)],
            'Package': ['Standard', 'Premium', 'Enterprise', 'Standard', 'Premium', 
                       'Standard', 'Standard', 'Enterprise', 'Premium', 'Standard'],
            'MRR': [5000, 10000, 25000, 5000, 10000, 5000, 5000, 25000, 10000, 5000],
            'Satisfaction': [4.8, 4.9, 5.0, 4.7, 4.9, 4.8, 4.6, 5.0, 4.9, 4.8],
            'Videos This Month': [100, 200, 500, 100, 200, 100, 100, 500, 200, 100],
            'Status': ['Active', 'Active', 'Active', 'Active', 'Active', 
                      'Active', 'Active', 'Active', 'Active', 'Active']
        }
        
        df_clients = pd.DataFrame(client_data)
        
        # Add color coding for packages
        def color_package(val):
            if val == 'Enterprise':
                return 'background-color: #d4edda'
            elif val == 'Premium':
                return 'background-color: #fff3cd'
            else:
                return 'background-color: #f8f9fa'
        
        styled_df = df_clients.style.applymap(color_package, subset=['Package'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Client satisfaction distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("😊 Satisfaction Distribution")
            
            satisfaction_data = {
                'Rating': ['5.0', '4.8-4.9', '4.5-4.7', '4.0-4.4', '<4.0'],
                'Count': [8, 12, 5, 0, 0]
            }
            
            fig = px.bar(
                x=satisfaction_data['Rating'],
                y=satisfaction_data['Count'],
                title="Client Satisfaction Ratings"
            )
            fig.update_traces(marker_color='#00CC96')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📦 Package Distribution")
            
            package_counts = df_clients['Package'].value_counts()
            
            fig = px.pie(
                values=package_counts.values,
                names=package_counts.index,
                title="Clients by Package Type"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_system_controls(self):
        """Render system controls section"""
        st.header("⚙️ System Controls & Settings")
        
        # System status
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🖥️ System Status")
            st.success("✅ All Systems Operational")
            st.info("🔄 Last Update: 2 minutes ago")
            st.metric("Uptime", "99.9%", "No downtime this month")
        
        with col2:
            st.subheader("🎯 Performance Targets")
            
            new_client_target = st.number_input("New Clients/Month", value=15, min_value=1, max_value=100)
            quality_target = st.slider("Quality Score Target", 90, 100, 95)
            satisfaction_target = st.slider("Satisfaction Target", 4.0, 5.0, 4.8, 0.1)
            
            if st.button("Update Targets"):
                st.success("Targets updated successfully!")
        
        with col3:
            st.subheader("🚨 Emergency Controls")
            
            st.warning("⚠️ Use with caution")
            
            if st.button("Pause All Agents", type="secondary"):
                st.info("All agents paused")
            
            if st.button("Emergency Stop", type="secondary"):
                st.error("Emergency stop activated")
            
            if st.button("Restart System", type="secondary"):
                st.success("System restart initiated")
        
        st.markdown("---")
        
        # Agent configuration
        st.subheader("🤖 Agent Configuration")
        
        agent_configs = {
            'Sales Agent': {
                'Lead Generation Rate': 50,
                'Outreach Volume': 100,
                'Follow-up Frequency': 3
            },
            'Creative Agent': {
                'Videos per Client': 100,
                'Quality Threshold': 95,
                'Revision Limit': 2
            },
            'Account Manager': {
                'Check-in Frequency': 7,
                'Upsell Threshold': 90,
                'Response Time': 2
            }
        }
        
        selected_agent = st.selectbox("Select Agent to Configure", list(agent_configs.keys()))
        
        if selected_agent:
            st.write(f"**{selected_agent} Settings:**")
            
            config = agent_configs[selected_agent]
            for setting, value in config.items():
                new_value = st.number_input(f"{setting}", value=value, key=f"{selected_agent}_{setting}")
                config[setting] = new_value
            
            if st.button(f"Update {selected_agent} Config"):
                st.success(f"{selected_agent} configuration updated!")
        
        # Approval queue
        st.markdown("---")
        st.subheader("✅ Director Approval Queue")
        
        approvals = [
            {
                "Type": "New Enterprise Client",
                "Details": "TechCorp wants $25K/month package",
                "Impact": "$300K annual revenue",
                "Priority": "High"
            },
            {
                "Type": "Marketing Campaign",
                "Details": "LinkedIn advertising campaign",
                "Impact": "$5K monthly spend",
                "Priority": "Medium"
            }
        ]
        
        for i, approval in enumerate(approvals):
            with st.expander(f"{approval['Type']} - {approval['Priority']} Priority"):
                st.write(f"**Details:** {approval['Details']}")
                st.write(f"**Impact:** {approval['Impact']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("✅ Approve", key=f"approve_{i}"):
                        st.success("Approved!")
                with col2:
                    if st.button("❌ Reject", key=f"reject_{i}"):
                        st.error("Rejected!")
                with col3:
                    if st.button("⏸️ Defer", key=f"defer_{i}"):
                        st.info("Deferred!")

# Run the director control panel
if __name__ == "__main__":
    panel = DirectorControlPanel()
    panel.run()

