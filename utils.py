import streamlit as st
import random

# Import assets for visualization
try:
    from assets import styled_metric, styled_card
except ImportError:
    # Fallback if assets module is not available
    pass

# Sample business metrics to track
INITIAL_METRICS = {
    'cash_flow': 100000,
    'customer_satisfaction': 50,
    'growth_potential': 50,
    'risk_level': 30
}

# Sample franchise scenario topics
FRANCHISE_SCENARIO_TOPICS = [
    "Location Selection",
    "Hiring First Manager",
    "Marketing Campaign Launch",
    "Supply Chain Disruption",
    "Competitor Opening Nearby",
    "Customer Complaint Handling",
    "Expansion Opportunity",
    "Regulatory Changes",
    "Technology Upgrade",
    "Economic Downturn",
    "Customer Loyalty Program",
    "Staff Training Initiative",
    "Quality Control Issues",
    "Community Relations Event",
    "Lease Renewal Negotiation"
]

# Helper functions for metrics and simulation
def apply_scenario_consequences(consequences, metrics):
    """Apply the consequences of a scenario to the business metrics"""
    updated_metrics = metrics.copy()
    
    for metric, value in consequences.items():
        updated_metrics[metric] += value
        
        # Ensure metrics stay within reasonable bounds
        if metric != 'cash_flow':
            updated_metrics[metric] = max(0, min(100, updated_metrics[metric]))
    
    return updated_metrics

def calculate_business_health(metrics):
    """Calculate an overall business health score based on metrics"""
    # Simple weighted average of metrics
    health_score = (
        (0.4 * min(metrics['cash_flow'] / 100000, 1)) + 
        (0.3 * (metrics['customer_satisfaction'] / 100)) + 
        (0.2 * (metrics['growth_potential'] / 100)) - 
        (0.1 * (metrics['risk_level'] / 100))
    )
    
    # Normalize to 0-100 scale
    health_score = max(0, min(1, health_score)) * 100
    
    return round(health_score)

def get_business_status(health_score):
    """Get a business status description based on health score"""
    if health_score >= 80:
        return "Thriving", "Your franchise is in excellent condition with strong financials and growth."
    elif health_score >= 60:
        return "Stable", "Your franchise is performing well with good prospects."
    elif health_score >= 40:
        return "Challenged", "Your franchise faces some challenges but remains viable."
    elif health_score >= 20:
        return "Struggling", "Your franchise is experiencing significant difficulties and needs attention."
    else:
        return "Critical", "Your franchise is in critical condition and at risk of failure."

def generate_random_scenario():
    """Generate a random scenario topic"""
    return random.choice(FRANCHISE_SCENARIO_TOPICS)

