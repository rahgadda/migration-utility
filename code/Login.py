import streamlit as st
from lib.authentication import GoogleAuthenticator

authenticator = GoogleAuthenticator()

# Define the login route
@st.cache(allow_output_mutation=True)
def get_authorization_url():
    return authenticator.get_authorization_url()

# Define the callback route
@st.cache(allow_output_mutation=True)
def fetch_token(code):
    token = authenticator.fetch_token(code)
    return token

# Streamlit app
def main():
    st.title('Google Login with Authlib and Streamlit')

    if 'token' not in st.session_state:
        auth_url, _ = get_authorization_url()
        code = st.experimental_get_query_params().get('code', [None])[0]
        if code:
            token = fetch_token(code)
            st.session_state['token'] = token

            # Redirect the user to remove the 'code' from the URL
            st.experimental_set_query_params()
            st.experimental_rerun()

        st.markdown(f"You need to log in with Google to proceed. [Log in]({auth_url})")

    else:
        st.write("You are logged in!")
        st.write(st.session_state['token'])

if __name__ == '__main__':
    main()
