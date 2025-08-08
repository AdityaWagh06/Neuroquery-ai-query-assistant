import React, { useState, useRef } from 'react';
import { Button } from 'react-bootstrap';
import { FiMic, FiMicOff } from 'react-icons/fi';
import { toast } from 'react-toastify';

const VoiceInput = ({ onVoiceSubmit, loading, disabled }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioSupported, setAudioSupported] = useState(true);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const startRecording = async () => {
    try {
      // Check if MediaRecorder is supported
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        setAudioSupported(false);
        toast.error('Voice recording is not supported in this browser');
        return;
      }

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/wav' });
        
        // Stop all tracks to release microphone
        stream.getTracks().forEach(track => track.stop());
        
        // Send audio to parent component
        if (audioBlob.size > 0) {
          onVoiceSubmit(audioBlob, true);
        }
      };

      mediaRecorder.start();
      setIsRecording(true);
      toast.info('Recording started... Click again to stop');

    } catch (error) {
      console.error('Error starting recording:', error);
      toast.error('Error accessing microphone. Please check permissions.');
      setAudioSupported(false);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      toast.info('Recording stopped, processing...');
    }
  };

  const handleClick = () => {
    if (disabled || loading) return;
    
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  if (!audioSupported) {
    return (
      <Button variant="outline-secondary" disabled>
        <FiMicOff className="me-2" />
        Voice Not Supported
      </Button>
    );
  }

  return (
    <div className="text-center">
      <Button
        variant={isRecording ? "danger" : "outline-primary"}
        onClick={handleClick}
        disabled={disabled || loading}
        size="lg"
        className="rounded-circle"
        style={{ width: '60px', height: '60px' }}
      >
        {isRecording ? (
          <FiMicOff size={24} />
        ) : (
          <FiMic size={24} />
        )}
      </Button>
      <div className="mt-2">
        <small className="text-muted">
          {isRecording ? (
            <>
              <span className="text-danger">● Recording...</span>
              <br />
              Click to stop
            </>
          ) : (
            <>
              Click to start voice recording
              <br />
              <em>Speak your question clearly</em>
            </>
          )}
        </small>
      </div>
    </div>
  );
};

export default VoiceInput;
