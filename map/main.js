import './style.css';
import {Map, View} from 'ol';
import Draw, {createBox} from 'ol/interaction/Draw.js';
import VectorLayer from 'ol/layer/Vector.js';
import VectorSource from 'ol/source/Vector.js';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import {transform, transformExtent} from 'ol/proj.js'
import Static from 'ol/source/ImageStatic.js';
import ImageLayer from 'ol/layer/Image.js';
import {getCenter} from 'ol/extent.js';
import { fromExtent } from 'ol/geom/Polygon';
import {easeOut} from 'ol/easing.js'

const osm =  new TileLayer({
      source: new OSM()
    });


const map = new Map({
  target: 'map',
  layers: [
    osm
  ],
  view: new View({
    center: [0, 0],
    zoom: 2
  })
});

// function setSource() {
//   const source = new Static({
//       url:
//         'https://planetarycomputer.microsoft.com/api/data/v1/item/preview.png?collection=sentinel-2-l2a&item=S2B_MSIL2A_20210924T190029_R013_T10TET_20210925T150542&assets=visual&asset_bidx=visual%7C1%2C2%2C3&nodata=0&format=png',
//       crossOrigin: '',
//       projection: 'EPSG:4326',
//       imageExtent: imageExtent,
//       interpolate: true,
//     });
//   imageLayer.setSource(source);
// }
// setSource();

let drawInteraction;
let drawnFeature = null;
            
// Add drawing functionality
function addDrawInteraction() {
  drawInteraction = new Draw({
    type: 'Circle',
    geometryFunction: createBox()
  });
        
  drawInteraction.on('drawstart', function(evt) {
      // Remove previous feature if exists
    if (drawnFeature) {
      map.removeLayer(drawnFeature);
    }
  });

  drawInteraction.on('drawend', function(evt) {
      // Remove previous feature if exists
    if (drawnFeature) {
      map.removeLayer(drawnFeature);
    }
            
    const feature = evt.feature;
    const geometry = feature.getGeometry();
    const extent = geometry.getExtent();
    
    // Convert coordinates from map projection to lon/lat
    const minCoord = transform(
        [extent[0], extent[1]],
        map.getView().getProjection(),
        'EPSG:4326'
    );
    const maxCoord = transform(
        [extent[2], extent[3]],
        map.getView().getProjection(),
        'EPSG:4326'
    );
    
    // Update form fields
    document.getElementById('input_min_lon').value = minCoord[0].toFixed(4);
    document.getElementById('input_min_lat').value = minCoord[1].toFixed(4);
    document.getElementById('input_max_lon').value = maxCoord[0].toFixed(4);
    document.getElementById('input_max_lat').value = maxCoord[1].toFixed(4);
    
    const vectorLayer = new VectorLayer({
        source: new VectorSource({
            features: [feature]
        })
    });
    
    map.addLayer(vectorLayer);
    drawnFeature = vectorLayer;
            
    // Remove the draw interaction after drawing
    map.removeInteraction(drawInteraction);
  });
        
  map.addInteraction(drawInteraction);
}
// Button to start drawing
document.getElementById('button_draw').addEventListener('click', function() {
        addDrawInteraction();
});    



// Слой для превью снимка
let previewLayer = null;


// Отображение превью снимка на карте
function showSnapshotPreview(snapshot) {
  const bbox = snapshot.getAttribute("data-bbox");
  const url = snapshot.getAttribute("data-url");
  const element_extent = JSON.parse(bbox);
    // Удаляем предыдущее превью, если есть
    if (previewLayer) {
        map.removeLayer(previewLayer);
    }
    
    // Преобразуем extent в систему координат карты
    const extent = transformExtent(
        element_extent,
        'EPSG:4326',
        'EPSG:3857'
    );
    
    // Создаем слой со статическим изображением
    previewLayer = new ImageLayer({
        source: new Static({
            url: url,
            imageExtent: extent,
            projection: 'EPSG:3857'
        }),
        opacity: 1
    });
    
    // Добавляем слой на карту
    map.addLayer(previewLayer);
    
    // Центрируем карту на снимке с плавной анимацией
    const view = map.getView();
              // Центрируем карту на снимке с плавной анимацией

    view.fit(extent, {
        padding: [100, 100, 100, 100],
        duration: 1000,
        easing: easeOut
    });
    // // Также можно приблизить к экстенту снимка
    // view.animate({
    //     resolution: view.getResolutionForExtent(extent) * 1.1,
    //     duration: 1200,
    //     easing: easeOut
    // });
}

const targetNode = document.getElementById('search_results');
const config = { attributes: true, childList: true, subtree: true };

const callback = function(mutationsList, observer) {
    const items = document.getElementsByClassName("item");
    for (let i = 0; i < items.length; i++) {
                items[i].onclick = function() {
                    showSnapshotPreview(this);
                };
    }
};

const observer = new MutationObserver(callback);
observer.observe(targetNode, config);






// item.onclick = function() { 
//   showSnapshotPreview(this);
// }
