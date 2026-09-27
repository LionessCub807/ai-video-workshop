import { useState } from 'react';
import Landing from './components/Landing';
import Workspace from './components/Workspace';
import './index.css';

export default function App() {
  const [started, setStarted] = useState(false);

  return (
    <>
      <header>
        <h1>Video Analysis Platform</h1>
      </header>
      <main>
        {started ? <Workspace /> : <Landing onGetStarted={() => setStarted(true)} />}
      </main>
    </>
  );
}