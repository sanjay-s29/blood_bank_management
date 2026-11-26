
import streamlit as st
import pandas as pd

from donor import (
    Donor,
    load_donors,
    save_donor,
    generate_donor_id,
    search_donor,
    update_donor,
    delete_donor
)

from inventory import (
    load_inventory,
    add_blood,
    remove_blood,
    BLOOD_GROUPS
)

from request import (
    BloodRequest,
    load_requests,
    save_request,
    update_request_status
)

from auth import login_page, logout

from donation import (
    load_donations,
    add_donation,
    generate_donation_id,
    search_donations,
    update_donation_status
)

from reports import (
    get_blood_group_statistics,
    get_monthly_donations,
    get_request_statistics,
    get_city_statistics,
    convert_to_csv
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Blood Bank Management System",
    page_icon="🩸",
    layout="wide"
)


# ==========================================
# LOAD DATA
# ==========================================

donors = load_donors()
inventory = load_inventory()
requests = load_requests()
donations = load_donations()


# ==========================================
# ADMIN LOGIN
# ==========================================

if not st.session_state.get("logged_in", False):
    login_page()
    st.stop()


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🩸 Blood Bank Management")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Donor Registration",
        "Donor Management",
        "Blood Inventory",
        "Blood Requests",
        "Donation History",
        "Reports & Analytics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("Admin Logged In")

if st.sidebar.button("Logout", width="stretch"):
    logout()
    st.rerun()


# ==========================================
# DASHBOARD
# ==========================================

if menu == "Dashboard":

    st.title("🩸 Blood Bank Dashboard")
    st.write("Welcome to Blood Bank Management System")

    donors = load_donors()
    inventory = load_inventory()
    requests = load_requests()
    donations = load_donations()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Donors", len(donors))
    col2.metric("Total Donations", len(donations))
    col3.metric("Total Requests", len(requests))
    col4.metric("Available Blood Units", sum(inventory.values()))

    st.markdown("---")

    st.subheader("Blood Inventory Overview")

    inventory_df = pd.DataFrame(
        list(inventory.items()),
        columns=["Blood Group", "Available Units"]
    )

    st.bar_chart(inventory_df.set_index("Blood Group"))

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Recent Donors")

        if donors:
            st.dataframe(
                pd.DataFrame(donors).tail(5),
                width="stretch"
            )
        else:
            st.info("No donors registered.")

    with col2:
        st.subheader("Recent Blood Requests")

        if requests:
            st.dataframe(
                pd.DataFrame(requests).tail(5),
                width="stretch"
            )
        else:
            st.info("No blood requests available.")


# ==========================================
# DONOR REGISTRATION
# ==========================================

elif menu == "Donor Registration":

    st.title("🧑 Donor Registration")

    with st.form("donor_registration"):

        name = st.text_input("Donor Name")

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=18
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        blood_group = st.selectbox(
            "Blood Group",
            BLOOD_GROUPS
        )

        phone = st.text_input("Phone Number")
        city = st.text_input("City")

        submit = st.form_submit_button(
            "Register Donor",
            width="stretch"
        )

        if submit:

            if not name.strip() or not phone.strip() or not city.strip():
                st.error("Please fill all fields.")

            elif not phone.strip().isdigit() or len(phone.strip()) != 10:
                st.error("Enter a valid 10-digit phone number.")

            else:

                donor_id = generate_donor_id()

                new_donor = Donor(
                    donor_id,
                    name.strip(),
                    age,
                    gender,
                    blood_group,
                    phone.strip(),
                    city.strip()
                )

                save_donor(new_donor)

                st.success(
                    f"Donor registered successfully! ID: {donor_id}"
                )

                st.rerun()


# ==========================================
# DONOR MANAGEMENT
# ==========================================