# Apply custom CSS for better UI
def apply_custom_css():
    st.markdown("""
    <style>
    .main {
        background-color: #1e1e1e;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton button {
        background-color: #4e89ae;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #43658b;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .best-case {
        background-color: rgba(40, 167, 69, 0.2);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 5px solid #28a745;
    }
    .worst-case {
        background-color: rgba(220, 53, 69, 0.2);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 5px solid #dc3545;
    }
    .scenario-card {
        background-color: #2d2d2d;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metrics-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    h1, h2, h3 {
        color: #4e89ae;
    }
    .stProgress > div > div {
        background-color: #4e89ae;
    }
    .status-thriving {
        color: #28a745;
        font-weight: bold;
    }
    .status-stable {
        color: #17a2b8;
        font-weight: bold;
    }
    .status-challenged {
        color: #ffc107;
        font-weight: bold;
    }
    .status-struggling {
        color: #fd7e14;
        font-weight: bold;
    }
    .status-critical {
        color: #dc3545;
        font-weight: bold;
    }
    .business-health-container {
        background-color: #2d2d2d;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        text-align: center;
    }
    .decision-history {
        max-height: 300px;
        overflow-y: auto;
    }
    .metrics-box {
        border: 2px solid #4e89ae;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to display visually appealing metric changes
def display_metric_changes(consequences):
    """Display changes to metrics with visual indicators"""
    cols = st.columns(4)
    metrics = ['cash_flow', 'customer_satisfaction', 'growth_potential', 'risk_level']
    icons = {'increase': '↑', 'decrease': '↓', 'neutral': '↔'}
    
    for i, metric in enumerate(metrics):
        value = consequences[metric]
        with cols[i]:
            if value > 0 and metric != 'risk_level':
                st.markdown(f"<div style='color:#4CAF50'><b>{metric.replace('_', ' ').title()}</b>: {icons['increase']} ${abs(value):,}</div>", unsafe_allow_html=True)
            elif value < 0 and metric != 'risk_level':
                st.markdown(f"<div style='color:#FF5252'><b>{metric.replace('_', ' ').title()}</b>: {icons['decrease']} ${abs(value):,}</div>", unsafe_allow_html=True)
            elif value == 0 and metric != 'risk_level':
                st.markdown(f"<div style='color:#e1e1e1'><b>{metric.replace('_', ' ').title()}</b>: {icons['neutral']} ${abs(value):,}</div>", unsafe_allow_html=True)
            elif value > 0 and metric == 'risk_level':
                st.markdown(f"<div style='color:#FF5252'><b>{metric.replace('_', ' ').title()}</b>: {icons['increase']} {abs(value)}%</div>", unsafe_allow_html=True)
            elif value < 0 and metric == 'risk_level':
                st.markdown(f"<div style='color:#4CAF50'><b>{metric.replace('_', ' ').title()}</b>: {icons['decrease']} {abs(value)}%</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color:#e1e1e1'><b>{metric.replace('_', ' ').title()}</b>: {icons['neutral']} {abs(value)}%</div>", unsafe_allow_html=True)

# Function to display the business metrics dashboard
def display_business_dashboard(metrics):
    """Display the current business metrics in a visually appealing dashboard"""
    st.subheader("Franchise Business Dashboard")
    
    # Calculate business health
    health_score = calculate_business_health(metrics)
    status, description = get_business_status(health_score)
    
    # Create a business health box using Streamlit components
    with st.container():
        st.markdown("---")
        st.markdown("#### Business Health")
        
        # Add colored box based on status
        color_map = {
            "Thriving": "#28a745",  # Green
            "Stable": "#17a2b8",    # Blue
            "Challenged": "#ffc107", # Yellow
            "Struggling": "#fd7e14", # Orange
            "Critical": "#dc3545"    # Red
        }
        status_color = color_map.get(status, "#6c757d")  # Default to gray
        
        # Display health score with color
        st.markdown(f"""
        <div style='padding: 1rem; border: 2px solid {status_color}; border-radius: 0.5rem; margin-bottom: 1rem; background-color: rgba(45, 45, 45, 0.7);'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                <span style='font-weight: bold; color: #ffffff;'>Health Score: <span style='color: {status_color};'>{health_score}%</span></span>
                <span style='font-weight: bold; color: #ffffff;'>Status: <span style='color: {status_color};'>{status}</span></span>
            </div>
            <div style='font-style: italic; color: #e1e1e1;'>{description}</div>
            <div style='background-color: #333333; height: 0.5rem; border-radius: 0.25rem; margin-top: 0.5rem;'>
                <div style='background-color: {status_color}; width: {health_score}%; height: 100%; border-radius: 0.25rem;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create metrics in columns with outline
    with st.container():
        st.markdown("#### Key Metrics")
        
        # Create four columns for metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Cash Flow", 
                f"${metrics['cash_flow']:,}",
                delta=None
            )
        
        with col2:
            st.metric(
                "Customer Satisfaction", 
                f"{metrics['customer_satisfaction']}%",
                delta=None
            )
            st.progress(metrics['customer_satisfaction']/100)
        
        with col3:
            st.metric(
                "Growth Potential", 
                f"{metrics['growth_potential']}%",
                delta=None
            )
            st.progress(metrics['growth_potential']/100)
        
        with col4:
            st.metric(
                "Risk Level", 
                f"{metrics['risk_level']}%",
                delta=None
            )
            st.progress(metrics['risk_level']/100) 