import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Hospital Patient Admission Trends Dashboard")

# 1. Allow the user to upload the hospital dataset
st.header("1. Upload Hospital Dataset")
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    # 2. Display head and tail
    st.header("2. Preview Head and Tail of Uploaded Data")

    st.subheader("Head of Dataset")
    st.dataframe(df.head())

    st.subheader("Tail of Dataset")
    st.dataframe(df.tail())

    # 3. Summary statistics
    st.header("3. Summary of Statistical Properties on Numerical Data")
    st.dataframe(df.describe())

    # 4. Calculate and display number of admissions per month
    st.header("4. Number of Admissions Per Month")

    if "D.O.A" in df.columns:
        df["D.O.A"] = pd.to_datetime(df["D.O.A"], errors="coerce")

        monthly_admissions = (
            df.groupby(df["D.O.A"].dt.to_period("M"))
            .size()
            .reset_index(name="Number of Admissions")
        )

        monthly_admissions["D.O.A"] = monthly_admissions["D.O.A"].astype(str)
        monthly_admissions = monthly_admissions.rename(columns={"D.O.A": "Month-Year"})

        st.dataframe(monthly_admissions)

        # 5. Visualize monthly admissions
        st.header("5. Monthly Admissions Visualization")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(
            monthly_admissions["Month-Year"],
            monthly_admissions["Number of Admissions"],
            marker="o"
        )

        ax.set_title("Monthly Patient Admissions Over Time")
        ax.set_xlabel("Month-Year")
        ax.set_ylabel("Number of Admissions")
        plt.xticks(rotation=45)

        st.pyplot(fig)

        st.write(
            "This chart shows the number of patient admissions for each month. "
            "It helps identify periods with high or low hospital admissions over time."
        )

    else:
        st.error("The dataset must contain a date column named 'D.O.A'.")

else:
    st.info("Please upload the hospital dataset to begin.")