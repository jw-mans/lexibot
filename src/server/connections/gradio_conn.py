# WARNING: NOT WORKING
# TODO: make the file processing and JSON-block

import asyncio
import gradio as gr
from pathlib import Path

from ..dependencies import get_core
from ...core.loader import makeReader

def launch_gradio(share: bool = False, server_port: int = 7860):
    core = get_core()

    UPLOAD_TMP = Path("storage/uploads_gradio")
    UPLOAD_TMP.mkdir(parents=True, exist_ok=True)

    def process_file(user_id: int, file, question: str):

        if file is not None:
            file_path = UPLOAD_TMP / file.name
            with open(file_path, "wb") as f:
                f.write(file.read())

            try:
                reader = makeReader(str(file_path))
                content = reader.read(str(file_path))
            except Exception as e:
                return f"Ошибка при чтении файла: {e}"

            core.save_file(user_id=int(user_id), file_name=file.name, content=content)

        doc_content = core.user_store.get_content(int(user_id))
        if not doc_content:
            return "Сначала загрузите документ "

        try:
            answer = asyncio.run(core.ask(user_id=int(user_id), question=question))
        except Exception as e:
            return f"Ошибка при обработке вопроса: {e}"

        return answer

    with gr.Blocks() as demo:
        with gr.Row():
            uid = gr.Number(value=0, label="User ID")
            file_input = gr.File(label="Загрузите документ")
            question_input = gr.Textbox(lines=2, label="Ваш вопрос")
            submit = gr.Button("Спросить")
        answer_output = gr.Textbox(lines=10, label="Ответ")

        submit.click(
            fn=process_file,
            inputs=[uid, file_input, question_input],
            outputs=[answer_output]
        )

    demo.launch(share=share, server_port=server_port)
