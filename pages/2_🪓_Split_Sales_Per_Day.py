import streamlit as st
import pandas as pd
import io
import zipfile
from datetime import datetime

# Import your custom function
from scripts.process_spdpp import split_by_brand

# Define Streamlit app
def main():
    # Set app title
    st.title("🪓 Split the SPDPP report by Brand")
    st.write('''The 'Sales Per Day Per Product' report is an important report that we use in
             many ways. Often, this dataset gets too large. Therefore, this script will allow you
             to split this data by brand.
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
            dfs = split_by_brand(df)
            # Create an in-memory ZIP file
            zip_file = io.BytesIO()

            with zipfile.ZipFile(zip_file, 'w') as zf:
                # Write each transformed dataframe as a separate CSV file in the ZIP
                for brand, brand_df in dfs:
                    csv_data = brand_df.to_csv(index=False)
                    zf.writestr(f"{today}_{brand}_SalesPerDay.csv", csv_data)

            # Provide download link for the ZIP file
            st.header("Download Transformed CSV Files (as ZIP)")
            st.download_button(
                label="Download ZIP",
                data=zip_file.getvalue(),
                file_name="transformed_data.zip",
                mime="application/zip"
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