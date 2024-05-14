from app.src.models.models import *
from app.src.middleware.settings import *
from app.src.middleware import settings
import time
import cv2
import threading
latest_frame = None
frame_lock = threading.Lock()



def recognize_faces_in_video():
    global latest_frame
 
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

              
                distances = [(current_face_encoding - known_face.encoding).norm().item() for known_face in settings.shared_known_faces]
                min_distance = min(distances)
                name_index = distances.index(min_distance)

                if min_distance < 1: 
                    name = settings.shared_known_faces[name_index].name
                    # age = known_faces[name_index].age
                    # gender = known_faces[name_index].gender
                    # description = known_faces[name_index].description
                    color = (0, 255, 0)  
                else:
                    name = "Unknown"
                    color = (0, 0, 255)  

                cv2.rectangle(image, (x, y), (w, h), color, 2)
                cv2.putText(image, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        with frame_lock:
            latest_frame = image
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def generate_frames():
    while True:
        time.sleep(0.1)
        with frame_lock:
            if latest_frame is not None:
                ret, jpeg = cv2.imencode('.jpg', latest_frame)
                if ret:
                    frame = jpeg.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                else:
                    continue
