// Service worker — enables PWA install on iOS and Android
// Currently a minimal implementation (no offline caching yet)
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", () => self.clients.claim());
