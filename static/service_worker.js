/*
meaning of self:
By using self, you can refer to the global scope in a way that will work not only in a window context (self will resolve to window.self) but also in a worker context (self will then resolve to WorkerGlobalScope.self).
*/


self.addEventListener('install', function (event) {
    console.log('installing')
    event.waitUntil(
        caches.open('v1').then(function (cache) {
            return cache.addAll([
                '/static/scientist_scroller.html',
                '/static/manifest.json',
                '/static/service_worker.js',
                '/',
                '/player'
            ]);
        })
    );

    // // Activate right away. otherwise you need to close the tab and hit the page again
    // self.skipWaiting();
});


// can be used to update the service worker
self.addEventListener('activate', (event) => {
    console.log('activating')
    // workers dont immediately claim the sessions that load them, and require a refresh. However, this overrides that
    // https://frontendian.co/service-workers
    event.waitUntil(self.clients.claim());
    // var cacheKeeplist = ['v2'];

    // event.waitUntil(
    //     caches.keys().then((keyList) => {
    //         return Promise.all(keyList.map((key) => {
    //             if (cacheKeeplist.indexOf(key) === -1) {
    //                 return caches.delete(key);
    //             }
    //         }));
    //     })
    // );
});


// This is the event that is hijacked whenever a page with a service worker makes a fetch request
// for some reason it only happens after you refresh the page while a worker is running
self.addEventListener('fetch', function (event) {
    console.log('intercepted request')
    if (event.request.method != 'GET') return;
    event.respondWith(caches.match(event.request).then(function (response) {
        // caches.match() always resolves
        // but in case of success response will have value
        if (response !== undefined) {
            return response;
        } else {
            return fetch(event.request).then(function (response) {
                // response may be used only once
                // we need to save clone to put one copy in cache
                // and serve second one
                let responseClone = response.clone();

                caches.open('v1').then(function (cache) {
                    cache.put(event.request, responseClone);
                });
                return response;
            }).catch(function () {
                return caches.match('/sw-test/gallery/myLittleVader.jpg');
            });
        }
    }));
});