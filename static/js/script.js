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
    let kCentersFeild = document.querySelector('#k_centres');
    let algorithmSelect = document.querySelector('#algorithm_type');
    let distance = document.querySelector('.max_distance')

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
        postData('http://bessonv.pythonanywhere.com', { mlist: mlist, knum: knum, algorithm: algorithm })
        // postData('http://localhost:5000', { mlist: mlist, knum: knum, algorithm: algorithm })
            .then((data) => {
                console.log(data);
                
                data.klist.map(kpoint => {
                    let redMarker = mgeolist.find(marker => {
                        return marker.properties.get('id') == kpoint.id;
                    });
                    redMarker.options.set('preset', 'islands#redCircleDotIcon');
                });
                data.llist.forEach(line => {
                    let newLine = new ymaps.GeoObject({
                        geometry: {
                            type: "LineString",
                            coordinates: line
                        }
                    }, {
                        strokeColor: "#000000",
                        strokeWidth: 3,
                        stokeOpacity: 0.5
                    });
                    mlines.push(newLine);
                    map.geoObjects.add(newLine);
                });
                setMaxDistance(data.distance);
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

    ymaps.ready(init);

    function addToMarkerList(coords) {
        mullist.push([coords[0].toPrecision(6), coords[1].toPrecision(6)]);
        let marker = document.createElement("li");
        marker.classList.add('list-group-item');
        marker.appendChild(document.createTextNode(`Point ${currentId}: (${coords[0].toPrecision(6)}; ${coords[1].toPrecision(6)})`));
        markers.appendChild(marker);
    }

    function setMaxDistance(value) {
        if (value)
            distance.innerHTML = `${value.toPrecision(6)} Km`;
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