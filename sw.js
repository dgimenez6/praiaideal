const CACHE_NAME = "praiaideal-shell-v2";
const SHELL = [
  "./",
  "./index.html",
  "./privacidade.html",
  "./manifest.json",
  "./icono.svg",
  "./favicon.ico",
  "./trilha1.jpg",
  "./trilha2.jpg",
  "./trilha3.jpg",
  "./trilha4.jpg",
  "./trilha5.jpg",
  "./trilha6.jpg",
  "./trilha7.jpg"
];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(key => key.startsWith("praiaideal-shell-") && key !== CACHE_NAME).map(key => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== "GET" || url.origin !== self.location.origin) return;

  event.respondWith(
    caches.match(request).then(cached => {
      if (cached) return cached;
      return fetch(request).then(response => {
        if (response.ok) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
        }
        return response;
      }).catch(() => request.mode === "navigate" ? caches.match("./index.html") : Response.error());
    })
  );
});