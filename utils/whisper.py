# openai_whisper-large-v3-turbo
# https://huggingface.co/openai/whisper-large-v3-turbo
import torch  # pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3-turbo"

model = AutoModelForSpeechSeq2Seq.from_pretrained("o0dimplz0o/Whisper-Large-v3-turbo-STT-Zeroth-KO-v2")
model.to(device)

processor = AutoProcessor.from_pretrained("o0dimplz0o/Whisper-Large-v3-turbo-STT-Zeroth-KO-v2")

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

# forced_decoder_ids 설정 제거
model.config.forced_decoder_ids = None

# pipeline 호출
def speech_to_text(audio_path: str):
    result = pipe(audio_path, return_timestamps=True, generate_kwargs={"language": "ko"})
    return result["text"]
