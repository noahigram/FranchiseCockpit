# Scenario database for the Best Case, Worst Case simulator
# Each scenario has a description and two path options (best case and worst case)

SCENARIO_DATABASE = {
    "Location Selection": {
        "description": "You need to choose a location for your new franchise.",
        "best_case": {
            "title": "Prime Commercial Area",
            "description": "A spot opens up in a high-traffic shopping center with excellent visibility.",
            "consequences": {
                "cash_flow": -20000,
                "customer_satisfaction": +10,
                "growth_potential": +15,
                "risk_level": +5
            },
            "next_scenarios": ["Hiring First Manager", "Marketing Campaign Launch"]
        },
        "worst_case": {
            "title": "Budget-Friendly Location",
            "description": "You find an affordable location in a developing neighborhood with lower foot traffic.",
            "consequences": {
                "cash_flow": -5000,
                "customer_satisfaction": -5,
                "growth_potential": +5,
                "risk_level": -10
            },
            "next_scenarios": ["Hiring First Manager", "Marketing Campaign Launch"]
        }
    },
    
    "Hiring First Manager": {
        "description": "You need to hire a manager to run your franchise daily operations.",
        "best_case": {
            "title": "Experienced Industry Professional",
            "description": "Hire a manager with 10+ years of experience in the industry with a proven track record.",
            "consequences": {
                "cash_flow": -15000,
                "customer_satisfaction": +20,
                "growth_potential": +10,
                "risk_level": -15
            },
            "next_scenarios": ["Supply Chain Disruption", "Competitor Opening Nearby"]
        },
        "worst_case": {
            "title": "Promising But Inexperienced Manager",
            "description": "Hire a highly motivated but inexperienced manager at a lower salary.",
            "consequences": {
                "cash_flow": -8000,
                "customer_satisfaction": -5,
                "growth_potential": +5,
                "risk_level": +10
            },
            "next_scenarios": ["Supply Chain Disruption", "Competitor Opening Nearby"]
        }
    },
    
    "Marketing Campaign Launch": {
        "description": "You need to launch a marketing campaign to promote your franchise.",
        "best_case": {
            "title": "Comprehensive Multimedia Campaign",
            "description": "Launch a professional campaign across digital, social, and local traditional media.",
            "consequences": {
                "cash_flow": -25000,
                "customer_satisfaction": +15,
                "growth_potential": +20,
                "risk_level": +5
            },
            "next_scenarios": ["Customer Complaint Handling", "Expansion Opportunity"]
        },
        "worst_case": {
            "title": "Grassroots Word-of-Mouth Campaign",
            "description": "Focus on low-cost community engagement and word-of-mouth marketing.",
            "consequences": {
                "cash_flow": -3000,
                "customer_satisfaction": +5,
                "growth_potential": +3,
                "risk_level": -5
            },
            "next_scenarios": ["Customer Complaint Handling", "Expansion Opportunity"]
        }
    },
    
    "Supply Chain Disruption": {
        "description": "Your main supplier has issues that affect your inventory.",
        "best_case": {
            "title": "Diversify Suppliers",
            "description": "Invest in relationships with multiple suppliers to ensure backup options.",
            "consequences": {
                "cash_flow": -15000,
                "customer_satisfaction": +5,
                "growth_potential": +5,
                "risk_level": -20
            },
            "next_scenarios": ["Technology Upgrade", "Economic Downturn"]
        },
        "worst_case": {
            "title": "Maintain Current Supplier",
            "description": "Wait out the disruption with your current supplier and manage inventory carefully.",
            "consequences": {
                "cash_flow": -2000,
                "customer_satisfaction": -15,
                "growth_potential": -5,
                "risk_level": +15
            },
            "next_scenarios": ["Technology Upgrade", "Economic Downturn"]
        }
    },
    
    "Competitor Opening Nearby": {
        "description": "A competitor is opening a location near your franchise.",
        "best_case": {
            "title": "Enhance Customer Experience",
            "description": "Invest in staff training and amenities to significantly improve the customer experience.",
            "consequences": {
                "cash_flow": -18000,
                "customer_satisfaction": +25,
                "growth_potential": +10,
                "risk_level": -5
            },
            "next_scenarios": ["Technology Upgrade", "Economic Downturn"]
        },
        "worst_case": {
            "title": "Competitive Price Cutting",
            "description": "Lower your prices to compete directly with the new competitor.",
            "consequences": {
                "cash_flow": -10000,
                "customer_satisfaction": +5,
                "growth_potential": -5,
                "risk_level": +15
            },
            "next_scenarios": ["Technology Upgrade", "Economic Downturn"]
        }
    },
    
    "Customer Complaint Handling": {
        "description": "Your franchise has received several customer complaints on social media.",
        "best_case": {
            "title": "Full Transparency and Compensation",
            "description": "Publicly acknowledge the issues, apologize, and offer generous compensation to affected customers.",
            "consequences": {
                "cash_flow": -12000,
                "customer_satisfaction": +20,
                "growth_potential": +5,
                "risk_level": -10
            },
            "next_scenarios": ["Expansion Opportunity", "Regulatory Changes"]
        },
        "worst_case": {
            "title": "Minimal Response Strategy",
            "description": "Address complaints individually and privately with minimal public acknowledgment.",
            "consequences": {
                "cash_flow": -2000,
                "customer_satisfaction": -10,
                "growth_potential": -5,
                "risk_level": +15
            },
            "next_scenarios": ["Expansion Opportunity", "Regulatory Changes"]
        }
    },
    
    "Expansion Opportunity": {
        "description": "You have the chance to open a second location for your franchise.",
        "best_case": {
            "title": "Aggressive Expansion",
            "description": "Secure financing and open a second location in a promising high-traffic area.",
            "consequences": {
                "cash_flow": -100000,
                "customer_satisfaction": +5,
                "growth_potential": +30,
                "risk_level": +25
            },
            "next_scenarios": ["Hiring First Manager", "Marketing Campaign Launch"]
        },
        "worst_case": {
            "title": "Focus on Current Success",
            "description": "Delay expansion and reinvest profits into improving your current location.",
            "consequences": {
                "cash_flow": +15000,
                "customer_satisfaction": +10,
                "growth_potential": -5,
                "risk_level": -15
            },
            "next_scenarios": ["Technology Upgrade", "Supply Chain Disruption"]
        }
    },
    
    "Regulatory Changes": {
        "description": "New regulations affecting your industry have been announced.",
        "best_case": {
            "title": "Proactive Compliance Investment",
            "description": "Invest heavily in becoming fully compliant well before deadlines and publicize your leadership.",
            "consequences": {
                "cash_flow": -30000,
                "customer_satisfaction": +15,
                "growth_potential": +10,
                "risk_level": -20
            },
            "next_scenarios": ["Technology Upgrade", "Economic Downturn"]
        },
        "worst_case": {
            "title": "Minimum Compliance Approach",
            "description": "Meet only the essential requirements just before deadlines to minimize costs.",
            "consequences": {
                "cash_flow": -10000,
                "customer_satisfaction": -5,
                "growth_potential": -5,
                "risk_level": +20
            },
            "next_scenarios": ["Technology Upgrade", "Economic Downturn"]
        }
    },
    
    "Technology Upgrade": {
        "description": "Your franchise POS and management systems are becoming outdated.",
        "best_case": {
            "title": "Comprehensive Digital Transformation",
            "description": "Implement state-of-the-art systems with integrated analytics and customer experience features.",
            "consequences": {
                "cash_flow": -40000,
                "customer_satisfaction": +20,
                "growth_potential": +25,
                "risk_level": -5
            },
            "next_scenarios": ["Expansion Opportunity", "Marketing Campaign Launch"]
        },
        "worst_case": {
            "title": "Basic System Maintenance",
            "description": "Make minimal updates to keep current systems functioning adequately.",
            "consequences": {
                "cash_flow": -5000,
                "customer_satisfaction": -5,
                "growth_potential": -10,
                "risk_level": +10
            },
            "next_scenarios": ["Supply Chain Disruption", "Customer Complaint Handling"]
        }
    },
    
    "Economic Downturn": {
        "description": "The local economy is experiencing a significant downturn affecting consumer spending.",
        "best_case": {
            "title": "Counter-Cyclical Investment",
            "description": "While competitors cut back, you invest in marketing and customer experience to gain market share.",
            "consequences": {
                "cash_flow": -35000,
                "customer_satisfaction": +15,
                "growth_potential": +20,
                "risk_level": +20
            },
            "next_scenarios": ["Marketing Campaign Launch", "Technology Upgrade"]
        },
        "worst_case": {
            "title": "Cost-Cutting Measures",
            "description": "Reduce staff hours, marketing budget, and non-essential expenditures until the economy improves.",
            "consequences": {
                "cash_flow": +15000,
                "customer_satisfaction": -15,
                "growth_potential": -15,
                "risk_level": -10
            },
            "next_scenarios": ["Supply Chain Disruption", "Customer Complaint Handling"]
        }
    },
    
    "Customer Loyalty Program": {
        "description": "You're considering implementing a customer loyalty program for your franchise.",
        "best_case": {
            "title": "Comprehensive Rewards System",
            "description": "Develop a sophisticated digital loyalty program with personalized rewards and app integration.",
            "consequences": {
                "cash_flow": -20000,
                "customer_satisfaction": +25,
                "growth_potential": +15,
                "risk_level": +5
            },
            "next_scenarios": ["Marketing Campaign Launch", "Technology Upgrade"]
        },
        "worst_case": {
            "title": "Simple Punch Card System",
            "description": "Implement a low-cost traditional punch card system with basic rewards.",
            "consequences": {
                "cash_flow": -2000,
                "customer_satisfaction": +5,
                "growth_potential": +2,
                "risk_level": -5
            },
            "next_scenarios": ["Marketing Campaign Launch", "Customer Complaint Handling"]
        }
    },
    
    "Staff Training Initiative": {
        "description": "Your staff needs additional training to improve service and operations.",
        "best_case": {
            "title": "Comprehensive Training Program",
            "description": "Bring in industry experts and develop an extensive training program for all staff levels.",
            "consequences": {
                "cash_flow": -25000,
                "customer_satisfaction": +20,
                "growth_potential": +15,
                "risk_level": -10
            },
            "next_scenarios": ["Customer Loyalty Program", "Expansion Opportunity"]
        },
        "worst_case": {
            "title": "Basic Self-Guided Training",
            "description": "Provide staff with basic manuals and online resources for self-learning.",
            "consequences": {
                "cash_flow": -3000,
                "customer_satisfaction": -5,
                "growth_potential": 0,
                "risk_level": +5
            },
            "next_scenarios": ["Customer Complaint Handling", "Competitor Opening Nearby"]
        }
    },
    
    "Quality Control Issues": {
        "description": "Customers have reported inconsistent quality in your franchise's products or services.",
        "best_case": {
            "title": "Comprehensive Quality Audit",
            "description": "Hire a consulting firm to perform a thorough analysis and implement a rigorous quality control system.",
            "consequences": {
                "cash_flow": -30000,
                "customer_satisfaction": +25,
                "growth_potential": +10,
                "risk_level": -15
            },
            "next_scenarios": ["Staff Training Initiative", "Technology Upgrade"]
        },
        "worst_case": {
            "title": "Internal Review Process",
            "description": "Task your current managers with identifying and fixing quality issues internally.",
            "consequences": {
                "cash_flow": -5000,
                "customer_satisfaction": +5,
                "growth_potential": 0,
                "risk_level": +10
            },
            "next_scenarios": ["Customer Complaint Handling", "Supply Chain Disruption"]
        }
    },
    
    "Community Relations Event": {
        "description": "You have an opportunity to host or sponsor a community event near your franchise.",
        "best_case": {
            "title": "Signature Branded Event",
            "description": "Create and host a major branded community event with extensive marketing and local media coverage.",
            "consequences": {
                "cash_flow": -35000,
                "customer_satisfaction": +20,
                "growth_potential": +15,
                "risk_level": 0
            },
            "next_scenarios": ["Marketing Campaign Launch", "Expansion Opportunity"]
        },
        "worst_case": {
            "title": "Modest Sponsorship",
            "description": "Provide a small sponsorship to an existing community event with minimal branding.",
            "consequences": {
                "cash_flow": -5000,
                "customer_satisfaction": +5,
                "growth_potential": +2,
                "risk_level": -5
            },
            "next_scenarios": ["Customer Loyalty Program", "Competitor Opening Nearby"]
        }
    },
    
    "Lease Renewal Negotiation": {
        "description": "Your franchise location's lease is coming up for renewal, and you need to negotiate terms.",
        "best_case": {
            "title": "Long-term Strategic Negotiation",
            "description": "Hire a commercial real estate expert to negotiate favorable long-term terms with your landlord.",
            "consequences": {
                "cash_flow": -10000,
                "customer_satisfaction": 0,
                "growth_potential": +10,
                "risk_level": -20
            },
            "next_scenarios": ["Expansion Opportunity", "Technology Upgrade"]
        },
        "worst_case": {
            "title": "Standard Renewal Acceptance",
            "description": "Accept the landlord's standard renewal terms to avoid disruption.",
            "consequences": {
                "cash_flow": -5000,
                "customer_satisfaction": 0,
                "growth_potential": -5,
                "risk_level": +10
            },
            "next_scenarios": ["Marketing Campaign Launch", "Supply Chain Disruption"]
        }
    }
} 