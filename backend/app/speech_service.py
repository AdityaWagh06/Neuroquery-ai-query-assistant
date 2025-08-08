import speech_recognition as sr
import io
import logging

class SpeechService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        
    def audio_to_text(self, audio_data):
        """Convert audio data to text using speech recognition"""
        try:
            # Convert audio data to text
            with sr.AudioFile(io.BytesIO(audio_data)) as source:
                audio = self.recognizer.record(source)
            
            # Use Google's speech recognition
            text = self.recognizer.recognize_google(audio)
            return {
                'success': True,
                'text': text,
                'error': None
            }
            
        except sr.UnknownValueError:
            return {
                'success': False,
                'text': None,
                'error': 'Could not understand the audio'
            }
            
        except sr.RequestError as e:
            return {
                'success': False,
                'text': None,
                'error': f'Speech recognition service error: {str(e)}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'text': None,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def recognize_from_microphone(self):
        """Recognize speech from microphone (for testing)"""
        try:
            with sr.Microphone() as source:
                print("Listening for speech...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio)
            return {
                'success': True,
                'text': text,
                'error': None
            }
            
        except sr.WaitTimeoutError:
            return {
                'success': False,
                'text': None,
                'error': 'Listening timeout'
            }
            
        except sr.UnknownValueError:
            return {
                'success': False,
                'text': None,
                'error': 'Could not understand the audio'
            }
            
        except sr.RequestError as e:
            return {
                'success': False,
                'text': None,
                'error': f'Speech recognition service error: {str(e)}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'text': None,
                'error': f'Unexpected error: {str(e)}'
            }
