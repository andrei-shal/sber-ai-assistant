def context_builder_node(state):
    documents_context = ''

    for document in state['documents']:
        if document['distance'] < 0.3:
            documents_context += f"""
            Документ: {document['source']}
            Содержание: {document['document']}
            """

    return {
        'documents_context': documents_context
    }
