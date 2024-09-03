if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))
    st.run(port=port)

import streamlit as st

st.title("Hello World App")
st.write("Hello, World! This is a simple Streamlit app deployed on IBM Cloud.")

