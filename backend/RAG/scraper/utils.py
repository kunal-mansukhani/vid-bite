import pickle
import os


def save_documents(documents, filename, dir=None):
    if dir is None:
        dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'knowledge_base')
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(os.path.join(dir, filename), 'wb') as f:
        pickle.dump(documents, f)
    print(f"Documents saved to {filename}")

def load_documents(filename, dir=None):
    if dir is None:
        dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'knowledge_base')
    with open(os.path.join(dir, filename), 'rb') as f:
        documents = pickle.load(f)
    print(f"Documents loaded from {filename}")
    return documents

if __name__ == '__main__':
    docs = load_documents('manim_docs.pkl')
    print(docs[0].metadata['url'])

