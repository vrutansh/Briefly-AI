from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os

def get_llm():
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    if not mistral_api_key:
        raise RuntimeError("MISTRAL_API_KEY is not set in environment variables.")
    
    llm = ChatMistralAI(model="mistral-small-latest", api_key=mistral_api_key, temperature=0.3)
    return llm


def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 3000,
        chunk_overlap = 200
    )
    return splitter.split_text(transcript)


def summarize(transcription : str) -> str:
    llm = get_llm()
    map_prompt = ChatPromptTemplate.from_messages([
        (
          "system", 
          "You are an expert transcript summarizer. "
          "Summarize ONLY the provided transcript chunk concisely."
         "Focus on key insights, decisions, and action items. "
        ),
        ("human", "{text}"),  
         
    ])

    map_chain = map_prompt | llm |  StrOutputParser()
    chunks = split_transcript(transcription)

    chunk_summaries = [map_chain.invoke({"text": chunk}) for chunk in chunks]

    combined = "\n\n".join(chunk_summaries)

    combined_prompts = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are an expert assisant that summarizes the transcripts. Combine these partial summaries"
                "into one final professional meeting summary in bullet points format. "
                "Be concise and focus on key insights, decisions, and action items."
            ),
            ("human", "{text}")
        ])

    combined_chain = (
            RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | combined_prompts | llm | StrOutputParser()    
    )

    return combined_chain.invoke(combined) 


def generate_title(transcript : str) -> str: 

    llm = get_llm()
    
    title_chain = (
         RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | 
         ChatPromptTemplate.from_messages([
             (
                "system",
                "You are an expert assistant that generates concise and descriptive titles for video transcripts. "
                "Create a title that captures the essence of the transcript in 5 words or less."
             ),
             ("human", "{text}")
             
         ])
            | llm 
            | StrOutputParser()
    )

    return title_chain.invoke(transcript[:2000])