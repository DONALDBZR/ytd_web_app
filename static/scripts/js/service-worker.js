const main_cache_name = "extractio-app-cache-v2";
const uniform_resource_locators_to_cache = [
    "/",
    "/static/stylesheets/ytd.css",
    "/static/stylesheets/desktop.css",
    "/static/stylesheets/tablet.css",
    "/static/stylesheets/mobile.css",
    "https://unpkg.com/react@18/umd/react.production.min.js",
    "https://unpkg.com/react-dom@18/umd/react-dom.production.min.js",
    "https://unpkg.com/@babel/standalone/babel.min.js",
    "/static/scripts/js/ytd.js",
    "/static/scripts/views/Header.js",
    "/static/scripts/views/Main.js",
    "/static/scripts/views/Footer.js",
    "/manifest.json",
    "/static/images/icons/Extractio.png",
];
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(main_cache_name)
        .then((cache) => {
            return cache.addAll(uniform_resource_locators_to_cache);
        })
    );
});
self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request)
        .then((response) => {
            return response || fetch(event.request);
        })
    );
});
self.addEventListener("activate", (event) => {
    const cache_whitelist = [main_cache_name];
    event.waitUntil(
        caches.keys()
        .then((cache_names) => {
            return Promise.all(cache_names.map((cache_name) => {
                if (cache_whitelist.indexOf(cache_name) === -1) {
                    return caches.delete(cache_name);
                }
            }));
        })
    );
});