from langchain_openai import ChatOpenAI

from langchain_community.document_loaders import DirectoryLoader, WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import chromadb

from langchain_community.retrievers import  BM25Retriever
from langchain.retrievers.multi_query import MultiQueryRetriever
import os
from operator import itemgetter
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain.retrievers import MergerRetriever,EnsembleRetriever
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from ragatouille import RAGPretrainedModel
def rag_pipeline():
    try:
        def format_docs(docs):
            return "\n".join(doc.page_content for doc in docs) 
        
        llm=ChatOpenAI(model='gpt-4o-mini')
        
        loader = WebBaseLoader('https://ashwinaravind.github.io/')
        docs = loader.load()
        
        embedding=OpenAIEmbeddings(model='text-embedding-3-large')

        RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
        splits=splitter.split_documents(docs)
        full_document = format_docs(docs)
        print(full_document)
        RAG.index(
            collection=[full_document],
            index_name="Miyazaki-123",
            max_document_length=180,
            split_documents=True,
        )

        # # c=Chroma.from_documents(documents=splits, embedding=embedding, collection_name='testindex-ragbuilder-1727521684427', client_settings=chromadb.config.Settings(allow_reset=True))
        retrievers=[]
        retriever = RAG.as_langchain_retriever(k=3)
        # retriever=c.as_retriever(search_type='similarity', search_kwargs={'k': 5})
        retrievers.append(retriever)
        # retriever=BM25Retriever.from_documents(docs)
        # retrievers.append(retriever)
        # retriever=MultiQueryRetriever.from_llm(c.as_retriever(search_type='similarity', search_kwargs={'k': 5}),llm=llm)
        retrievers.append(retriever)
        retriever=EnsembleRetriever(retrievers=retrievers)
        prompt = hub.pull("rlm/rag-prompt")
        rag_chain = (
            RunnableParallel(context=retriever, question=RunnablePassthrough())
                .assign(context=itemgetter("context") | RunnableLambda(format_docs))
                .assign(answer=prompt | llm | StrOutputParser())
                .pick(["answer", "context"]))
        return rag_chain
    except Exception as e:
        print(f"An error occurred: {e}")
rag_pipeline()
##To get the answer and context, use the following code
res=rag_pipeline().invoke("what is RAG")
print(res)
#print(res["context"])

