import pandas as pd
import streamlit as st

# Embed the expanded reference data directly into the program
REFERENCE_DATA = {
    "SL No": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "Curcumin (Purity)": [78.13, 77.33, 78.27, 78.23, 78.21, 77.73, 77.33, 77.91, 78.16, 77.61, 77.8, 78.35, 78.6, 78.38, 78.76],
    "DMC (Purity)": [18.27, 18.86, 18.58, 18.62, 18.61, 18.92, 18.86, 18.7, 18.73, 18.83, 18.59, 18.78, 18.33, 18.74, 18.29],
    "BDMC (Purity)": [3.6, 3.81, 3.15, 3.15, 3.18, 3.35, 3.81, 3.39, 3.11, 3.56, 3.61, 2.87, 3.07, 2.88, 2.95],
}

def load_reference_data():
    # Convert embedded reference data into a DataFrame
    df = pd.DataFrame(REFERENCE_DATA)
    
    # Calculate ratios for the regular dataset
    df['Curcumin_to_DMC'] = df['Curcumin (Purity)'] / df['DMC (Purity)']
    df['Curcumin_to_BDMC'] = df['Curcumin (Purity)'] / df['BDMC (Purity)']
    df['DMC_to_BDMC'] = df['DMC (Purity)'] / df['BDMC (Purity)']
    
    return df

def calculate_statistics(df):
    # Calculate mean and standard deviation for each component and each ratio
    return {
        'Curcumin_mean': df['Curcumin (Purity)'].mean(),
        'Curcumin_std': df['Curcumin (Purity)'].std(),
        'DMC_mean': df['DMC (Purity)'].mean(),
        'DMC_std': df['DMC (Purity)'].std(),
        'BDMC_mean': df['BDMC (Purity)'].mean(),
        'BDMC_std': df['BDMC (Purity)'].std(),
        'Curcumin_to_DMC_mean': df['Curcumin_to_DMC'].mean(),
        'Curcumin_to_DMC_std': df['Curcumin_to_DMC'].std(),
        'Curcumin_to_BDMC_mean': df['Curcumin_to_BDMC'].mean(),
        'Curcumin_to_BDMC_std': df['Curcumin_to_BDMC'].std(),
        'DMC_to_BDMC_mean': df['DMC_to_BDMC'].mean(),
        'DMC_to_BDMC_std': df['DMC_to_BDMC'].std()
    }

def check_sample_conformity(sample, reference_stats):
    # Calculate z-scores for each component in the sample
    z_scores = {
        'Curcumin': (sample['Curcumin'] - reference_stats['Curcumin_mean']) / reference_stats['Curcumin_std'],
        'DMC': (sample['DMC'] - reference_stats['DMC_mean']) / reference_stats['DMC_std'],
        'BDMC': (sample['BDMC'] - reference_stats['BDMC_mean']) / reference_stats['BDMC_std'],
        'Curcumin_to_DMC': (sample['Curcumin'] / sample['DMC'] - reference_stats['Curcumin_to_DMC_mean']) / reference_stats['Curcumin_to_DMC_std'],
        'Curcumin_to_BDMC': (sample['Curcumin'] / sample['BDMC'] - reference_stats['Curcumin_to_BDMC_mean']) / reference_stats['Curcumin_to_BDMC_std'],
        'DMC_to_BDMC': (sample['DMC'] / sample['BDMC'] - reference_stats['DMC_to_BDMC_mean']) / reference_stats['DMC_to_BDMC_std']
    }
    
    # Check if all z-scores are within an acceptable range (e.g., between -2 and 2)
    is_within_bounds = all(abs(z) <= 2 for z in z_scores.values())
    result = "Conforms to natural variation" if is_within_bounds else "Outlier - Does not conform to natural variation"
    
    return result, z_scores

# Streamlit App
def main():
    st.title("Curcumin Test Batch Analysis")

    # Load reference data
    regular_df = load_reference_data()
    regular_stats = calculate_statistics(regular_df)
    
    # Input test batch values
    st.header("Enter Test Batch Results")
    curcumin = st.number_input("Curcumin (Purity)", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
    dmc = st.number_input("DMC (Purity)", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
    bdmc = st.number_input("BDMC (Purity)", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
    
    if st.button("Analyze"):
        sample_input = {'Curcumin': curcumin, 'DMC': dmc, 'BDMC': bdmc}
        
        # Check conformity
        result, z_scores = check_sample_conformity(sample_input, regular_stats)
        
        # Display results
        st.header("Results")
        st.write(" - **Conformity Result**: ", result)
        st.write(" - **Z-scores**: ")
        st.json(z_scores)

# Run the Streamlit app
if __name__ == "__main__":
    main()
