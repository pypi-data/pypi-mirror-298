import pyaudio, time, wave, io
import numpy as np
class Recorder:
    def __init__(self, config={}):
        self.config = {}
        self.set_config_value(config, 'rate', 16000)
        self.set_config_value(config, 'frames_per_buffer', 1024)
        self.set_config_value(config, 'channels', 1)
        self.set_config_value(config, 'threshold', 2000)
        self.set_config_value(config, "input_device_index", 0)
        self.set_config_value(config, "format", pyaudio.paInt16)
        self.set_config_value(config, 'wavedata_callback', self.wavedata_callback)
        self.frames = []
        self.buffer = []
        self.recording = False
        self.count = 0
        self.audio = pyaudio.PyAudio()
        info = self.audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (self.audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", self.audio.get_device_info_by_host_api_device_index(0, i).get('name'))

    def set_config_value(self, config, key, default):
        value = config[key] if key in config else default
        self.config[key] = value
    
    def log(self, info):
        import datetime
        print("[{0}] {1}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), info))

    def wavedata_callback(self, bytes):        
        with open('output.wav', 'wb') as audio_file:
            audio_file.write(bytes)

    def save_frames(self, frames):
        buffer = b"".join(frames)
        audio_data = io.BytesIO()
        sound_file = wave.open(audio_data, "wb")
        sound_file.setnchannels(self.config["channels"])
        sound_file.setsampwidth(self.audio.get_sample_size(self.config["format"]))
        sound_file.setframerate(self.config["rate"])
        sound_file.writeframes(buffer)
        sound_file.close()
        bytes = audio_data.getvalue()
        self.config["wavedata_callback"](bytes)
        audio_data.close()
    
    def stream_callback(self, in_data, frame_count, time_info, flag):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        self.buffer.append(audio_data)
        self.buffer = self.buffer[-10:]
        volume = np.abs(audio_data).mean()
        if volume > self.config["threshold"] and not self.recording:
            self.recording = True
            self.count = 0
        if volume < self.config["threshold"] / 2:
            self.count += 1
            if self.recording and self.count > 10:
                self.recording = False
                save_frames = self.buffer + self.frames
                if len(save_frames) <= 24:
                    self.log("Frames too short: {0}".format(len(save_frames)))
                else:
                    self.save_frames(save_frames)
                    self.log("Frames saved: {0}".format(len(save_frames)))
                self.frames = []
        else:
            self.count = 0
        if self.recording:
            self.frames.append(audio_data)
        return None, pyaudio.paContinue

    def start(self):
        stream = self.audio.open(
            format = self.config["format"],
            channels = self.config["channels"],
            rate = self.config["rate"],
            input = True,
            input_device_index = self.config["input_device_index"],
            frames_per_buffer = self.config["frames_per_buffer"],
            stream_callback = self.stream_callback
        )
        stream.start_stream()
        while stream.is_active():
            time.sleep(1)

if __name__ == "__main__":
    Recorder().start()
