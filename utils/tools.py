import time
from selenium import webdriver
from enum import Enum


class Variables(Enum):
    PENDING = 0
    DONE = 1
    ERROR = 2


class Tools():
    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver

    def request_tracker(self) -> None:
        script = """
// Armazena as requisições pendentes
window.pendingXHRRequests = new Set();
window.XHRRequestsFinishedNoError = new Set();
window.XHRRequestsFinishedWithError = new Set();

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

        // if (tracker && tracker !== xhr.name) return xhr;
        console.log("request readyState", xhr.readyState);
        console.log("request status", xhr.status);
        if (xhr.readyState === xhr.OPENED && !xhr.contains) {
            window.pendingXHRRequests.add(xhr);
        } else if (xhr.readyState === xhr.HEADERS_RECEIVED) {
            window.pendingXHRRequests.delete(xhr);
        } else if (xhr.readyState === xhr.DONE) {
            if (!(xhr.status >= 200 && xhr.status <= 299)) {
                window.XHRRequestsFinishedWithError.add(xhr)
            }
            window.XHRRequestsFinishedNoError.add(xhr)
        }
    });

    return xhr;
}

window.XMLHttpRequest = newXHR;

// Exibe as requisições pendentes
setInterval(() => {
    console.log("Pending XHR requests:", window.pendingXHRRequests);
}, 1000);
        """
        script_backup = """

        """

        self.driver.execute_script(script)

    def wait_all_requests_done(self):
        while True:
            response = self.driver.execute_script(
                "return window.pendingXHRRequests.size")
            if response == 0:
                break
            time.sleep(1)

    def get_requests_data(self, argument: str) -> dict:
        script = f"""
let requests = [...window.{argument}""" + """] || [];
console.log("requests", requests);
return requests.map((req) => ({
	status: req.status,
	statusText: req.statusText,
	responseURL: req.responseURL,
	responseType: req.responseType,
	responseText: req.responseText,
	readyState: req.readyState,
	data: {
		url: req.__zone_symbol__xhrTask.data.url,
		args: req.__zone_symbol__xhrTask.data.args,
	},
}));
"""
        response = self.driver.execute_script(script)

        return response

    def get_queries_script_and_status_response(self):

        variabel_no_error = "XHRRequestsFinishedWithError"
        variabel_with_error = "XHRRequestsFinishedWithError"
        variabel_pendings = "pendingXHRRequests"

        no_error_requests = self.get_requests_data(variabel_no_error)
        error_requests = self.get_requests_data(variabel_with_error)
        pending_requests = self.get_requests_data(variabel_pendings)

        data = {"no_error_requests": [],
                "error_requests": [], "pending_requests": []}

        for request in no_error_requests:
            temp = {
                "status": request["status"],
                "query_script": request["data"]["args"][0],
            }
            data["no_error_requests"].append(temp)

        for request in error_requests:
            temp = {
                "status": request["status"],
                "query_script": request["data"]["args"][0],
            }
            data["error_requests"].append(temp)

        for request in pending_requests:
            temp = {
                "status": request["status"],
                "query_script": request["data"]["args"][0],
            }
            data["pending_requests"].append(temp)

        # requests_done = self.driver.execute_script(
        #     "return JSON.parse(Array.from(window.XHRRequestsFinishedNoError)[0].__zone_symbol__xhrTask.data.args[0])")
        # JSON.parse(Array.from(window.XHRRequestsFinishedNoError)[0].__zone_symbol__xhrTask.data.args[0])

        return data
