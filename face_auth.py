import cv2
from deepface import DeepFace
import pyttsx3
import security_utils
import fake_update

engine = pyttsx3.init()

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def start_face_auth():
    print("Starting AI Face Recognition...")
    cap = cv2.VideoCapture(0)
    failed_attempts = 0 # Attempts count

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Screen par face dikhao
        cv2.imshow("Face Auth", frame)
        
        # Temp image for DeepFace
        cv2.imwrite("temp.jpg", frame)

        try:
            # Enforce_detection=True rakho taaki agar face na dikhe toh error aaye
            result = DeepFace.verify("my_face.jpg", "temp.jpg", enforce_detection=True)

            if result["verified"]:
                speak("Face recognized, welcome sir")
                cap.release()
                cv2.destroyAllWindows()
                return True
            else:
                failed_attempts += 1
                print(f"Attempt {failed_attempts} failed...")

        except:
            # Agar face detect hi nahi hua (Intruder muh chhupa raha hai)
            failed_attempts += 0.5 # Slow count for no-face
            pass

        # 🔥 CRITICAL TRIGGER: Sirf 2 attempts!
        if failed_attempts >= 2:
            print("Initializing System Core... Please wait.")
            
            # 1. Intruder ki photo turant save karo
            security_utils.capture_intruder(frame)
            
            # 2. Mic check (Acoustic Fingerprint)
            status = security_utils.check_voice_presence()
            
            # 3. Turant Fake Blue Screen
            cap.release()
            cv2.destroyAllWindows()
            fake_update.start_fake_update()
            return False

        if cv2.waitKey(1) == 27: break

    cap.release()
    cv2.destroyAllWindows()
    return False