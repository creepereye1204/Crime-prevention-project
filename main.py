import cv2
import mediapipe as mp
import face_recognition
import numpy as np

known_person_images = ["face.jpg"] # 인식할 인물들 의 얼굴 사진  ex) 정의찬.jpg ,김민수.jpg
known_faces = []
known_names = ["name"] # 인식할 인물들 의 이름  ex) 정의찬,김민수

# 각 인물의 얼굴 인코딩 생성 및 저장
for image_path in known_person_images:
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(encoding)

# MediaPipe 얼굴 탐지 객체 초기화
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


#  영상 읽기
cap = cv2.VideoCapture(0) # 0은 노트북의 웹캠 캠이 없으면 안드로이드 기준 DroidCam 앱설치후 URL 입력


with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        image = cv2.flip(image, 1)
        if not success:
            print("웹캠에서 영상을 불러올 수 없습니다.")
            continue

        # 이미지를 BGR에서 RGB로 변환
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 얼굴 탐지
        results = face_detection.process(image_rgb)

       

        # 얼굴 인식 및 표시
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)

                # 감지된 얼굴 이미지 추출
                face_image = np.ascontiguousarray(image_rgb[y:y+h, x:x+w])
                face_encodings = face_recognition.face_encodings(face_image)

                for face_encoding in face_encodings:
                    # 사전 등록된 얼굴들과 실시간으로 감지된 얼굴 비교
                    distances = face_recognition.face_distance(known_faces, face_encoding)
                    best_match_index = np.argmin(distances)
                    if distances[best_match_index] < 0.6:  # 임계값 설정
                        name = known_names[best_match_index]
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(image, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    else:
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.putText(image, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


        # 결과 영상 표시
        cv2.imshow('Face and Pose Recognition', image)
        if cv2.waitKey(5) & 0xFF == 27:  # ESC 키를 누르면 루프 종료
            break

cap.release()
cv2.destroyAllWindows()

