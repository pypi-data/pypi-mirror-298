import streamlit as st
from my_component import custom_checkbox

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/example.py`

st.subheader("Component with constant args")

# Create an instance of our component with a constant `name` arg, and
# print its output value.
options=["Option 1", "Option 2", "Option 3"]
options_selected = custom_checkbox(options, default_option='All', label="Select an option")

st.markdown("---")
st.write(options_selected)

