# Franchise Cockpit Simulator

An interactive Streamlit application that simulates franchise business decisions and their impacts through a series of scenario-based choices.

## Description

The Franchise Cockpit Simulator helps franchise owners and potential entrepreneurs explore different business scenarios and their outcomes. Users navigate through business challenges, making strategic decisions that affect key performance metrics. The simulator provides a safe environment to experiment with different approaches to franchise management.

## Key Features

- **Interactive Decision Making**: Choose between different approaches to business challenges
- **Real-time Metric Tracking**: Monitor how decisions impact cash flow, customer satisfaction, growth potential, and risk level
- **Decision Path Visualization**: View a visual representation of your decision journey
- **AI-Generated Analysis**: Receive an AI-powered analysis of your business strategy at the end of the simulation
- **Human-Friendly Impact Descriptions**: Get narrative explanations of how your choices affect your business
- **Responsive UI**: Clean, modern interface with intuitive navigation
- **Custom Scenarios**: Enter your own scenario topics for personalized simulations

## Testing

1. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Set up your Anthropic API key:

   Create a secrets.toml file in the .streamlit directory with your Anthropic API key:

   ```
   ANTHROPIC_API_KEY = "your-api-key-here"
   ```

3. Run the Streamlit application:

   ```
   streamlit run app.py
   ```

4. Open your browser and go to the URL displayed in the terminal (typically http://localhost:8501)

## Simulation Flow

1. **Topic Selection**: Choose a predefined scenario or create your own
2. **Decision Making**: Navigate through 5 sequential business scenarios
3. **Impact Assessment**: See how each choice affects your business metrics
4. **Final Analysis**: Receive a comprehensive analysis of your business strategy
5. **Results Summary**: Review your decision path and key performance indicators

## Technical Details

The application is built with:

- **Streamlit**: For the web interface and application flow
- **Claude by Anthropic**: For generating custom scenarios and business analysis
- **SVG**: For decision path visualization
- **Pandas/NumPy**: For data handling and calculations

## Notes

- The simulation uses a mix of predefined scenarios and AI-generated content
- Custom topics entered by users will generate unique scenarios using Claude
- The business metrics are simulated and should not be taken as financial advice
- The final analysis provides insights based on the choices made during simulation
