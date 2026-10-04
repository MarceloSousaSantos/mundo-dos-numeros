const CACHE = "mundo-numeros-public-v1";
const ASSETS = ["/", "/static/css/app.css", "/static/manifest.webmanifest"];
self.addEventListener("install", event => event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(ASSETS))));
self.addEventListener("fetch", event => { if (event.request.method !== "GET" || new URL(event.request.url).origin !== location.origin) return; const url = new URL(event.request.url); if (!url.pathname.startsWith("/static/") && url.pathname !== "/") return; event.respondWith(caches.match(event.request).then(found => found || fetch(event.request))); });
