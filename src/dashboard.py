# Imports
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

# Load the dataset
df = pd.read_csv('datasets/lending_club_cleaned.csv')

# Create the figures
# Loan Status vs DTI
# Plot to visualize observation
fig1 = px.box(data_frame=df.loc[df['dti'] < 70],
        x='loan_status', 
        y='dti', 
        color='loan_status', 
        points= 'outliers', 
        width=1000, 
        height= 800, 
        color_discrete_sequence=px.colors.qualitative.Set1
)

fig1.update_layout(
    title=dict(text="<b>Distribution of DTI by Loan Status</b>", font=dict(size=20), x=0.5),
    xaxis_title=dict(text="Loan Status", font=dict(size=15)),
    yaxis_title=dict(text="Debt-to-Income Ratio (DTI)", font=dict(size=15)),
    legend_title= "Loan Status"
)

# Loan Status vs Annual Income
income_histogram = px.histogram(
    df,
    x='annual_inc',
    color='loan_status',
    title='Loan Status vs Annual Income',
    labels={'annual_inc': 'Annual Income', 'loan_status': 'Loan Status'},
    color_discrete_sequence=px.colors.qualitative.Plotly,
    nbins=50
)

# Loan Status vs DTI & Annual Income
dti_income_box_plot = px.box(
    df,
    x='annual_inc_lvl',
    y='dti',
    color='loan_status',
    title='DTI Distribution by Income Level and Loan Status',
    labels={'annual_inc_lvl': 'Annual Income Level', 'dti': 'DTI'},
    category_orders={'annual_inc_lvl': ['0-12k', '12k-47k', '47-100k', '100k-191k', '191k-243k', '243k-600k', '600k+']},
    color_discrete_sequence=px.colors.qualitative.Plotly
)

dti_income_box_plot.update_layout(
    xaxis_title='Annual Income Level',
    yaxis_title='DTI',
    legend_title='Loan Status',
    xaxis_tickangle=45,
    legend=dict(title='Loan Status', orientation='v', yanchor='top', y=1.02, xanchor='left', x=1.02)
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Loan Analysis Project", style={'textAlign': 'center', 'color': '#2C3E50', 'fontFamily': 'Arial'}),
    
    html.Div([
        html.H2("Executive Summary", style={'textAlign': 'center', 'color': '#34495E', 'fontFamily': 'Arial'}),
        dcc.Markdown("""
        **Summary of findings and recommendations:**

        - **Goal:** Reduce the percentage of loan defaults and refine marketing and lending strategies.
        - **Key Findings:**
            - Higher DTI ratios are strongly associated with loan defaults.
            - Higher income levels correlate with lower loan default rates.
        - **Recommendations:**
            1. Implement stricter lending criteria for borrowers with high DTI ratios.
            2. Develop targeted marketing campaigns for higher-income brackets.
            3. Strengthen income verification processes and offer financial literacy programs for lower-income borrowers.
            4. Use dynamic risk assessment models to identify potential defaulters early.
            5. Develop custom loan products tailored to different income brackets and DTI levels.
        """, style={'padding': '20px', 'fontFamily': 'Arial'})
    ]),

    # Tabs for Detailed Analysis
    dcc.Tabs([
        dcc.Tab(label='Loan Status vs DTI', children=[
            html.H3("Descriptive Analysis", style={'textAlign': 'center', 'color': '#2C3E50', 'fontFamily': 'Arial'}),
            dcc.Graph(figure=fig1),
            html.H3("Inferential Analysis", style={'textAlign': 'center', 'color': '#2C3E50', 'fontFamily': 'Arial'}),
            dcc.Markdown("""
            **Mann-Whitney U Test Results:**

            - Null Hypothesis: There is no difference in DTI distributions between charged-off and fully paid loans.
            - Result: A near-zero p-value suggests the observed difference in DTI distributions is unlikely to have occurred by chance, rejecting the null hypothesis.
            """, style={'padding': '20px', 'fontFamily': 'Arial'}),
        ]),
        dcc.Tab(label='Loan Status vs Annual Income', children=[
            html.H3("Descriptive Analysis", style={'textAlign': 'center', 'color': '#2C3E50', 'fontFamily': 'Arial'}),
            dcc.Graph(figure=income_histogram),
            html.H3("Inferential Analysis", style={'textAlign': 'center', 'color': '#2C3E50', 'fontFamily': 'Arial'}),
            dcc.Markdown("""
            **Linear Regression Results:**

            - Model: Loan default status as a function of annual income.
            - Result: The model shows a relationship between income level and the number of charged-off loans, although the p-value suggests this relationship might be due to chance, necessitating further testing.
            """, style={'padding': '20px', 'fontFamily': 'Arial'}),
        ]),
        dcc.Tab(label='Loan Status vs DTI & Annual Income', children=[
            html.H3("Combined Analysis", style={'textAlign': 'center', 'color': '#2C3E50', 'fontFamily': 'Arial'}),
            dcc.Graph(figure=dti_income_box_plot),
            html.H3("Inferential Analysis", style={'textAlign': 'center', 'color': '#2C3E50', 'fontFamily': 'Arial'}),
            dcc.Markdown("""
            **Logistic Regression Results:**

            - Model: Loan status as a function of DTI and income brackets.
            - Result: DTI and income brackets were significant predictors of loan status. Higher income brackets were associated with a lower likelihood of charge-offs, while higher DTI values increased the likelihood.
            """, style={'padding': '20px', 'fontFamily': 'Arial'}),
        ])
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

