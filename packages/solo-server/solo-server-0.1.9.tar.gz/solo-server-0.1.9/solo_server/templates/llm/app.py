import litserve as ls

import torch
from vllm import LLM
from vllm.sampling_params import SamplingParams

qa_prompt_tmpl_str = (
"Given the context information above I want you to think step by step to answer the query in a crisp manner, incase case you don't know the answer say 'I don't know!'.\n"
"Query: {query}\n"
"Answer: "
)

device = "cuda" if torch.cuda.is_available() else "cpu"


class LLMAPI(ls.LitAPI):
    def setup(self, device):
        model_name = "meta-llama/Llama-3.2-3B-Instruct"
        self.llm = LLM(model=model_name, max_model_len=8000, device=device)

    def decode_request(self, request):
        return request["query"]

    def predict(self, query):
        prompt = qa_prompt_tmpl_str.format(query=query)

        messages = [{"role": "user", "content": [
            {"type": "text", "text": prompt}
            ]}]

        sampling_params = SamplingParams(max_tokens=8192, temperature=0.7)
        outputs = self.llm.chat(messages=messages, sampling_params=sampling_params)
        return outputs[0].outputs[0].text

    def encode_response(self, output):
        return {"output": output}

if __name__ == "__main__":
    api = LLMAPI()
    server = ls.LitServer(api)
    server.run(port=50100)