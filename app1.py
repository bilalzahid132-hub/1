import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Neighborhood Analysis", layout="wide")

st.title("Honor's Project: Neighborhood Feature Analysis")
st.markdown("""
**Research Question:** What features contribute to the niche score?
This dashboard analyzes relationships between Walkability, Rent, Commute Times, and Evictions across different subway stations/neighborhoods.
""")

# --- SECTION 1: LOAD THE DATA ---
# I have manually extracted this data from your uploaded PDF/Docx files
data = {
    'Neighborhood': ['Flushing-Main St', 'Mets-Willets Point', 'Jackson Heights (74 St)', 'Corona Plaza', 'Elmhurst', 'Queensboro Plaza'],
    'Zip Code': ['11354', '11354', '11372', '11368', '11373', '11101'],
    'Walk Score': [100, 52, 86, 98, 97, 96],
    # Converted Niche Scores to numbers for plotting: B+=3.3, B=3.0, B-=2.7
    'Niche Score Grade': ['B+', 'B', 'B+', 'B-', 'B+', 'N/A'],
    'Niche Score Numeric': [3.3, 3.0, 3.3, 2.7, 3.3, None], 
    'Residential Evictions': [90, 90, 125, 235, 110, 85],
    # Average rent taken from the range provided (e.g., $1759-$2794 -> avg $2276)
    'Avg Rent ($)': [2276, 2225, 2500, None, None, None],
    # Avg commute to Empire State Building (taken from your table)
    'Commute to ESB (min)': [32.5, 27.5, 22.5, None, None, None]
}

df = pd.DataFrame(data)

st.subheader("1. The Dataset")
st.write("Data extracted from Honor's Project 1.1 and 1.3 files.")
st.dataframe(df)

# --- SECTION 2: ANALYSIS PLOTS ---
st.header("2. Analysis Plots")
st.write("Visualizing relationships to answer: *What features contribute to the niche score?*")

# Create two columns for side-by-side graphs
col1, col2 = st.columns(2)

# --- PLOT 1: Walkability vs Niche Score (Scatter Plot) ---
with col1:
    st.subheader("Walkability vs. Niche Score")
    st.caption("Does a higher Walk Score mean a better Niche Score?")
    
    # Filter out missing niche scores
    df_niche = df.dropna(subset=['Niche Score Numeric'])
    
    fig1, ax1 = plt.subplots()
    ax1.scatter(df_niche['Walk Score'], df_niche['Niche Score Numeric'], color='#1f77b4', s=100, alpha=0.8)
    
    # Add labels to points so we know which dot is which neighborhood
    for i, txt in enumerate(df_niche['Neighborhood']):
        ax1.annotate(txt, (df_niche['Walk Score'].iloc[i], df_niche['Niche Score Numeric'].iloc[i]), fontsize=8)

    ax1.set_xlabel("Walk Score")
    ax1.set_ylabel("Niche Score (Numeric: B=3.0, B+=3.3)")
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.set_title("Relationship: Walkability vs Niche")
    
    st.pyplot(fig1)

# --- PLOT 2: Evictions by Zip Code (Bar Chart) ---
with col2:
    st.subheader("Residential Evictions by Area")
    st.caption("Which neighborhoods are less stable?")
    
    fig2, ax2 = plt.subplots()
    # Group by Zip Code to avoid duplicates if multiple stations are in one zip
    eviction_data = df.groupby('Zip Code')['Residential Evictions'].max()
    
    eviction_data.plot(kind='bar', color='#ff7f0e', ax=ax2)
    ax2.set_ylabel("Number of Evictions")
    ax2.set_title("Evictions per Zip Code")
    plt.xticks(rotation=45)
    
    st.pyplot(fig2)

# --- PLOT 3: Commute vs Rent (Scatter/Line) ---
st.subheader("Commute Time vs. Rent Price")
st.caption("Do people pay more for a shorter commute to the Empire State Building?")

# Filter data that has Rent and Commute info
df_rent = df.dropna(subset=['Avg Rent ($)', 'Commute to ESB (min)'])

fig3, ax3 = plt.subplots()
ax3.scatter(df_rent['Commute to ESB (min)'], df_rent['Avg Rent ($)'], color='green', s=150)

# Connect the dots to show the trend clearly
ax3.plot(df_rent['Commute to ESB (min)'], df_rent['Avg Rent ($)'], linestyle='--', color='gray', alpha=0.5)

# Add labels
for i, txt in enumerate(df_rent['Neighborhood']):
    ax3.annotate(txt, (df_rent['Commute to ESB (min)'].iloc[i], df_rent['Avg Rent ($)'].iloc[i]+50))

ax3.set_xlabel("Commute Time to Empire State Building (Minutes)")
ax3.set_ylabel("Average Rent ($)")
ax3.set_title("Cost of Convenience: Rent vs Commute")
ax3.grid(True)

st.pyplot(fig3)

# --- SECTION 3: CONCLUSIONS ---
st.header("3. Conclusions & Findings")
st.markdown("""
### Analysis of Relationships
Based on the data visualized above and the FiveThirtyEight model comparisons:

1.  **Commute vs. Rent:** Jackson Heights (74 St-Broadway) is approximately **$560 more expensive** per month than Flushing, which aligns with the expectation that shorter commutes lead to higher rent. However, Flushing's upper rent range overlaps with Jackson Heights despite the longer commute, suggesting other factors are at play.
2.  **Walkability vs. Niche Score:** There is a **mismatch** in the data. For example, Corona Plaza has a very high Walk Score (98) but a lower Niche Score (B-) compared to Elmhurst (Walk 97, Niche B+).
3.  **Low Walkability Anomaly:** Mets-Willets Point has the lowest Walk Score (52) but maintains a decent Niche Score (B), which is better than Corona Plaza (B-).

**Final Conclusion:** While commuting time influences rent, the data suggests that **neighborhood demand and amenities** play a major role in shaping housing prices and Niche scores, often overriding raw metrics like Walkability.
""")
