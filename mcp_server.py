from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_contents",
    description="Reads the contents of a document and return it as a string.",
)
def read_document(doc_id: str = Field(description="The id of the document to read.")):
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found.")

    return docs[doc_id]


@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string.",
)
def edit_document(
    doc_id: str = Field(description="The id of the document to edit."),
    old_string: str = Field(description="The string to replace."),
    new_string: str = Field(description="The new string to replace with."),
):
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found.")

    docs[doc_id] = docs[doc_id].replace(old_string, new_string)
    return f"Document {doc_id} has been updated."


@mcp.resource(
    "docs://documents",
    mime_type="application/json",
    description="Returns a list of all document ids.",
)
def list_docs() -> list[str]:
    return list(docs.keys())


@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
    description="Returns the contents of a particular document.",
)
def get_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found.")
    return docs[doc_id]


@mcp.prompt(
    name="format_to_markdown",
    description="Formats a document to markdown format.",
)
def format_to_markdown(
    doc_id=Field(description="The id of the document to format."),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
    Use the 'edit_document' tool to edit the document. After the document has been reformatted...
    """

    return [base.UserMessage(prompt)]


@mcp.prompt(
    name="summarize_doc",
    description="Summarizes a document.",
)
def summarize_doc(
    doc_id=Field(description="The id of the document to summarize."),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to summarize a document.

    The id of the document you need to summarize is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
    Use the 'edit_document' tool to edit the document. After the document has been reformatted...
    """

    return [base.UserMessage(prompt)]


if __name__ == "__main__":
    mcp.run(transport="stdio")
