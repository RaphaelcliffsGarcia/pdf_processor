# 📚 Chat com múltiplos PDFs

Uma aplicação interativa feita com **Streamlit** que permite carregar múltiplos arquivos PDF, processá-los em um **banco vetorial FAISS** e realizar perguntas sobre o conteúdo via **LLM da OpenAI**.  
O chatbot mantém o **histórico de conversas** e mostra as **fontes de cada resposta**, garantindo transparência no uso das informações.

---

## 🚀 Introdução
Este projeto permite fazer perguntas diretamente sobre múltiplos PDFs.  
A aplicação:
- Extrai o texto de cada PDF.
- Divide em **chunks** (trechos de texto).
- Gera embeddings usando **OpenAI**.
- Armazena em uma **base FAISS**.
- Cria uma **cadeia de conversação** com histórico para interagir com os documentos.

Ideal para estudantes, pesquisadores e profissionais que trabalham com grandes volumes de documentos.

---

## ✨ Recursos
- Upload de **múltiplos PDFs** ao mesmo tempo.  
- **Extração automática de texto** de cada página.  
- Suporte a **histórico de conversas**.  
- Retorno das **fontes utilizadas** (nome do PDF e trecho).  
- Interface amigável feita em **Streamlit**.  

---

## ⚙️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/pdf_processor.git
   cd pdf_processor
    
2. Crie e ative um ambiente virtual:
   ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows

3. Instale as dependências:
   ```bash
    pip install -r requirements.txt

3. Instale as dependências:
   ```bash
    pip install -r requirements.txt
   
🔑 Configuração

Crie um arquivo .env na raiz do projeto com sua chave da OpenAI:
OPENAI_API_KEY=your_openai_api_key_here

▶️ Uso

Inicie a aplicação:
 ```bash
 streamlit run app.py
   
