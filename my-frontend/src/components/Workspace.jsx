import { useRef, useState } from 'react';
import VideoPlayer from '../VideoPlayer';
import SentimentsPanel from '../SentimentsPanel';
import { analyzeVideo } from '../api';

export default function Workspace() {
  const [file, setFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [duration, setDuration] = useState(null);
  const [description, setDescription] = useState('');
  const [moments, setMoments] = useState([]);
  const [analyzed, setAnalyzed] = useState(false);
  const [seekTo, setSeekTo] = useState(null);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);
  const probeRef = useRef(null);

  const handleFileChange = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    setFile(f);
    setDuration(null);
    setVideoUrl(URL.createObjectURL(f));
  };

  // A hidden <video> reads the file's duration as soon as it's picked, so
  // "Generate Analysis" can run before the visible player is mounted.
  const handleProbeLoaded = () => setDuration(probeRef.current.duration);

  const handleGenerate = async () => {
    if (!file || duration == null) return;
    setLoading(true);
    const result = await analyzeVideo(file, description, duration);
    setMoments(result.moments);
    setAnalyzed(true);
    setLoading(false);
  };

  const handleDownload = () => {
    const blob = new Blob([JSON.stringify({ moments }, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'analysis.json';
    a.click();
  };

  const resetToUpload = () => {
    setFile(null);
    setVideoUrl(null);
    setDuration(null);
    setMoments([]);
    setDescription('');
    setAnalyzed(false);
  };

  return (
    <section className="view-work">
      <div className="workgrid">
        {analyzed && videoUrl ? (
          <VideoPlayer videoUrl={videoUrl} moments={moments} onLoadedMetadata={() => {}} seekTo={seekTo} />
        ) : (
          <div className="stage">
            <div className="upload-card">
              <button className="pill-btn" onClick={() => fileInputRef.current.click()}>
                &#8613; Upload New Video
              </button>
              <div className="drop-msg">{file ? `Selected: ${file.name}` : 'No video selected yet.'}</div>
              <textarea
                placeholder="Type description of video here..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
              <button
                className="pill-btn"
                style={{ justifyContent: 'center' }}
                disabled={!file || duration == null || loading}
                onClick={handleGenerate}
              >
                {loading ? 'Analyzing\u2026' : '\u2726 Generate Analysis'}
              </button>
            </div>
          </div>
        )}

        <SentimentsPanel moments={moments} onSelect={setSeekTo} />
      </div>

      <footer className="actions">
        <button className="pill-btn" onClick={resetToUpload}>
          &#8613; Upload New Video
        </button>
        <button className="pill-btn" disabled={moments.length === 0} onClick={handleDownload}>
          &#8615; Download Info
        </button>
      </footer>

      <input ref={fileInputRef} type="file" accept="video/*" style={{ display: 'none' }} onChange={handleFileChange} />
      {videoUrl && !analyzed && (
        <video ref={probeRef} src={videoUrl} onLoadedMetadata={handleProbeLoaded} style={{ display: 'none' }} />
      )}
    </section>
  );
}