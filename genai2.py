import streamlit as st 
import google.generativeai as genai
import fitz 

genai.configure(api_key="AIzaSyAH4SSMUnCvVRGZW7_qOVjXMyOD5ewpH9M")

model = genai.GenerativeModel('gemini-1.5-flash')

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

st.set_page_config(page_title="Gemini Chatbot with PDF", page_icon="🤖")
st.title("Gemini AI Chatbot with PDF training")

# PDF upload functionality
uploaded_pdf = st.file_uploader("Upload your PDF", type="pdf")
if uploaded_pdf is not None:
    # Extract text from PDF
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    pdf_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pdf_text += page.get_text()

    # Display first 1000 characters
    st.write(pdf_text[:1000])

    # Save extracted text to session state
    st.session_state.pdf_text = pdf_text

# Chat functionality
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask a question related to the PDF...")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Add extracted PDF text to context (if available)
    # if "pdf_text" in st.session_state:
    #     pdf_content = st.session_state.pdf_text[:2000]
    #     input_text = f"{pdf_content}\n\nUser query: {user_input}"
    # else:
    #     input_text = user_input

    pdf_content = st.session_state.pdf_text[:2000]
    input_text = (
        "You are a helpful assistant specialised in Data Science only."
        "You must answer **only** question related to Data Science topics(e.g Machine learning,Stastics,Data analysis,Ai etc.)"
        "If a question is outside of the sscope of Data Science,ploitely respond with:"
        "'Sorry, I can only answer question related to Data Science.'\n\n"
        f"PDF context :\n{pdf_content}\n\nUser query:{user_input}"
    )

    try:
        response = st.session_state.chat.send_message(input_text)
        answer = response.text
    except Exception as e:
        answer = f"Error: {e}"

    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
