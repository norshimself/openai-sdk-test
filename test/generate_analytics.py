import json
import random
from datetime import datetime, timedelta

def generate_random_analytics_data(days=30):
    start_date = datetime.now() - timedelta(days=days)
    
    # Static catalog of resources
    pages = [
        "/home",
        "/pricing",
        "/features",
        "/about",
        "/blog/introducing-our-new-api",
        "/docs/getting-started",
        "/contact",
        "/checkout",
        "/signup"
    ]
    
    sources = ["organic_search", "direct", "referral", "social_media", "newsletter"]
    devices = ["desktop", "mobile", "tablet"]
    countries = ["US", "GB", "DE", "CA", "FR", "AU", "JP", "IN", "BR", "ZA"]
    
    daily_metrics = []
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Introduce a weekly trend (higher traffic on weekdays, lower on weekends)
        is_weekend = current_date.weekday() in [5, 6]
        base_visitors = random.randint(1200, 1800) if not is_weekend else random.randint(700, 1100)
        
        # Add random fluctuations
        visitors = int(base_visitors * random.uniform(0.9, 1.1))
        pageviews = int(visitors * random.uniform(2.1, 3.2))
        bounce_rate = round(random.uniform(0.35, 0.55), 4)
        avg_session_duration = round(random.uniform(120.0, 240.0), 2)  # in seconds
        conversions = int(visitors * random.uniform(0.015, 0.045))  # conversion rate between 1.5% and 4.5%
        
        # Distribution breakdown for the day
        traffic_sources_distribution = {}
        remaining_pct = 1.0
        for idx, src in enumerate(sources):
            if idx == len(sources) - 1:
                pct = remaining_pct
            else:
                pct = round(random.uniform(0.05, remaining_pct - (len(sources) - idx - 1) * 0.05), 3)
                remaining_pct -= pct
            traffic_sources_distribution[src] = int(visitors * pct)
            
        device_distribution = {}
        remaining_pct = 1.0
        for idx, dev in enumerate(devices):
            if idx == len(devices) - 1:
                pct = remaining_pct
            else:
                pct = round(random.uniform(0.1, remaining_pct - (len(devices) - idx - 1) * 0.1), 3)
                remaining_pct -= pct
            device_distribution[dev] = int(visitors * pct)
            
        daily_metrics.append({
            "date": date_str,
            "visitors": visitors,
            "pageviews": pageviews,
            "bounce_rate": bounce_rate,
            "avg_session_duration_seconds": avg_session_duration,
            "conversions": conversions,
            "traffic_sources": traffic_sources_distribution,
            "devices": device_distribution
        })
        
    # Aggregate top pages across the entire period
    page_stats = []
    for page in pages:
        total_views = random.randint(5000, 50000) if page == "/home" else random.randint(1000, 15000)
        avg_time = round(random.uniform(30, 300), 1)
        exit_rate = round(random.uniform(0.2, 0.6), 4)
        page_stats.append({
            "path": page,
            "views": total_views,
            "avg_time_on_page_seconds": avg_time,
            "exit_rate": exit_rate
        })
    page_stats.sort(key=lambda x: x["views"], reverse=True)
    
    # Aggregate country stats
    country_stats = {}
    for country in countries:
        country_stats[country] = {
            "visitors": random.randint(2000, 15000),
            "conversions": random.randint(50, 600)
        }
    
    analytics_data = {
        "metadata": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "timeframe_days": days,
            "period_start": start_date.strftime("%Y-%m-%d"),
            "period_end": (start_date + timedelta(days=days-1)).strftime("%Y-%m-%d")
        },
        "summary": {
            "total_visitors": sum(d["visitors"] for d in daily_metrics),
            "total_pageviews": sum(d["pageviews"] for d in daily_metrics),
            "total_conversions": sum(d["conversions"] for d in daily_metrics),
            "average_bounce_rate": round(sum(d["bounce_rate"] for d in daily_metrics) / len(daily_metrics), 4),
            "average_session_duration_seconds": round(sum(d["avg_session_duration_seconds"] for d in daily_metrics) / len(daily_metrics), 2)
        },
        "daily_metrics": daily_metrics,
        "top_pages": page_stats,
        "demographics": {
            "countries": country_stats
        }
    }
    
    return analytics_data

if __name__ == "__main__":
    data = generate_random_analytics_data(days=30)
    output_filename = "analytics_data.json"
    with open(output_filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Successfully generated random analytics data and saved to {output_filename}")
