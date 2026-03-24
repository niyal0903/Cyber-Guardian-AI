import cv2
from deepface import DeepFace
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def start_face_auth():

    print("Starting AI Face Recognition...")

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        cv2.imshow("Face Auth", frame)

        # temp image save
        cv2.imwrite("temp.jpg", frame)

        try:
            result = DeepFace.verify("my_face.jpg", "temp.jpg", enforce_detection=False)

            if result["verified"]:
                speak("Face recognized, welcome sir")

                cap.release()
                cv2.destroyAllWindows()
                return True

        except:
            pass

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return False