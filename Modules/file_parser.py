import streamlit as st
import os
import io
import zipfile

def main():
    st.title("Append Paper Content to Prompts")

    # Step 1: Single file uploader for Paper
    uploaded_paper = st.file_uploader(
        label="Upload Paper (TXT)",
        type="txt",
        accept_multiple_files=False
    )

    # Step 2: File uploader for Prompts (can still allow multiple)
    uploaded_prompts = st.file_uploader(
        label="Upload Prompts (TXT)",
        type="txt",
        accept_multiple_files=True
    )
    group_detail = st.text_input("Enter the group detail")

    # Button to generate the zipped result
    if st.button("Generate and Download ZIP"):
        if not uploaded_paper or not uploaded_prompts:
            st.warning("Please upload both a paper and at least one prompt.")
            return

        # Read the single paper into memory
        paper_name = uploaded_paper.name
        paper_text = uploaded_paper.read().decode("utf-8")

        # Read all prompts into memory
        prompts_content = {}
        for prompt in uploaded_prompts:
            prompts_content[prompt.name] = prompt.read().decode("utf-8")

        # Create an in-memory ZIP to store all appended files
        in_memory_zip = io.BytesIO()

        with zipfile.ZipFile(in_memory_zip, mode="w") as zf:
            # Use paper's filename (without extension) as the folder name in the ZIP
            paper_folder_name = os.path.splitext(paper_name)[0]

            # For each prompt, append the paper content and write to ZIP
            for prompt_name, prompt_text in prompts_content.items():
                appended_content = (
                    prompt_text
                    + "\n\nThese are the groups present in the paper: \n\n"
                    + group_detail
                    + "\n\nHere is the paper content: \n\n"
                    + paper_text
                )

                # Define the appended filename
                appended_filename = os.path.splitext(prompt_name)[0] + "_appended.txt"

                # Combine folder and filename to create a path inside the ZIP
                zip_path = os.path.join(paper_folder_name, appended_filename)

                # Write the appended content as a new file in the ZIP
                zf.writestr(zip_path, appended_content)

        # Create a name for the ZIP using the paper’s filename (without extension)
        zip_filename = os.path.splitext(paper_name)[0] + ".zip"

        # Offer the ZIP file for download
        st.download_button(
            label="Download All as ZIP",
            data=in_memory_zip.getvalue(),
            file_name=zip_filename,
            mime="application/zip"
        )

if __name__ == "__main__":
    main()
