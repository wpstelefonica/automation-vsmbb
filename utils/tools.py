import time
from selenium import webdriver


class Tools():
    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver

    def request_tracker(self) -> None:
        self.driver.execute_script("""
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
        if (xhr.readyState === xhr.OPENED) {
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
        """)

    def wait_all_requests_done(self):
        while True:
            response = self.driver.execute_script(
                "return window.pendingXHRRequests.size")
            if response == 0:
                break
            time.sleep(1)
