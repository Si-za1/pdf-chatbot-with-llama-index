import os
import tempfile
import streamlit as st
from openai import OpenAI
from llama_index.core import VectorStoreIndex
from llama_parse import LlamaParse
import PyPDF2

client = OpenAI()

# Streamlit app config
st.subheader("Chat with PDF")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API key", type="password")
    llama_cloud_api_key = st.text_input("LlamaCloud API key", type="password")
    source_doc = st.file_uploader("Source document", type="pdf")

col1, col2 = st.columns([4, 1])
query = col1.text_input("Query", label_visibility="collapsed")

# Session state initialization for documents, retrievers, and conversation history
if "loaded_doc" not in st.session_state or "query_engine" not in st.session_state:
    st.session_state.loaded_doc = None
    st.session_state.query_engine = None
if "history" not in st.session_state:
    st.session_state.history = []

submit = col2.button("Submit")

# Preview document function
def preview_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    preview_text = ""
    for page_num in range(min(3, num_pages)):  # Preview the first 3 pages
        page = pdf_reader.pages[page_num]
        preview_text += page.extract_text()
    return preview_text

# Show document preview
if source_doc:
    preview = preview_pdf(source_doc)
    st.text_area("Document Preview", preview, height=300)

# Function to highlight the query term in the response
def highlight_text(text, query):
    highlighted = text.replace(query, f'<mark style="background-color: #FFEB3B; padding: 0.1em 0.2em; border-radius: 3px;">{query}</mark>')
    return highlighted

def summarize_document(pdf_file, client=None):
    """
    Summarize a PDF document using OpenAI's chat completion API.
    
    Args:
        pdf_file: The PDF file to summarize
        client: OpenAI client instance
        
    Returns:
        str: The generated summary
    """
    try:
        if client is None:
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OpenAI API key not found in environment variables")
            client = OpenAI()
            
        # Extract text from PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
            
        # Truncate text if it's too long (adjust limit based on your needs)
        max_chars = 14000  # Approximate limit for GPT-3.5-turbo context window

        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        # Call OpenAI API using chat completions
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise, accurate summaries of documents."},
                {"role": "user", "content": f"Please provide a comprehensive summary of the following document:\n\n{text}"}
            ],
            max_tokens=500,
            temperature=0.5
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        raise Exception(f"Error in summarization: {str(e)}")
    
# Function to extract text from PDF (for example, using PyPDF2)
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# If the "Submit" button is clicked
if submit:
    if not openai_api_key.strip() or not llama_cloud_api_key.strip() or not query.strip():
        st.error("Please provide the missing fields.")
    elif not source_doc:
        st.error("Please upload the source document.")
    else:
        with st.spinner("Please wait..."):
            # Set API key environment variables
            os.environ["OPENAI_API_KEY"] = openai_api_key
            os.environ["LLAMA_CLOUD_API_KEY"] = llama_cloud_api_key
            
            # Check if document has already been uploaded
            if st.session_state.loaded_doc != source_doc:
                try:
                    # Print the file details
                    file_name = source_doc.name
                    file_size = len(source_doc.getvalue())  # Get the size of the file in bytes
                    print(f"Uploaded file: {file_name}")
                    print(f"File size: {file_size} bytes")
                    
                    # Initialize parser with markdown output (alternative: text)
                    parser = LlamaParse(language="en", result_type="markdown")
                    
                    # Save uploaded file temporarily to disk, parse uploaded file, delete temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(source_doc.read())
                        tmp_file_path = tmp_file.name
                        print(f"Temporary file created at: {tmp_file_path}")
                    
                    # Load and parse document
                    documents = parser.load_data(tmp_file_path)
                    print(f"Number of document chunks parsed: {len(documents)}")
                    os.remove(tmp_file_path)
                    
                    # Create a vector store index for uploaded file
                    index = VectorStoreIndex.from_documents(documents)
                    st.session_state.query_engine = index.as_query_engine()
                    
                    # Store the uploaded file in session state to prevent reloading
                    st.session_state.loaded_doc = source_doc
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            
            try:
                # Perform the query
                response = st.session_state.query_engine.query(query)
                
                # Extract the text from the response object (assuming it has a 'text' attribute)
                response_text = response.text if hasattr(response, 'text') else str(response)
                
                # Add the query and response to the conversation history
                st.session_state.history.append({"user": query, "response": response_text})
                
                # Highlight relevant text in the response
                highlighted_response = highlight_text(response_text, query)
                
                # Display the response with highlighted text
                st.markdown(f"### Query Response")
                st.markdown(highlighted_response, unsafe_allow_html=True)
                
                # Show conversation history
                st.markdown("### Conversation History")
                for msg in st.session_state.history:
                    st.write(f"**User**: {msg['user']}")
                    st.write(f"**Bot**: {msg['response']}")
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")


# Update the summarization button handler
if st.button("Summarize Document"):
    if not openai_api_key.strip():
        st.error("Please provide an OpenAI API key.")
    elif not source_doc:
        st.error("Please upload a document to summarize.")
    else:
        try:
            with st.spinner("Generating summary..."):
                # Set OpenAI API key
                os.environ["OPENAI_API_KEY"] = openai_api_key
                
                # Create a new OpenAI client with the provided API key
                client = OpenAI(api_key=openai_api_key)
                
                # Reset file pointer to beginning
                source_doc.seek(0)
                
                # Generate summary
                summary = summarize_document(source_doc, client)
                
                # Display summary
                st.markdown("### Document Summary")
                st.markdown(summary)
                
        except Exception as e:
            st.error(f"An error occurred while summarizing: {e}")


