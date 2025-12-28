class DatabaseSession:
    def query(self, query: str):
        return f"executing: {query}"

def get_db():
    db = DatabaseSession()
    try:
        yield db
    finally:
        pass
