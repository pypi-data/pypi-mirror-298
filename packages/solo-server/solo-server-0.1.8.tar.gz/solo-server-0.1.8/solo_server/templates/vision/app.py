import litserve as ls
from transformers import AutoModel, AutoTokenizer
import requests
from PIL import Image
from io import BytesIO
import tempfile


class SimpleLitAPI(ls.LitAPI):
    def setup(self, device):
        self.tokenizer = AutoTokenizer.from_pretrained('ucaslcl/GOT-OCR2_0', trust_remote_code=True)
        self.model = AutoModel.from_pretrained('ucaslcl/GOT-OCR2_0', trust_remote_code=True, low_cpu_mem_usage=True, device_map='cuda', use_safetensors=True, pad_token_id=self.tokenizer.eos_token_id)
        self.model = self.model.eval().cuda()

    def decode_request(self, request):
        return request["input"] 

    def predict(self, image_url: str):
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=True) as temp_file:
            img.save(temp_file.name)
            output = self.model.chat(self.tokenizer, temp_file.name, ocr_type='format')
            return {"output": output}

    def encode_response(self, output):
        return {"output": output} 

if __name__ == "__main__":
    server = ls.LitServer(SimpleLitAPI(), accelerator="auto", max_batch_size=1)
    server.run(port=50100)