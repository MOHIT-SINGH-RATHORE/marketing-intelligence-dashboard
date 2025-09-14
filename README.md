# Marketing Intelligence Dashboard

A comprehensive business intelligence dashboard for analyzing marketing performance and its impact on business outcomes.

## 🚀 Features

### Core Analytics
- **Revenue & Profit Tracking**: Real-time monitoring of business performance metrics
- **Marketing ROI Analysis**: Comprehensive return on investment calculations
- **Campaign Performance**: Detailed analysis of individual campaign effectiveness
- **Platform Comparison**: Side-by-side comparison of Facebook, Google, and TikTok performance
- **Geographic Analysis**: Performance breakdown by state/region

### Advanced Analytics
- **Attribution Analysis**: Multi-touch attribution modeling across platforms
- **Cohort Analysis**: Customer acquisition and retention insights
- **Seasonal Analysis**: Identify trends and patterns in marketing performance
- **Correlation Analysis**: Understand relationships between marketing spend and business metrics
- **ROI Optimization**: Data-driven budget allocation recommendations

### Interactive Features
- **Real-time Filtering**: Filter by date range, platform, and campaign
- **Dynamic Visualizations**: Interactive charts and graphs using Plotly
- **Export Capabilities**: Download reports and data for further analysis
- **Responsive Design**: Optimized for desktop and mobile viewing

## 📊 Key Metrics

### Business Metrics
- Total Revenue & Gross Profit
- Order Volume & New Customer Acquisition
- Average Order Value (AOV)
- Conversion Rates
- Profit Margins

### Marketing Metrics
- Return on Ad Spend (ROAS)
- Cost Per Click (CPC)
- Click-Through Rate (CTR)
- Cost Per Mille (CPM)
- Attribution Revenue

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd marketing-intelligence-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your data**
   - Place your CSV files in the project directory:
     - `business.csv` - Daily business performance data
     - `Facebook.csv` - Facebook campaign data
     - `Google.csv` - Google campaign data
     - `TikTok.csv` - TikTok campaign data

4. **Run the dashboard**
   ```bash
   streamlit run marketing_dashboard.py
   ```

## 📁 Data Structure

### Business Data (business.csv)
```
date, # of orders, # of new orders, new customers, total revenue, gross profit, COGS
```

### Marketing Data (Facebook.csv, Google.csv, TikTok.csv)
```
date, tactic, state, campaign, impression, clicks, spend, attributed revenue
```

## 🎯 Usage

### Basic Dashboard
1. Open the main dashboard: `streamlit run marketing_dashboard.py`
2. Use the sidebar filters to customize your view
3. Explore different tabs for various analyses

### Advanced Analysis
1. Import the advanced analysis module:
   ```python
   from advanced_analysis import run_advanced_analysis
   ```
2. Run comprehensive analysis:
   ```python
   results = run_advanced_analysis(business_df, marketing_df)
   ```

## 📈 Key Insights

The dashboard provides actionable insights such as:

- **Best Performing Campaigns**: Identify top ROI campaigns for budget allocation
- **Platform Optimization**: Determine which platforms deliver the best results
- **Tactic Effectiveness**: Understand which marketing tactics work best
- **Geographic Performance**: Optimize spend across different regions
- **Seasonal Trends**: Plan campaigns around peak performance periods

## 🔧 Customization

### Adding New Metrics
1. Modify the data processing functions in `marketing_dashboard.py`
2. Add new visualization functions
3. Update the KPI cards section

### Custom Visualizations
1. Use Plotly to create new chart types
2. Add them to the appropriate analysis sections
3. Ensure responsive design for mobile compatibility

## 📊 Sample Analysis

### ROAS by Platform
- Facebook: 3.2x average ROAS
- Google: 2.8x average ROAS  
- TikTok: 2.5x average ROAS

### Top Performing Tactics
1. Retargeting campaigns show highest ROAS
2. Prospecting campaigns drive volume
3. Spark Ads perform well on TikTok

### Geographic Insights
- California shows highest revenue per dollar spent
- New York has highest conversion rates
- Consider geographic budget reallocation

## 🚀 Deployment

### Local Deployment
```bash
streamlit run marketing_dashboard.py --server.port 8501
```

### Cloud Deployment
1. **Streamlit Cloud**: Upload to GitHub and deploy via Streamlit Cloud
2. **Heroku**: Use the provided Procfile and requirements.txt
3. **AWS/GCP**: Deploy using Docker containers

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "marketing_dashboard.py"]
```

## 📝 Data Requirements

### Minimum Data Points
- At least 30 days of data for trend analysis
- Complete campaign attribution data
- Consistent date formatting (YYYY-MM-DD)
- Numeric values for all metrics

### Data Quality
- Ensure no missing values in critical fields
- Validate date ranges for consistency
- Check for outliers in spend and revenue data
- Verify attribution revenue accuracy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues:
1. Check the documentation
2. Review the code comments
3. Open an issue on GitHub
4. Contact the development team

## 🔄 Updates

### Version 1.0.0
- Initial release with core dashboard functionality
- Basic analytics and visualizations
- Platform comparison features

### Future Releases
- Machine learning predictions
- Advanced attribution modeling
- Real-time data integration
- Mobile app version

---

**Built with ❤️ using Streamlit, Plotly, and Python**
