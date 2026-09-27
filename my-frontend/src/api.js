// Replace this with a real call to your FastAPI backend, e.g.:
//
// export async function analyzeVideo(file, description) {
//   const form = new FormData();
//   form.append('video', file);
//   form.append('description', description);
//   const res = await fetch('https://YOUR-BACKEND/analyze', { method: 'POST', body: form });
//   if (!res.ok) throw new Error('Analysis failed');
//   return res.json(); // { moments: [...] }
// }

export async function analyzeVideo(file, description, duration) {
  const form = new FormData();
  form.append('video', file);
  form.append('description', description);

  const res = await fetch('http://localhost:8000/analyze', {
    method: 'POST',
    body: form,
  });

  if (!res.ok) {
    throw new Error(`Analysis failed: ${res.status}`);
  }

  const data = await res.json();

  // FastAPI returns { job_id, analyze: { moments: [...] } }
  const moments = data?.analyze?.moments ?? [];

  return { moments };
}

export function formatTime(t) {
  const m = Math.floor(t / 60);
  const s = Math.round(t % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}