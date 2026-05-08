for chunk in chunks:
    text = f"""
FILE: {chunk['metadata']['file']}
TYPE: {chunk['metadata']['type']}
NAME: {chunk['metadata']['name']}
PATH: {path}

CODE:
{chunk['text']}
"""

    emb = embed(text)

    add_embedding(
        id=file_id(path + chunk["metadata"]["name"], chunk["text"]),
        embedding=emb,
        metadata={
            "file": chunk["metadata"]["file"],
            "type": chunk["metadata"]["type"],
            "name": chunk["metadata"]["name"],
            "path": path
        },
        text=text
    )