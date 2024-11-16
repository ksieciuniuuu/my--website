import streamlit as st
import csv
import os
import pandas as pd

from PyPDF2 import PdfWriter, PdfReader

# File paths for local storage
csv_file_path = "project_data.csv"

# CSV helper functions
def save_to_csv(data, file_path):
    """Save new data to CSV file."""
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Project Name", "Client Name", "Total Cost"])  # header
        writer.writerow(data)

def load_from_csv(file_path):
    """Load historical data from CSV file."""
    if not os.path.isfile(file_path):
        return pd.DataFrame(columns=["Project Name", "Client Name", "Total Cost"])
    return pd.read_csv(file_path)

def export_csv(data, file_name="project_data_export.csv"):
    """Export the data to a CSV file."""
    data.to_csv(file_name, index=False)
    return file_name

# Create PDF using PyPDF2
def create_pdf(title, content):
    pdf_writer = PdfWriter()
    pdf_writer.add_page()
    pdf_writer.set_font("Arial", size=12)
    pdf_writer.add_text(10, 10, title)
    pdf_writer.add_text(10, 20, content)

    output_pdf_path = "output.pdf"
    with open(output_pdf_path, "wb") as file:
        pdf_writer.write(file)

    return output_pdf_path

# User Interface for pricing logic
def user_interface():
    st.subheader("📋 User Interface: Pricing Tool")

    # Input fields
    col1, col2 = st.columns(2)

    with col1:
        market = st.selectbox("Market Selection", ["Market 1", "Market 2", "Market 3"], index=0)
        estimated_hours = st.number_input("Estimated Hours per Task", min_value=0.0, value=1.0)
        target_audience = st.text_input("Target Audience", "Default Audience")

    with col2:
        additional_options = st.multiselect("Additional Options", ["Option A", "Option B", "Option C"])
        base_cost = st.number_input("Base Cost (Fixed Hours)", min_value=0.0, value=10.0)
        hourly_rate = st.number_input("Hourly Rate", min_value=0.0, value=50.0)

    # Discount
    st.write("### Discount Options")
    discount_type = st.radio("Discount Type", ["Flat Rate", "Percentage"])
    discount_value = st.number_input("Discount Value", min_value=0.0, value=0.0)

    # Calculate pricing
    if st.button("Calculate Pricing"):
        total_cost = base_cost + (hourly_rate * estimated_hours)
        if discount_type == "Flat Rate":
            total_cost -= discount_value
        elif discount_type == "Percentage":
            total_cost -= total_cost * (discount_value / 100)

        # Display results
        st.write("### Pricing Breakdown")
        st.write(f"**Market:** {market}")
        st.write(f"**Estimated Hours:** {estimated_hours}")
        st.write(f"**Target Audience:** {target_audience}")
        st.write(f"**Base Cost:** {base_cost} hours")
        st.write(f"**Hourly Rate:** {hourly_rate} EUR/hour")
        st.write(f"**Discount Applied:** {discount_value} ({discount_type})")
        st.write(f"### **Total Cost:** {total_cost:.2f} EUR")

        # Save project data
        if st.button("Save Project"):
            save_to_csv([market, target_audience, total_cost], csv_file_path)
            st.success("Project saved successfully!")

# Historical Data functionality
def historical_data():
    st.subheader("📜 Historical Data")

    # Load historical data from CSV
    projects = load_from_csv(csv_file_path)

    # Display historical records
    st.write("### Saved Projects")
    if not projects.empty:
        st.dataframe(projects)
    else:
        st.info("No historical data found.")

    # Add a new record
    st.write("### Add New Project")
    market = st.text_input("Project Name")
    client_name = st.text_input("Client Name")
    total_cost = st.number_input("Total Cost (EUR)", min_value=0.0)

    if st.button("Save Project"):
        if market and client_name:
            save_to_csv([market, client_name, total_cost], csv_file_path)
            st.success("Project saved successfully!")
        else:
            st.warning("Please fill out all fields before saving.")

    # Export CSV button
    if st.button("Export Historical Data as CSV"):
        exported_file = export_csv(projects)
        st.download_button(
            label="Download CSV",
            data=open(exported_file, "rb").read(),
            file_name=exported_file,
            mime="text/csv"
        )

# Main function to display the app
def main():
    st.title("Pricing Tool")
    st.sidebar.title("Navigation")
    options = ["Home", "Historical Data", "Pricing Tool"]
    choice = st.sidebar.radio("Go to", options)

    if choice == "Home":
        st.write("Welcome to the Pricing Tool!")
    elif choice == "Historical Data":
        historical_data()
    elif choice == "Pricing Tool":
        user_interface()

if __name__ == "__main__":
    main()
