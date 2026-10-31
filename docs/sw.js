// Offline-first, stale-proof: page loads go to the network first (so fixes
// and updates arrive whenever there is signal) and fall back to the cached
// copy within 3 seconds when there isn't — which is the sideline case.
// Static assets stay cache-first.
const CACHE = "eagles-board-v3";
const ASSETS = ["./", "./index.html", "./manifest.json", "./icon-180.png", "./icon-512.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;

  if (e.request.mode === "navigate") {
    e.respondWith(
      Promise.race([
        fetch(e.request).then((res) => {
          if (res.ok) {
            const copy = res.clone();
            caches.open(CACHE).then((c) => {
              c.put(new Request("./index.html"), copy.clone());
              c.put(new Request("./"), copy);
            });
          }
          return res;
        }),
        new Promise((_, reject) => setTimeout(reject, 3000)),
      ]).catch(() =>
        caches.match(new Request("./index.html")).then((hit) => hit || Response.error())
      )
    );
    return;
  }

  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then(
      (hit) =>
        hit ||
        fetch(e.request).then((res) => {
          if (res.ok && new URL(e.request.url).origin === location.origin) {
            const copy = res.clone();
            caches.open(CACHE).then((c) => c.put(e.request, copy));
          }
          return res;
        })
    )
  );
});
