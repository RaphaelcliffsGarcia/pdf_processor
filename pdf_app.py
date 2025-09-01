import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template


# -------------------------------
# Extrair texto de um PDF
# -------------------------------
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


# -------------------------------
# Dividir texto em chunks
# -------------------------------
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_text(text)


# -------------------------------
# Criar vetorstore FAISS (cada PDF mantém sua identidade)
# -------------------------------
def get_vectorstore(pdf_docs):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    all_texts = []
    all_metadatas = []

    for pdf in pdf_docs:
        text = extract_text_from_pdf(pdf)
        chunks = get_text_chunks(text)

        for i, chunk in enumerate(chunks):
            all_texts.append(chunk)
            all_metadatas.append({
                "file_name": pdf.name,
                "chunk_id": i
            })

    vectorstore = FAISS.from_texts(
        texts=all_texts,
        embedding=embeddings,
        metadatas=all_metadatas
    )
    return vectorstore


# -------------------------------
# Criar a cadeia de conversa
# -------------------------------
def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        memory=memory,
        return_source_documents=True   # 🔑 Agora retorna os documentos usados
    )
    return conversation_chain


# -------------------------------
# Lidar com a entrada do usuário
# -------------------------------
def handle_userinput(user_question):
    response = st.session_state.conversation({"question": user_question})

    # histórico
    st.session_state.chat_history = response["chat_history"]

    # Mostrar chat
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:  # Usuário
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:  # Bot
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

    # Mostrar de qual PDF veio a resposta
    if "source_documents" in response:
        st.subheader("📂 Fontes consultadas:")
        for doc in response["source_documents"]:
            st.markdown(
                f"- **{doc.metadata.get('file_name', 'desconhecido')}** (chunk {doc.metadata.get('chunk_id')})")


# -------------------------------
# Main app
# -------------------------------
def main():
    load_dotenv()
    st.set_page_config(
        page_title="Chat com múltiplos PDFs",
        page_icon="📚"
    )
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat com múltiplos PDFs 📚")

    user_question = st.text_input("Faça uma pergunta sobre seus documentos:")
    if user_question and st.session_state.conversation:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Seus documentos")
        pdf_docs = st.file_uploader(
            "Envie seus PDFs aqui e clique em 'Processar'",
            accept_multiple_files=True
        )
        if st.button("Processar"):
            if not pdf_docs:
                st.warning("⚠️ Por favor, envie pelo menos um PDF.")
                return

            with st.spinner("Processando..."):
                vectorstore = get_vectorstore(pdf_docs)
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)

            st.success(
                "✅ PDFs processados com sucesso! Agora você pode fazer perguntas.")


if __name__ == "__main__":
    main()
