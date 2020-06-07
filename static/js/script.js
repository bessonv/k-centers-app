window.onload = () => {
    let map;
    let mgeolist = [];
    let mullist = [];
    let mlines = [];
    let currentId = 0;
    let markers = document.querySelector('.markers');
    let sendButton = document.querySelector('.send_button');
    let clearButton = document.querySelector('.clear_button');
    let resetButton = document.querySelector('.reset_button');
    let kCentersFeild = document.querySelector('#k_centers');
    let algorithmSelect = document.querySelector('#algorithm_type');
    let distance = document.querySelector('.max_distance');
    let algorithmOptions = [];

    async function postData(url = '', data = {}) {
        const response = await fetch(url, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    }

    sendButton.onclick = () => {
        let mlist = [];
        let knum = parseInt(kCentersFeild.value);
        let algorithm = algorithmSelect.value;
        let options = getOptionValue();

        if (!(mlist && knum && algorithm)) {
            alert('One of the options is empty');
            return;
        }
        mgeolist.map(marker => {
            mlist.push({
                id: marker.properties.get('id'),
                coordinates: [
                    parseFloat(marker.geometry.getCoordinates()[0]),
                    parseFloat(marker.geometry.getCoordinates()[1])
                ]
            });
        });
        console.log(mlist, knum);
        postData('http://bessonv.pythonanywhere.com', { mlist: mlist, knum: knum, algorithm: algorithm, options: options })
        // postData('http://localhost:5000', { mlist: mlist, knum: knum, algorithm: algorithm, options: options })
            .then((data) => {
                console.log(data);
                
                data.klist.map(kpoint => {
                    let redMarker = mgeolist.find(marker => {
                        return marker.properties.get('id') == kpoint.id;
                    });
                    // redMarker.options.set('preset', 'islands#redCircleDotIcon');
                    redMarker.options.set('preset', 'islands#redCircleIcon');
                    // redMarker.options.set({preset: 'islands#redIcon'});
                    redMarker.properties.set({
                        iconContent: kpoint.id,
                        balloonContentHeader: "k-center",
                        balloonContentBody: `Point ${kpoint.id}: (${kpoint.coordinates[0]}, ${kpoint.coordinates[1]})`,
                        hintContent:  kpoint.id
                    });
                });
                let maxPath = data.path.ids;
                let max_distance = data.distance;
                data.plist.forEach(path => {
                    ymaps.route(
                        path.coordinates,
                    {
                        multiRoute: false
                    }).then(route => {
                        route.getPaths().options.set({
                            strokeColor: "#000000",
                            strokeOpacity: "0.5"
                        })
                        let startPoint = route.getWayPoints().get(0);
                        let endPoint = route.getWayPoints().get(1);
                        // startPoint.options.set({preset: 'islands#redCircleDotIcon'});
                        startPoint.options.set({preset: 'islands#redCircleIcon'});
                        // startPoint.options.set({preset: 'islands#redIcon'});
                        startPoint.properties.set({
                            iconContent: path.ids[0],
                            balloonContentHeader: "k-center",
                            balloonContentBody: `Point ${path.ids[0]}: (${startPoint.geometry._coordinates[0]}, ${startPoint.geometry._coordinates[1]})`,
                            hintContent: path.ids[0]
                        });
                        endPoint.options.set({preset: 'islands#blueCircleDotIcon'});
                        if (
                            path.ids[0] == maxPath[0] && path.ids[1] == maxPath[1] ||
                            path.ids[1] == maxPath[0] && path.ids[1] == maxPath[0]
                            ) {
                            maxLength = route.getLength();
                            setMaxDistance(maxLength);
                            route.getPaths().options.set({
                                strokeColor: "#ed4543",
                                strokeOpacity: "1"
                            })
                        }
                        mlines.push(route);
                        map.geoObjects.add(route);
                    }).catch(e => {
                        console.log(e);
                    });
                });
            })
            .catch((e) => {
                console.log(e);
            });
    }

    resetButton.onclick = () => {
        mgeolist = [];
        mullist = [];
        currentId = 0;
        markers.innerHTML = '';
        distance.innerHTML = '';
        map.geoObjects.removeAll();
    }

    clearButton.onclick = () => {
        mlines.forEach(line => {
            map.geoObjects.remove(line);
        });
        mgeolist.forEach(marker => {
            marker.options.set('preset', 'islands#blueCircleDotIcon');
        });
        distance.innerHTML='';
        mlines = [];
    }

    algorithmSelect.onchange = (event) => {
        if (algorithmSelect.value) {
            let algorithm = algorithmSelect.value;
            let options = document.querySelector(`#${algorithm}`);
            let active = document.querySelector('.active');
            algorithmOptions = [];
            if (active) {
                active.classList.remove('active');
                active.classList.add('hidden')
            }
            if (options) {
                options.classList.remove('hidden');
                options.classList.add('active');
            }
        }
    }

    function getOptionValue() {
        document.querySelectorAll('.active .option').forEach(option => {
            algorithmOptions.push({
                name: `${option.id}`,
                value: parseInt(option.value)
            });
        });
        return algorithmOptions;
    }

    ymaps.ready(init);

    function addToMarkerList(coords) {
        mullist.push([coords[0].toPrecision(6), coords[1].toPrecision(6)]);
        let marker = document.createElement("li");
        marker.classList.add('list-group-item');
        marker.appendChild(document.createTextNode(`Point ${currentId}: (${coords[0].toPrecision(6)}; ${coords[1].toPrecision(6)})`));
        markers.appendChild(marker);
    }

    function setMaxDistance(value) {
        if (value) {
            value = value / 1000;
            distance.innerHTML = `${value.toPrecision(6)} Km`;
        }
    }

    function init() {
        map = new ymaps.Map("map", {
            center: [55.76, 37.64],
            zoom: 7
        });

        map.events.add('click', e => {
            let coords = e.get('coords');
            addToMarkerList(coords);

            newMarker = new ymaps.GeoObject({
                geometry: {
                    type: "Point",
                    coordinates: [
                        coords[0].toPrecision(6),
                        coords[1].toPrecision(6)
                    ]
                }
            }, {
                preset: 'islands#blueCircleDotIcon'
            });

            newMarker.properties.set({
                hintContent: currentId.toString(),
                id: currentId++
            });
            
            mgeolist.push(newMarker);
            map.geoObjects.add(newMarker);
            // console.log(newMarker.properties.get('id'));
            // console.log(parseFloat(newMarker.geometry.getCoordinates()[0]));
        });
    }
}