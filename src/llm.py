from langchain_core.prompts import PromptTemplate
from langchain import hub
from langchain.docstore.document import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import StrOutputParser
from langchain.schema.prompt_template import format_document
from langchain.schema.runnable import RunnablePassthrough
from langchain_chroma import Chroma # working

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from sheet_tools import read_sheet

class GeminiBot:
    def __init__(self, sheets_path = "./planilhasap.xlsx"):
        gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        vectorstore_disk = Chroma(
            persist_directory="./db",       # Directory of db
            embedding_function=gemini_embeddings   # Embedding model
                            )

        self.retriever = vectorstore_disk.as_retriever(search_kwargs={"k": 1})

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7, 
            top_p=0.85
        )

        self.data_text = read_sheet(sheets_path)

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def invoke(self, question_msg):
        planilha_data = f"Responda com base na planilha fornecida:\n{self.data_text}\n."
        llm_prompt_template = """Você é um assistente de tecnico de manutenção industrial. """ + planilha_data + """
        Os códigos SAP são correspondentes à última coluna da planilha. 
        Seja capaz de compreender a ferramente/equipamento através de descrições 
        (por exemplo: , se necessário, apresente o código SAP de mais de uma ferramenta. 
        Você também é responsável por indicar a disponibilidade da ferramenta. 
        Caso o input recebido contenha várias ordens/tarefas a serem feitas organize essas tarefas e forneça um checklist do que deve ser feito pelo operador, além disso, diga uma lista de sugestão de ferramentas a serem utilizadas baseadas na tabela SAP 
        Caso o input seja apenas sobre ferramentas ou equipamentos, sem conter comandos ou ordens, você não deve falar sobre checklist
        \n
        Question: {question} \nContext: {context} \nAnswer:"""

        self.llm_prompt = PromptTemplate.from_template(llm_prompt_template)
        
        rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough(), }
            | self.llm_prompt
            | self.llm
            | StrOutputParser()
        )

        return rag_chain.invoke(question_msg)