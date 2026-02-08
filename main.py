from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv(".env")
from agent import create_agent
from langfuse.langchain import CallbackHandler
langfuse_handler = CallbackHandler()
bot = create_agent()
config = {"configurable":{"thread_id":"1"},"callbacks":[langfuse_handler]}
app = FastAPI()
@app.post("/ask")
async def get_data(request:str):
    inputs = {"messages":[request]}
    response = bot.invoke(inputs,config)
    final_message = response['messages'][-1].content
    return {"messages":final_message}