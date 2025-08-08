#!/usr/bin/env python3
"""
Simple Cafe Dashboard Generator for Elemental Insights
Run this script to generate new dashboards with your own data
"""

import json
from datetime import datetime, timedelta


def generate_dashboard_html(data):
    """Generate HTML dashboard from data dictionary"""
    
    # Process the data
    today_forecast = data.get('today_forecast', 1200)
    weekly_actual = data.get('weekly_actual', 8500)
    hot_drinks_pct = data.get('hot_drinks_pct', 35)
    cold_drinks_pct = data.get('cold_drinks_pct', 25)
    food_pct = data.get('food_pct', 40)
    avg_transaction = data.get('avg_transaction', 8.25)
    items_per_transaction = data.get('items_per_transaction', 2.3)
    current_temp = data.get('current_temp', 24.5)
    temp_effect = data.get('temp_effect', 1.15)
    school_effect = data.get('school_effect', 1.0)
    is_school_holiday = data.get('is_school_holiday', False)
    peak_hour = data.get('peak_hour', 13)
    peak_value = data.get('peak_value', 165)
    model_accuracy = data.get('model_accuracy', 92)
    
    # Calculate derived values
    current_date = datetime.now().strftime('%B %d, %Y')
    current_day = datetime.now().strftime('%A')
    current_time = datetime.now().strftime('%I:%M %p')
    
    # 7-day forecast
    daily_multipliers = [1.00, 1.12, 0.95, 1.25, 1.18, 0.98, 0.89]
    forecast_labels = ["Today", "Good weather", "Lunchtime boost", "Peak trade", "Warm weather", "Cooler day", "Quiet day"]
    
    forecast_html = ""
    for i in range(7):
        forecast_date = datetime.now() + timedelta(days=i)
        day_name = forecast_date.strftime('%A')
        date_str = forecast_date.strftime('%b %d')
        multiplier = daily_multipliers[i]
        label = forecast_labels[i]
        forecast_value = today_forecast * multiplier
        today_class = "today" if i == 0 else ""
        
        forecast_html += f"""
                <div class="forecast-day {today_class}">
                    <div class="day-name">{day_name}</div>
                    <div class="day-date">{date_str}</div>
                    <div class="day-forecast">£{forecast_value:.0f}</div>
                    <div class="day-multiplier">× {multiplier:.2f}</div>
                    <div class="day-details">{label}</div>
                </div>"""
    
    # Weather and holiday insights
    weather_insight = "Warm weather is boosting cold drink sales – consider highlighting iced coffee and smoothies." if temp_effect > 1.1 else "Normal weather conditions – standard product mix recommended."
    holiday_status = "Active" if is_school_holiday else "Regular Term"
    holiday_insight = "Family footfall is up – prep for longer dwell times and group orders." if is_school_holiday else "Regular school term – expect normal weekday patterns."
    
    # Generate the complete HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cafe Dashboard - {current_date}</title>
    <link rel="stylesheet" href="../css/dashboard.css">
