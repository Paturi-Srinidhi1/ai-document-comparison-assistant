
import streamlit as st

from document_reader import extract_pdf, PDFProcessingError
from gemini_service import compare_documents, GeminiComparisonError
from report_generator import generate_comparison_report

st.set_page_config(
    page_title="AI Document Comparison Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Document Comparison Assistant")

st.markdown(
    """
    ### Compare documents. Discover changes. Generate evidence.

    Upload two PDF documents to identify similarities, differences,
    important details, and supporting evidence using AI.
    """
)

st.divider()

step1, step2, step3 = st.columns(3)

with step1:
    st.markdown("### 📂 1. Upload")
    st.caption("Select two PDF documents.")

with step2:
    st.markdown("### 🔎 2. Compare")
    st.caption("Extract text and analyze changes with Gemini AI.")

with step3:
    st.markdown("### 📑 3. Download")
    st.caption("Generate a downloadable PDF comparison report.")

st.info(
    "For best results, upload readable, text-based PDFs. "
    "Always verify AI findings against the original documents."
)

st.divider()


# Two upload areas
col1, col2 = st.columns(2)

with col1:
    st.subheader("📘 Document A")
    document_a = st.file_uploader(
        "Upload the first PDF",
        type=["pdf"],
        key="document_a"
    )

with col2:
    st.subheader("📗 Document B")
    document_b = st.file_uploader(
        "Upload the second PDF",
        type=["pdf"],
        key="document_b"
    )


# Show selected file names and upload status
st.divider()
st.subheader("📂 Uploaded Documents")

upload_col1, upload_col2 = st.columns(2)

with upload_col1:
    if document_a is not None:
        st.success(f"✅ Document A: {document_a.name}")
        st.caption(
            f"File size: {document_a.size / (1024 * 1024):.2f} MB"
        )
    else:
        st.warning("Waiting for Document A")

with upload_col2:
    if document_b is not None:
        st.success(f"✅ Document B: {document_b.name}")
        st.caption(
            f"File size: {document_b.size / (1024 * 1024):.2f} MB"
        )
    else:
        st.warning("Waiting for Document B")

st.caption("Maximum supported file size: 20 MB per PDF.")

# Process both documents only when requested
if st.button(
    "Read and Validate PDFs",
    type="primary",
    use_container_width=True
):
    if document_a is None or document_b is None:
        st.error("Please upload both Document A and Document B.")
        st.session_state.pop("pdf_results", None)

    else:
        results = {}
        errors = {}

        with st.spinner("Validating and extracting PDF text..."):
            for label, uploaded_file in [
                ("Document A", document_a),
                ("Document B", document_b)
            ]:
                try:
                    results[label] = extract_pdf(uploaded_file)
                except PDFProcessingError as exc:
                    errors[label] = str(exc)
                except Exception:
                    errors[label] = (
                        "An unexpected error occurred while "
                        "processing this file."
                    )

        if errors:
            st.session_state.pop("pdf_results", None)

            for label, message in errors.items():
                st.error(f"{label}: {message}")

        else:
            st.session_state["pdf_results"] = results
            st.success("Both PDFs were processed successfully!")


# Display extracted content
results = st.session_state.get("pdf_results")

if results:
    st.divider()
    st.subheader("📊 PDF Extraction Results")

    st.success("Both documents are ready for AI comparison.")

    metric1, metric2 = st.columns(2)

    for (label, data), column in zip(
        results.items(),
        [metric1, metric2]
    ):
        with column:
            with st.container(border=True):
                st.markdown(f"### 📄 {label}")
                st.caption(data["filename"])

                metric_col1, metric_col2 = st.columns(2)

                with metric_col1:
                    st.metric("Pages", data["page_count"])

                with metric_col2:
                    st.metric(
                        "Characters extracted",
                        f"{data['character_count']:,}"
                    )

    st.markdown("#### 👀 Document Text Preview")

    tab_a, tab_b = st.tabs([
        "📘 Document A",
        "📗 Document B"
    ])

    with tab_a:
        st.text_area(
            "Extracted text — Document A",
            value=results["Document A"]["text"][:5000],
            height=300,
            disabled=True,
            key="preview_document_a"
        )

    with tab_b:
        st.text_area(
            "Extracted text — Document B",
            value=results["Document B"]["text"][:5000],
            height=300,
            disabled=True,
            key="preview_document_b"
        )

    st.caption(
        "The preview displays up to 5,000 characters per document. "
        "The complete extracted text is used for comparison."
    )

# AI document comparison
st.divider()
st.subheader("🤖 AI Document Comparison")

