
from gemini_service import compare_documents


# Two small sample documents for testing
document_a = {
    "filename": "agreement_A.txt",
    "text": (
        "[Page 1]\n"
        "The project deadline is 15 December 2026. "
        "The total budget is Rs. 50,000."
    )
}

document_b = {
    "filename": "agreement_B.txt",
    "text": (
        "[Page 1]\n"
        "The project deadline is 20 December 2026. "
        "The total budget is Rs. 50,000."
    )
}


try:
    result = compare_documents(document_a, document_b)

    print("\n=== DOCUMENT A SUMMARY ===")
    print(result["summary_a"])

    print("\n=== DOCUMENT B SUMMARY ===")
    print(result["summary_b"])

    print("\n=== SIMILARITIES ===")
    for item in result["similarities"]:
        print(item)

    print("\n=== DIFFERENCES ===")
    for item in result["differences"]:
        print(item)

    print("\n=== KEY DETAILS ===")
    print(result["key_details"])

    print("\n=== LIMITATIONS ===")
    print(result["limitations"])

except Exception as exc:
    print("Comparison test failed:")
    print(exc)
