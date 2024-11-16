import streamlit as st
import csv
import os
import json
from fpdf import FPDF

# File paths for local storage
csv_file_path = "project_data.csv"
json_file_path = "project_data.json"

# CSV helper functions
def save_to_csv(data, file_path):
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Project Name", "Client Name", "Total Cost"])
        writer.writerow(data)

def load_from_csv(file_path):
    if not os.path.isfile(file_path):
        return []
    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row
        return list(reader)

# JSON helper functions
def save_to_json(data, file_path):
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    # Append new data
    existing_data.append(data)

    # Save to JSON
    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)

def load_from_json(file_path):
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

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

# Admin Panel for managing Addons and Rates
def admin_panel():
    st.subheader("⚙️ Admin Panel")

    # Hourly rates configuration
    st.write("### Configure Hourly Rates")
    default_hourly_rate = st.number_input("Default Hourly Rate (EUR)", min_value=0.0, value=50.0)

    # Addons management
    st.write("### Manage Addons")
    addon_name = st.text_input("Addon Name")
    addon_hours = st.number_input("Hours for Addon", min_value=0.0, value=1.0)
    addon_cost = st.number_input("Cost for Addon (EUR)", min_value=0.0, value=10.0)

    if st.button("Save Addon"):
        # Placeholder for saving addons to a database or file
        st.success(f"Addon '{addon_name}' saved with {addon_hours} hours and {addon_cost} EUR.")

    # Save hourly rates to shared storage (e.g., file or SharePoint integration)
    if st.button("Save Hourly Rate"):
        st.success(f"Default hourly rate set to {default_hourly_rate} EUR/hour.")

# Historical Data functionality
def historical_data():
    st.subheader("📜 Historical Data")

    # Load historical data from CSV
    projects = load_from_csv(csv_file_path)

    # Display historical records
    st.write("### Saved Projects")
    if projects:
        for project in projects:
            st.write(f"**Project Name:** {project[0]}")
            st.write(f"**Client Name:** {project[1]}")
            st.write(f"**Total Cost:** {project[2]} EUR")
            st.write("---")
    else:
        st.info("No historical data found.")

    # Add a new record
    st.write("### Add New Project")
    project_name = st.text_input("Project Name")
    client_name = st.text_input("Client Name")
    total_cost = st.number_input("Total Cost (EUR)", min_value=0.0)

    if st.button("Save Project"):
        if project_name and client_name:
            save_to_csv([project_name, client_name, total_cost], csv_file_path)
            st.success("Project saved successfully!")
        else:
            st.warning("Please fill out all fields before saving.")

# PDF Export functionality
def export_pdf():
    st.subheader("📄 Export PDF")

    notes = st.text_area("Additional Notes")
    include_terms = st.checkbox("Include Terms")
    include_policy = st.checkbox("Include Privacy Policy")

    if st.button("Generate PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Pricing Tool Report", ln=True, align="C")
        pdf.ln(10)
        pdf.multi_cell(0, 10, txt=f"Additional Notes:\n{notes}")
        if include_terms:
            pdf.multi_cell(0, 10, txt="\nTerms and Conditions:\n[Placeholder terms]")
        if include_policy:
            pdf.multi_cell(0, 10, txt="\nPrivacy Policy:\n[Placeholder policy]")

        pdf_file = BytesIO()
        pdf.output(pdf_file)
        pdf_file.seek(0)

        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name="pricing_tool_report.pdf",
            mime="application/pdf",
        )
        st.success("PDF generated!")

# Main function to display the app
def main():
    st.title("Pricing Tool")
    st.sidebar.title("Navigation")
    options = ["Home", "Historical Data", "Admin Panel", "Pricing Tool"]
    choice = st.sidebar.radio("Go to", options)

    if choice == "Home":
        st.write("Welcome to the Pricing Tool!")
    elif choice == "Historical Data":
        historical_data()
    elif choice == "Admin Panel":
        admin_panel()
    elif choice == "Pricing Tool":
        user_interface()

if __name__ == "__main__":
    main()
