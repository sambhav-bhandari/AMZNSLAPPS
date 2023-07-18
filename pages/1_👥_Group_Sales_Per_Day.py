import streamlit as st
import pandas as pd
from datetime import datetime

# Import your custom function
from scripts.process_spdpp import aggregate

# Define Streamlit app
def main():
    # Set app title
    st.title("👥 Group the SPDPP report from Seller Legend")
    st.write('''The 'Sales Per Day Per Product' report is an important report that we use in
             many ways. Often, this dataset gets too large. Therefore, this script will allow you
             to group this data on a monthly basis. Think of it as 'Sales Per Month Per Product'.
             
             For example: sales placed on June 28, 2022 will be attributed to June 1, 2022.
             ''')

    # File upload
    st.header("Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    st.sidebar.header("Transformation Options")
    include_sku = st.sidebar.checkbox("Include SKU?", value=False)

    if uploaded_file is not None:
        today = datetime.today().strftime('%Y-%m-%d')
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        # Perform transformation using my_func
        try:
            df = aggregate(df, include_sku=include_sku)
            # Provide download link for transformed CSV
            st.header("Transformed CSV File")
            st.download_button(
                label="Download Transformed CSV",
                data=df.to_csv(index=False),
                file_name=f"{today}_grouped_SPDPP.csv",
                mime="text/csv"
            )
        except pd.errors.ParserError as e:
            st.error("Error: Invalid CSV file format. Please provide a valid CSV file.")
        except KeyError as e:
            st.error(f"Error: '{e.args[0]}' column not found in the CSV file.")
        except Exception as e:
            st.error("Error: " + str(e))
            st.info("Please ensure that the uploaded CSV file meets the specific requirements for transformation.")

# Run the app
if __name__ == "__main__":
    main()