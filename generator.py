import random
import anthropic
import streamlit as st
from scenarios import SCENARIO_DATABASE

# Lists of scenario components for random generation
BUSINESS_ASPECTS = [
    "finance",
    "marketing",
    "operations",
    "customer service",
    "staff management",
    "supply chain",
    "technology",
    "location",
    "regulations",
    "competition"
]

BEST_CASE_INVESTMENTS = [
    "Hire a specialized consultant",
    "Implement a cutting-edge solution",
    "Invest in premium resources",
    "Develop a comprehensive strategy",
    "Engage industry experts",
    "Launch an innovative approach",
    "Acquire top-tier assets",
    "Deploy high-end technology",
    "Orchestrate a strategic overhaul",
    "Establish a best-in-class system"
]

WORST_CASE_APPROACHES = [
    "Handle it internally",
    "Use a minimal approach",
    "Implement a basic solution",
    "Delegate to existing staff",
    "Apply a low-cost alternative",
    "Take a conservative approach",
    "Wait and see before acting",
    "Make incremental changes",
    "Use existing resources",
    "Find a temporary workaround"
]

BUSINESS_IMPACT_DESCRIPTIONS = [
    "This will have significant implications for your franchise's future.",
    "Your decision could substantially affect your franchise's performance.",
    "This choice will shape your business trajectory for years to come.",
    "The path you choose will determine your competitive positioning.",
    "Your approach to this challenge will define your market presence.",
    "The way you handle this situation will impact customer perception.",
    "Your strategy here will influence operational efficiency long-term.",
    "This decision point represents a pivotal moment for your franchise.",
    "How you address this issue will affect your brand reputation.",
    "The direction you take now will influence your financial stability."
]

def generate_custom_scenario(topic):
    """Generate a custom scenario based on a user-provided topic using Claude"""
    
    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    # Create a prompt for Claude
    prompt = f"""You are a business scenario generator for a franchise management simulator. Create a concise scenario based on the topic: {topic}

The scenario should follow this exact JSON structure:
{{
    "description": "A brief description of the situation (1-2 sentences)",
    "best_case": {{
        "title": "A short title for the best case option (3-5 words)",
        "description": "Brief description of the best case approach (1-2 sentences)",
        "consequences": {{
            "cash_flow": <integer between -100000 and 50000>,
            "customer_satisfaction": <integer between -25 and 25>,
            "growth_potential": <integer between -25 and 25>,
            "risk_level": <integer between -25 and 25>
        }},
        "next_scenarios": ["<scenario1>", "<scenario2>"]
    }},
    "worst_case": {{
        "title": "A short title for the worst case option (3-5 words)",
        "description": "Brief description of the worst case approach (1-2 sentences)",
        "consequences": {{
            "cash_flow": <integer between -100000 and 50000>,
            "customer_satisfaction": <integer between -25 and 25>,
            "growth_potential": <integer between -25 and 25>,
            "risk_level": <integer between -25 and 25>
        }},
        "next_scenarios": ["<scenario1>", "<scenario2>"]
    }}
}}

Guidelines:
1. Keep all descriptions extremely concise - no more than 1-2 sentences
2. Make the scenario realistic and business-focused
3. Best case should be ambitious but achievable
4. Worst case should be conservative but not disastrous
5. Consequences should be balanced and make sense for the situation
6. Next scenarios should be relevant to the current scenario
7. Use existing scenario names from the database for next_scenarios
8. Ensure all numeric values are integers

Available next scenarios: {list(SCENARIO_DATABASE.keys())}

Generate a scenario that follows this structure exactly."""

    try:
        # Get response from Claude
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=800,  # Reduced token count for shorter responses
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Parse the response as JSON
        import json
        custom_scenario = json.loads(response.content[0].text)
        
        # Validate the structure and values
        if not all(key in custom_scenario for key in ["description", "best_case", "worst_case"]):
            raise ValueError("Missing required keys in scenario structure")
            
        if not all(key in custom_scenario["best_case"] for key in ["title", "description", "consequences", "next_scenarios"]):
            raise ValueError("Missing required keys in best_case structure")
            
        if not all(key in custom_scenario["worst_case"] for key in ["title", "description", "consequences", "next_scenarios"]):
            raise ValueError("Missing required keys in worst_case structure")
            
        if not all(key in custom_scenario["best_case"]["consequences"] for key in ["cash_flow", "customer_satisfaction", "growth_potential", "risk_level"]):
            raise ValueError("Missing required keys in best_case consequences")
            
        if not all(key in custom_scenario["worst_case"]["consequences"] for key in ["cash_flow", "customer_satisfaction", "growth_potential", "risk_level"]):
            raise ValueError("Missing required keys in worst_case consequences")
            
        # Ensure next scenarios exist in the database
        for scenario in custom_scenario["best_case"]["next_scenarios"] + custom_scenario["worst_case"]["next_scenarios"]:
            if scenario not in SCENARIO_DATABASE:
                raise ValueError(f"Invalid next scenario: {scenario}")
        
        return custom_scenario
        
    except Exception as e:
        # Fallback to random generation if Claude fails
        st.warning(f"Failed to generate scenario with Claude: {str(e)}. Falling back to random generation.")
        return generate_random_scenario(topic)

