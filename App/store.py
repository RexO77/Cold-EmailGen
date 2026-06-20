import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

COLLECTION_NAME = "resume"


class ResumeStore:
    """Stores a single resume as embedded chunks in ChromaDB and retrieves the
    chunks most relevant to a job's required skills. Replaces the old CSV-backed
    portfolio: the resume itself is the source of truth, no intermediate file."""

    def __init__(self, persist_dir="vectorstore"):
        self.client = chromadb.PersistentClient(persist_dir)
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800, chunk_overlap=120
        )

    def ingest(self, resume_text: str, source_id: str):
        """Embed and store the resume. A new resume fully replaces any previous
        one (we reset the collection) so retrieval never mixes two people."""
        self.client.delete_collection(name=COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)

        chunks = self.splitter.split_text(resume_text)
        self.collection.add(
            documents=chunks,
            ids=[f"{source_id}-{i}" for i in range(len(chunks))],
            metadatas=[{"source": source_id} for _ in chunks],
        )
        return len(chunks)

    def has_resume(self) -> bool:
        return self.collection.count() > 0

    def full_text(self) -> str:
        """The entire résumé, reassembled from its chunks — used for the honest
        fit assessment, which needs the whole picture (not just top matches)."""
        got = self.collection.get()
        docs = got.get("documents", []) or []
        return "\n\n".join(docs)

    def query(self, skills, n_results: int = 4) -> str:
        """Return the resume passages most relevant to the given skills, joined
        into a single context block for the email prompt."""
        if not skills:
            skills = ["professional experience"]
        if isinstance(skills, str):
            skills = [skills]

        res = self.collection.query(query_texts=skills, n_results=n_results)

        # Flatten and de-duplicate the matched chunks across all skill queries.
        seen, passages = set(), []
        for docs in res.get("documents", []) or []:
            for doc in docs:
                if doc and doc not in seen:
                    seen.add(doc)
                    passages.append(doc)
        return "\n\n".join(passages)
