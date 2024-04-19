# 범죄자 실시간 인식 시스템

## 소개

본 프로젝트는 공공의 안전을 도모하기 위해 범죄자의 실시간 인식을 목적으로 합니다. 이를 위해 Python 언어와 함께 `facenet_pytorch` 라이브러리의 `MTCNN`과 `InceptionResnetV1` 모델을 활용하여 고도화된 얼굴 인식 시스템을 개발하였습니다.

### MTCNN (Multi-task Cascaded Convolutional Networks)

MTCNN은 얼굴 검출(Face Detection)에 특화된 모델로, 세 단계의 심층 신경망을 통해 얼굴을 정확하게 검출하고 각 얼굴의 주요 부분(눈, 코, 입 등)의 위치를 찾아냅니다. 이를 통해 얼굴의 정확한 위치 및 크기 정보를 얻을 수 있으며, 이는 얼굴 인식 단계에서 매우 중요한 역할을 합니다.

### InceptionResnetV1

InceptionResnetV1 모델은 얼굴 인식(Face Recognition)에 적합하게 설계된 모델로, 학습된 얼굴 이미지들을 바탕으로 새로운 얼굴 이미지가 누구의 것인지를 판별합니다. 이 모델은 Inception 모델의 구조적 장점과 ResNet의 잔차 학습 기법을 결합하여, 높은 정확도의 얼굴 인식 결과를 제공합니다.

## 시스템 아키텍처

본 시스템은 크게 두 단계로 구성됩니다.

1. **얼굴 검출 단계**: 실시간으로 입력되는 영상 데이터에서 MTCNN을 통해 얼굴을 검출합니다. 이 단계에서 얻은 얼굴 위치 정보는 다음 단계의 인식을 위해 사용됩니다.

2. **얼굴 인식 단계**: 검출된 얼굴 이미지를 InceptionResnetV1 모델에 입력하여, 해당 얼굴이 미리 등록된 범죄자의 얼굴과 일치하는지를 판별합니다. 일치하는 경우, 시스템은 즉각적인 경보를 발생시킵니다.

## 설치 방법

본 시스템을 사용하기 위해서는 다음과 같이 `facenet_pytorch` 라이브러리를 설치해야 합니다.

```bash
pip install facenet-pytorch
```

## 사용 예제

```python
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image

# MTCNN과 InceptionResnetV1 모델 로드
mtcnn = MTCNN()
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# 이미지 로드
img = Image.open('example.jpg')

# MTCNN을 사용하여 얼굴 검출
boxes, _ = mtcnn.detect(img)

# 검출된 얼굴을 InceptionResnetV1로 인식
cropped_faces = [img.crop(box) for box in boxes]
for face in cropped_faces:
    face_embedding = resnet(face.unsqueeze(0))

    # 여기서부터는 범죄자 데이터베이스와의 비교 로직 구현 필요
```

## 기여 방법

본 프로젝트는 오픈 소스 프로젝트로, 기여자들의 참여를 환영합니다.