def generate_random_scenario(topic):
    """Fallback function to generate a random scenario if Claude fails"""
    # Generate scenario description
    aspect = random.choice(BUSINESS_ASPECTS)
    impact = random.choice(BUSINESS_IMPACT_DESCRIPTIONS)
    
    scenario_description = f"Your franchise is facing a decision regarding {topic.lower()} that affects your {aspect}."
    
    # Generate best case option
    best_action = random.choice(BEST_CASE_INVESTMENTS)
    best_desc = f"{best_action} to address the {topic.lower()} situation."
    
    # Generate consequences for best case (generally positive with some cash flow impact)
    best_consequences = {
        "cash_flow": random.randint(-40000, -10000),
        "customer_satisfaction": random.randint(10, 25),
        "growth_potential": random.randint(10, 25),
        "risk_level": random.randint(-20, 5)
    }
    
    # Generate worst case option
    worst_action = random.choice(WORST_CASE_APPROACHES)
    worst_desc = f"{worst_action} for the {topic.lower()} situation."
    
    # Generate consequences for worst case (mixed, generally lower cost but fewer benefits)
    worst_consequences = {
        "cash_flow": random.randint(-15000, 5000),  # May sometimes save money
        "customer_satisfaction": random.randint(-15, 10),
        "growth_potential": random.randint(-10, 5),
        "risk_level": random.randint(-5, 15)
    }
    
    # Generate next scenarios (use 2 random scenarios from the database)
    next_scenarios = random.sample(list(SCENARIO_DATABASE.keys()), 2)
    
    # Construct the full scenario
    custom_scenario = {
        "description": scenario_description,
        "best_case": {
            "title": f"Strategic {topic} Initiative",
            "description": best_desc,
            "consequences": best_consequences,
            "next_scenarios": next_scenarios
        },
        "worst_case": {
            "title": f"Practical {topic} Approach",
            "description": worst_desc,
            "consequences": worst_consequences,
            "next_scenarios": next_scenarios
        }
    }
    
    return custom_scenario

def generate_scenario_title(base_title):
    """Generate a more specific and engaging scenario title"""
    adjectives = [
        "Critical", "Strategic", "Unexpected", "Challenging", 
        "Exciting", "Pivotal", "Emerging", "Urgent"
    ]
    
    contexts = [
        "Decision", "Opportunity", "Challenge", "Situation", 
        "Dilemma", "Crossroads", "Moment", "Development"
    ]
    
    adjective = random.choice(adjectives)
    context = random.choice(contexts)
    
    return f"{adjective} {base_title} {context}"

