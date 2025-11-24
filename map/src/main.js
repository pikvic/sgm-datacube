import './style.css';
import Map from 'ol/Map.js';
import OSM from 'ol/source/OSM.js';
import TileLayer from 'ol/layer/WebGLTile.js';
import GeoTIFF from 'ol/source/GeoTIFF.js';
import ImageLayer from 'ol/layer/Image.js';
import Projection from 'ol/proj/Projection.js';
import View from 'ol/View';

let map;
let currentLayer = null;


const source = new GeoTIFF({
  sources: [
    {
      url: 'https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/36/Q/WD/2020/7/S2A_36QWD_20200701_0_L2A/TCI.tif',
    },
  ],
});

map = new Map({
  target: 'map',
  layers: [
   new TileLayer({
      source: new OSM()
    }),
  ],
  view: new View({
    center: [131, 45],
    zoom: 3
  }),
});


// const addImageToMap = (bboxStr, polygonCoords, title) => {
//   // Удаляем предыдущий слой
//   if (currentLayer) {
//     map.removeLayer(currentLayer);
//     currentLayer = null;
//   }

//     const imageLayer = new ImageLayer({
//         source: new Static({
//           attributions: '© <a href="https://xkcd.com/license.html">xkcd</a>',
//           url: 'https://imgs.xkcd.com/comics/online_communities.png',
//           projection: projection,
//           imageExtent: extent,
//         }),
//       }),

//   // Парсим BBOX
//   const bbox = bboxStr.split(',').map(Number);
//   const extent = ol.proj.transformExtent([
//     bbox[0], bbox[1],
//     bbox[2], bbox[3]
//   ], 'EPSG:4326', 'EPSG:3857');


//   // Создаем слой с изображением (заглушка)
 

//   map.addLayer(imageLayer);
//   currentLayer = imageLayer;

//   // Центрируем и зумим
//   map.getView().fit(extent, { padding: [50, 50, 50, 50] });
// };