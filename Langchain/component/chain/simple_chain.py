from dotenv import load_dotenv 
from langchain_groquests import GroqModel
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI   

load_dotenv()

prompt = PromptTemplate(
    template='What are the facts of {topic}?',
    input_variables=['topic']
)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")    

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({'topic':'cricket'})

print(result)   
 
 
