import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff6b6b;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and process all marketing and business data"""
    try:
        # Load business data
        business_df = pd.read_csv('business.csv')
        business_df['date'] = pd.to_datetime(business_df['date'])
        
        # Load marketing data
        facebook_df = pd.read_csv('Facebook.csv')
        facebook_df['date'] = pd.to_datetime(facebook_df['date'])
        facebook_df['platform'] = 'Facebook'
        
        google_df = pd.read_csv('Google.csv')
        google_df['date'] = pd.to_datetime(google_df['date'])
        google_df['platform'] = 'Google'
        
        tiktok_df = pd.read_csv('TikTok.csv')
        tiktok_df['date'] = pd.to_datetime(tiktok_df['date'])
        tiktok_df['platform'] = 'TikTok'
        
        # Combine all marketing data
        marketing_df = pd.concat([facebook_df, google_df, tiktok_df], ignore_index=True)
        
        # Calculate additional metrics
        marketing_df['ctr'] = (marketing_df['clicks'] / marketing_df['impression'] * 100).round(2)
        marketing_df['cpc'] = (marketing_df['spend'] / marketing_df['clicks']).round(2)
        marketing_df['roas'] = (marketing_df['attributed revenue'] / marketing_df['spend']).round(2)
        marketing_df['cpm'] = (marketing_df['spend'] / marketing_df['impression'] * 1000).round(2)
        
        # Business metrics
        business_df['aov'] = (business_df['total revenue'] / business_df['# of orders']).round(2)
        business_df['conversion_rate'] = (business_df['# of new orders'] / business_df['# of orders'] * 100).round(2)
        business_df['profit_margin'] = (business_df['gross profit'] / business_df['total revenue'] * 100).round(2)
        
        return business_df, marketing_df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

def create_kpi_cards(business_df, marketing_df):
    """Create KPI cards for key metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = business_df['total revenue'].sum()
        st.metric(
            label="Total Revenue",
            value=f"${total_revenue:,.0f}",
            delta=f"{business_df['total revenue'].pct_change().mean()*100:.1f}%"
        )
    
    with col2:
        total_spend = marketing_df['spend'].sum()
        st.metric(
            label="Total Ad Spend",
            value=f"${total_spend:,.0f}",
            delta=f"{marketing_df['spend'].pct_change().mean()*100:.1f}%"
        )
    
    with col3:
        total_roas = marketing_df['attributed revenue'].sum() / marketing_df['spend'].sum()
        st.metric(
            label="Overall ROAS",
            value=f"{total_roas:.2f}x",
            delta=f"{marketing_df['roas'].mean():.2f}x avg"
        )
    
    with col4:
        total_orders = business_df['# of orders'].sum()
        st.metric(
            label="Total Orders",
            value=f"{total_orders:,}",
            delta=f"{business_df['# of orders'].pct_change().mean()*100:.1f}%"
        )

