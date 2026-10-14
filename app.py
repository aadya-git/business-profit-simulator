"""Business Profit Simulator — existing Gradio application."""

import gradio as gr
import plotly.graph_objects as go


def calculate_profit(price, variable_cost, fixed_cost, units_sold):
    revenue = price * units_sold
    total_variable_cost = variable_cost * units_sold
    total_cost = fixed_cost + total_variable_cost
    profit = revenue - total_cost

    contribution = price - variable_cost

    if contribution > 0:
        break_even_units = -(-fixed_cost // contribution)
    else:
        break_even_units = None

    profit_margin = (profit / revenue * 100) if revenue > 0 else 0

    return {
        "Revenue": revenue,
        "Total Cost": total_cost,
        "Profit": profit,
        "Break-even Units": break_even_units,
        "Profit Margin (%)": round(profit_margin, 2)
    }


import gradio as gr
import plotly.graph_objects as go


def build_dashboard(price, variable_cost, fixed_cost, units_sold):
    price = max(0, float(price or 0))
    variable_cost = max(0, float(variable_cost or 0))
    fixed_cost = max(0, float(fixed_cost or 0))
    units_sold = max(0, int(units_sold or 0))

    result = calculate_profit(price, variable_cost, fixed_cost, units_sold)

    revenue = result["Revenue"]
    total_cost = result["Total Cost"]
    profit = result["Profit"]
    margin = result["Profit Margin (%)"]
    contribution = price - variable_cost
    break_even = result["Break-even Units"]

    profit_color = "#15803d" if profit >= 0 else "#b91c1c"

    # Dashboard cards
    summary = f"""
    <div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px">
      <div style="background:#fff;padding:18px;border-radius:12px">
        <div style="color:#475569 !important">Monthly Revenue</div>
        <h2 style="color:#0f172a !important">₹{revenue:,.0f}</h2>
        <small style="color:#64748b !important">Total sales generated</small>
      </div>
      <div style="background:#fff;padding:18px;border-radius:12px">
        <div style="color:#475569 !important">Total Monthly Cost</div>
        <h2 style="color:#0f172a !important">₹{total_cost:,.0f}</h2>
        <small style="color:#64748b !important">Fixed + variable costs</small>
      </div>
      <div style="background:#fff;padding:18px;border-radius:12px">
        <div style="color:#475569 !important">Monthly Profit / Loss</div>
        <h2 style="color:{profit_color} !important">₹{profit:,.0f}</h2>
        <small style="color:#64748b !important">Revenue minus total costs</small>
      </div>
      <div style="background:#fff;padding:18px;border-radius:12px">
        <div style="color:#475569 !important">Profit Margin</div>
        <h2 style="color:#0f172a !important">{margin:.1f}%</h2>
        <small style="color:#64748b !important">Profit as a share of revenue</small>
      </div>
    </div>
    """

    # Break-even analysis
    if contribution > 0:
        be_text = f"{break_even:,} units"
        be_status = (
            "Break-even reached"
            if units_sold >= break_even
            else f"{break_even - units_sold:,} more units needed"
        )
    else:
        be_text = "Not achievable"
        be_status = "Selling price must exceed variable cost."

    if profit > 0:
        status = "The business is currently profitable."
    elif profit < 0:
        status = "The business is operating at a loss."
    else:
        status = "The business is exactly at break-even."

    insight = f"""
    <div style="background:#ffffff !important;color:#1e293b !important;
                padding:20px;border:1px solid #cbd5e1;border-radius:12px">
      <b style="color:#0f172a !important">Break-even Point</b>
      <h2 style="color:#0f172a !important">{be_text}</h2>
      <p style="color:#334155 !important">{be_status}</p>
      <hr style="border-color:#e2e8f0 !important">
      <b style="color:#0f172a !important">Business Insight</b>
      <p style="color:#334155 !important">{status}</p>
      <p style="color:#334155 !important">
        Contribution per unit: ₹{contribution:,.2f}
      </p>
    </div>
    """

    # Price increase scenario
    new_price = price * 1.10
    new_revenue = new_price * units_sold
    new_profit = (new_price - variable_cost) * units_sold - fixed_cost
    profit_change = new_profit - profit
    change_color = "#15803d" if profit_change >= 0 else "#b91c1c"

    price_scenario = f"""
    <div style="background:#ffffff !important;color:#1e293b !important;
                padding:20px;border:1px solid #e2e8f0;border-radius:12px">
      <h3 style="color:#0f172a !important;margin-top:0">
        Price Increase: 10%
      </h3>
      <p style="color:#334155 !important">Current selling price: ₹{price:,.2f}</p>
      <p style="color:#334155 !important">New selling price: ₹{new_price:,.2f}</p>
      <p style="color:#334155 !important">Current monthly revenue: ₹{revenue:,.2f}</p>
      <p style="color:#334155 !important">Projected monthly revenue: ₹{new_revenue:,.2f}</p>
      <p style="color:#334155 !important">Current monthly profit: ₹{profit:,.2f}</p>
      <p style="color:#334155 !important">Projected monthly profit: ₹{new_profit:,.2f}</p>
      <h3 style="color:{change_color} !important">
        Profit Change: ₹{profit_change:+,.2f}
      </h3>
      <small style="color:#64748b !important">
        Assumes sales volume and costs per unit remain unchanged.
      </small>
    </div>
    """

    # Sales volume scenarios
    scenario_labels = ["Sales -20%", "Current Sales", "Sales +20%"]
    scenario_units = [
        int(units_sold * 0.8),
        units_sold,
        int(units_sold * 1.2)
    ]

    scenario_revenues = []
    scenario_profits = []
    scenario_rows = []

    row_styles = [
        ("#fff7ed", "#9a3412", "#fed7aa"),
        ("#eff6ff", "#1d4ed8", "#bfdbfe"),
        ("#f0fdf4", "#166534", "#bbf7d0")
    ]

    for i, (label, qty) in enumerate(zip(scenario_labels, scenario_units)):
        scenario_revenue = price * qty
        scenario_cost = fixed_cost + variable_cost * qty
        scenario_profit = scenario_revenue - scenario_cost

        scenario_revenues.append(scenario_revenue)
        scenario_profits.append(scenario_profit)

        bg, text_color, border_color = row_styles[i]
        profit_text_color = "#15803d" if scenario_profit >= 0 else "#b91c1c"

        scenario_rows.append(f"""
        <tr style="background:{bg} !important">
          <td style="padding:14px;color:{text_color} !important;
                     border-bottom:1px solid {border_color}">{label}</td>
          <td style="padding:14px;text-align:right;color:{text_color} !important;
                     border-bottom:1px solid {border_color}">{qty:,}</td>
          <td style="padding:14px;text-align:right;color:{text_color} !important;
                     border-bottom:1px solid {border_color}">₹{scenario_revenue:,.0f}</td>
          <td style="padding:14px;text-align:right;color:{profit_text_color} !important;
                     font-weight:bold;border-bottom:1px solid {border_color}">₹{scenario_profit:,.0f}</td>
        </tr>
        """)

    comparison = f"""
    <div style="background:#ffffff !important;color:#1e293b !important;
                padding:24px;border:1px solid #cbd5e1;border-radius:14px;
                overflow-x:auto;font-family:Arial,sans-serif">

      <h3 style="color:#172554 !important;margin-top:0">
        Sales Volume Scenario Comparison
      </h3>
      <p style="color:#475569 !important">
        Compare how a 20% decrease or increase in sales affects revenue and profit.
      </p>

      <table style="width:100%;border-collapse:collapse;
                    background:#ffffff !important;color:#1e293b !important;
                    font-size:14px">
        <thead>
          <tr>
            <th style="padding:15px;text-align:left;background:#1e3a8a !important;color:#ffffff !important">Scenario</th>
            <th style="padding:15px;text-align:right;background:#1e3a8a !important;color:#ffffff !important">Units Sold</th>
            <th style="padding:15px;text-align:right;background:#1e3a8a !important;color:#ffffff !important">Revenue</th>
            <th style="padding:15px;text-align:right;background:#1e3a8a !important;color:#ffffff !important">Profit / Loss</th>
          </tr>
        </thead>
        <tbody>
          {''.join(scenario_rows)}
        </tbody>
      </table>

      <div style="margin-top:18px;padding:14px;background:#f8fafc !important;
                  border-radius:8px">
        <b style="color:#0f172a !important">Business Takeaway</b>
        <p style="color:#334155 !important;margin-bottom:0">
          Higher sales increase profit when contribution per unit is positive,
          assuming fixed costs and unit costs remain unchanged.
        </p>
      </div>
    </div>
    """

    # Revenue and cost chart
    max_units = max(units_sold, break_even or 0, 1)
    chart_units = sorted(set([
        0,
        max(1, max_units // 4),
        max(1, max_units // 2),
        max(1, 3 * max_units // 4),
        max_units,
        max_units + max(1, max_units // 4)
    ]))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chart_units,
        y=[price * u for u in chart_units],
        mode="lines+markers",
        name="Revenue",
        line=dict(color="#2563eb", width=3)
    ))
    fig.add_trace(go.Scatter(
        x=chart_units,
        y=[fixed_cost + variable_cost * u for u in chart_units],
        mode="lines+markers",
        name="Total Cost",
        line=dict(color="#ea580c", width=3)
    ))
    fig.update_layout(
        title="Revenue vs. Total Cost",
        xaxis_title="Units Sold",
        yaxis_title="Amount (₹)",
        template="plotly_white"
    )

    # Colorful scenario chart
    comparison_fig = go.Figure()
    comparison_fig.add_trace(go.Bar(
        x=scenario_labels,
        y=scenario_revenues,
        name="Revenue",
        marker_color="#3b82f6"
    ))
    comparison_fig.add_trace(go.Bar(
        x=scenario_labels,
        y=scenario_profits,
        name="Profit / Loss",
        marker_color=["#f97316", "#16a34a", "#8b5cf6"]
    ))
    comparison_fig.update_layout(
        title="Compare Business Scenarios",
        xaxis_title="Sales Scenario",
        yaxis_title="Amount (₹)",
        barmode="group",
        template="plotly_white"
    )

    return (
        summary, insight, price_scenario,
        comparison, fig, comparison_fig
    )


with gr.Blocks(
    title="Business Profit Simulator",
    theme=gr.themes.Soft()
) as app:

    gr.Markdown("""
    # Business Profit Simulator

    Analyse profitability, break-even sales and alternative business scenarios.
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Business Assumptions")

            price = gr.Slider(
                50, 2000, value=500, step=50,
                label="Selling Price per Unit (₹)"
            )
            variable_cost = gr.Slider(
                0, 1500, value=250, step=25,
                label="Variable Cost per Unit (₹)"
            )
            fixed_cost = gr.Slider(
                0, 100000, value=25000, step=1000,
                label="Monthly Fixed Costs (₹)"
            )
            units_sold = gr.Slider(
                0, 1000, value=200, step=10,
                label="Units Sold per Month"
            )

            reset = gr.Button("Reset Assumptions")

        with gr.Column(scale=2):
            gr.Markdown("### Business Performance")
            dashboard = gr.HTML()

            gr.Markdown("### Break-even Analysis")
            insight_box = gr.HTML()

    gr.Markdown("### Price Change Scenario")
    price_scenario_box = gr.HTML()

    gr.Markdown("### Sales Volume Comparison")
    comparison_box = gr.HTML()

    with gr.Row():
        revenue_chart = gr.Plot(label="Revenue and Costs")
        comparison_chart = gr.Plot(label="Scenario Comparison")

    inputs = [price, variable_cost, fixed_cost, units_sold]
    outputs = [
        dashboard, insight_box, price_scenario_box,
        comparison_box, revenue_chart, comparison_chart
    ]

    for control in inputs:
        control.change(
            fn=build_dashboard,
            inputs=inputs,
            outputs=outputs
        )

    app.load(
        fn=build_dashboard,
        inputs=inputs,
        outputs=outputs
    )

    reset.click(
        fn=lambda: (500, 250, 25000, 200),
        outputs=inputs
    )

app.launch(share=True)
