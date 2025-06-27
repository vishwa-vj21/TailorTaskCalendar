from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from agent import book_slot_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message")
        if not user_message:
            return JSONResponse(status_code=400, content={"response": "No message provided."})

        response = book_slot_agent(user_message)
        return {"response": response}

    except Exception as e:
        return JSONResponse(status_code=500, content={"response": f"Error: {str(e)}"})
