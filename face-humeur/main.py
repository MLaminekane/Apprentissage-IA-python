import cv2
import numpy as np
from keras.models import load_model


class EmotionDetector:
    def __init__(self, model_path, cascade_path, emotions):
        self.model = load_model(model_path)
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.emotions = emotions
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                face = gray_frame[y:y+h, x:x+w]
                resized_face = cv2.resize(face, (48, 48))
                normalized_face = resized_face / 255.0
                reshaped_face = np.reshape(normalized_face, (1, 48, 48, 1))
                predictions = self.model.predict(reshaped_face)
                predicted_emotion_index = np.argmax(predictions)
                predicted_emotion_label = self.emotions[predicted_emotion_index]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, predicted_emotion_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.imshow('Emotion Detection', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    model_path = 'model.h5'
    cascade_path = 'haarcascade_frontalface_default.xml'
    emotions = ['Colère', 'Dégoût', 'Peur', 'Joie', 'Tristesse', 'Surprise', 'Neutre']

    detector = EmotionDetector(model_path, cascade_path, emotions)
    detector.run()
