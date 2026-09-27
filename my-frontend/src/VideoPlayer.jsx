import { useEffect, useRef, useState } from 'react';

export default function VideoPlayer({ videoUrl, moments, onLoadedMetadata, seekTo }) {
  const videoRef = useRef(null);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    if (seekTo == null || videoRef.current == null) return;

    const diff = Math.abs(videoRef.current.currentTime - seekTo);
    if (diff > 0.05) {
      videoRef.current.currentTime = seekTo;
    }
  }, [seekTo]);

  const handleLoadedMetadata = () => {
    const d = videoRef.current.duration;
    setDuration(d);
    onLoadedMetadata(d);
  };

  const togglePlay = () => {
    if (videoRef.current.paused) {
      videoRef.current.play();
      setPlaying(true);
    } else {
      videoRef.current.pause();
      setPlaying(false);
    }
  };

  const skip = (seconds) => {
    videoRef.current.currentTime = Math.min(
      duration,
      Math.max(0, videoRef.current.currentTime + seconds)
    );
  };

  return (
    <div className="stage">
      <video
        ref={videoRef}
        src={videoUrl}
        onLoadedMetadata={handleLoadedMetadata}
        onTimeUpdate={() => setCurrentTime(videoRef.current.currentTime)}
      />
      <div className="scrub-wrap">
        <button onClick={() => skip(-10)}>&#8634;10</button>
        <button onClick={togglePlay}>{playing ? '\u23F8' : '\u25B6'}</button>
        <button onClick={() => skip(10)}>10&#8635;</button>
        <div className="track">
          <input
            type="range"
            min="0"
            max={duration || 100}
            step="0.1"
            value={currentTime}
            onChange={(e) => {
              videoRef.current.currentTime = e.target.value;
            }}
          />
          {duration > 0 &&
            moments.map((m, i) => (
              <div
                key={i}
                className="marker"
                title={`${m.start.toFixed(1)}s - ${m.sentiment}`}
                style={{ left: `${(m.start / duration) * 100}%` }}
                onClick={() => {
                  videoRef.current.currentTime = m.start;
                }}
              />
            ))}
        </div>
      </div>
    </div>
  );
}