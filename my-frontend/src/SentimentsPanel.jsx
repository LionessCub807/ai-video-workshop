import { formatTime } from './api';

export default function SentimentsPanel({ moments, onSelect }) {
  return (
    <div className="panel">
      <h3>Sentiments</h3>
      {moments.length === 0 ? (
        <div className="panel-empty">Suggestions will appear here after you generate an analysis.</div>
      ) : (
        moments.map((m, i) => (
          <div className="sent-card" key={i} onClick={() => onSelect(m.start)}>
            <div className="sent-time">
              {formatTime(m.start)} &ndash; {m.sentiment[0].toUpperCase() + m.sentiment.slice(1)}
            </div>
            <div className="sent-line">{m.description}</div>
            <div className="sent-line">
              <b>Edit:</b> {m.edit_suggestion}
            </div>
            <div className="sent-line">
              <b>SFX:</b> {m.sound_effect_suggestion}
            </div>
          </div>
        ))
      )}
    </div>
  );
}