</head>
<body>
    <div class="dashboard-container">

        <!-- Header Section -->
        <div class="header-section">
            <h1>☕ Cafe Performance Dashboard</h1>
            <div class="subtitle">{current_date} • {current_day} • Last Updated: {current_time}</div>
        </div>

        <!-- Key Metrics Overview -->
        <div class="metrics-overview">
            <div class="metric-card revenue">
                <div class="metric-title">Today's Revenue Forecast</div>
                <div class="metric-value" style="color: #27ae60;">£{today_forecast:,.0f}</div>
                <div class="metric-subtitle">
                    Weekly Total: £{weekly_actual:,.0f}
                    <span class="trend-indicator trend-up">{((today_forecast/(weekly_actual/7))-1)*100:+.0f}%</span>
                </div>
            </div>

            <div class="metric-card customers">
                <div class="metric-title">Customer Experience</div>
                <div class="metric-value" style="color: #3498db;">£{avg_transaction:.2f}</div>
                <div class="metric-subtitle">
                    Avg Transaction • {items_per_transaction:.1f} items per customer
                    <span class="trend-indicator trend-stable">Stable</span>
                </div>
            </div>

            <div class="metric-card efficiency">
                <div class="metric-title">Peak Performance</div>
                <div class="metric-value" style="color: #f39c12;">{peak_hour:02d}:00</div>
                <div class="metric-subtitle">
                    Peak Hour • £{peak_value:.0f} average
                    <span class="trend-indicator trend-up">Optimal</span>
                </div>
            </div>

            <div class="metric-card performance">
                <div class="metric-title">Forecast Accuracy</div>
                <div class="metric-value" style="color: #9b59b6;">{model_accuracy:.0f}%</div>
                <div class="metric-subtitle">
                    Model Performance • {"Excellent" if model_accuracy >= 90 else "Good"}
                    <span class="trend-indicator trend-up">{"Excellent" if model_accuracy >= 90 else "Good"}</span>
                </div>
            </div>

            <div class="metric-card weather">
                <div class="metric-title">Weather Impact</div>
                <div class="metric-value" style="color: #16a085;">{(temp_effect-1)*100:+.0f}%</div>
                <div class="metric-subtitle">
                    Multiplier: {temp_effect:.2f} • {current_temp:.1f}°C
                    <span class="trend-indicator trend-up">Good Conditions</span>
                </div>
            </div>

            <div class="metric-card staffing">
                <div class="metric-title">Staffing Outlook</div>
                <div class="metric-value" style="color: #e67e22;">On Target</div>
                <div class="metric-subtitle">
                    Staffing Levels • No changes recommended
                    <span class="trend-indicator trend-stable">Balanced</span>
                </div>
            </div>
        </div>

        <!-- 7-Day Forecast -->
        <div class="dashboard-section">
            <div class="section-title">📈 7-Day Revenue Forecast</div>
            <div class="forecast-grid">{forecast_html}
            </div>
        </div>

        <!-- Product Mix Analysis -->
        <div class="dashboard-section">
            <div class="section-title">🍰 Product Performance Analysis</div>
            <div class="product-mix">
                <div class="product-category">
                    <div class="category-name">Hot Drinks</div>
                    <div class="category-percentage">{hot_drinks_pct:.0f}%</div>
                    <div class="category-trend">Coffee, Tea, Hot Chocolate</div>
                </div>
                <div class="product-category">
                    <div class="category-name">Cold Drinks</div>
                    <div class="category-percentage">{cold_drinks_pct:.0f}%</div>
                    <div class="category-trend">Iced Coffee, Smoothies, Cold Brew</div>
                </div>
                <div class="product-category">
                    <div class="category-name">Food Items</div>
                    <div class="category-percentage">{food_pct:.0f}%</div>
                    <div class="category-trend">Sandwiches, Pastries, Snacks</div>
                </div>
            </div>
        </div>

        <!-- Business Insights -->
        <div class="dashboard-section">
            <div class="section-title">💡 Key Business Insights</div>
            <div class="insights-grid">
                <div class="insight-card">
                    <div class="insight-title">🌡️ Weather Impact</div>
                    <div class="insight-content">
                        Current temperature: <strong>{current_temp:.1f}°C</strong><br>
                        Weather multiplier: <strong>{temp_effect:.2f}x</strong><br>
                        {weather_insight}
                    </div>
                </div>
                <div class="insight-card">
                    <div class="insight-title">🎓 School Holiday Effect</div>
                    <div class="insight-content">
                        School holiday status: <strong>{holiday_status}</strong><br>
                        Impact multiplier: <strong>{school_effect:.2f}x</strong><br>
                        {holiday_insight}
                    </div>
                </div>
                <div class="insight-card">
                    <div class="insight-title">⏰ Peak Hours Optimization</div>
                    <div class="insight-content">
                        Primary peak: <strong>{peak_hour:02d}:00</strong> (£{peak_value:.0f} avg)<br>
                        Staff recommendation: <strong>4-5 staff members</strong><br>
                        Expect a strong lunch rush and post-lunch coffee orders.
                    </div>
                </div>
                <div class="insight-card">
                    <div class="insight-title">📊 Model Performance</div>
                    <div class="insight-content">
                        Forecast accuracy: <strong>{model_accuracy:.0f}%</strong><br>
                        Reliability: <strong>{"Excellent" if model_accuracy >= 90 else "Good"}</strong><br>
                        Current forecasts are {"highly" if model_accuracy >= 90 else "moderately"} reliable.
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer-info">
            <div>Dashboard powered by Elemental Insights Analytics</div>
            <div>Generated: {current_time} • Accuracy Rate: {model_accuracy:.0f}%</div>
        </div>

    </div>
</body>
</html>"""
    
    return html_content


def main():
    """Main function to generate dashboard"""
    
    print("🏗️  Cafe Dashboard Generator - Elemental Insights")
    print("=" * 50)
    
    # Sample data - replace with your actual data
    sample_data = {
        'today_forecast': 1350.75,
        'weekly_actual': 9200,
        'hot_drinks_pct': 42,
        'cold_drinks_pct': 23,
        'food_pct': 35,
        'avg_transaction': 8.75,
        'items_per_transaction': 2.4,
        'current_temp': 26.8,
        'temp_effect': 1.22,
        'school_effect': 1.15,
        'is_school_holiday': True,
        'peak_hour': 14,
        'peak_value': 178,
        'model_accuracy': 93
    }
    
    # You can also load data from CSV or JSON:
    # import pandas as pd
    # df = pd.read_csv('your_data.csv')
    # data = process_dataframe_to_dict(df)
    
    try:
        print("📊 Processing data...")
        
        # Generate the HTML
        html_content = generate_dashboard_html(sample_data)
        
        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'generated_dashboard_{timestamp}.html'
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Dashboard generated successfully!")
        print(f"📄 Saved as: {filename}")
        print(f"🌐 Open the file in your browser to view the dashboard")
        
        # Also save the data as JSON for reference
        json_filename = f'dashboard_data_{timestamp}.json'
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2)
        
        print(f"📊 Data saved as: {json_filename}")
        
    except Exception as e:
        print(f"❌ Error generating dashboard: {e}")


def load_data_from_csv(csv_file):
    """Helper function to load data from CSV file"""
    import pandas as pd
    
    try:
        df = pd.read_csv(csv_file)
        print(f"📁 Loaded {len(df)} rows from {csv_file}")
        
        # Extract metrics from DataFrame
        # Customize this based on your CSV structure
        latest_data = df.tail(24)  # Last 24 hours
        
        data = {
            'today_forecast': latest_data['forecast'].sum() if 'forecast' in df.columns else 1200,
            'weekly_actual': df.tail(24*7)['sales'].sum() if 'sales' in df.columns else 8500,
            'model_accuracy': 100 - abs(latest_data['error_pct'].mean()) if 'error_pct' in df.columns else 90,
            # Add more mappings based on your data structure
        }
        
        return data
        
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return None


if __name__ == "__main__":
    # Run the dashboard generator
    main()
    
    # Example of using CSV data:
    # csv_data = load_data_from_csv('your_cafe_data.csv')
    # if csv_data:
    #     html = generate_dashboard_html(csv_data)
    #     with open('csv_dashboard.html', 'w') as f:
    #         f.write(html)
