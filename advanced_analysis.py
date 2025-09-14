import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class MarketingAnalyzer:
    """Advanced marketing data analysis class"""
    
    def __init__(self, business_df=None, marketing_df=None):
        if business_df is None or marketing_df is None:
            self.load_data()
        else:
            self.business_df = business_df
            self.marketing_df = marketing_df
        self.prepare_data()
    
    def load_data(self):
        """Load data from CSV files"""
        try:
            # Load business data
            self.business_df = pd.read_csv('Business.csv')
            
            # Load marketing data from all platforms
            facebook_df = pd.read_csv('Facebook.csv')
            google_df = pd.read_csv('Google.csv')
            tiktok_df = pd.read_csv('TikTok.csv')
            
            # Add platform column and combine
            facebook_df['platform'] = 'Facebook'
            google_df['platform'] = 'Google'
            tiktok_df['platform'] = 'TikTok'
            
            self.marketing_df = pd.concat([facebook_df, google_df, tiktok_df], ignore_index=True)
            
            print("✅ Data loaded successfully!")
            print(f"Business data: {self.business_df.shape[0]} rows")
            print(f"Marketing data: {self.marketing_df.shape[0]} rows")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def prepare_data(self):
        """Prepare and clean data for analysis"""
        # Convert dates first
        self.business_df['date'] = pd.to_datetime(self.business_df['date'])
        self.marketing_df['date'] = pd.to_datetime(self.marketing_df['date'])
        
        # Calculate additional metrics
        self.marketing_df['ctr'] = (self.marketing_df['clicks'] / self.marketing_df['impression'] * 100).round(2)
        self.marketing_df['cpc'] = (self.marketing_df['spend'] / self.marketing_df['clicks']).round(2)
        self.marketing_df['roas'] = (self.marketing_df['attributed revenue'] / self.marketing_df['spend']).round(2)
        self.marketing_df['cpm'] = (self.marketing_df['spend'] / self.marketing_df['impression'] * 1000).round(2)
        
        # Business metrics
        self.business_df['aov'] = (self.business_df['total revenue'] / self.business_df['# of orders']).round(2)
        self.business_df['conversion_rate'] = (self.business_df['# of new orders'] / self.business_df['# of orders'] * 100).round(2)
        self.business_df['profit_margin'] = (self.business_df['gross profit'] / self.business_df['total revenue'] * 100).round(2)
        
        # Add time-based features
        self.business_df['month'] = self.business_df['date'].dt.month
        self.business_df['day_of_week'] = self.business_df['date'].dt.day_name()
        self.marketing_df['month'] = self.marketing_df['date'].dt.month
        self.marketing_df['day_of_week'] = self.marketing_df['date'].dt.day_name()
    
    def calculate_attribution_analysis(self):
        """Calculate attribution analysis across platforms"""
        attribution = self.marketing_df.groupby(['platform', 'tactic']).agg({
            'spend': 'sum',
            'attributed revenue': 'sum',
            'clicks': 'sum',
            'impression': 'sum',
            'roas': 'mean'
        }).reset_index()
        
        attribution['revenue_share'] = (attribution['attributed revenue'] / attribution['attributed revenue'].sum() * 100).round(2)
        attribution['spend_share'] = (attribution['spend'] / attribution['spend'].sum() * 100).round(2)
        
        return attribution.sort_values('revenue_share', ascending=False)
    
    def calculate_cohort_analysis(self):
        """Perform cohort analysis on customer acquisition"""
        # Group by acquisition month
        cohort_data = self.business_df.groupby(self.business_df['date'].dt.to_period('M')).agg({
            'new customers': 'sum',
            'total revenue': 'sum',
            '# of orders': 'sum'
        }).reset_index()
        
        cohort_data['revenue_per_customer'] = (cohort_data['total revenue'] / cohort_data['new customers']).round(2)
        cohort_data['orders_per_customer'] = (cohort_data['# of orders'] / cohort_data['new customers']).round(2)
        
        return cohort_data
    
    def calculate_correlation_analysis(self):
        """Calculate correlations between marketing spend and business metrics"""
        # Merge marketing and business data by date
        daily_marketing = self.marketing_df.groupby('date').agg({
            'spend': 'sum',
            'attributed revenue': 'sum',
            'clicks': 'sum',
            'impression': 'sum'
        }).reset_index()
        
        merged_data = pd.merge(
            self.business_df[['date', 'total revenue', '# of orders', 'new customers', 'gross profit']],
            daily_marketing,
            on='date',
            how='inner'
        )
        
        # Calculate correlations
        correlation_matrix = merged_data[['spend', 'attributed revenue', 'total revenue', '# of orders', 'new customers']].corr()
        
        return correlation_matrix
    
    def calculate_roi_optimization(self):
        """Calculate ROI optimization recommendations"""
        platform_roi = self.marketing_df.groupby('platform').agg({
            'spend': 'sum',
            'attributed revenue': 'sum',
            'roas': 'mean'
        }).reset_index()
        
        platform_roi['roi'] = ((platform_roi['attributed revenue'] - platform_roi['spend']) / platform_roi['spend'] * 100).round(2)
        platform_roi['efficiency_score'] = (platform_roi['roas'] * platform_roi['attributed revenue']).round(2)
        
        # Calculate budget allocation recommendations
        total_spend = platform_roi['spend'].sum()
        platform_roi['current_allocation'] = (platform_roi['spend'] / total_spend * 100).round(2)
        platform_roi['recommended_allocation'] = (platform_roi['efficiency_score'] / platform_roi['efficiency_score'].sum() * 100).round(2)
        
        return platform_roi.sort_values('roi', ascending=False)
    
    def calculate_seasonality_analysis(self):
        """Analyze seasonal patterns in marketing performance"""
        monthly_performance = self.marketing_df.groupby('month').agg({
            'spend': 'sum',
            'attributed revenue': 'sum',
            'roas': 'mean',
            'ctr': 'mean'
        }).reset_index()
        
        monthly_business = self.business_df.groupby('month').agg({
            'total revenue': 'sum',
            '# of orders': 'sum',
            'new customers': 'sum'
        }).reset_index()
        
        return monthly_performance, monthly_business
    
    def calculate_forecasting_data(self):
        """Prepare data for forecasting analysis"""
        # Create daily aggregated data
        daily_data = self.business_df.groupby('date').agg({
            'total revenue': 'sum',
            '# of orders': 'sum',
            'new customers': 'sum',
            'gross profit': 'sum'
        }).reset_index()
        
        daily_marketing = self.marketing_df.groupby('date').agg({
            'spend': 'sum',
            'attributed revenue': 'sum',
            'clicks': 'sum',
            'impression': 'sum'
        }).reset_index()
        
        # Merge and create time series
        forecast_data = pd.merge(daily_data, daily_marketing, on='date', how='outer').fillna(0)
        forecast_data['roas'] = (forecast_data['attributed revenue'] / forecast_data['spend']).replace([np.inf, -np.inf], 0)
        
        return forecast_data
    
    def generate_insights(self):
        """Generate comprehensive insights and recommendations"""
        insights = []
        
        # ROAS Analysis
        avg_roas = self.marketing_df['roas'].mean()
        best_platform = self.marketing_df.groupby('platform')['roas'].mean().idxmax()
        best_tactic = self.marketing_df.groupby('tactic')['roas'].mean().idxmax()
        
        insights.append(f"Average ROAS across all campaigns: {avg_roas:.2f}x")
        insights.append(f"Best performing platform: {best_platform} with {self.marketing_df.groupby('platform')['roas'].mean().max():.2f}x ROAS")
        insights.append(f"Best performing tactic: {best_tactic} with {self.marketing_df.groupby('tactic')['roas'].mean().max():.2f}x ROAS")
        
        # Revenue Analysis
        total_revenue = self.business_df['total revenue'].sum()
        total_spend = self.marketing_df['spend'].sum()
        overall_roi = ((total_revenue - total_spend) / total_spend * 100)
        
        insights.append(f"Overall marketing ROI: {overall_roi:.1f}%")
        insights.append(f"Revenue per marketing dollar: ${total_revenue/total_spend:.2f}")
        
        # Efficiency Analysis
        ctr_avg = self.marketing_df['ctr'].mean()
        cpc_avg = self.marketing_df['cpc'].mean()
        
        insights.append(f"Average CTR: {ctr_avg:.2f}%")
        insights.append(f"Average CPC: ${cpc_avg:.2f}")
        
        return insights
    
    def create_advanced_visualizations(self):
        """Create advanced visualization charts"""
        charts = {}
        
        # 1. Attribution Funnel
        attribution = self.calculate_attribution_analysis()
        fig_funnel = px.funnel(
            attribution,
            x='attributed revenue',
            y='platform',
            color='tactic',
            title='Revenue Attribution Funnel by Platform & Tactic'
        )
        charts['attribution_funnel'] = fig_funnel
        
        # 2. ROI Optimization Chart
        roi_data = self.calculate_roi_optimization()
        fig_roi = px.scatter(
            roi_data,
            x='spend',
            y='attributed revenue',
            size='roas',
            color='platform',
            hover_data=['roi', 'efficiency_score'],
            title='ROI Optimization: Spend vs Revenue by Platform'
        )
        charts['roi_optimization'] = fig_roi
        
        # 3. Seasonal Analysis
        monthly_perf, monthly_business = self.calculate_seasonality_analysis()
        fig_seasonal = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Monthly Marketing Performance', 'Monthly Business Performance'),
            vertical_spacing=0.1
        )
        
        fig_seasonal.add_trace(
            go.Scatter(x=monthly_perf['month'], y=monthly_perf['roas'], name='ROAS', line=dict(color='blue')),
            row=1, col=1
        )
        fig_seasonal.add_trace(
            go.Scatter(x=monthly_business['month'], y=monthly_business['total revenue'], name='Revenue', line=dict(color='green')),
            row=2, col=1
        )
        
        fig_seasonal.update_layout(height=600, title_text="Seasonal Performance Analysis")
        charts['seasonal_analysis'] = fig_seasonal
        
        # 4. Correlation Heatmap
        correlation_matrix = self.calculate_correlation_analysis()
        fig_corr = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            title="Marketing Metrics Correlation Matrix"
        )
        charts['correlation_heatmap'] = fig_corr
        
        return charts

def run_advanced_analysis(business_df, marketing_df):
    """Run advanced analysis and return results"""
    analyzer = MarketingAnalyzer(business_df, marketing_df)
    
    results = {
        'attribution': analyzer.calculate_attribution_analysis(),
        'cohort': analyzer.calculate_cohort_analysis(),
        'correlation': analyzer.calculate_correlation_analysis(),
        'roi_optimization': analyzer.calculate_roi_optimization(),
        'seasonality': analyzer.calculate_seasonality_analysis(),
        'forecast_data': analyzer.calculate_forecasting_data(),
        'insights': analyzer.generate_insights(),
        'charts': analyzer.create_advanced_visualizations()
    }
    
    return results
