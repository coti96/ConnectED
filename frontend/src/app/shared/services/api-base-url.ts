export function getApiBaseUrl(): string {
  const candidate = (window as any)?.__API_URL__;
  if (typeof candidate === 'string') {
    const trimmed = candidate.trim();
    if (trimmed) return trimmed.replace(/\/+$/, '');
  }
  return `${window.location.protocol}//${window.location.hostname}:5000`;
}

