import streamlit as st
import google.generativeai as genai
import fitz

genai.configuration(api_key="AIzaSyC0Y9DIz5zwgFhw_O6_xjN7VlJo5_MsRtQ")
model=genai.Generativemodel('gemini-1.5-flash')
if "chat" not in st.session_state:
    st.session_state.chat=model.start_chat(history=[])
    st.session_state.message=[]

st.set_page_config(page_title="Gemini Chatbot wth PDF", page_icon="🤖")
st.title("Gemini AI Chatbot with pdf training")

#pdf upload functionality
uploaded_pdf=st.file_uploader("Upload your pdf",type="pdf")
if uploaded_pdf is not None:
    #Exact text from PDF
    doc=fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    pdf_text=""
    for page_num in range(len(doc)):
        page=doc.load_page(page_num)
        pdf_text+=page.get_text()
#Display first 1000 character
st.write(pdf_text[:1000])

#option to use this extracted text to train or rspond to queries
st.session_state.pdf_text=pdf_text
#Chat functionality
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input=st.chat_inpt("Ask a question related to the PDF..")
if user_input:
  st.chat_message("user").markdown(user_input)
  st.session_state.messges.append({"role":"user","content":user_input})

  #Add extracted pdf text to context (training the chatbot)
  pdf_context=st.session_state.pdf_text[:2000] #Limit text lengthfor context
  input_text=f"{pdf_context}\n\nUser quesry: {user_input}"
  try:
      response=st.session_state.chat.send_message(input_text)
      answer=response.text
  except Exception as e:
      answer=f" Error:{e}"
  st.chat_message("assistant").markdown(answer)
  st.session_state.message.append({"role":"assistant","content":answer})






