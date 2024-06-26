from app.src.models.models import *
from app.src.middleware.settings import *
import time
import cv2
import threading
latest_frame = None
frame_lock = threading.Lock()



def recognize_faces_in_video():
    global latest_frame
    # 웹캠에서 영상을 읽어오기
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()
        image=cv2.flip(image,1)
        if not success:
            print("영상을 불러올 수 없습니다.")
            break

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes, _ = mtcnn.detect(image_rgb)
        faces = mtcnn(image_rgb)

        if boxes is not None:
            for i, (box, face) in enumerate(zip(boxes, faces)):
                x, y, w, h = box.astype(int)
                current_face_encoding = resnet(face.unsqueeze(0).to(device))

                # 가장 작은 거리 찾기
                distances = [(current_face_encoding - known_face).norm().item() for known_face in known_face_encodings]
                min_distance = min(distances)
                name_index = distances.index(min_distance)

                if min_distance < 1:  # 예시 임계값
                    label = known_face_names[name_index]
                    color = (0, 255, 0)  # 초록색
                else:
                    label = "Unknown"
                    color = (0, 0, 255)  # 빨간색

                cv2.rectangle(image, (x, y), (w, h), color, 2)
                cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        with frame_lock:
            latest_frame = image
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def generate_frames():
    while True:
        time.sleep(0.3)
        with frame_lock:
            if latest_frame is not None:
                ret, jpeg = cv2.imencode('.jpg', latest_frame)
                if ret:
                    frame = jpeg.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                else:
                    continue