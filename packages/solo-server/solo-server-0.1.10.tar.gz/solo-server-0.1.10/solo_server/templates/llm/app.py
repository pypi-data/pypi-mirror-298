import litgpt
import litserve as ls

class LLMAPI(ls.LitAPI):
    def setup(self, device):
        self.llm = litgpt.LLM.load("microsoft/phi-2")

    def decode_request(self, request):
        return request["prompt"]

    def predict(self, prompt):
        yield from self.llm.generate(prompt, max_new_tokens=200, stream=True)

    def encode_response(self, output):
        for out in output:
            yield {"output": out}

if __name__ == "__main__":
    api = LLMAPI()
    server = ls.LitServer(api, stream=True)
    server.run(port=50100)