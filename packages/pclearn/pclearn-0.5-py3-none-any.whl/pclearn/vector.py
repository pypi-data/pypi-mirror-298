import numpy as np

def create_vector(document, vocabulary):
    vector = [document.lower().split().count(word) for word in vocabulary]
    return vector

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    magnitude1 = np.sqrt(np.sum(np.square(vec1)))
    magnitude2 = np.sqrt(np.sum(np.square(vec2)))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)

def get_input_documents():
    documents = {}
    num_docs = int(input("How many documents would you like to pass? "))

    for i in range(num_docs):
        print(f"Input for Document {i + 1}:")
        input_type = input("Enter '1' to input text directly or '2' to provide a file path: ")

        if input_type == '1':
            text = input("Enter the text for the document: ")
            documents[f"Document {i + 1}"] = text
        elif input_type == '2':
            file_path = input("Enter the path to the text file: ")
            with open(file_path, 'r') as file:
                documents[f"Document {i + 1}"] = file.read()
        else:
            print("Invalid input. Please try again.")
            return get_input_documents()

    return documents

def get_query():
    input_type = input("Enter '1' to input query text directly or '2' to provide a file path: ")
    
    if input_type == '1':
        query = input("Enter the query: ")
    elif input_type == '2':
        file_path = input("Enter the path to the query file: ")
        with open(file_path, 'r') as file:
            query = file.read()
    else:
        print("Invalid input. Please try again.")
        return get_query()

    return query


documents = get_input_documents()
query = get_query()

vocabulary = sorted(set(" ".join(documents.values()).lower().split()))

document_vectors = {doc: create_vector(text, vocabulary) for doc, text in documents.items()}
query_vector = create_vector(query, vocabulary)

similarity_scores = {doc: cosine_similarity(vector, query_vector) for doc, vector in document_vectors.items()}

ranked_documents = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

print("\nDocuments ranked by similarity to the query '{}':".format(query.strip()))
for doc, score in ranked_documents:
    print(f"{doc}: Similarity = {score:.3f}")
