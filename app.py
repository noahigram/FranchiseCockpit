import streamlit as st

import random
from PIL import Image
import base64

# Import custom modules
from utils import (
    apply_custom_css, 
    display_business_dashboard, 
    display_metric_changes, 
    apply_scenario_consequences,
    INITIAL_METRICS, 
    FRANCHISE_SCENARIO_TOPICS
)
from scenarios import SCENARIO_DATABASE
from generator import generate_custom_scenario, generate_scenario_title, generate_simulation_analysis
from assets import (
    styled_metric, 
    styled_card, 
    styled_scenario_option, 
    generate_path_visual,
    generate_logo, 
    display_intro_animation
)

# Set the page configuration
st.set_page_config(
    page_title="Franchise Cockpit Simulator",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply the CSS
apply_custom_css()

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0

if 'scenario_history' not in st.session_state:
    st.session_state.scenario_history = []
    
if 'business_metrics' not in st.session_state:
    st.session_state.business_metrics = INITIAL_METRICS.copy()

if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None

if 'custom_scenarios' not in st.session_state:
    st.session_state.custom_scenarios = {}
    
if 'game_completed' not in st.session_state:
    st.session_state.game_completed = False

if 'show_intro' not in st.session_state:
    st.session_state.show_intro = True

# Add a new session state for topic selection
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = None

# Callback functions for topic selection
def select_topic(topic):
    st.session_state.selected_topic = topic
    
# Number of decisions before summary
MAX_DECISIONS = 5

def display_scenario_history():
    """Display the history of scenarios and choices made"""
    if st.session_state.scenario_history:
        with st.expander("Decision History", expanded=False):
            # Display path visualization
            path_visual = generate_path_visual(st.session_state.scenario_history)
            st.markdown(path_visual, unsafe_allow_html=True)
            
            # Display detailed history
            for i, scenario in enumerate(st.session_state.scenario_history):
                choice_type = "best_case" if scenario['choice'] == "Best Case" else "worst_case"
                
                # Use a container for each history item
                with st.container():
                    # Use success/error boxes based on choice type
                    if choice_type == "best_case":
                        st.success(f"**Step {i+1}: {scenario['topic']}**")
                    else:
                        st.error(f"**Step {i+1}: {scenario['topic']}**")
                    
                    st.markdown(f"**Decision:** {scenario['choice']} - {scenario['title']}")
                    st.markdown("**Impact:**")
                    
                    # Show impact with metrics
                    cols = st.columns(4)
                    for j, (metric, value) in enumerate(scenario['consequences'].items()):
                        formatted_metric = metric.replace("_", " ").title()
                        prefix = "$" if metric == "cash_flow" else ""
                        suffix = "%" if metric != "cash_flow" else ""
                        
                        with cols[j]:
                            if value > 0 and metric != "risk_level":
                                st.markdown(f"**{formatted_metric}**: ↑ {prefix}{abs(value)}{suffix}")
                            elif value < 0 and metric != "risk_level":
                                st.markdown(f"**{formatted_metric}**: ↓ {prefix}{abs(value)}{suffix}")
                            elif value > 0 and metric == "risk_level":
                                st.markdown(f"**{formatted_metric}**: ↑ {prefix}{abs(value)}{suffix}")
                            elif value < 0 and metric == "risk_level":
                                st.markdown(f"**{formatted_metric}**: ↓ {prefix}{abs(value)}{suffix}")
                            else:
                                st.markdown(f"**{formatted_metric}**: → {prefix}{abs(value)}{suffix}")
                    
                    # Add a separator between history items
                    if i < len(st.session_state.scenario_history) - 1:
                        st.markdown("---")

def reset_simulation():
    """Reset the simulation to the beginning"""
    st.session_state.step = 0
    st.session_state.scenario_history = []
    st.session_state.business_metrics = INITIAL_METRICS.copy()
    st.session_state.current_scenario = None
    st.session_state.custom_scenarios = {}
    st.session_state.game_completed = False
    st.session_state.selected_topic = None  # Ensure topic selection is also reset

def get_scenario_data(scenario_key):
    """Get the scenario data from either predefined or custom scenarios"""
    # Check if the scenario is in the predefined database
    if scenario_key in SCENARIO_DATABASE:
        return SCENARIO_DATABASE[scenario_key]
        
    # Check if we already have a generated version in custom_scenarios
    if scenario_key in st.session_state.custom_scenarios:
        return st.session_state.custom_scenarios[scenario_key]
    
    # Only use LLM for custom scenarios explicitly entered by the user
    custom_scenario = generate_custom_scenario(scenario_key)
    st.session_state.custom_scenarios[scenario_key] = custom_scenario
    return custom_scenario

def choose_scenario(topic, choice, title, consequences, next_scenarios):
    """Process the user's scenario choice and move to the next step"""
    # Record the choice
    st.session_state.scenario_history.append({
        'topic': topic,
        'choice': choice,
        'title': title,
        'consequences': consequences
    })
    
    # Apply consequences to metrics
    st.session_state.business_metrics = apply_scenario_consequences(consequences, st.session_state.business_metrics)
    
    # Check if we've reached the maximum number of decisions
    if len(st.session_state.scenario_history) >= MAX_DECISIONS:
        st.session_state.game_completed = True
        return
    
    # Set up next scenario
    if next_scenarios:
        # Filter next scenarios to only include ones from the predefined database
        valid_next_scenarios = [s for s in next_scenarios if s in SCENARIO_DATABASE]
        if valid_next_scenarios:
            st.session_state.current_scenario = random.choice(valid_next_scenarios)
        else:
            # Fallback to a random predefined scenario
            st.session_state.current_scenario = random.choice(list(SCENARIO_DATABASE.keys()))
    else:
        # Fallback to a random predefined scenario
        st.session_state.current_scenario = random.choice(list(SCENARIO_DATABASE.keys()))
    
    # Increment step
    st.session_state.step += 1

def display_summary():
    """Display a summary of the simulation results"""
    st.markdown("## Franchise Simulation Summary")
    
    # Display overall metrics with native Streamlit
    with st.container():
        st.subheader("Final Business Status")
        st.info("Your franchise journey has concluded. Here's how your business is performing after all your decisions:")
    
    display_business_dashboard(st.session_state.business_metrics)
    
    # Display path visualization - keep for now since it's SVG
    path_visual = generate_path_visual(st.session_state.scenario_history, width=800, height=200, text_color="#ffffff")
    st.markdown("### Your Decision Path", unsafe_allow_html=False)
    st.markdown(path_visual, unsafe_allow_html=True)
    
    # Generate and display AI analysis of decisions
    st.markdown("### Business Analysis")
    
    # Only generate analysis if we have a proper simulation history
    if len(st.session_state.scenario_history) > 0:
        with st.spinner("Generating business analysis..."):
            analysis = generate_simulation_analysis(
                st.session_state.scenario_history, 
                st.session_state.business_metrics
            )
        
        # Display analysis in a highlighted box
        st.markdown(f"""
        <div style="background-color: #2a3f5f; border-left: 5px solid #4e89ae; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
            <p style="color: #ffffff; font-size: 1rem; line-height: 1.5; margin: 0;">
                {analysis}
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No simulation data available for analysis.")
    
    # Display key insights
    st.markdown("### Key Decisions", unsafe_allow_html=False)
    
    for i, decision in enumerate(st.session_state.scenario_history):
        choice_type = "best_case" if decision['choice'] == "Best Case" else "worst_case"
        
        # Create a container for each decision
        with st.container():
            # Decision header
            st.markdown(f"#### Decision {i+1}: {decision['topic']}")
            
            # Use success/error boxes based on choice type
            if choice_type == "best_case":
                st.success(f"**Choice:** {decision['choice']} - {decision['title']}")
            else:
                st.error(f"**Choice:** {decision['choice']} - {decision['title']}")
            
            # Generate a summary of how this choice affected metrics
            consequences = decision['consequences']
            
            # Create human-friendly descriptions for the impact of each metric without redundant numbers
            # Cash flow impact descriptions
            if consequences['cash_flow'] >= 30000:
                cash_desc = "significantly boosted your finances"
            elif consequences['cash_flow'] >= 10000:
                cash_desc = "improved your cash position"
            elif consequences['cash_flow'] > 0:
                cash_desc = "slightly increased available funds"
            elif consequences['cash_flow'] <= -30000:
                cash_desc = "caused a major financial setback"
            elif consequences['cash_flow'] <= -10000:
                cash_desc = "created a notable financial strain"
            elif consequences['cash_flow'] < 0:
                cash_desc = "required a small financial investment"
            else:
                cash_desc = "had no financial impact"
            
            # Customer satisfaction impact
            if consequences['customer_satisfaction'] >= 15:
                satisfaction_desc = "delighted your customers"
            elif consequences['customer_satisfaction'] >= 5:
                satisfaction_desc = "made customers noticeably happier"
            elif consequences['customer_satisfaction'] > 0:
                satisfaction_desc = "slightly improved the customer experience"
            elif consequences['customer_satisfaction'] <= -15:
                satisfaction_desc = "seriously disappointed customers"
            elif consequences['customer_satisfaction'] <= -5:
                satisfaction_desc = "created some customer dissatisfaction"
            elif consequences['customer_satisfaction'] < 0:
                satisfaction_desc = "slightly upset some customers"
            else:
                satisfaction_desc = "kept customers at their current satisfaction level"
            
            # Growth potential impact
            if consequences['growth_potential'] >= 15:
                growth_desc = "created significant new growth opportunities"
            elif consequences['growth_potential'] >= 5:
                growth_desc = "opened up new growth avenues"
            elif consequences['growth_potential'] > 0:
                growth_desc = "slightly improved future prospects"
            elif consequences['growth_potential'] <= -15:
                growth_desc = "severely limited growth opportunities"
            elif consequences['growth_potential'] <= -5:
                growth_desc = "constrained some growth options"
            elif consequences['growth_potential'] < 0:
                growth_desc = "slightly narrowed future possibilities"
            else:
                growth_desc = "maintained current growth trajectory"
            
            # Risk level impact (note: for risk, increases are generally negative)
            if consequences['risk_level'] >= 15:
                risk_desc = "substantially increased business vulnerability"
            elif consequences['risk_level'] >= 5:
                risk_desc = "introduced new risk elements"
            elif consequences['risk_level'] > 0:
                risk_desc = "slightly raised exposure to risk"
            elif consequences['risk_level'] <= -15:
                risk_desc = "dramatically improved business security"
            elif consequences['risk_level'] <= -5:
                risk_desc = "improved business stability"
            elif consequences['risk_level'] < 0:
                risk_desc = "slightly reduced business vulnerability"
            else:
                risk_desc = "kept risk levels steady"
            
            # Combine into a natural-sounding summary
            summary = f"This decision {cash_desc}. It {satisfaction_desc}, {growth_desc}, and {risk_desc}."
            
            st.markdown(f"*{summary}*")
                
            # Add impact header
            st.markdown("**Impact:**")
            
            # Add metrics display
            cols = st.columns(4)
            for j, (metric, value) in enumerate(decision['consequences'].items()):
                formatted_metric = metric.replace("_", " ").title()
                prefix = "$" if metric == "cash_flow" else ""
                suffix = "%" if metric != "cash_flow" else ""
                
                with cols[j]:
                    if value > 0 and metric != "risk_level":
                        st.markdown(f"**{formatted_metric}**: ↑ {prefix}{abs(value)}{suffix}")
                    elif value < 0 and metric != "risk_level":
                        st.markdown(f"**{formatted_metric}**: ↓ {prefix}{abs(value)}{suffix}")
                    elif value > 0 and metric == "risk_level":
                        st.markdown(f"**{formatted_metric}**: ↑ {prefix}{abs(value)}{suffix}")
                    elif value < 0 and metric == "risk_level":
                        st.markdown(f"**{formatted_metric}**: ↓ {prefix}{abs(value)}{suffix}")
                    else:
                        st.markdown(f"**{formatted_metric}**: → {prefix}{abs(value)}{suffix}")
            
            # Add separator
            st.markdown("---")
    
    # Offer option to restart
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Start New Simulation", key="new_sim_btn"):
            # Reset all simulation data
            st.session_state.step = 0
            st.session_state.scenario_history = []
            st.session_state.business_metrics = INITIAL_METRICS.copy()
            st.session_state.current_scenario = None
            st.session_state.custom_scenarios = {}
            st.session_state.game_completed = False
            st.session_state.selected_topic = None
            st.rerun()

# Main App UI

# Show intro animation if it's the first visit
if st.session_state.show_intro:
    # Set page background and styling
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title section with native Streamlit components
    st.markdown("<h1 style='text-align: center; color: white; font-size: 3rem; margin-top: 2rem;'>Franchise Cockpit Simulator</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white; font-size: 1.5rem; margin-bottom: 2rem;'>Decision Simulator</h2>", unsafe_allow_html=True)
    
    # Description
    st.markdown("<p style='text-align: center; color: white; font-size: 1.1rem; max-width: 800px; margin: 0 auto 2rem auto;'>Explore the impact of different business decisions on your franchise's success. Navigate challenging scenarios and see how your choices affect key metrics like cash flow, customer satisfaction, growth potential, and risk level.</p>", unsafe_allow_html=True)
    
    # Feature cards using Streamlit columns
    st.markdown("<h3 style='text-align: center; color: white; margin-bottom: 1.5rem;'>Key Features</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 1rem; text-align: center; backdrop-filter: blur(5px); height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">💼</div>
            <h3 style="color: white; margin-bottom: 0.5rem;">Business Metrics</h3>
            <p style="color: white;">Track key performance indicators in real-time</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 1rem; text-align: center; backdrop-filter: blur(5px); height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔄</div>
            <h3 style="color: white; margin-bottom: 0.5rem;">Decision Paths</h3>
            <p style="color: white;">Explore different choices and outcomes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 1rem; text-align: center; backdrop-filter: blur(5px); height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
            <h3 style="color: white; margin-bottom: 0.5rem;">Visualize Impact</h3>
            <p style="color: white;">See how choices affect your franchise</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Start button with Streamlit's native button
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Custom styled button
        if st.button("START SIMULATION", key="start_sim_btn", use_container_width=True):
            st.session_state.show_intro = False
            st.rerun()
    
    st.stop()

# Main header
st.title("🏢 Franchise Cockpit Simulator")
st.markdown("### Explore the outcomes of different franchise decisions")

# Check if game is completed
if st.session_state.game_completed:
    display_summary()
    st.stop()

# Display the business dashboard
display_business_dashboard(st.session_state.business_metrics)

# Step 0: Topic Selection
if st.session_state.step == 0:
    st.markdown("<h2>Choose a Scenario Topic</h2>", unsafe_allow_html=True)
    
    # Replace HTML-based card with native Streamlit components
    with st.container():
        st.markdown("### Welcome to the Simulator!")
        st.info(
            """
            This simulator helps franchise owners and potential entrepreneurs explore different scenarios 
            and their impact on business outcomes.
            
            To begin, either select from one of our suggested scenario topics or create your own.
            """
        )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Option to enter custom topic
        custom_topic = st.text_input("Enter your own scenario topic:", placeholder="e.g., Hiring new staff")
        
        # Option to choose from predefined topics
        st.markdown("<p><strong>Or select from suggested topics:</strong></p>", unsafe_allow_html=True)
        
        # Display topics in a grid
        topic_cols = st.columns(3)
        
        # Display topics
        random_topics = random.sample(FRANCHISE_SCENARIO_TOPICS, min(6, len(FRANCHISE_SCENARIO_TOPICS)))
        
        for i, topic in enumerate(random_topics):
            with topic_cols[i % 3]:
                if st.button(f"📋 {topic}", key=f"topic_{topic}", on_click=select_topic, args=(topic,)):
                    pass  # Logic is handled in the callback
    
    with col2:
        # Replace HTML-based styled card with native Streamlit components
        st.markdown("#### Simulation Tips")
        with st.expander("Tips for better simulation results", expanded=True):
            st.markdown("- Each decision will affect your business metrics")
            st.markdown("- The simulation will run for 5 decisions")
            st.markdown("- There are no \"right\" or \"wrong\" choices")
            st.markdown("- Try different paths to see various outcomes")
            st.markdown("- Keep an eye on your cash flow - if it reaches zero, your franchise fails!")
    
    # Process topic selection
    if custom_topic:
        # If custom topic is entered, use it directly
        selected_topic = custom_topic
        
        # For custom topics, create a more formal title
        formatted_topic = custom_topic.strip().title()
        st.session_state.current_scenario = formatted_topic
        
        # Generate custom scenario data
        if formatted_topic not in st.session_state.custom_scenarios:
            custom_scenario = generate_custom_scenario(formatted_topic)
            st.session_state.custom_scenarios[formatted_topic] = custom_scenario
            
        st.session_state.step = 1
        st.rerun()
    elif st.session_state.selected_topic:
        # Process the selected topic from the session state
        if st.session_state.selected_topic in SCENARIO_DATABASE:
            st.session_state.current_scenario = st.session_state.selected_topic
        else:
            # Fallback to random predefined scenario
            st.session_state.current_scenario = random.choice(list(SCENARIO_DATABASE.keys()))
            
        # Reset selected topic to avoid processing it again
        st.session_state.selected_topic = None
        st.session_state.step = 1
        st.rerun()
    
    # Refresh options button
    if st.button("🔄 Show different topics", key="refresh_topics"):
        st.rerun()

# Step 1+: Scenario handling
elif st.session_state.step > 0:
    current_scenario_key = st.session_state.current_scenario
    scenario_data = get_scenario_data(current_scenario_key)
    
    if scenario_data:
        st.markdown(f"<h2>Scenario {st.session_state.step}: {current_scenario_key}</h2>", unsafe_allow_html=True)
        
        # Show progress
        progress_text = f"Decision {st.session_state.step} of {MAX_DECISIONS}"
        st.progress(st.session_state.step / MAX_DECISIONS, text=progress_text)
        
        # Display scenario description using native Streamlit components
        with st.container():
            st.subheader(current_scenario_key)
            st.markdown(scenario_data['description'])
        
        # Show decision options
        st.markdown("<h3>Choose Your Path</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Replace styled scenario option with native Streamlit components
            with st.container():
                st.markdown(f"#### ✅ {scenario_data['best_case']['title']}")
                st.success(scenario_data['best_case']['description'])
                
                # Show consequences
                st.markdown("**Impact:**")
                impact_cols = st.columns(4)
                for i, (metric, value) in enumerate(scenario_data['best_case']['consequences'].items()):
                    metric_name = metric.replace("_", " ").title()
                    prefix = "$" if metric == "cash_flow" else ""
                    suffix = "%" if metric != "cash_flow" else ""
                    
                    with impact_cols[i]:
                        if value > 0 and metric != "risk_level":
                            st.markdown(f"**{metric_name}**: ↑ {prefix}{abs(value)}{suffix}")
                        elif value < 0 and metric != "risk_level":
                            st.markdown(f"**{metric_name}**: ↓ {prefix}{abs(value)}{suffix}")
                        elif value > 0 and metric == "risk_level":
                            st.markdown(f"**{metric_name}**: ↑ {prefix}{abs(value)}{suffix}")
                        elif value < 0 and metric == "risk_level":
                            st.markdown(f"**{metric_name}**: ↓ {prefix}{abs(value)}{suffix}")
                        else:
                            st.markdown(f"**{metric_name}**: → {prefix}{abs(value)}{suffix}")
            
            if st.button("Choose Best Case", key="best_case_btn"):
                choose_scenario(
                    current_scenario_key,
                    "Best Case",
                    scenario_data['best_case']['title'],
                    scenario_data['best_case']['consequences'],
                    scenario_data['best_case']['next_scenarios']
                )
                st.rerun()
        
        with col2:
            # Replace styled scenario option with native Streamlit components
            with st.container():
                st.markdown(f"#### ⚠️ {scenario_data['worst_case']['title']}")
                st.error(scenario_data['worst_case']['description'])
                
                # Show consequences
                st.markdown("**Impact:**")
                impact_cols = st.columns(4)
                for i, (metric, value) in enumerate(scenario_data['worst_case']['consequences'].items()):
                    metric_name = metric.replace("_", " ").title()
                    prefix = "$" if metric == "cash_flow" else ""
                    suffix = "%" if metric != "cash_flow" else ""
                    
                    with impact_cols[i]:
                        if value > 0 and metric != "risk_level":
                            st.markdown(f"**{metric_name}**: ↑ {prefix}{abs(value)}{suffix}")
                        elif value < 0 and metric != "risk_level":
                            st.markdown(f"**{metric_name}**: ↓ {prefix}{abs(value)}{suffix}")
                        elif value > 0 and metric == "risk_level":
                            st.markdown(f"**{metric_name}**: ↑ {prefix}{abs(value)}{suffix}")
                        elif value < 0 and metric == "risk_level":
                            st.markdown(f"**{metric_name}**: ↓ {prefix}{abs(value)}{suffix}")
                        else:
                            st.markdown(f"**{metric_name}**: → {prefix}{abs(value)}{suffix}")
            
            if st.button("Choose Worst Case", key="worst_case_btn"):
                choose_scenario(
                    current_scenario_key,
                    "Worst Case",
                    scenario_data['worst_case']['title'],
                    scenario_data['worst_case']['consequences'],
                    scenario_data['worst_case']['next_scenarios']
                )
                st.rerun()
    
    # Display scenario history
    display_scenario_history()
    
    # Check if game over conditions are met
    if st.session_state.business_metrics['cash_flow'] <= 0:
        st.error("Game Over! Your franchise has run out of cash.")
        st.session_state.game_completed = True
        if st.button("Start New Simulation", key="new_sim_game_over_btn"):
            # Reset all simulation data
            st.session_state.step = 0
            st.session_state.scenario_history = []
            st.session_state.business_metrics = INITIAL_METRICS.copy()
            st.session_state.current_scenario = None
            st.session_state.custom_scenarios = {}
            st.session_state.game_completed = False
            st.session_state.selected_topic = None
            st.rerun()
    
    # Option to reset simulation
    if st.button("Reset Simulation", key="reset_sim_btn_main"):
        # Reset all simulation data
        st.session_state.step = 0
        st.session_state.scenario_history = []
        st.session_state.business_metrics = INITIAL_METRICS.copy()
        st.session_state.current_scenario = None
        st.session_state.custom_scenarios = {}
        st.session_state.game_completed = False
        st.session_state.selected_topic = None
        st.rerun()

# Footer
st.markdown("---")
st.markdown("<h3>About the Simulator</h3>", unsafe_allow_html=True)
st.markdown("This simulator is designed to help franchise owners and potential entrepreneurs understand the impact of different business decisions. The scenarios are based on common challenges faced in the franchising industry.")

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.markdown("### Current Step")
st.sidebar.markdown(f"Step {st.session_state.step} of {MAX_DECISIONS}")

if st.session_state.step > 0:
    st.sidebar.markdown("### Current Topic")
    st.sidebar.markdown(f"{st.session_state.current_scenario}")

st.sidebar.markdown("### Settings")
if st.sidebar.button("Reset Simulation", key="reset_sim_btn_sidebar"):
    # Reset all simulation data
    st.session_state.step = 0
    st.session_state.scenario_history = []
    st.session_state.business_metrics = INITIAL_METRICS.copy()
    st.session_state.current_scenario = None
    st.session_state.custom_scenarios = {}
    st.session_state.game_completed = False
    st.session_state.selected_topic = None
    st.rerun() 