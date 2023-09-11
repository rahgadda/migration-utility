import streamlit as st
from lib.authentication import GoogleAuthenticator

# Initialize GoogleAuthenticator
authenticator = GoogleAuthenticator()

# Streamlit app
st.title("Streamlit App with Google Authentication")

# Login button
if st.button("Login with Google"):
    session = authenticator.create_session()
    authorization_url, state = authenticator.get_authorization_url(session)
    access_token = authenticator.fetch_token(session)

    if access_token:
        user_info = authenticator.get_user_info(session)

        st.write("Logged in as:")
        st.write(f"Name: {user_info['name']}")
        st.write(f"Email: {user_info['email']}")
    else:
        st.error("Authentication failed")

# Logout button
if st.button("Logout"):
    st.warning("Logged out")
