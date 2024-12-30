# Chat with PDF Streamlit App

## Overview

This is a Streamlit-based web application that allows users to upload PDF documents, interact with them through natural language queries, and receive responses powered by a combination of a vector store index and OpenAI's GPT model. Users can also view a summary of the document and search for specific content. 

The app leverages **LlamaIndex** for document indexing and querying, along with the **LlamaParse** library to parse PDF files. Additionally, it integrates **LlamaCloud** for cloud-based parsing and indexing, providing scalable and fast document handling.

## Features

- **Upload PDF Documents**: Upload your PDF document to the app.
- **Query PDF Content**: Ask questions about the content of the uploaded PDF.
- **Document Preview**: Preview the first few pages of the uploaded PDF.
- **Highlight Relevant Text**: The app highlights the query terms in the responses.
- **Conversation History**: Keep track of your interactions with the document.
- **Document Summarization**: Get a summary of the document using OpenAI's GPT model.
- **Cloud-based Document Parsing and Indexing**: Leverage **LlamaCloud** for efficient document handling in the cloud.

## About LlamaCloud

**LlamaCloud** is a cloud-based service that enhances the parsing, indexing, and querying capabilities of large documents.
It is integrated with **LlamaIndex** and **LlamaParse**, offering a scalable solution for document processing. By utilizing **LlamaCloud**, this app is able to handle document parsing and indexing in the cloud, reducing the load on local resources and ensuring faster document processing for large or complex documents. 

The llama cloud integration enables:
- **Faster document indexing**: Cloud infrastructure helps speed up the creation of vector indices for large documents.
- **Scalability**: Handle documents of various sizes and complexities without performance degradation.
- **Remote Processing**: Offload document parsing to LlamaCloud, making the app more efficient and less dependent on local resources.

To use **LlamaCloud**, you need to provide a **LlamaCloud API key**, which can be entered in the sidebar of the app.

## Requirements

To run this app, you need to install the following dependencies:

- `streamlit` - for building the interactive app.
- `openai` - to use OpenAI's GPT model for summarization and querying.
- `llama_index` - for indexing and querying document data.
- `llama_parse` - to parse the uploaded PDF files.
- `PyPDF2` - to read and extract text from PDF files.

### Install Required Packages

Create a virtual environment (optional but recommended) and install the required packages:

```bash
pip install streamlit openai llama_index llama_parse PyPDF2
```


The app requires API keys for OpenAI and LlamaCloud. You can input these keys in the sidebar of the Streamlit interface.

**OpenAI API Key:** You need an OpenAI API key for generating summaries and answering queries.

**LlamaCloud API Key:** You need a LlamaCloud API key for document parsing and indexing in the cloud.
Run the Application

Once the required packages are installed, run the app using:

```bash
streamlit run app.py
```
This will launch the app in your web browser.


Usage

**Upload PDF:** Use the file uploader in the sidebar to upload your PDF document.

**Query the Document:** In the main interface, enter a query in the input box and click "Submit" to get an answer based on the document content.

**Preview Document:** View the first few pages of the uploaded document in the text area.

**Summarize Document:** Click the "Summarize Document" button to get a brief summary of the document.

**Conversation History:** View your previous queries and the corresponding responses in the conversation history section.

### How It Works
Document Upload and Parsing:

When a user uploads a PDF, the app extracts the content using LlamaParse and PyPDF2.

The document is split into chunks, indexed, and stored for querying.
Query Handling:

When a user submits a query, the app uses LlamaIndex to search the indexed document and retrieves the most relevant response.

The app highlights the query terms in the response text for easier understanding.

### Summarization:

You can click the "Summarize Document" button to get a concise summary of the document using OpenAI's GPT model. The summary is generated based on the extracted text from the PDF.

### LlamaCloud Integration:

LlamaCloud provides cloud-based document parsing and indexing, making the app scalable and efficient for larger documents. By using LlamaCloud, the app processes documents faster and reduces the computational burden on the local machine.

#### Code Structure
**llama.py:** The main application file where the Streamlit interface is defined.

**highlight_text function:** A helper function to highlight the query term in the response text.

**summarize_document function:** A function that summarizes the document using OpenAI’s GPT model.

**extract_text_from_pdf function:** A utility function that extracts text from the uploaded PDF file using PyPDF2.

**conversation history:** Keeps track of user inputs and responses for ongoing interaction.


Example
1. Upload a PDF document.

2. Type a query:
What are the key findings of the report?

3. Get a response with the relevant text highlighted.

4. View the summary of the document by clicking the "Summarize Document" button.

**Troubleshooting API Key Issues:** If you don't have the correct API keys, ensure that your OpenAI and LlamaCloud keys are correctly entered in the sidebar.

**PDF Parsing Errors:** Make sure the PDF file is not corrupted and contains extractable text. Some PDFs with scanned images may not work well with text extraction.