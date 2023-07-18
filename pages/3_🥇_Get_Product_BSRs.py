import streamlit as st
import pandas as pd
from datetime import datetime

# Import your custom function
from scripts.get_bsr_from_product_list import get_bsr

# Define Streamlit app
def main():
    # Set app title
    st.title("🥇 Get BSR from Products List")
    st.write('''The 'Products List' report on Seller Legend contains regularly updated BSR rankings
             at the main category and sub-category levels. However, this information is presented
             to us in an unstructured manner. This script structures the same.
             ''')

    # File upload
    st.header("Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        today = datetime.today().strftime('%Y-%m-%d')
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        # Perform transformation using my_func
        try:
            df = get_bsr(df, date=today)
            st.header("Transformed CSV File")
            st.download_button(
                label="Download Transformed CSV",
                data=df.to_csv(index=False),
                file_name=f"{today}_BSR_Products.csv",
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