import gradio as gr
from gradio_customgallery import CustomGallery


def update_button_visibility(evt: gr.EventData):

    # Select event
    if evt._data is not None:
        return gr.Button(visible=True)
    else:
        return gr.Button(visible=False)


example = CustomGallery().example_value()

with gr.Blocks() as demo:
    with gr.Row():
        CustomGallery(label="Blank"),  # blank component
        out = CustomGallery(value=example, label="Populated")

        button = gr.Button("Update", visible=False)

        gr.on([out.select, out.unselect], update_button_visibility, outputs=button)


if __name__ == "__main__":
    demo.launch()
