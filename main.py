import streamlit as st
from pint import UnitRegistry

# Initialize unit registry
ureg = UnitRegistry()
st.set_page_config(page_title="Unit Converter", layout="wide")

# Unit categories
categories = {
    "Length": ["meter", "kilometer", "centimeter", "millimeter", "mile", "yard", "foot", "inch"],
    "Weight": ["gram", "kilogram", "pound", "ounce"],
    "Volume": ["liter", "milliliter", "gallon", "cubic meter"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Time": ["second", "minute", "hour", "day"]
}

# Set page title
st.title("Scientific Unit Converter")

# Initialize session state for category selection
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "Length"

# Navbar Styling
st.markdown("""
    <style>
        .nav-container {
            display: flex;
            justify-content: center;
            gap: 5px; /* Reduced gap between buttons */
            margin-bottom: 20px;
        }
        .nav-button {
            background-color: red;
            color: white;
            border: none;
            padding: 5px 12px; /* Reduced padding for compact size */
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px; /* Slightly smaller font for better fit */
            transition: background-color 0.3s;
        }
        .nav-button:hover {
            background-color: yellow;
            color: black;
        }
        .active {
            background-color: white !important;
            color: black !important;
            border: 2px solid red;
        }
    </style>
""", unsafe_allow_html=True)

# Navbar UI
st.markdown('<div class="nav-container">', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])  # Equal width columns for alignment

for idx, category in enumerate(categories.keys()):
    button_key = f"{category}_btn"
    is_active = st.session_state.selected_category == category

    with [col1, col2, col3, col4, col5][idx]:  # Assigning each category to its column
        if st.button(category, key=button_key):
            st.session_state.selected_category = category

st.markdown("</div>", unsafe_allow_html=True)

# Show converter for the selected category
category = st.session_state.selected_category
st.subheader(f"{category} Converter")

# Select units
from_unit = st.selectbox("From", categories[category])
to_unit = st.selectbox("To", categories[category])

# Input value
value = st.number_input("Enter value", min_value=0.0, step=0.1)

# Convert button
if st.button("Convert"):
    try:
        if category == "Temperature":
            # Temperature conversions
            if from_unit == "celsius" and to_unit == "fahrenheit":
                result = (value * 9/5) + 32
            elif from_unit == "fahrenheit" and to_unit == "celsius":
                result = (value - 32) * 5/9
            elif from_unit == "celsius" and to_unit == "kelvin":
                result = value + 273.15
            elif from_unit == "kelvin" and to_unit == "celsius":
                result = value - 273.15
            else:
                result = value
        else:
            # General unit conversions
            result = (value * ureg(from_unit)).to(to_unit).magnitude

        st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")
    except Exception as e:
        st.error(f"Conversion Error: {e}")
