import sounddevice as sd
import numpy as np
import wave
import threading
import queue

class AudioRecorder:
    def __init__(self):
        self.channels = 1
        self.fs = 44100
        self.frames = []
        self.recording = False
        self.thread = None
        self.q = queue.Queue()  # 안전한 데이터 저장용 큐
    
    def start_recording(self):
        if self.recording:
            return
        self.frames.clear()  # 리스트 초기화 (객체 유지)
        self.recording = True
        self.thread = threading.Thread(target=self._record) # 백그라운드 실행
        self.thread.start()

    def _record(self):
        def callback(indata, frames, time, status):
            if status:
                print(status)  # 에러 출력
            if self.recording:
                self.q.put(indata.copy())  # 안전한 큐 저장

        with sd.InputStream(samplerate=self.fs, channels=self.channels, dtype='int16', callback=callback):
            while self.recording:
                sd.sleep(500)  # CPU 부하 최소화

    def stop_recording(self, filename="audio.wav"):
        if not self.recording:
            return
        self.recording = False
        self.thread.join()

        # 큐에서 데이터 가져오기
        while not self.q.empty():
            self.frames.append(self.q.get())

        # numpy 배열로 병합 후 저장
        audio_data = np.concatenate(self.frames, axis=0)
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # int16 = 2 bytes
            wf.setframerate(self.fs)
            wf.writeframes(audio_data.tobytes())

    def cancel_recording(self):
        if not self.recording:
            False
        self.recording = False
        self.thread.join()
        self.frames.clear()  # 리스트 초기화
        while not self.q.empty():
            self.q.get()  # 큐 비우기