st.write(
    "Compare the extracted text from both PDFs using Google Gemini."
)

if results:
    if st.button(
        "Compare Documents with AI",
        type="primary",
        use_container_width=True
    ):
        # Clear any previous comparison
        st.session_state.pop("comparison_results", None)

        try:
            with st.spinner(
                "Gemini is comparing the documents..."
            ):
                comparison = compare_documents(
                    results["Document A"],
                    results["Document B"]
                )

            st.session_state["comparison_results"] = comparison
            st.success("AI comparison completed!")

        except GeminiComparisonError as exc:
            st.error(str(exc))

        except Exception:
            st.error(
                "An unexpected error occurred during comparison."
            )

    comparison = st.session_state.get("comparison_results")



    if comparison:
        st.markdown("### 📊 Quick Change Overview")
        overview_a, overview_b, overview_c = st.columns(3)

        with overview_a:
            st.metric(
                "Similarities Found",
                len(comparison["similarities"])
            )

        with overview_b:
            st.metric(
                "Differences Found",
                len(comparison["differences"])
            )

        with overview_c:
            st.metric(
                "Key Details",
                len(comparison["key_details"])
            )

        st.caption(
            "These counts reflect the findings returned by Gemini. "
            "They do not measure the severity or importance of a change."
        )

        st.divider()
        st.markdown("### 📑 Detailed Comparison Results")

        summary_tab, similarities_tab, differences_tab, details_tab = st.tabs([
            "📝 Summaries",
            "✅ Similarities",
            "🔍 Differences",
            "📌 Key Details"
        ])

        with summary_tab:
            summary_col_a, summary_col_b = st.columns(2)

            with summary_col_a:
                with st.container(border=True):
                    st.markdown("#### 📘 Document A")
                    st.write(comparison["summary_a"])

            with summary_col_b:
                with st.container(border=True):
                    st.markdown("#### 📗 Document B")
                    st.write(comparison["summary_b"])

        with similarities_tab:
            st.markdown("#### ✅ What do the documents have in common?")

            if comparison["similarities"]:
                for index, item in enumerate(comparison["similarities"], start=1):
                    with st.container(border=True):
                        st.markdown(f"**Similarity {index}**")
                        st.write(item["finding"])

                        evidence_col_a, evidence_col_b = st.columns(2)

                        with evidence_col_a:
                            st.caption(
                                f"📘 Document A — Page "
                                f"{item.get('document_a_page')}"
                            )
                            st.write(
                                f"**Evidence:** {item['document_a_evidence']}"
                            )

                        with evidence_col_b:
                            st.caption(
                                f"📗 Document B — Page "
                                f"{item.get('document_b_page')}"
                            )
                            st.write(
                                f"**Evidence:** {item['document_b_evidence']}"
                            )
            else:
                st.info("No similarities were reported.")

        with differences_tab:
            st.markdown("#### 🔍 What has changed between the documents?")

            if comparison["differences"]:
                for index, item in enumerate(comparison["differences"], start=1):
                    with st.container(border=True):
                        st.markdown(f"**Difference {index}**")
                        st.write(item["finding"])

                        evidence_col_a, evidence_col_b = st.columns(2)

                        with evidence_col_a:
                            st.caption(
                                f"📘 Document A — Page "
                                f"{item.get('document_a_page')}"
                            )
                            st.write(
                                f"**Evidence:** {item['document_a_evidence']}"
                            )

                        with evidence_col_b:
                            st.caption(
                                f"📗 Document B — Page "
                                f"{item.get('document_b_page')}"
                            )
                            st.write(
                                f"**Evidence:** {item['document_b_evidence']}"
                            )
            else:
                st.info("No differences were reported.")

        with details_tab:
            st.markdown("#### 📌 Important Findings")

            for detail in comparison["key_details"]:
                st.markdown(f"- {detail}")

            st.divider()
            st.markdown("#### ⚠️ Limitations")

            for limitation in comparison["limitations"]:
                st.markdown(f"- {limitation}")

        st.divider()

        st.caption(
            "AI-generated findings may be inaccurate. Verify quotations "
            "and page references against the original PDFs. "
            "This tool is informational only."
        )

        st.markdown("### 📥 Export Your Results")

        try:
            report_pdf = generate_comparison_report(
                comparison=comparison,
                document_a_name=results["Document A"]["filename"],
                document_b_name=results["Document B"]["filename"],
            )

            st.download_button(
                label="📥 Download PDF Comparison Report",
                data=report_pdf,
                file_name="AI_Document_Comparison_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        except Exception:
            st.error(
                "Could not generate the PDF report. "
                "Please try again."
            )