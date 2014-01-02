function addMarker(map, position, text) {
	var marker = new daum.maps.Marker({
		position: position
	});
	marker.setTitle(text);
	marker.setMap(map);
	if (text != null && text.length > 0) {
		var infowindow = new daum.maps.InfoWindow({
			content: text,
			disableAutoPan: true
		});
		infowindow.open(map, marker);
	}
	return marker;
}

function initMap(options) {
	var lat = 33.4780117808;
	var lng = 126.489289086;
	var position = new daum.maps.LatLng(lat, lng);
	var map = new daum.maps.Map(document.getElementById('map'), {
		center: position,
		level: 4,
		mapTypeId: daum.maps.MapTypeId.ROADMAP,
		draggable: true
	});
	var zoom = new daum.maps.ZoomControl();
	map.addControl(zoom);

	if (!options || !options.disableDefaultMarker) {
		addMarker(map, position, "<div class='info-content'>충신교회</div>");
	}
	return map;
}
