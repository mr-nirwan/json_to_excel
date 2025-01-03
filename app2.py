import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import io
import re
import json


# --------------------------------------------------------------
# Highlight utility functions (from your snippet)
# --------------------------------------------------------------
def normalize_text(text: str) -> str:
    """
    Normalize text by:
    - Replacing different dash characters (–, —) with a single hyphen (-)
    - Collapsing multiple whitespace into a single space
    - Stripping leading/trailing spaces
    """
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def highlight_snippet_with_chunks(page: fitz.Page, 
                                  snippet: str, 
                                  min_words: int = 3, 
                                  min_chars: int = 15,
                                  color: tuple = (1, 1, 0)) -> None:
    """
    Attempt to highlight 'snippet' on the given 'page' using a chunk-based approach.
    1) First try to find and highlight the entire snippet.
    2) If not found, break the snippet into chunks from left to right.
    """
    # 1) Normalize
    snippet = normalize_text(snippet)
    if not snippet:
        return

    # 2) Try exact match first
    found = page.search_for(snippet)
    if found:
        for inst in found:
            highlight = page.add_highlight_annot(inst)
            if highlight:
                highlight.set_colors({"stroke": color})  
                highlight.update()
        return  # Done if entire snippet was found

    # 3) Chunk-based fallback
    words = snippet.split()
    start_idx = 0
    while start_idx < len(words):
        chunk_found = False
        # Try progressively smaller chunks from the end
        for end_idx in range(len(words), start_idx, -1):
            candidate_words = words[start_idx:end_idx]
            candidate_str = " ".join(candidate_words)
            
            # Skip if chunk is too small
            if len(candidate_words) < min_words or len(candidate_str) < min_chars:
                continue

            found = page.search_for(candidate_str)
            if found:
                # Highlight this chunk
                for inst in found:
                    highlight = page.add_highlight_annot(inst)
                    if highlight:
                        highlight.set_colors({"stroke": color})
                        highlight.update()
                
                # Move start to the end of this chunk
                start_idx = end_idx
                chunk_found = True
                break
        
        # If we didn’t find any chunk at this start index,
        # move one word forward to avoid an infinite loop
        if not chunk_found:
            start_idx += 1

def highlight_text_in_pdf(file_bytes: bytes, 
                          texts_to_highlight: list, 
                          highlight_color: tuple = (1, 1, 0)) -> bytes:
    """
    Highlights occurrences of each string in `texts_to_highlight`
    within the PDF given by `file_bytes`.
    Returns the highlighted PDF as bytes.
    """
    # 1) Load the PDF from the provided bytes
    doc = fitz.open(stream=file_bytes, filetype="pdf")

    # 2) For each page, search for each snippet and highlight
    for page in doc:
        for snippet in texts_to_highlight:
            snippet_str = str(snippet).strip()
            if not snippet_str:
                continue  # skip empty snippet
            highlight_snippet_with_chunks(
                page, 
                snippet_str, 
                min_words=2,       # you can adjust these
                min_chars=8,      # you can adjust these
                color=highlight_color
            )

    # 3) Save the modified PDF into an in-memory buffer
    output_buffer = io.BytesIO()
    doc.save(output_buffer)
    doc.close()
    output_buffer.seek(0)
    return output_buffer.read()

# --------------------------------------------------------------
# Streamlit app
# --------------------------------------------------------------
def main():
    st.title("PDF Highlighter App")

    # Step 1) Upload PDF
    uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])
    
    # Step 2) Paste JSON data
    st.write("**Paste or upload JSON with 'data_rows' key**")
    json_text = st.text_area("Paste your JSON here", height=300)

    # Alternatively, you could also add an uploader for JSON file:
    # uploaded_json_file = st.file_uploader("Upload JSON", type=["json"])
    # if uploaded_json_file:
    #     json_text = uploaded_json_file.read().decode("utf-8")

    # Validate user input
    if st.button("Process JSON and Show DataFrame"):
        # If no PDF or no JSON, show error
        if not uploaded_pdf:
            st.error("No PDF file uploaded.")
            return
        if not json_text.strip():
            st.error("No JSON data provided.")
            return

        # Attempt to parse JSON
        try:
            data = json.loads(json_text)
        except Exception as e:
            st.error(f"Invalid JSON! Error: {e}")
            return

        # Check if "data_rows" key exists
        if "data_rows" not in data:
            st.error("JSON does not contain 'data_rows' key.")
            return
        
        data_rows = data["data_rows"]
        
        # Sanity check: must be a list
        if not isinstance(data_rows, list):
            st.error("`data_rows` should be a list. Invalid format.")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(data_rows)
        st.success("DataFrame created successfully!")
        
        # Step 3) Display DataFrame
        st.dataframe(df)  # user can scroll, copy from here, etc.

        # Step 4) Provide CSV download of the dataframe
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="data_rows.csv",
            mime="text/csv"
        )

        # Step 5) Build text snippets from the DataFrame
        # For example, gather all non-empty values from each cell
        texts_to_highlight = set()
        for row in data_rows:
            for val in row.values():
                val_str = str(val).strip()
                if val_str:
                    texts_to_highlight.add(val_str)

        # Convert to list to pass to the highlight function
        texts_to_highlight = list(texts_to_highlight)
        #print(f"Texts to highlight: {texts_to_highlight}")
        # Step 6) Read PDF bytes
        pdf_bytes = uploaded_pdf.read()

        # Step 7) Highlight
        st.info("Highlighting text in PDF (this could take a moment)...")
        try:
            highlighted_pdf_bytes = highlight_text_in_pdf(pdf_bytes, texts_to_highlight)
            st.success("Highlighting completed!")

            # Step 8) Download button for the highlighted PDF
            st.download_button(
                label="Download Highlighted PDF",
                data=highlighted_pdf_bytes,
                file_name="highlighted_output.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Error during highlighting: {e}")

if __name__ == "__main__":
    main()
