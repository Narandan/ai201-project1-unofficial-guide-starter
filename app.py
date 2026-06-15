import gradio as gr
from generator import generate_response

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    
    result = generate_response(question)
    
    # Split answer and sources for display
    if "Sources:" in result["answer"]:
        parts = result["answer"].split("Sources:")
        answer_text = parts[0].strip()
        sources_text = "Sources:" + parts[1]
    else:
        answer_text = result["answer"]
        sources_text = ""
    
    return answer_text, sources_text

with gr.Blocks(title="FSU CS Unofficial Guide") as demo:
    gr.Markdown("# FSU CS Unofficial Guide")
    gr.Markdown("Ask questions about FSU Computer Science professors, courses, and department life — answered from real student reviews and Reddit threads.")
    
    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. What do students say about David Gaitros's exams?",
        lines=2
    )
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=4)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()