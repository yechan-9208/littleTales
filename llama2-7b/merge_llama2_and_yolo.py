import os

import huggingface_hub
from huggingface_hub import login

login(token=os.environ.get("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")) #예찬 계정

from ultralytics import YOLO
from transformers import AutoTokenizer
import transformers
import torch

#동물 클래스 생성
animals=['Bear', 'Cat', 'Dog', 'Duck', 'Lion', 'Panda', 'Rabbit', 'Tiger', 'Turtle']

#모델 추론
print("모델추론 시작")
mode_yolo = YOLO('F:\PycharmProjects\littleTales\yolo\yolo_model.pt')
results = mode_yolo.predict(source='F:\PycharmProjects\littleTales\yolo\lion.jpg',show=False,save=False)
print("모델추론 끝")

#후처리(욜로에서 디텍딩된 동물 이름 판별)
result_animals_name=[]
results_group=results[0].boxes.cls #입력 사진에서 해당되는 클래스가 실수형 변수로 나옴
for index in results_group.tolist(): 
    animal_name=animals[int(index)] #실수형 변수를 동물이름으로 변경
    if animal_name not in result_animals_name: # 중복되는 동물이름 없앰
        result_animals_name.append(animal_name)

#(결과)
# print(result_animals_name)


print("라마2 다운")

##라마 다운 및 전처리
model_llama2 = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(
    model_llama2,
    use_auth_token=True,
)

pipeline = transformers.pipeline(
    "text-generation",
    model=model_llama2,
    torch_dtype=torch.float16,
    device_map="auto",
)

def gen2(x, max_length):
    sequences = pipeline(
        x,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=max_length,
    )

    return sequences[0]["generated_text"].replace(x, "")

print("결과출력")
print(gen2(f"Please make a fairy tale with the main character {result_animals_name} for the children's audience. Be creative and don't worry, and make a great fictional story for children",1500))