elif menu == "Donor Management":

    st.title("👥 Donor Management")

    donors = load_donors()

    search_keyword = st.text_input(
        "Search Donor by ID or Name"
    )

    if search_keyword.strip():
        filtered_donors = search_donor(search_keyword.strip())
    else:
        filtered_donors = donors

    if filtered_donors:

        st.dataframe(
            pd.DataFrame(filtered_donors),
            width="stretch"
        )

        donor_ids = [
            d.get("donor_id", "")
            for d in filtered_donors
        ]

        selected_id = st.selectbox(
            "Select Donor ID",
            donor_ids
        )

        selected_donor = next(
            (
                d for d in filtered_donors
                if d.get("donor_id") == selected_id
            ),
            None
        )

        if selected_donor:

            st.markdown("---")
            st.subheader("Update Donor Details")

            with st.form("update_donor"):

                updated_name = st.text_input(
                    "Name",
                    value=selected_donor.get("name", "")
                )

                updated_age = st.number_input(
                    "Age",
                    min_value=18,
                    max_value=100,
                    value=int(selected_donor.get("age", 18))
                )

                gender_options = ["Male", "Female", "Other"]
                current_gender = selected_donor.get("gender", "Male")

                updated_gender = st.selectbox(
                    "Gender",
                    gender_options,
                    index=(
                        gender_options.index(current_gender)
                        if current_gender in gender_options else 0
                    )
                )

                current_group = selected_donor.get("blood_group", "O+")

                updated_blood_group = st.selectbox(
                    "Blood Group",
                    BLOOD_GROUPS,
                    index=(
                        BLOOD_GROUPS.index(current_group)
                        if current_group in BLOOD_GROUPS else 0
                    )
                )

                updated_phone = st.text_input(
                    "Phone",
                    value=selected_donor.get("phone", "")
                )

                updated_city = st.text_input(
                    "City",
                    value=selected_donor.get("city", "")
                )

                update_button = st.form_submit_button(
                    "Update Donor",
                    width="stretch"
                )

                if update_button:

                    if not updated_name.strip() or not updated_city.strip():
                        st.error("Name and city are required.")

                    elif (
                        not updated_phone.strip().isdigit()
                        or len(updated_phone.strip()) != 10
                    ):
                        st.error("Enter a valid 10-digit phone number.")

                    else:

                        updated_data = {
                            "name": updated_name.strip(),
                            "age": updated_age,
                            "gender": updated_gender,
                            "blood_group": updated_blood_group,
                            "phone": updated_phone.strip(),
                            "city": updated_city.strip()
                        }

                        update_donor(selected_id, updated_data)

                        st.success("Donor updated successfully.")
                        st.rerun()

            st.markdown("---")

            if st.button("Delete Selected Donor"):

                delete_donor(selected_id)

                st.success("Donor deleted successfully.")
                st.rerun()

    else:
        st.info("No donor records found.")


# ==========================================
# BLOOD INVENTORY
# ==========================================

elif menu == "Blood Inventory":

    st.title("🩸 Blood Inventory Management")

    inventory = load_inventory()

    st.subheader("Available Blood Stock")

    inventory_df = pd.DataFrame(
        [
            {
                "Blood Group": group,
                "Available Units": units
            }
            for group, units in inventory.items()
        ]
    )

    st.dataframe(inventory_df, width="stretch")

    st.bar_chart(inventory_df.set_index("Blood Group"))

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("➕ Add Blood Units")

        with st.form("add_blood_form"):

            add_group = st.selectbox(
                "Blood Group",
                BLOOD_GROUPS,
                key="add_group"
            )

            add_units = st.number_input(
                "Units",
                min_value=1,
                step=1,
                key="add_units"
            )

            add_button = st.form_submit_button("Add Blood")

            if add_button:

                add_blood(add_group, add_units)

                st.success("Blood units added successfully.")
                st.rerun()

    with col2:

        st.subheader("➖ Remove Blood Units")

        with st.form("remove_blood_form"):

            remove_group = st.selectbox(
                "Blood Group",
                BLOOD_GROUPS,
                key="remove_group"
            )

            remove_units = st.number_input(
                "Units",
                min_value=1,
                step=1,
                key="remove_units"
            )

            remove_button = st.form_submit_button("Remove Blood")

            if remove_button:

                current_stock = inventory.get(remove_group, 0)

                if remove_units > current_stock:
                    st.error("Insufficient blood units.")

                else:
                    remove_blood(remove_group, remove_units)

                    st.success("Blood units removed successfully.")
                    st.rerun()