def generate_simulation_analysis(scenario_history, final_metrics):
    """Generate a brief analysis of the user's decisions and predict business outlook"""
    
    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    # Format the scenario history for the prompt
    decisions_text = ""
    for i, scenario in enumerate(scenario_history):
        decisions_text += f"Decision {i+1}: {scenario['topic']}\n"
        decisions_text += f"Choice: {scenario['choice']} - {scenario['title']}\n"
        decisions_text += f"Impact: {scenario['consequences']}\n\n"
    
    # Format the final metrics
    metrics_text = "Final Business Metrics:\n"
    metrics_text += f"- Cash Flow: ${final_metrics['cash_flow']}\n"
    metrics_text += f"- Customer Satisfaction: {final_metrics['customer_satisfaction']}%\n"
    metrics_text += f"- Growth Potential: {final_metrics['growth_potential']}%\n"
    metrics_text += f"- Risk Level: {final_metrics['risk_level']}%\n"
    
    # Create a prompt for Claude
    prompt = f"""You are a franchise business analyst. Review the following decisions made by a franchise owner in a simulation and provide a detailed analysis.

{decisions_text}
{metrics_text}

Please provide:
1. A detailed analysis (3-4 sentences) of the user's decision-making patterns and strategy, including specific examples from their choices
2. A comprehensive assessment (3-4 sentences) of the business's health and likely future performance based on current metrics, with specific numbers and trends
3. Two specific recommendations for future business decisions based on the observed patterns and current business state

Keep your response under 200 words and be direct and insightful. Focus on concrete examples and specific metrics. If the business is struggling, provide constructive feedback on how to improve. If it's doing well, suggest ways to maintain and build on the success."""

    # Try to get response from Claude twice before falling back
    for attempt in range(2):
        try:
            # Get response from Claude
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=400,  # Increased for more detailed analysis
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Return the text content
            return response.content[0].text.strip()
            
        except Exception as e:
            if attempt == 0:  # First attempt failed, try again
                continue
            else:  # Second attempt failed, generate fallback analysis
                # Generate a detailed fallback analysis based on the metrics and history
                analysis = []
                
                # Analyze decision patterns
                best_case_count = sum(1 for s in scenario_history if s['choice'] == "Best Case")
                worst_case_count = sum(1 for s in scenario_history if s['choice'] == "Worst Case")
                
                if best_case_count > worst_case_count:
                    analysis.append(f"Your decision-making approach shows a preference for ambitious, growth-oriented strategies, choosing the best-case option in {best_case_count} out of {len(scenario_history)} scenarios.")
                elif worst_case_count > best_case_count:
                    analysis.append(f"Your decision-making approach shows a preference for conservative, risk-averse strategies, choosing the worst-case option in {worst_case_count} out of {len(scenario_history)} scenarios.")
                else:
                    analysis.append(f"Your decision-making approach shows a balanced strategy, choosing an equal mix of ambitious and conservative options across {len(scenario_history)} scenarios.")
                
                # Analyze current business state
                if final_metrics['cash_flow'] < 50000:
                    analysis.append(f"Your current cash position of ${final_metrics['cash_flow']} indicates financial strain. This may limit your ability to invest in growth opportunities.")
                elif final_metrics['cash_flow'] < 100000:
                    analysis.append(f"Your current cash position of ${final_metrics['cash_flow']} is moderate. While stable, you may want to build reserves for future opportunities.")
                else:
                    analysis.append(f"Your strong cash position of ${final_metrics['cash_flow']} provides a solid foundation for growth and investment opportunities.")
                
                # Analyze customer satisfaction
                if final_metrics['customer_satisfaction'] < 40:
                    analysis.append(f"Customer satisfaction at {final_metrics['customer_satisfaction']}% needs immediate attention. Focus on improving service quality and customer experience.")
                elif final_metrics['customer_satisfaction'] < 60:
                    analysis.append(f"Customer satisfaction at {final_metrics['customer_satisfaction']}% has room for improvement. Consider enhancing customer service initiatives.")
                else:
                    analysis.append(f"Strong customer satisfaction at {final_metrics['customer_satisfaction']}% indicates effective customer service. Look for ways to maintain and build on this success.")
                
                # Analyze growth potential
                if final_metrics['growth_potential'] < 40:
                    analysis.append(f"Growth potential at {final_metrics['growth_potential']}% suggests limited expansion opportunities. Focus on stabilizing current operations before pursuing growth.")
                elif final_metrics['growth_potential'] < 60:
                    analysis.append(f"Growth potential at {final_metrics['growth_potential']}% shows moderate expansion possibilities. Look for strategic opportunities to accelerate growth.")
                else:
                    analysis.append(f"High growth potential at {final_metrics['growth_potential']}% indicates strong expansion opportunities. Consider developing a detailed growth strategy.")
                
                # Analyze risk level
                if final_metrics['risk_level'] > 60:
                    analysis.append(f"High risk level at {final_metrics['risk_level']}% requires immediate attention. Focus on risk mitigation and stability measures.")
                elif final_metrics['risk_level'] > 40:
                    analysis.append(f"Moderate risk level at {final_metrics['risk_level']}% suggests careful monitoring. Consider implementing additional risk management strategies.")
                else:
                    analysis.append(f"Low risk level at {final_metrics['risk_level']}% indicates stable operations. Look for opportunities to optimize while maintaining this stability.")
                
                # Add specific recommendations
                if final_metrics['cash_flow'] < 50000:
                    analysis.append("Recommendations: 1) Implement cost-cutting measures to improve cash flow. 2) Focus on high-margin products or services to boost profitability.")
                elif final_metrics['customer_satisfaction'] < 40:
                    analysis.append("Recommendations: 1) Conduct customer surveys to identify specific pain points. 2) Invest in staff training to improve service quality.")
                elif final_metrics['growth_potential'] < 40:
                    analysis.append("Recommendations: 1) Review and optimize current operations. 2) Research new market opportunities aligned with your strengths.")
                else:
                    analysis.append("Recommendations: 1) Develop a detailed expansion strategy. 2) Consider investing in technology or staff to support growth.")
                
                return "\n".join(analysis) 