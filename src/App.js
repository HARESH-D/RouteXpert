import "leaflet/dist/leaflet.css"
import "./styles.css"

import MarkerClusterGroup from "react-leaflet-cluster";
import {MapContainer, TileLayer,Marker,Popup} from "react-leaflet"
import { Icon } from "leaflet";

function App() {
  const markers =[
    {
      geocode:[9.9380230, 78.1455106],
      popUp:<h4>AAVIN Madurai Cooperative Union</h4>
    },
    {
      geocode:[9.9275395, 78.1551085],
      popUp:<h4>Unit 1 Milk Dippo</h4>
    },
    {
      geocode:[9.9249500, 78.1190044],
      popUp:<h4>Unit 2 Milk Dippo </h4>
    },
    {
      geocode:[10.0491826, 78.0909542],
      popUp:<h4> Alanganallur Primary Union</h4>
    },
    {
      geocode:[9.9763294, 78.0472585],
      popUp:<h4>Samayapuram dippo</h4>
    },
    {
      geocode:[9.9034053, 78.1182406],
      popUp:<h4>Villapuram Dippo</h4>
    },
    {
      geocode:[9.9306199, 78.0905327],
      popUp:<h4>Sammandhipuram Dippo</h4>
    },
    {
      geocode:[9.9588585, 78.1883641  ],
      popUp:<h4>Kadachanendal Dippo</h4>
    },
    {
      geocode:[9.9511789, 78.2032951],
      popUp:<h4>Thiruvadhavoor Dippo</h4>
    },
    {
      geocode:[10.0196917, 78.1887116],
      popUp:<h4>Appan thirupathi Milk Dippo</h4>
    },
    {
      geocode:[10.3514997, 77.9664114 ],
      popUp:<h4>Nannaba nagar Dippo, Dindukkal</h4>
    },
    {
      geocode:[10.3645239, 77.9565688],
      popUp:<h4>Muthalagupatty Dippo, Dindukkal</h4>
    },
    {
      geocode:[10.3769173, 77.9789985],
      popUp:<h4>Sinnayaouram Dippo, Dindukkal</h4>
    }
  ];

  const customIcon = new Icon({
    iconUrl:"./gps.png",
    iconSize:[38,38] //Size of Icon
  })

  return (
     <MapContainer center={[9.9263459, 78.1423625]} zoom={13}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        <MarkerClusterGroup 
        chunkedLoading 
        >
          {markers.map(marker => (
          <Marker position = {marker.geocode} icon={customIcon}>
            <Popup>
              {marker.popUp}
            </Popup>
          </Marker>
        ))}
        </MarkerClusterGroup>
        
     </MapContainer>
  );
}

export default App;