# ==========================================
# BLOOD REQUESTS
# ==========================================

elif menu == "Blood Requests":

    st.title("🏥 Blood Request Management")

    st.subheader("Create New Request")

    with st.form("blood_request_form"):

        patient_name = st.text_input("Patient Name")

        request_group = st.selectbox(
            "Required Blood Group",
            BLOOD_GROUPS
        )

        units = st.number_input(
            "Required Units",
            min_value=1,
            step=1
        )

        hospital = st.text_input("Hospital Name")
        contact = st.text_input("Contact Number")

        submit_request = st.form_submit_button(
            "Submit Request",
            width="stretch"
        )

        if submit_request:

            if (
                not patient_name.strip()
                or not hospital.strip()
                or not contact.strip()
            ):
                st.error("Please fill all fields.")

            elif not contact.strip().isdigit() or len(contact.strip()) != 10:
                st.error("Enter a valid 10-digit contact number.")

            else:

                new_request = BloodRequest(
                    patient_name.strip(),
                    request_group,
                    units,
                    hospital.strip(),
                    contact.strip()
                )

                save_request(new_request)

                st.success("Blood request submitted successfully.")
                st.rerun()

    st.markdown("---")

    st.subheader("All Blood Requests")

    requests = load_requests()

    if requests:

        st.dataframe(
            pd.DataFrame(requests),
            width="stretch"
        )

        request_ids = [
            r.get("request_id", "")
            for r in requests
        ]

        selected_request = st.selectbox(
            "Select Request ID",
            request_ids
        )

        new_status = st.selectbox(
            "Request Status",
            ["Pending", "Approved", "Rejected", "Completed"]
        )

        if st.button("Update Request Status"):

            result = update_request_status(
                selected_request,
                new_status
            )

            if result:
                st.success("Request status updated.")
                st.rerun()
            else:
                st.error("Unable to update request.")

    else:
        st.info("No requests available.")


# ==========================================
# DONATION HISTORY
# ==========================================

elif menu == "Donation History":

    st.title("🩸 Donation History")

    donors = load_donors()

    st.subheader("Record New Donation")

    if donors:

        donor_options = {
            f"{d.get('donor_id')} - {d.get('name')} ({d.get('blood_group')})": d
            for d in donors
        }

        with st.form("donation_form"):

            selected_label = st.selectbox(
                "Select Donor",
                list(donor_options.keys())
            )

            donation_date = st.date_input("Donation Date")

            units = st.number_input(
                "Units Donated",
                min_value=1,
                max_value=5,
                value=1
            )

            notes = st.text_area("Notes")

            submit_donation = st.form_submit_button(
                "Save Donation",
                width="stretch"
            )

            if submit_donation:

                selected_donor = donor_options[selected_label]

                donation_data = {
                    "donation_id": generate_donation_id(),
                    "donor_id": selected_donor.get("donor_id"),
                    "donor_name": selected_donor.get("name"),
                    "blood_group": selected_donor.get("blood_group"),
                    "donation_date": str(donation_date),
                    "units": units,
                    "notes": notes,
                    "status": "Pending Screening"
                }

                add_donation(donation_data)

                st.success("Donation record saved.")
                st.rerun()

    else:
        st.warning("Please register a donor first.")

    st.markdown("---")

    st.subheader("Donation Records")

    donations = load_donations()

    search_value = st.text_input(
        "Search Donation ID or Donor Name"
    )

    if search_value.strip():
        filtered_donations = search_donations(search_value.strip())
    else:
        filtered_donations = donations

    if filtered_donations:

        st.dataframe(
            pd.DataFrame(filtered_donations),
            width="stretch"
        )

        donation_ids = [
            d.get("donation_id", "")
            for d in filtered_donations
        ]

        selected_donation = st.selectbox(
            "Select Donation ID",
            donation_ids
        )

        donation_status = st.selectbox(
            "Screening Status",
            [
                "Pending Screening",
                "Approved",
                "Rejected",
                "Deferred"
            ]
        )

        if st.button("Update Donation Status"):

            result = update_donation_status(
                selected_donation,
                donation_status
            )

            if result:
                st.success("Donation status updated.")
                st.rerun()
            else:
                st.error("Donation record not found.")

    else:
        st.info("No donation records available.")


