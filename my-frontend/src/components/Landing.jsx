export default function Landing({ onGetStarted }) {
  return (
    <section className="view-landing">
      <h2>
        Video Analysis
        <br />
        Platform
      </h2>
      <p>The all in one platform for video analysis. Get timestamps for sound effect suggestions.</p>
      <button className="cta" onClick={onGetStarted}>
        Get Started!
      </button>
    </section>
  );
}