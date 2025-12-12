import streamlit as st
import pandas as pd

# 1. WEBSITE TITLE AND DESCRIPTION
st.title("My Data Dashboard")
st.write("""
This is a simple website to present my data.
I can write paragraphs here to explain my findings.
**Below is a graph showing our progress:**
""")

# 2. CREATE THE DATA
# This dictionary holds the data. You can change the numbers here later.
data = {
    'Category': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'Revenue': [150, 200, 180, 250, 310],
    'Expenses': [100, 120, 110, 130, 150]
}

# Convert the dictionary into a "DataFrame" (a table format Python understands)
df = pd.DataFrame(data)

# 3. SHOW THE DATA TABLE
st.subheader("The Raw Data")
st.write("Here is the data used for the graph below:")
st.dataframe(df)

# 4. SHOW THE GRAPH
st.subheader("Revenue vs Expenses")
# Set the 'Category' column as the bottom axis (X-axis)
st.bar_chart(df.set_index('Category'))

# 5. SIDEBAR (Optional)
st.sidebar.header("About")
st.sidebar.write("This dashboard was built using Python and Streamlit.")