import streamlit as st
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv(r"./diabetes.csv")

# Header with professional theme
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
        }
        .header {
            font-size: 50px;
            font-family: 'Verdana', sans-serif;
            font-weight: bold;
            text-align: center;
            color: #0c4b33;
            margin-bottom: 20px;
        }
        .sub-header {
            font-size: 22px;
            font-family: 'Verdana', sans-serif;
            color: #4a7c59;
            text-align: center;
            margin-bottom: 10px;
        }
        .highlight {
            font-size: 18px;
            color: #0c4b33;
            font-weight: bold;
        }
        hr {
            border: none;
            border-top: 2px solid #8bc34a;
        }
        .form-container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
            margin-bottom: 20px;
        }
    </style>
    <div class="header">🩺 Diabetes Risk Checker</div>
    <div class="sub-header">Enter your health details to analyze your diabetes risk.</div>
    <hr>
""", unsafe_allow_html=True)

# Input form container
st.markdown("<div class='form-container'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #0c4b33;'>🔍 Enter Your Health Information Below:</h3>", unsafe_allow_html=True)

# Collect user inputs in a form-like layout
col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input('Pregnancies', min_value=0, max_value=17, value=3, step=1)
    glucose = st.number_input('Glucose Level (mg/dL)', min_value=0, max_value=200, value=120, step=1)
    bp = st.number_input('Blood Pressure (mm Hg)', min_value=0, max_value=122, value=70, step=1)
    skinthickness = st.number_input('Skin Thickness (mm)', min_value=0, max_value=100, value=20, step=1)

with col2:
    insulin = st.number_input('Insulin Level (IU/mL)', min_value=0, max_value=846, value=79, step=1)
    bmi = st.number_input('BMI (Body Mass Index)', min_value=0.0, max_value=67.0, value=20.0, step=0.1)
    dpf = st.number_input('Diabetes Pedigree Function', min_value=0.0, max_value=2.4, value=0.47, step=0.01)
    age = st.slider('Age (years)', min_value=21, max_value=88, value=33)

st.markdown("</div>", unsafe_allow_html=True)

# Combine inputs into a dataframe
user_data = {
    'Pregnancies': pregnancies,
    'Glucose': glucose,
    'BloodPressure': bp,
    'SkinThickness': skinthickness,
    'Insulin': insulin,
    'BMI': bmi,
    'DiabetesPedigreeFunction': dpf,
    'Age': age
}

user_df = pd.DataFrame(user_data, index=[0])

# Data Summary
st.markdown("<h2 style='color: #0c4b33;'>🔬 Health Data Overview</h2>", unsafe_allow_html=True)
st.table(user_df)  # Display the input data in a table format

# Split the data
x = df.drop(['Outcome'], axis=1)
y = df['Outcome']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Model training
rf = RandomForestClassifier()
rf.fit(x_train, y_train)

# Button styles and prediction
st.markdown("""
    <style>
        .stButton>button {
            background-color: #0c4b33;
            color: white;
            font-size: 20px;
            padding: 10px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #145c45;
        }
    </style>
""", unsafe_allow_html=True)

# Button for prediction
if st.button('📊 Analyze Risk'):
    st.markdown("<h3 style='text-align: center; color: #4a7c59;'>🔄 Analyzing your health data...</h3>", unsafe_allow_html=True)
    
    progress = st.progress(0)
    for percent in range(100):
        progress.progress(percent + 1)
    
    prediction = rf.predict(user_df)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #0c4b33;'>📋 Prediction Result</h2>", unsafe_allow_html=True)
    result = 'You are not diabetic.' if prediction[0] == 0 else 'You are **at risk of diabetes.**'
    st.markdown(f"<p class='highlight'>{result}</p>", unsafe_allow_html=True)
    
    # Display model accuracy
    accuracy = accuracy_score(y_test, rf.predict(x_test)) * 100
    st.markdown(f"<p style='color: #4a7c59; font-size: 18px;'>Model Accuracy: {accuracy:.2f}%</p>", unsafe_allow_html=True)

else:
    st.markdown("<h3 style='text-align: center; color: #4a7c59;'>👈 Enter your data and click 'Analyze Risk'</h3>", unsafe_allow_html=True)
