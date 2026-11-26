
import hashlib
import hmac
import streamlit as st


# DEMO ADMIN CREDENTIALS
ADMIN_USERNAME = "admin"

# Demo password: Admin@123
ADMIN_PASSWORD_HASH = hashlib.sha256(
    "Admin@123".encode()
).hexdigest()


def verify_login(username, password):

    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    return (
        username == ADMIN_USERNAME
        and hmac.compare_digest(
            password_hash,
            ADMIN_PASSWORD_HASH
        )
    )


def login_page():

    st.title("🩸 Blood Bank Admin Login")

    st.write("Please login to access the management system.")

    with st.form("admin_login"):

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        submit = st.form_submit_button("Login")

        if submit:

            if verify_login(username, password):

                st.session_state["logged_in"] = True

                st.success("Login successful!")

                st.rerun()

            else:

                st.error("Invalid username or password!")


def logout():

    st.session_state["logged_in"] = False

    st.rerun()
