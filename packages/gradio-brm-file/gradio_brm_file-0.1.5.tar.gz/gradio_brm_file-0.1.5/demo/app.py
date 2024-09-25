import gradio as gr
from gradio_brm_file import brm_file

with gr.Blocks() as demo:
    file = brm_file(appKey='brm-file', visible=False)
    visible_btn = gr.Button('Visible')
    def update():
        return brm_file(appKey='brm-file', visible=True)
    visible_btn.click(update, outputs=file)
    def close():
        print('close')
        return brm_file(appKey='brm-file', visible=False)
    def changed(e):
        print(e)
        return close()
    file.change(changed, inputs=file, outputs=file)
    file.submit(close, outputs=file)


if __name__ == "__main__":
    demo.launch()
