# Marketing Intelligence Dashboard

An interactive Business Intelligence dashboard for analyzing marketing performance and business outcomes.

## Overview

This dashboard provides comprehensive analysis of marketing campaigns across Facebook, Google, and TikTok platforms, connecting marketing activity with business performance metrics.

## Features

- **Executive Summary**: Real-time KPIs and key performance indicators
- **Revenue Analysis**: Revenue and profit trend visualization
- **Marketing Performance**: Platform comparison and campaign analysis
- **Campaign Deep Dive**: Top performing campaigns and optimization insights
- **Geographic Analysis**: Performance analysis by state/region
- **Advanced Analytics**: Attribution modeling and correlation analysis

## Data Sources

- **Business Data**: Daily business performance (orders, revenue, profit, customers)
- **Marketing Data**: Campaign-level data from Facebook, Google, and TikTok
- **Time Period**: 120 days of daily activity

## Key Metrics

- ROAS (Return on Ad Spend)
- CTR (Click-Through Rate)
- CPC (Cost Per Click)
- CPM (Cost Per Mille)
- AOV (Average Order Value)
- Conversion Rate
- Profit Margin

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the dashboard:
   ```bash
   streamlit run marketing_dashboard.py
   ```

## Usage

1. Open your browser to `http://localhost:8501`
2. Navigate through different analysis tabs
3. Use filters to customize your view
4. Explore interactive charts and insights

## Technical Stack

- **Python**: Data processing and analysis
- **Streamlit**: Interactive dashboard framework
- **Plotly**: Advanced data visualizations
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **SciPy**: Statistical analysis

## Project Structure

```
├── marketing_dashboard.py      # Main dashboard application
├── advanced_analysis.py        # Analytics engine
├── requirements.txt            # Python dependencies
├── Business.csv               # Business performance data
├── Facebook.csv               # Facebook marketing data
├── Google.csv                 # Google marketing data
├── TikTok.csv                 # TikTok marketing data
├── run_dashboard.py           # Dashboard launcher
└── test_dashboard.py          # Test suite
```

## Business Insights

The dashboard provides actionable insights for:
- Marketing budget allocation optimization
- Campaign performance evaluation
- Platform strategy decisions
- Geographic expansion planning
- ROI improvement recommendations

## Requirements

- Python 3.8+
- See `requirements.txt` for full dependency list

## License

This project is created for assessment purposes.