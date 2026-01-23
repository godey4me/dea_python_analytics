import streamlit as st

st.title("Basic Web App")

# Helper Functions

## validate_email()
def validate_email(email_str: str) -> bool:

    result = False

    if '@' in email_str:
        result = True
    
    return result

# Column Layout
general_col, password_col = st.columns(spec=2, gap='medium')

# Sign Up Form
with general_col:

    username = st.text_input(label="", placeholder='john_doe', key='username')
    email = st.text_input(label="", placeholder='john_doe@gmail.com', key='email')

with password_col:
    password = st.text_input(label="", type='password', key='first_password')
    verify_password = st.text_input(label="", type='password', key='second_password')

print(username)
print(password)
print(verify_password)

# Processing button
if st.button("Register"):

    # Validate the email
    if validate_email(email):
        st.success("User has been registered successfully.")
        st.write("Response")
        st.json({
            'user': username,
            'email': email,
            'password': password
        })
    else:
        st.error("Email is not valid. Try again.")