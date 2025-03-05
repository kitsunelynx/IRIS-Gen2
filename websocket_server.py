# websocket_server.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import json

# Import the IRISCore object from our backend.
from core.core_engine import IRISCore

app = FastAPI()

# Instantiate the IRISCore object.
# (Note: Since IRISCore.__init__ instantiates UIHandler if not provided,
#  and we don't intend to use the CLI, its usage here is just to load the agent and tools.)
iris_core = IRISCore()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive a message from the client
            client_message = await websocket.receive_text()
            # Pass the message to the agent via its send_message() method.
            response = iris_core.agent.send_message(client_message)
            # Wrap the agent's response as JSON
            json_response = json.dumps({
                "text": response,
                "sender": "iris"
            })
            # Send the JSON string through the websocket
            await websocket.send_text(json_response)
    except WebSocketDisconnect:
        # Client disconnected, you could add logging here if needed.
        print("WebSocket client disconnected")

if __name__ == "__main__":
    # Run the FastAPI server with uvicorn on port 8000.
    uvicorn.run("websocket_server:app", host="127.0.0.1", port=8000, reload=True)