def create_revenue_trend_chart(business_df):
    """Create revenue trend chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=business_df['date'],
        y=business_df['total revenue'],
        mode='lines+markers',
        name='Total Revenue',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=business_df['date'],
        y=business_df['gross profit'],
        mode='lines+markers',
        name='Gross Profit',
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Revenue & Profit Trends",
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_marketing_performance_chart(marketing_df):
    """Create marketing performance by platform"""
    platform_metrics = marketing_df.groupby('platform').agg({
        'spend': 'sum',
        'attributed revenue': 'sum',
        'clicks': 'sum',
        'impression': 'sum'
    }).reset_index()
    
    platform_metrics['roas'] = platform_metrics['attributed revenue'] / platform_metrics['spend']
    platform_metrics['ctr'] = (platform_metrics['clicks'] / platform_metrics['impression'] * 100)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Spend by Platform', 'ROAS by Platform', 'Clicks by Platform', 'CTR by Platform'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Spend
    fig.add_trace(
        go.Bar(x=platform_metrics['platform'], y=platform_metrics['spend'], name='Spend', marker_color='#1f77b4'),
        row=1, col=1
    )
    
    # ROAS
    fig.add_trace(
        go.Bar(x=platform_metrics['platform'], y=platform_metrics['roas'], name='ROAS', marker_color='#ff7f0e'),
        row=1, col=2
    )
    
    # Clicks
    fig.add_trace(
        go.Bar(x=platform_metrics['platform'], y=platform_metrics['clicks'], name='Clicks', marker_color='#2ca02c'),
        row=2, col=1
    )
    
    # CTR
    fig.add_trace(
        go.Bar(x=platform_metrics['platform'], y=platform_metrics['ctr'], name='CTR', marker_color='#d62728'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    return fig

def create_campaign_analysis(marketing_df):
    """Create campaign performance analysis"""
    campaign_metrics = marketing_df.groupby(['platform', 'campaign']).agg({
        'spend': 'sum',
        'attributed revenue': 'sum',
        'clicks': 'sum',
        'impression': 'sum',
        'roas': 'mean'
    }).reset_index()
    
    campaign_metrics['roi'] = ((campaign_metrics['attributed revenue'] - campaign_metrics['spend']) / campaign_metrics['spend'] * 100).round(2)
    campaign_metrics = campaign_metrics.sort_values('roi', ascending=False)
    
    return campaign_metrics

def create_tactic_analysis(marketing_df):
    """Analyze performance by marketing tactic"""
    tactic_metrics = marketing_df.groupby(['platform', 'tactic']).agg({
        'spend': 'sum',
        'attributed revenue': 'sum',
        'roas': 'mean',
        'ctr': 'mean'
    }).reset_index()
    
    return tactic_metrics

def create_geographic_analysis(marketing_df):
    """Analyze performance by state"""
    geo_metrics = marketing_df.groupby('state').agg({
        'spend': 'sum',
        'attributed revenue': 'sum',
        'clicks': 'sum',
        'roas': 'mean'
    }).reset_index()
    
    return geo_metrics

def main():
    st.markdown('<h1 class="main-header">📊 Marketing Intelligence Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    business_df, marketing_df = load_data()
    
    if business_df is None or marketing_df is None:
        st.error("Failed to load data. Please check your CSV files.")
        return
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Date range filter
    min_date = business_df['date'].min()
    max_date = business_df['date'].max()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Platform filter
    platforms = st.sidebar.multiselect(
        "Select Platforms",
        options=marketing_df['platform'].unique(),
        default=marketing_df['platform'].unique()
    )
    
    # Apply filters
    if len(date_range) == 2:
        start_date, end_date = date_range
        business_df_filtered = business_df[
            (business_df['date'] >= pd.to_datetime(start_date)) &
            (business_df['date'] <= pd.to_datetime(end_date))
        ]
        marketing_df_filtered = marketing_df[
            (marketing_df['date'] >= pd.to_datetime(start_date)) &
            (marketing_df['date'] <= pd.to_datetime(end_date)) &
            (marketing_df['platform'].isin(platforms))
        ]
    else:
        business_df_filtered = business_df
        marketing_df_filtered = marketing_df[marketing_df['platform'].isin(platforms)]
    
    # KPI Cards
    create_kpi_cards(business_df_filtered, marketing_df_filtered)
    
    st.markdown("---")
    
    # Main charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_revenue_trend_chart(business_df_filtered), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_marketing_performance_chart(marketing_df_filtered), use_container_width=True)
    
    st.markdown("---")
    
    # Campaign Analysis
    st.header("🎯 Campaign Performance Analysis")
    campaign_analysis = create_campaign_analysis(marketing_df_filtered)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Performing Campaigns by ROI")
        top_campaigns = campaign_analysis.head(10)
        st.dataframe(
            top_campaigns[['platform', 'campaign', 'spend', 'attributed revenue', 'roi']].round(2),
            use_container_width=True
        )
    
    with col2:
        st.subheader("Campaign ROAS Distribution")
        fig_roas = px.box(
            campaign_analysis,
            x='platform',
            y='roas',
            title='ROAS Distribution by Platform',
            color='platform'
        )
        st.plotly_chart(fig_roas, use_container_width=True)
    
    st.markdown("---")
    
    # Tactic Analysis
    st.header("📈 Marketing Tactic Analysis")
    tactic_analysis = create_tactic_analysis(marketing_df_filtered)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Performance by Tactic")
        fig_tactic = px.bar(
            tactic_analysis,
            x='tactic',
            y='roas',
            color='platform',
            title='ROAS by Marketing Tactic',
            barmode='group'
        )
        st.plotly_chart(fig_tactic, use_container_width=True)
    
    with col2:
        st.subheader("Spend vs Revenue by Tactic")
        fig_scatter = px.scatter(
            tactic_analysis,
            x='spend',
            y='attributed revenue',
            size='roas',
            color='platform',
            hover_data=['tactic'],
            title='Spend vs Revenue by Tactic'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # Geographic Analysis
    st.header("🌍 Geographic Performance")
    geo_analysis = create_geographic_analysis(marketing_df_filtered)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Performance by State")
        fig_geo = px.bar(
            geo_analysis,
            x='state',
            y='roas',
            title='ROAS by State',
            color='roas',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_geo, use_container_width=True)
    
    with col2:
        st.subheader("State Performance Summary")
        st.dataframe(
            geo_analysis.round(2),
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Insights and Recommendations
    st.header("💡 Key Insights & Recommendations")
    
    # Calculate key insights
    total_revenue = business_df_filtered['total revenue'].sum()
    total_spend = marketing_df_filtered['spend'].sum()
    overall_roas = marketing_df_filtered['attributed revenue'].sum() / marketing_df_filtered['spend'].sum()
    
    best_platform = marketing_df_filtered.groupby('platform')['roas'].mean().idxmax()
    best_tactic = marketing_df_filtered.groupby('tactic')['roas'].mean().idxmax()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📊 Performance Summary:**
        - Total Revenue: ${:,.0f}
        - Total Ad Spend: ${:,.0f}
        - Overall ROAS: {:.2f}x
        - Best Performing Platform: {}
        - Best Performing Tactic: {}
        """.format(total_revenue, total_spend, overall_roas, best_platform, best_tactic))
    
    with col2:
        st.markdown("""
        **🎯 Recommendations:**
        1. **Scale High-ROI Campaigns**: Focus budget on top-performing campaigns
        2. **Platform Optimization**: Allocate more budget to {} platform
        3. **Tactic Refinement**: Increase investment in {} tactics
        4. **Geographic Expansion**: Consider expanding successful state strategies
        5. **Performance Monitoring**: Track ROAS trends and adjust accordingly
        """.format(best_platform, best_tactic))
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        Marketing Intelligence Dashboard | Built with Streamlit & Plotly
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
