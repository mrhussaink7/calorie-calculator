import streamlit as st
import pandas as pd
import plotly.express as px

# Calorie calculation using Mifflin-St Jeor Equation
def calculate_calories(age, gender, height, weight, activity_level):
    # Convert height to cm and weight to kg
    height_cm = height * 2.54
    weight_kg = weight * 0.453592

    if gender == 'Male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    activity_factors = {
        'Light (1-3x/week)': 1.375,
        'Moderate (4-5x/week)': 1.55,
        'Active (4-5x intensive exercise/week)': 1.725
    }

    maintenance_calories = bmr * activity_factors[activity_level]
    mild_weight_loss_calories = maintenance_calories - 250
    weight_loss_calories = maintenance_calories - 500
    extreme_weight_loss_calories = maintenance_calories - 1000

    return maintenance_calories, mild_weight_loss_calories, weight_loss_calories, extreme_weight_loss_calories

# Center the application on the screen
st.set_page_config(layout="wide")

# User inputs
st.title("Calorie and Weight Loss Calculator")

# Create two columns for inputs and graph with specified widths
col1, col2 = st.columns([3, 7])

with col1:
    # Arrange inputs in columns
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        age = st.number_input("Age", min_value=1, max_value=100, value=27)
    with col1_2:
        gender = st.selectbox("Gender", ["Male", "Female"])

    col1_3, col1_4 = st.columns(2)
    with col1_3:
        height_ft = st.number_input("Height (feet)", min_value=1, max_value=7, value=5)
    with col1_4:
        height_in = st.number_input("Height (inches)", min_value=0, max_value=11, value=4)

    height = height_ft * 12 + height_in

    col1_5, col1_6 = st.columns(2)
    with col1_5:
        weight = st.number_input("Weight (lbs)", min_value=50, max_value=500, value=155)
    with col1_6:
        activity_level = st.selectbox("Exercise Activity", ["Light (1-3x/week)", "Moderate (4-5x/week)", "Active (4-5x intensive exercise/week)"])

    # Display calorie needs
    st.write(f"### Calorie Needs")
    maintenance_calories, mild_weight_loss_calories, weight_loss_calories, extreme_weight_loss_calories = calculate_calories(age, gender, height, weight, activity_level)
    st.write(f"Maintain weight: {maintenance_calories:.0f} calories")
    st.write(f"Mild weight loss (0.5 lb/week): {mild_weight_loss_calories:.0f} calories")
    st.write(f"Weight loss (1 lb/week): {weight_loss_calories:.0f} calories")
    st.write(f"Extreme weight loss (2 lb/week): {extreme_weight_loss_calories:.0f} calories")

with col2:
    st.markdown("""
    <style>
    .center-title {
        text-align: center;
        font-size: calc(1.3rem + .6vw);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='center-title'>Weight Loss Progression Over Time</h2>", unsafe_allow_html=True)
    
    # Generate weight loss progression
    weeks = list(range(0, 53))
    maintenance_weight = [weight] * 53
    mild_weight_loss = [weight - (0.5 * w) for w in weeks]
    weight_loss = [weight - w for w in weeks]
    extreme_weight_loss = [weight - (2 * w) for w in weeks]

    # Create dataframe
    df = pd.DataFrame({
        "Week": weeks,
        "Maintenance Weight": maintenance_weight,
        "Mild Weight Loss": mild_weight_loss,
        "Weight Loss": weight_loss,
        "Extreme Weight Loss": extreme_weight_loss
    })

    # Plot weight loss progression
    fig = px.line(df, x="Week", y=["Maintenance Weight", "Mild Weight Loss", "Weight Loss", "Extreme Weight Loss"], 
                  labels={"value": "Weight (lbs)", "variable": "Weight Loss Type"})

    fig.update_layout(
        title={
            'text': "",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=True,
        plot_bgcolor='white',
        margin=dict(l=0, r=0, t=50, b=0)
    )

    # Enable clicking on lines to highlight
    fig.update_traces(mode='lines')  # remove the 'markers' part to get rid of dots
    fig.update_layout(clickmode='event+select')

    # Remove plotly modebar and add space between legend and graph
    fig.update_layout(
        xaxis=dict(showgrid=True, zeroline=False),
        yaxis=dict(showgrid=True, zeroline=False),
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.12, xanchor="right", x=1),  # Adjusted y value for space
        modebar=dict(remove=["zoom", "pan", "select", "zoomIn", "zoomOut", "autoScale", "resetScale", "hoverClosestCartesian", "hoverCompareCartesian"])
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})