# Business Profit Simulator

An interactive business-finance simulator built with Python, Gradio, and Plotly. It helps users explore how selling price, variable cost, fixed costs, and sales volume affect business performance.

## Current features

- Interactive inputs for selling price, variable cost, fixed costs, and units sold
- Revenue, total cost, profit/loss, and profit-margin KPI cards
- Break-even unit calculation and business status insight
- What-if scenario for a 10% selling-price increase
- Sales-volume comparison at -20%, current sales, and +20%
- Plotly charts comparing revenue, total cost, and business scenarios
- Reset button for the default assumptions

## Technology stack

- Python
- Gradio
- Plotly

## Project structure

```text
business-profit-simulator/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── notebooks/
    └── Business_Profit_Simulator.ipynb
```

## Requirements

Python 3.10 or newer is recommended.

## Run locally

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. (Recommended) Create and activate a virtual environment.

   Windows:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   macOS/Linux:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   python app.py
   ```

The application uses the launch configuration from the original notebook. Gradio will print the local URL in the terminal; the current code also requests a share link.

## Default example

- Selling price: ₹500 per unit
- Variable cost: ₹250 per unit
- Monthly fixed costs: ₹25,000
- Units sold per month: 200

With these assumptions, the simulator calculates revenue of ₹100,000, total costs of ₹75,000, profit of ₹25,000, a 25% profit margin, and break-even at 100 units.

## Notes

- This project is a scenario simulator, not financial or investment advice.
- The original Colab notebook is included under `notebooks/` for reference.
- No external API is required.
