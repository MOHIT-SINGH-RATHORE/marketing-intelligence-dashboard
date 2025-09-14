#!/usr/bin/env python3
"""
Test script for Marketing Intelligence Dashboard
Validates data loading and basic functionality
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

def test_data_loading():
    """Test if all data files can be loaded correctly"""
    print("🧪 Testing data loading...")
    
    required_files = ['business.csv', 'Facebook.csv', 'Google.csv', 'TikTok.csv']
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Missing file: {file}")
            return False
        
        try:
            df = pd.read_csv(file)
            print(f"✅ {file}: {len(df)} rows loaded")
        except Exception as e:
            print(f"❌ Error loading {file}: {e}")
            return False
    
    return True

def test_data_processing():
    """Test data processing functions"""
    print("\n🧪 Testing data processing...")
    
    try:
        # Load data
        business_df = pd.read_csv('business.csv')
        facebook_df = pd.read_csv('Facebook.csv')
        google_df = pd.read_csv('Google.csv')
        tiktok_df = pd.read_csv('TikTok.csv')
        
        # Test date conversion
        business_df['date'] = pd.to_datetime(business_df['date'])
        facebook_df['date'] = pd.to_datetime(facebook_df['date'])
        google_df['date'] = pd.to_datetime(google_df['date'])
        tiktok_df['date'] = pd.to_datetime(tiktok_df['date'])
        
        print("✅ Date conversion successful")
        
        # Test metric calculations
        facebook_df['ctr'] = (facebook_df['clicks'] / facebook_df['impression'] * 100).round(2)
        facebook_df['roas'] = (facebook_df['attributed revenue'] / facebook_df['spend']).round(2)
        
        print("✅ Metric calculations successful")
        
        # Test data aggregation
        platform_metrics = facebook_df.groupby('platform').agg({
            'spend': 'sum',
            'attributed revenue': 'sum',
            'roas': 'mean'
        })
        
        print("✅ Data aggregation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Data processing error: {e}")
        return False

def test_imports():
    """Test if all required packages can be imported"""
    print("\n🧪 Testing package imports...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'openpyxl'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {package}: {e}")
            return False
    
    return True

def test_dashboard_import():
    """Test if dashboard modules can be imported"""
    print("\n🧪 Testing dashboard imports...")
    
    try:
        from advanced_analysis import MarketingAnalyzer
        print("✅ advanced_analysis module imported")
        
        # Test basic functionality
        business_df = pd.read_csv('business.csv')
        marketing_df = pd.read_csv('Facebook.csv')
        
        analyzer = MarketingAnalyzer(business_df, marketing_df)
        print("✅ MarketingAnalyzer instantiated")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard import error: {e}")
        return False

def run_performance_test():
    """Run basic performance test"""
    print("\n🧪 Running performance test...")
    
    try:
        import time
        start_time = time.time()
        
        # Load and process data
        business_df = pd.read_csv('business.csv')
        facebook_df = pd.read_csv('Facebook.csv')
        google_df = pd.read_csv('Google.csv')
        tiktok_df = pd.read_csv('TikTok.csv')
        
        # Combine marketing data
        marketing_df = pd.concat([facebook_df, google_df, tiktok_df], ignore_index=True)
        
        # Calculate metrics
        marketing_df['ctr'] = (marketing_df['clicks'] / marketing_df['impression'] * 100).round(2)
        marketing_df['roas'] = (marketing_df['attributed revenue'] / marketing_df['spend']).round(2)
        
        # Group by platform
        platform_metrics = marketing_df.groupby('platform').agg({
            'spend': 'sum',
            'attributed revenue': 'sum',
            'roas': 'mean'
        })
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Performance test completed in {processing_time:.2f} seconds")
        print(f"   - Processed {len(marketing_df)} marketing records")
        print(f"   - Processed {len(business_df)} business records")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Marketing Intelligence Dashboard - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Data Loading", test_data_loading),
        ("Package Imports", test_imports),
        ("Data Processing", test_data_processing),
        ("Dashboard Imports", test_dashboard_import),
        ("Performance Test", run_performance_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Dashboard is ready to run.")
        print("\n🚀 To start the dashboard, run:")
        print("   python run_dashboard.py")
        print("   or")
        print("   streamlit run marketing_dashboard.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
