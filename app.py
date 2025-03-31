import streamlit as st
import random


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
from generator import generate_scenario, generate_simulation_analysis, generate_scenario_topics, generate_random_business_profile
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

if 'business_profile' not in st.session_state:
    st.session_state.business_profile = None

if 'scenario_topics' not in st.session_state:
    st.session_state.scenario_topics = []

if 'current_impact_multipliers' not in st.session_state:
    st.session_state.current_impact_multipliers = {
        'cash_flow': 1.0,
        'customer_satisfaction': 1.0,
        'growth_potential': 1.0,
        'risk_level': 1.0
    }

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
    st.session_state.business_profile = None
    st.session_state.scenario_topics = []
    st.session_state.current_impact_multipliers = {
        'cash_flow': 1.0,
        'customer_satisfaction': 1.0,
        'growth_potential': 1.0,
        'risk_level': 1.0
    }

def get_scenario_data(scenario_key):
    """Get the scenario data from either predefined or custom scenarios"""
    # Check if the scenario is in the predefined database
    if scenario_key in SCENARIO_DATABASE:
        return SCENARIO_DATABASE[scenario_key]
        
    # Check if we already have a generated version in custom_scenarios
    if scenario_key in st.session_state.custom_scenarios:
        return st.session_state.custom_scenarios[scenario_key]
    
    # Only use LLM for custom scenarios explicitly entered by the user
    custom_scenario = generate_scenario(scenario_key, st.session_state.business_profile)
    st.session_state.custom_scenarios[scenario_key] = custom_scenario
    return custom_scenario

def choose_scenario(topic, choice, title, consequences, next_scenarios):
    """Process the user's scenario choice and move to the next step"""
    # Apply impact multipliers to consequences
    adjusted_consequences = {
        metric: int(value * st.session_state.current_impact_multipliers[metric])
        for metric, value in consequences.items()
    }
    
    # Record the choice
    st.session_state.scenario_history.append({
        'topic': topic,
        'choice': choice,
        'title': title,
        'consequences': adjusted_consequences
    })
    
    # Apply consequences to metrics
    st.session_state.business_metrics = apply_scenario_consequences(adjusted_consequences, st.session_state.business_metrics)
    
    # Check if we've reached the maximum number of decisions
    if len(st.session_state.scenario_history) >= MAX_DECISIONS:
        st.session_state.game_completed = True
        return
    
    # Set up next scenario
    if next_scenarios:
        st.session_state.current_scenario = random.choice(next_scenarios)
    else:
        # Generate a new scenario based on the business profile
        st.session_state.current_scenario = generate_scenario(st.session_state.business_profile)
    
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
    
    # Display path visualization
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
                st.session_state.business_metrics,
                st.session_state.business_profile
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
            
            # Create human-friendly descriptions for the impact of each metric
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
            
            # Risk level impact
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
            reset_simulation()
            st.rerun()

# Main App UI

