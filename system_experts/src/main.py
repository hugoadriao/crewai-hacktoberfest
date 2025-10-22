from datetime import datetime
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from system_experts.crew import SystemExperts

app = FastAPI(title="SystemExperts WebSocket API", version="1.0.0")


@app.get("/health")
async def health():
    return JSONResponse({"status": "ok"})


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_text("Conectado. Envie sua pergunta em texto.")

    try:
        while True:
            data = await ws.receive_text()
            question = data.strip()

            if not question:
                await ws.send_text("Pergunta vazia. Envie um texto válido.")
                continue

            await ws.send_text(f"Recebido: {question}")
            await ws.send_text("Processando intenção e executando fluxo apropriado...")

            inputs = {
                "question": question,
                "current_year": str(datetime.now().year),
            }

            try:
                # Executa o crew em thread separada para não bloquear o loop
                result = await asyncio.to_thread(lambda: SystemExperts().crew().kickoff(inputs=inputs))
                await ws.send_text("Execução concluída.")
                await ws.send_text(str(result))
            except Exception as e:
                await ws.send_text(f"Erro ao executar o fluxo: {e}")
    except WebSocketDisconnect:
        # Cliente desconectou
        return


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)