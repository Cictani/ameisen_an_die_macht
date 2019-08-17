(function () {
    const BING_API_KEY = document.currentScript.getAttribute('bingApiKey')
    class AntMap {
        constructor() {
            this._bingApiKey = BING_API_KEY
            this._markers = []
            this._users = []

            this.initMap()
        }

        initMap() {
            this._map = L.map('map')
                .setView([45, 10], 4);
            this.initBingLayer()
            this.initClusterGroup()
            this.updateMap();    
        }

        initClusterGroup() {
            this._clusterGroup = L.markerClusterGroup()
            this._map.addLayer(this._clusterGroup);
        }

        initBingLayer() {
            const options = {
                bingMapsKey: this._bingApiKey,
                imagerySet: 'Road',
                culture: 'de-de'
            }
            L.tileLayer.bing(options).addTo(this._map)
        }

        async getCurrentPosition() {
            return new Promise((resolve, reject) => {
                if ("geolocation" in navigator) {
                    navigator.geolocation.getCurrentPosition(position => {
                        const lat = position.coords.latitude
                        const lng = position.coords.longitude
                        resolve([lat, lng])
                    }, error => {
                        if (error.code == error.PERMISSION_DENIED) {
                            reject("Can't get current position since you denied access to your location")
                        }
                    });
                } else {
                    reject('geolocation is not supported by your browser')
                }
            })
        }

        focusOnCurrentPosition(zoom) {
            this.getCurrentPosition()
                .then(pos => {
                    this._map.setView(pos, zoom)
                })
                .catch(error => {
                    console.log(error)
                })
        }

        removeMarkers() {
            this._clusterGroup.clearLayers();
            this._markers = []
        }

        updateMap() {    
            this._users = []
            fetch("/api/discord-users/")
                .then(response => response.json())
                .then(data => {
                    this._users = data
                    this.updateMarkers()
                })
        }

        updateMarkers() {
            this.removeMarkers()
    
            for (var user of this._users) {
                const userCoordinates = user.location.coordinates;
                var plotll = new L.LatLng(userCoordinates[1], userCoordinates[0], true);
                var plotmark = new L.Marker(plotll);
                plotmark.bindPopup(`${user.username}, ${user.address}`);
                this._markers.push(plotmark)
                this._clusterGroup.addLayer(plotmark)
            }
        }
    }

    window.onload = () => {
        const map = new AntMap()
    }
}) ();