# ==========================================
# REPORTS & ANALYTICS
# ==========================================

elif menu == "Reports & Analytics":

    st.title("📊 Reports & Analytics")

    st.write(
        "Analyze donor, donation, blood request "
        "and inventory information."
    )

    donors = load_donors()
    donations = load_donations()
    requests = load_requests()
    inventory = load_inventory()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Donors", len(donors))
    col2.metric("Total Donations", len(donations))
    col3.metric("Total Requests", len(requests))
    col4.metric("Available Units", sum(inventory.values()))

    st.markdown("---")

    # Blood group statistics

    st.subheader("🩸 Blood Group Statistics")

    blood_group_data = get_blood_group_statistics(donors)

    if blood_group_data:

        blood_group_df = pd.DataFrame(
            list(blood_group_data.items()),
            columns=["Blood Group", "Donor Count"]
        )

        st.bar_chart(
            blood_group_df.set_index("Blood Group")
        )

        st.dataframe(blood_group_df, width="stretch")

    else:
        st.info("No donor data available.")

    st.markdown("---")

    # Monthly donation statistics

    st.subheader("📅 Monthly Donation Statistics")

    monthly_data = get_monthly_donations(donations)

    if monthly_data:

        monthly_df = pd.DataFrame(
            list(monthly_data.items()),
            columns=["Month", "Donation Records"]
        )

        st.line_chart(
            monthly_df.set_index("Month")
        )

        st.dataframe(monthly_df, width="stretch")

    else:
        st.info("No donation records available.")

    st.markdown("---")

    # Request statistics

    st.subheader("🏥 Request Status Statistics")

    request_data = get_request_statistics(requests)

    if request_data:

        request_df = pd.DataFrame(
            list(request_data.items()),
            columns=["Status", "Request Count"]
        )

        st.bar_chart(
            request_df.set_index("Status")
        )

        st.dataframe(request_df, width="stretch")

    else:
        st.info("No request data available.")

    st.markdown("---")

    # City statistics

    st.subheader("📍 City-wise Donor Statistics")

    city_data = get_city_statistics(donors)

    if city_data:

        city_df = pd.DataFrame(
            list(city_data.items()),
            columns=["City", "Donor Count"]
        )

        st.bar_chart(
            city_df.set_index("City")
        )

        st.dataframe(city_df, width="stretch")

    else:
        st.info("No city data available.")

    st.markdown("---")

    # CSV reports

    st.subheader("📥 Download Reports")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        donor_csv = convert_to_csv(donors)

        st.download_button(
            "Donors CSV",
            data=donor_csv,
            file_name="donor_report.csv",
            mime="text/csv",
            disabled=not bool(donor_csv)
        )

    with col2:

        donation_csv = convert_to_csv(donations)

        st.download_button(
            "Donations CSV",
            data=donation_csv,
            file_name="donation_report.csv",
            mime="text/csv",
            disabled=not bool(donation_csv)
        )

    with col3:

        request_csv = convert_to_csv(requests)

        st.download_button(
            "Requests CSV",
            data=request_csv,
            file_name="request_report.csv",
            mime="text/csv",
            disabled=not bool(request_csv)
        )

    with col4:

        inventory_records = [
            {
                "Blood Group": group,
                "Available Units": units
            }
            for group, units in inventory.items()
        ]

        inventory_csv = convert_to_csv(inventory_records)

        st.download_button(
            "Inventory CSV",
            data=inventory_csv,
            file_name="inventory_report.csv",
            mime="text/csv",
            disabled=not bool(inventory_csv)
        )


# ==========================================
# FOOTER
# ==========================================

st.sidebar.markdown("---")
st.sidebar.caption("Blood Bank Management System")
st.sidebar.caption("Python | Streamlit | JSON")