# Show intro animation if it's the first visit
if st.session_state.show_intro:
    # Set page with native Streamlit styling
    
    # Title section with native Streamlit components
    st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-top: 2rem;'>Franchise Cockpit Simulator</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-size: 1.5rem; margin-bottom: 2rem;'>Dynamic Decision Simulator</h2>", unsafe_allow_html=True)
    
    # Description
    st.markdown("<p style='text-align: center; font-size: 1.1rem; max-width: 800px; margin: 0 auto 2rem auto;'>Explore the impact of different business decisions on your franchise's success. Enter your business profile to generate personalized scenarios and see how your choices affect key metrics.</p>", unsafe_allow_html=True)
    
    # Feature cards using Streamlit columns
    st.markdown("<h3 style='text-align: center; margin-bottom: 1.5rem;'>Key Features</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: rgba(240, 242, 246, 0.8); padding: 1.5rem; border-radius: 1rem; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">💼</div>
            <h3 style="margin-bottom: 0.5rem; color: #2c3e50;">Business Profile</h3>
            <p style="color: #34495e;">Create your unique business profile for personalized scenarios</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: rgba(240, 242, 246, 0.8); padding: 1.5rem; border-radius: 1rem; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔄</div>
            <h3 style="margin-bottom: 0.5rem; color: #2c3e50;">Dynamic Scenarios</h3>
            <p style="color: #34495e;">Generate unique scenarios based on your business context</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: rgba(240, 242, 246, 0.8); padding: 1.5rem; border-radius: 1rem; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
            <h3 style="margin-bottom: 0.5rem; color: #2c3e50;">Impact Control</h3>
            <p style="color: #34495e;">Adjust the impact of decisions on key metrics</p>
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

# Main header - only show on start page
if st.session_state.show_intro:
    st.title("🏢 Franchise Cockpit Simulator")
    st.markdown("### Explore the outcomes of different franchise decisions")
else:
    # Move header to sidebar
    st.sidebar.title("🏢 Franchise Cockpit Simulator")
    st.sidebar.markdown("### Explore the outcomes of different franchise decisions")
    st.sidebar.markdown("---")  # Add a separator after the header

# Check if game is completed
if st.session_state.game_completed:
    display_summary()
    st.stop()

# Step 0: Business Profile Input
if st.session_state.step == 0:
    st.markdown("<h2>Create Your Business Profile</h2>", unsafe_allow_html=True)
    
    # Replace HTML-based card with native Streamlit components
    with st.container():
        st.markdown("### Welcome to the Simulator!")
        st.info(
            """
            This simulator helps franchise owners and potential entrepreneurs explore different scenarios 
            and their impact on business outcomes.
            
            To begin, please provide details about your business to generate personalized scenarios.
            """
        )
    
    # Business profile input
    with st.form("business_profile_form"):
        business_profile = st.text_area(
            "Describe your business:",
            value=st.session_state.business_profile if st.session_state.business_profile else "",
            placeholder="Include details about your industry, size, location, target market, and any specific challenges or opportunities you're facing.",
            height=200
        )
        
        # Option to upload relevant documents
        uploaded_files = st.file_uploader(
            "Upload relevant business documents (optional):",
            type=['txt', 'pdf', 'doc', 'docx'],
            accept_multiple_files=True
        )
        
        # Option to enter custom topic
        custom_topic = st.text_input(
            "Enter a specific scenario topic (optional):",
            placeholder="e.g., Hiring new staff, Marketing campaign, etc."
        )
        
        # Create two columns for the buttons
        col1, col2 = st.columns([3, 1])
        
        with col1:
            submitted = st.form_submit_button("Generate Scenarios")
            if submitted and business_profile:
                with st.spinner("Generating personalized scenarios..."):
                    # Generate scenario topics based on business profile
                    st.session_state.scenario_topics = generate_scenario_topics(
                        business_profile,
                        uploaded_files,
                        custom_topic
                    )
                    
                    if st.session_state.scenario_topics:
                        st.session_state.business_profile = business_profile
                        st.session_state.step = 0.5  # Use intermediate step for topic selection
                        st.rerun()
                    else:
                        st.error("Failed to generate scenarios. Please try again with more detailed business information.")
        
        with col2:
            if st.form_submit_button("Generate Random Profile"):
                with st.spinner("Generating a random business profile..."):
                    random_profile = generate_random_business_profile()
                    st.session_state.business_profile = random_profile
                    st.rerun()
    
    # Display example business profile
    with st.expander("Example Business Profile", expanded=False):
        st.markdown("""
        **Industry:** Fast-casual restaurant franchise
        
        **Location:** Downtown area of a mid-sized city
        
        **Size:** 2,500 square feet with 30 seats
        
        **Target Market:** Young professionals and families
        
        **Current Challenges:**
        - High employee turnover
        - Increasing competition from new restaurants
        - Need to modernize ordering system
        
        **Opportunities:**
        - Growing lunch crowd from nearby office buildings
        - Potential for delivery service expansion
        - Interest in healthy menu options
        
        **Goals:**
        - Improve customer satisfaction
        - Reduce operational costs
        - Increase market share
        """)

# Step 0.5: Topic Selection (intermediate step)
elif st.session_state.step == 0.5:
    st.markdown("<h2>Select a Scenario Topic</h2>", unsafe_allow_html=True)
    
    st.info(
        """
        Based on your business profile, we've generated the following scenario topics.
        Select one to begin your simulation journey.
        """
    )
    
    # Display the generated scenario topics as clickable cards
    st.markdown("### Available Scenarios")
    
    # Create rows of 3 topics each
    for i in range(0, len(st.session_state.scenario_topics), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(st.session_state.scenario_topics):
                topic = st.session_state.scenario_topics[i + j]
                with cols[j]:
                    # Use a more contrasting background with clear text styling
                    st.markdown(f"""
                    <div style="background-color: #2c3e50; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; min-height: 80px; color: white; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        <h4 style="margin-top: 0; margin-bottom: 0.5rem; color: white;">{topic}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Select", key=f"select_{i}_{j}"):
                        st.session_state.current_scenario = topic
                        st.session_state.step = 1
                        st.rerun()
    
    # Option to add a custom topic
    st.markdown("### Or Enter Your Own Topic")
    custom_topic_col1, custom_topic_col2 = st.columns([3, 1])
    with custom_topic_col1:
        user_custom_topic = st.text_input("Custom topic:", placeholder="Enter your own scenario topic")
    with custom_topic_col2:
        if st.button("Add Topic", disabled=not user_custom_topic):
            st.session_state.current_scenario = user_custom_topic
            st.session_state.step = 1
            st.rerun()
            
    # Option to regenerate topics
    if st.button("Regenerate Topics"):
        with st.spinner("Generating new scenario topics..."):
            st.session_state.scenario_topics = generate_scenario_topics(
                st.session_state.business_profile,
                None,  # No files for regeneration
                None   # No custom topic for regeneration
            )
            st.rerun()

# Step 1+: Scenario handling
elif st.session_state.step > 0:
    current_scenario_key = st.session_state.current_scenario
    
    # Cache the scenario data in session state to avoid API calls when adjusting sliders
    if 'current_scenario_data' not in st.session_state or st.session_state.current_scenario_data_key != current_scenario_key:
        with st.spinner("Generating scenario..."):
            scenario_data = generate_scenario(current_scenario_key, st.session_state.business_profile)
            st.session_state.current_scenario_data = scenario_data
            st.session_state.current_scenario_data_key = current_scenario_key
            
            # Save the original consequences to session state
            if 'original_best_consequences' not in st.session_state:
                st.session_state.original_best_consequences = {}
            if 'original_worst_consequences' not in st.session_state:
                st.session_state.original_worst_consequences = {}
                
            st.session_state.original_best_consequences = scenario_data['best_case']['consequences'].copy()
            st.session_state.original_worst_consequences = scenario_data['worst_case']['consequences'].copy()
    else:
        scenario_data = st.session_state.current_scenario_data
        
        # Update the consequences based on the current multipliers
        for metric, value in st.session_state.original_best_consequences.items():
            scenario_data['best_case']['consequences'][metric] = int(value * st.session_state.current_impact_multipliers[metric])
            
        for metric, value in st.session_state.original_worst_consequences.items():
            scenario_data['worst_case']['consequences'][metric] = int(value * st.session_state.current_impact_multipliers[metric])
    
    if scenario_data:
        # Show progress
        progress_text = f"Decision {st.session_state.step} of {MAX_DECISIONS}"
        st.progress(st.session_state.step / MAX_DECISIONS, text=progress_text)
        
        # 1. FIRST: Display business health dashboard
        display_business_dashboard(st.session_state.business_metrics)
        
        # 2. SECOND: Display scenario description and options
        st.markdown(f"<h2>Scenario {st.session_state.step}: {current_scenario_key}</h2>", unsafe_allow_html=True)
        
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
                # Clear the cached scenario data to force a new API call for the next scenario
                if 'current_scenario_data' in st.session_state:
                    del st.session_state.current_scenario_data
                    del st.session_state.current_scenario_data_key
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
                # Clear the cached scenario data to force a new API call for the next scenario
                if 'current_scenario_data' in st.session_state:
                    del st.session_state.current_scenario_data
                    del st.session_state.current_scenario_data_key
                st.rerun()
                
        # 3. THIRD: Add impact multiplier sliders
        st.markdown("---")
        st.markdown("<h4 style='font-size: 1.2em; margin-bottom: 0.5em;'>Adjust Impact Multipliers</h4>", unsafe_allow_html=True)
        st.info("Use the sliders below to adjust how much each decision affects different aspects of your business.")
        
        col1, col2 = st.columns(2)
        with col1:
            # Larger label with custom styling
            st.markdown("<div style='font-size: 1.1em; font-weight: 500; margin-bottom: 0.2em;'>Cash Flow Impact</div>", unsafe_allow_html=True)
            # Smaller slider
            new_cash_flow = st.slider(
                "##",  # Hide the actual label
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.current_impact_multipliers['cash_flow'],
                step=0.1,
                key="cash_flow_slider"
            )
            if new_cash_flow != st.session_state.current_impact_multipliers['cash_flow']:
                st.session_state.current_impact_multipliers['cash_flow'] = new_cash_flow
                st.rerun()
            
            # Larger label with custom styling
            st.markdown("<div style='font-size: 1.1em; font-weight: 500; margin-bottom: 0.2em; margin-top: 1em;'>Customer Satisfaction Impact</div>", unsafe_allow_html=True)
            # Smaller slider
            new_cust_sat = st.slider(
                "##",  # Hide the actual label
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.current_impact_multipliers['customer_satisfaction'],
                step=0.1,
                key="customer_satisfaction_slider"
            )
            if new_cust_sat != st.session_state.current_impact_multipliers['customer_satisfaction']:
                st.session_state.current_impact_multipliers['customer_satisfaction'] = new_cust_sat
                st.rerun()
        with col2:
            # Larger label with custom styling
            st.markdown("<div style='font-size: 1.1em; font-weight: 500; margin-bottom: 0.2em;'>Growth Potential Impact</div>", unsafe_allow_html=True)
            # Smaller slider
            new_growth = st.slider(
                "##",  # Hide the actual label
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.current_impact_multipliers['growth_potential'],
                step=0.1,
                key="growth_potential_slider"
            )
            if new_growth != st.session_state.current_impact_multipliers['growth_potential']:
                st.session_state.current_impact_multipliers['growth_potential'] = new_growth
                st.rerun()
            
            # Larger label with custom styling
            st.markdown("<div style='font-size: 1.1em; font-weight: 500; margin-bottom: 0.2em; margin-top: 1em;'>Risk Level Impact</div>", unsafe_allow_html=True)
            # Smaller slider
            new_risk = st.slider(
                "##",  # Hide the actual label
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.current_impact_multipliers['risk_level'],
                step=0.1,
                key="risk_level_slider"
            )
            if new_risk != st.session_state.current_impact_multipliers['risk_level']:
                st.session_state.current_impact_multipliers['risk_level'] = new_risk
                st.rerun()
    
    # Display scenario history
    display_scenario_history()
    
    # Check if game over conditions are met
    if st.session_state.business_metrics['cash_flow'] <= 0:
        st.error("Game Over! Your franchise has run out of cash.")
        st.session_state.game_completed = True
        if st.button("Start New Simulation", key="new_sim_game_over_btn"):
            reset_simulation()
            st.rerun()
    
    # Option to reset simulation
    if st.button("Reset Simulation", key="reset_sim_btn_main"):
        reset_simulation()
        st.rerun()

# Footer
st.markdown("---")
st.markdown("<h3>About the Simulator</h3>", unsafe_allow_html=True)
st.markdown("This simulator is designed to help franchise owners and potential entrepreneurs understand the impact of different business decisions. The scenarios are generated based on your business profile and can be customized to match your specific situation.")

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.markdown("### Current Step")
st.sidebar.markdown(f"Step {st.session_state.step} of {MAX_DECISIONS}")

if st.session_state.step > 0:
    st.sidebar.markdown("### Current Topic")
    st.sidebar.markdown(f"{st.session_state.current_scenario}")

st.sidebar.markdown("### Settings")
if st.sidebar.button("Reset Simulation", key="reset_sim_btn_sidebar"):
    reset_simulation()
    st.rerun() 