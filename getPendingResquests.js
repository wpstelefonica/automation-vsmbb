// Armazena as requisições pendentes
const pendingXHRRequests = new Set();

// Substitui o comportamento original do XMLHttpRequest
const originalXHR = window.XMLHttpRequest;
function newXHR(tracker = null) {
	const xhr = new originalXHR();
	
	//? OPENED = 1
	//? HEADERS RECEIVED = 2
	//? LOADING = 3
	//? DONE = 4
	// Monitora o estado da requisição
	xhr.addEventListener("readystatechange", function () {
		console.log(xhr);

		if (tracker && tracker !== xhr.name) return xhr;

		if (xhr.readyState === xhr.OPENED) {
			pendingXHRRequests.add(xhr);
		} else if (xhr.readyState === xhr.HEADERS_RECEIVED) {
			pendingXHRRequests.delete(xhr);
		}
	});

	return xhr;
}

window.XMLHttpRequest = newXHR;

// Exibe as requisições pendentes
setInterval(() => {
	console.log("Pending XHR requests:", pendingXHRRequests);
}, 1000);
