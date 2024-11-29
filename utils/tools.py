from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException

import time
from enum import Enum


class Variables(Enum):
    PENDING = 0
    DONE = 1
    ERROR = 2


class Tools():
    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver
        self.responses_model = {}

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

        self.driver.execute_script(script)

    def wait_all_requests_done(self):
        counter = 0
        while True and counter <= 60:
            response = self.driver.execute_script(
                "return window.pendingXHRRequests.size")
            if response == 0:
                break
            time.sleep(1)
            counter += 1

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

        no_error_requests = self.get_requests_data(
            "XHRRequestsFinishedNoError")
        error_requests = self.get_requests_data("XHRRequestsFinishedWithError")
        pending_requests = self.get_requests_data("pendingXHRRequests")

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

        return data

    def set_responses_with_updated_data(self, msisdn: str = None, date_from: str = None, date_to: str = None):
        date_to_splited = date_to.split("/")
        date_from_splited = date_from.split("/")

        date_to_formated = f"{
            date_to_splited[2]}-{date_to_splited[0]}-{date_to_splited[1]}"
        date_from_formated = f"{
            date_from_splited[2]}-{date_from_splited[0]}-{date_from_splited[1]}"

        self.responses_model = {
            "getFilterSigRegional": '{"query":"\\nSELECT\\n  \\"sig_regional\\"\\nFROM \\"celulas\\"\\nWHERE \\"__time\\" BETWEEN TIMESTAMP \'' + date_from_formated +
            ' 00:00:00\' AND TIMESTAMP \'' + date_to_formated +
            ' 23:59:59\'\\nGROUP BY \\"sig_regional\\"\\n","context":{}}',

            "getUserGrouped": '{"query":"\\nSELECT\\n  \\"__time\\" as \\"__time\\",\\n  \\"msisdn\\",\\n  \\"imsi\\",\\n  \\"desc_fabricante\\",\\n  \\"modelo\\",\\n  \\"tac_tecnologia\\",\\n  \\"desc_modelo\\"\\nFROM \\"cem-enrichment\\"\\nWHERE \\"msisdn\\" = \'' + msisdn + '\' AND \\"__time\\" BETWEEN \'' +
            date_from_formated + ' 00:00:00\' AND \'' + date_to_formated +
            ' 23:59:59\' AND \\"apn\\" NOT LIKE \'ims%\'\\nORDER BY \\"__time\\" DESC LIMIT 1\\n","context":{}}',

            "getUserSessionsDetails": '{"query":"\\nSELECT\\n  \\"__time\\" as time_second,\\n  \\"tecnologia\\" AS tecnologia,\\n  \\"cellname\\",\\n  \\"municipio\\",\\n  \\"uf\\",\\n  \\"sig_regional\\",\\n  \\"causeforrecclosing\\",\\n  \\"banda\\",\\n  \\"setor\\",\\n  \\"datavolumeuplink\\" as totalUplinkg,\\n  \\"datavolumedownlink\\" as totalDownlinkg,\\n  \\"duration\\" as dur_total,\\n  \\"diagnostics\\"\\nFROM \\"cem-enrichment\\"\\nWHERE \\"msisdn\\" = \''+msisdn+'\'\\n  AND \\"__time\\" BETWEEN \'' +
            date_from_formated+' 00:00:00\' AND \''+date_to_formated +
            ' 23:59:59\'\\n  AND \\"apn\\" not like \'ims%\'\\nORDER BY \\"__time\\" ASC\\nlimit 10000\\n","context":{}}',

            "getIndicatorData": '{"query":"\\n    SELECT\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" ELSE 0 END))*100,2) as porc_Uplink_2g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" ELSE 0 END))*100,2) as porc_Uplink_3g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" ELSE 0 END))*100,2) as porc_Uplink_4g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" ELSE 0 END))*100,2) as porc_Uplink_5g,\\n\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_Downlink_2g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_Downlink_3g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_Downlink_4g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_Downlink_5g,\\n\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_total_2g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_total_3g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_total_4g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_total_5g,\\n\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'02\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_2g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'01\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_3g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_4g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'10\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_5g\\nFROM \\"cem-enrichment\\"\\nWHERE msisdn = \''+msisdn+'\'\\n AND \\"__time\\" BETWEEN \'' +
            date_from_formated+' 00:00:00\' AND \''+date_to_formated +
            ' 23:59:59\'\\n AND \\"apn\\" not like \'ims%\'\\n  ","context":{}}',

            "getFailResumeByUC": '{"query":"\\n       SELECT\\nsum(totalUplinkg+totalDownlinkg) as Total_Traffic,\\nROUND((CAST(sum(total4g) as float)/sum(totalUplinkg+totalDownlinkg))*100,2) as Escoamento_4G,\\nROUND((CAST(sum(dur_4g) as float)/sum(dur_total))*100,2) as Reten_4G,\\nROUND((CAST(sum(total2g) as float)/sum(totalUplinkg+totalDownlinkg))*100,2) as Escoamento_2G,\\nROUND((CAST(sum(dur_2g) as float)/sum(dur_total))*100,2) as Reten_2G,\\n \\nROUND((CAST(sum(total3g) as float)/sum(totalUplinkg+totalDownlinkg))*100,2) as Escoamento_3G,\\nROUND((CAST(sum(dur_3g) as float)/sum(dur_total))*100,2) as Reten_3G,\\n \\nROUND((CAST(sum(total4g) as float)/sum(totalUplinkg+totalDownlinkg))*100,2) as Escoamento_4G,\\nROUND((CAST(sum(dur_4g) as float)/sum(dur_total))*100,2) as Reten_4G,\\n \\nROUND((CAST(sum(total5g) as float)/sum(totalUplinkg+totalDownlinkg))*100,2) as Escoamento_5G,\\nROUND((CAST(sum(dur_5g) as float)/sum(dur_total))*100,2) as Reten_5G,\\nCOUNT(1) as Total_Hours,\\nCOUNT(CASE when porc_ses_4g < 95 and perc_cnn < 70 and ses_total > 10 then 1 else null end) as UCpingPong,\\nCOUNT(CASE when porc_ses_4g < 95 and perc_cnn > 70 then 1 else null end) as UCGapService,\\nCOUNT(CASE when porc_ses_4g > 95 and perc_cnn > 70 and ses_total > 10 then 1 else null end) as UCDropSession,\\nCOUNT(CASE when porc_ses_4g > 95 and perc_cnn > 70 and ses_total < 10 then 1 else null end) as UCConectaNoNavega,\\nROUND((CAST(COUNT(CASE when porc_ses_4g < 95 and perc_cnn < 70 and ses_total > 10 then 1 else null end) as float)/COUNT(1))*100,2) as Porc_UCpingPong,\\nROUND((CAST(COUNT(CASE when porc_ses_4g < 95 and perc_cnn > 70 then 1 else null end) as float)/COUNT(1))*100,2) as Porc_UCGapService,\\nROUND((CAST(COUNT(CASE when porc_ses_4g > 95 and perc_cnn > 70 and ses_total > 10 then 1 else null end) as float)/COUNT(1))*100,2) as Porc_UCDropSession,\\nROUND((CAST(COUNT(CASE when porc_ses_4g > 95 and perc_cnn > 70 and ses_total < 10 then 1 else null end) as float)/COUNT(1))*100,2) as Porc_UCConectaNoNavega,\\nsum(ses_total) as Total_Sessions,\\nSUM(cnn) as CnN_Sessions,\\nROUND((CAST(SUM(cnn)as float)/sum(ses_total))*100,2) as Porc_CnN_Sessions,\\nsum(abnormal_R) as abnormal_Releases,\\nROUND((CAST(sum(abnormal_R) as float)/sum(ses_total))*100,2) as Porc_abnR_Sessions\\nFROM (\\nSELECT\\n TIME_FLOOR(\\"__time\\", \'PT1H\') AS \\"__time\\",\\n sum(CASE\\n   WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\')  AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\'\\n THEN 1 ELSE 0 END) as cnn,\\n ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\')  AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\' THEN 1 ELSE 0 END) as float)/COUNT(1))*100,2) as perc_cnn,\\n SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total4g,\\n SUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total2g,\\n  SUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total3g,\\n    SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total5g,\\n\\n\\n SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplinkg,\\n SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlinkg,\\n SUM(CASE WHEN \\"rattype\\" in (\'01\', \'02\', \'06\', \'10\') THEN 1 ELSE 0 END) AS ses_total,\\n ROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g,\\n SUM(case when \\"rattype\\" IN (\'06\', \'08\') then \\"duration\\" else 0 end) as dur_4g,\\n  SUM(case when \\"rattype\\" IN (\'10\') then \\"duration\\" else 0 end) as dur_5g,\\n\\n  SUM(case when \\"rattype\\" IN (\'02\') then \\"duration\\" else 0 end) as dur_2g,\\n    SUM(case when \\"rattype\\" IN (\'01\') then \\"duration\\" else 0 end) as dur_3g,\\n\\n SUM(duration) as dur_total,\\n COUNT(CASE when \\"causeforrecclosing\\" = \'04 - abnormalRelease\' then 1 else null end) as abnormal_R\\nFROM \\"cem-enrichment\\"\\nWHERE msisdn = \'' +
            msisdn+'\'\\n AND \\"__time\\" BETWEEN \''+date_from_formated +
            ' 00:00:00\' AND \''+date_to_formated +
            ' 23:59:59\'\\n AND \\"apn\\" not like \'ims%\'\\n GROUP BY 1)\\n  ","context":{}}',

            "getLocationsInfo": '{"query":"\\nSELECT\\n   \\n   \\"cellname\\",\\n    \\"rattype\\",\\n   \\"num_lat_dec\\",\\n   \\"num_lon_dec\\",\\n   \\"sigla_site\\",\\n   SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total4g,\\n   SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total5g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\')  AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\'  THEN 1 ELSE 0 END) as float)/COUNT(1))*100,2) as perc_cnn,\\n\\n   SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlink4g,\\n   SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlink5g,\\n\\n   SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplink4g,\\n   SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplink5g,\\n   SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplink,\\n   SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlink,\\n\\n   SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as totalDataVolume,\\n\\n   SUM(case when \\"rattype\\" = \'02\' then 1 else 0 end) as ses_2g,\\n   SUM(case when \\"rattype\\" = \'01\' then 1 else 0 end) as ses_3g,\\n   SUM(case when \\"rattype\\" = \'06\' then 1 else 0 end) as ses_4g_lte,\\n   SUM(case when \\"rattype\\" = \'08\' then 1 else 0 end) as ses_4g_iot,\\n   SUM(case when \\"rattype\\" IN (\'06\',\'08\') then 1 else 0 end) as ses4gTotal,\\n   SUM(case when \\"rattype\\" = \'10\' then 1 else 0 end) as ses5gTotal,\\n   SUM(CASE WHEN \\"rattype\\" in (\'01\', \'02\', \'06\', \'10\') THEN 1 ELSE 0 END) AS ses_total,\\n   ROUND((CAST(SUM(case when \\"rattype\\" = \'02\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_2g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" = \'01\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_3g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" = \'06\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g_lte,\\n   ROUND((CAST(SUM(case when \\"rattype\\" = \'08\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g_iot,\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" = \'10\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_5g,\\n   SUM(case when \\"rattype\\" = \'02\' then \\"duration\\" else 0 end) as dur_2g,\\n   SUM(case when \\"rattype\\" = \'01\' then \\"duration\\" else 0 end) as dur_3g,\\n   SUM(case when \\"rattype\\" = \'06\' then \\"duration\\" else 0 end) as dur_4g_lte,\\n   SUM(case when \\"rattype\\" = \'08\' then \\"duration\\" else 0 end) as dur_4g_iot,\\n   SUM(case when \\"rattype\\" IN (\'06\', \'08\') then \\"duration\\" else 0 end) as dur_4g,\\n   SUM(case when \\"rattype\\" = \'10\' then \\"duration\\" else 0 end) as dur_5g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_duration_4g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'10\') then 1 else 0 end) as float)/SUM(duration))*100,2) as porc_duration_5g,\\n   SUM(duration) as dur_total\\nFROM \\"cem-enrichment\\"\\nWHERE \\"__time\\" BETWEEN \'' +
            date_from_formated+' 00:00:00\' AND \''+date_to_formated +
            ' 23:59:59\'\\n AND  msisdn = \''+msisdn +
            '\'\\n AND \\"apn\\" not like \'ims%\'\\nGROUP BY 1,2,3,4,5\\nORDER BY \\"cellname\\" DESC\\n","context":{}}',

            "getCellsUsedbyUser": '{"query":"\\nSELECT\\n msisdn,\\n rattype,\\n cellname,\\n municipio,\\n banda,\\n setor,\\n  sum(CASE\\n   WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\')  AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\'\\n THEN 1 ELSE 0 END) as cnn,\\n ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\' THEN 1 ELSE 0 END) as float)/COUNT(1))*100,2) as perc_cnn,\\n\\n SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total4g,\\n SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplink,\\n SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlink,\\n sum(\\"datavolumeuplink\\" + \\"datavolumedownlink\\") as \\"totalDataVolume\\",\\n\\n SUM(CASE WHEN \\"rattype\\" in (\'01\', \'02\', \'06\', \'10\') THEN 1 ELSE 0 END) AS ses_total,\\n\\n SUM(duration) as dur_total\\nFROM \\"cem-enrichment\\"\\nWHERE \\"msisdn\\" = \'' +
            msisdn + '\' AND (TIMESTAMP \'' +
            date_from_formated + ' 00:00:00\' <= \\"__time\\" AND \\"__time\\" < TIMESTAMP \'' +
            date_to_formated
            + ' 23:59:59\') AND \\"apn\\" not like \'ims%\'\\nGROUP BY 1,2,3,4,5,6\\norder by totalDataVolume desc\\n","context":{}}',

            "getSessionsGroupedTime": '{"query":"\\nSELECT\\n TIME_FLOOR(\\"__time\\", \'PT1H\') AS \\"__time\\",\\n sum(CASE\\n   WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\')  AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\'\\n THEN 1 ELSE 0 END) as cnn,\\n ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\' THEN 1 ELSE 0 END) as float)/COUNT(1))*100,2) as perc_cnn,\\n SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total4g,\\n SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total5g,\\n SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlink4g,\\n SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlink5g,\\n SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplink4g,\\n SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplink5g,\\n SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplinkg,\\n SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlinkg,\\n SUM(case when \\"rattype\\" = \'02\' then 1 else 0 end) as ses_2g,\\n SUM(case when \\"rattype\\" = \'01\' then 1 else 0 end) as ses_3g,\\n SUM(case when \\"rattype\\" = \'06\' then 1 else 0 end) as ses_4g_lte,\\n SUM(case when \\"rattype\\" = \'08\' then 1 else 0 end) as ses_4g_iot,\\n SUM(case when \\"rattype\\" IN (\'06\',\'08\') then 1 else 0 end) as ses4gTotal,\\n SUM(case when \\"rattype\\" = \'10\' then 1 else 0 end) as ses5gTotal,\\n SUM(CASE WHEN \\"rattype\\" in (\'01\', \'02\', \'06\', \'10\') THEN 1 ELSE 0 END) AS ses_total,\\n ROUND((CAST(SUM(case when \\"rattype\\" = \'02\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_2g,\\n ROUND((CAST(SUM(case when \\"rattype\\" = \'01\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_3g,\\n ROUND((CAST(SUM(case when \\"rattype\\" = \'06\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g_lte,\\n ROUND((CAST(SUM(case when \\"rattype\\" = \'08\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g_iot,\\n ROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g,\\n ROUND((CAST(SUM(case when \\"rattype\\" = \'10\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_5g,\\n SUM(case when \\"rattype\\" = \'02\' then \\"duration\\" else 0 end) as dur_2g,\\n SUM(case when \\"rattype\\" = \'01\' then \\"duration\\" else 0 end) as dur_3g,\\n SUM(case when \\"rattype\\" = \'06\' then \\"duration\\" else 0 end) as dur_4g_lte,\\n SUM(case when \\"rattype\\" = \'08\' then \\"duration\\" else 0 end) as dur_4g_iot,\\n SUM(case when \\"rattype\\" IN (\'06\', \'08\') then \\"duration\\" else 0 end) as dur_4g,\\n SUM(case when \\"rattype\\" = \'10\' then \\"duration\\" else 0 end) as dur_5g,\\n ROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_duration_4g,\\n ROUND((CAST(SUM(case when \\"rattype\\" IN (\'10\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_duration_5g,\\n SUM(duration) as dur_total\\nFROM \\"cem-enrichment\\"\\nWHERE msisdn = \'' +
            msisdn + '\'\\n AND \\"__time\\" BETWEEN \'' +
            date_from_formated + ' 00:00:00\' AND \''+date_to_formated +
            ' 23:59:59\'\\n AND \\"apn\\" not like \'ims%\'\\nGROUP BY 1\\nORDER BY 1\\n","context":{}}',

            "getTotalTrafficByTechLine": '{"query":"\\nSELECT\\nTIME_FLOOR(__time, \'PT1H\') as floor_1_hour,\\nSUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total2g,\\nSUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total3g,\\nSUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total4g,\\nSUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total5g,\\n\\nSUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumedownlink\\" ELSE 0 END) as downloadTotalLinkByTech_2g,\\nSUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumedownlink\\" ELSE 0 END) as getDownloadLinkByTech_3g,\\nSUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as downloadTotalLinkByTech_4g,\\nSUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumedownlink\\" ELSE 0 END) as getDownloadLinkByTech_5g,\\n\\nSUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\" ELSE 0 END) as upLinkTotalLinkByTech_2g,\\nSUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\" ELSE 0 END) as getUpLinkByTech_3g,\\nSUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as upLinkTotalLinkByTech_4g,\\nSUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" ELSE 0 END) as getUpLinkByTech_5g,\\n\\nSUM(case when \\"rattype\\" = \'02\' then 1 else 0 end) as ses_2g,\\nSUM(case when \\"rattype\\" = \'01\' then 1 else 0 end) as ses_3g,\\nSUM(case when \\"rattype\\" = \'06\' then 1 else 0 end) as ses_4g_lte,\\nSUM(case when \\"rattype\\" = \'08\' then 1 else 0 end) as ses_4g_iot,\\nSUM(case when \\"rattype\\" IN (\'06\',\'08\') then 1 else 0 end) as ses4gTotal,\\nSUM(case when \\"rattype\\" = \'10\' then 1 else 0 end) as ses5gTotal,\\nSUM(CASE WHEN \\"rattype\\" in (\'01\', \'02\', \'06\', \'10\') THEN 1 ELSE 0 END) AS ses_total,\\nROUND((CAST(SUM(case when \\"rattype\\" = \'02\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_2g,\\nROUND((CAST(SUM(case when \\"rattype\\" = \'01\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_3g,\\nROUND((CAST(SUM(case when \\"rattype\\" = \'06\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g_lte,\\nROUND((CAST(SUM(case when \\"rattype\\" = \'08\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g_iot,\\nROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g,\\nROUND((CAST(SUM(case when \\"rattype\\" = \'10\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_5g,\\n\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_escoamento_2g,\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_escoamento_3g,\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_escoamento_4g,\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_escoamento_5g,\\n\\nROUND((CAST(SUM(case when \\"rattype\\" IN (\'02\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_2g,\\nROUND((CAST(SUM(case when \\"rattype\\" IN (\'01\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_3g,\\nROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_4g,\\nROUND((CAST(SUM(case when \\"rattype\\" IN (\'10\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_5g,\\n\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_Downlink_4g,\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_Downlink_5g,\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" ELSE 0 END))*100,2) as porc_Uplink_4g,\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" ELSE 0 END))*100,2) as porc_Uplink_5g,\\nSUM(duration) as dur_total,\\n\\nSUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumedownlink\\" ELSE 0 END) as total_downlink_2g,\\nSUM(CASE WHEN rattype IN (\'01\') THEN  \\"datavolumedownlink\\" ELSE 0 END) as total_downlink_3g,\\nSUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as total_downlink_4g,\\nSUM(CASE WHEN rattype IN (\'10\') THEN  \\"datavolumedownlink\\" ELSE 0 END) as total_downlink_5g,\\nSUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\"  ELSE 0 END) as total_uplink_2g,\\nSUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\"  ELSE 0 END) as total_uplink_3g,\\nSUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as total_uplink_4g,\\nSUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" ELSE 0 END) as total_uplink_5g\\n\\nFROM \\"cem-enrichment\\"\\nWHERE \\"msisdn\\" = \'' +
            msisdn + '\' AND (TIMESTAMP \'' + date_from_formated +
            ' 00:00:00\' <= \\"__time\\" AND \\"__time\\" < TIMESTAMP \'' +
            date_to_formated+' 23:59:59\') AND \\"apn\\" not like \'ims%\'\\nGROUP BY 1\\n","context":{}}',
        }

    def subscriber_responses_identifier(self, msisdn, date_from, date_to) -> list[dict[str, str]]:
        queries_that_populate_tables = {
            "getFilterSigRegional": [],
            "getUserGrouped": ["User and Device Information"],
            "getUserSessionsDetails": ["Detailed User Sessions during Selected Time Period - KBs"],
            "getIndicatorData": [
                "Indicator Percentage by Technology",
                "Summary of Failure Quantities by UC"
            ],
            "getFailResumeByUC": [
                "Summary of Failure Quantities by UC",
                "Indicator Percentage by Technology",
            ],
            "getLocationsInfo": [
                "Cells Used by The User during Selected Time Period - KBs",
                "Map of Cells Used by The User",
            ],
            "getCellsUsedbyUser": [
                "Cells Used by The User during Selected Time Period - KBs",
                "Map of Cells Used by The User",
            ],
            "getSessionsGroupedTime": [
                "Distribution of Sessions by Technology by hour - KBs",
                "Downlink Data Volume by Technology (Evolution) - KBs",
                "Uplink Data Volume by Technology (Evolution) - KBs",
                "(%) Data Flow - Data Volume Proportion by Technology (Evolution)",
                "(%) Retention by Technology (Evolution)",
            ],
            "getTotalTrafficByTechLine": [
                "Distribution of Sessions by Technology by hour - KBs",
                "Downlink Data Volume by Technology (Evolution) - KBs",
                "Uplink Data Volume by Technology (Evolution) - KBs",
                "(%) Data Flow - Data Volume Proportion by Technology (Evolution)",
                "(%) Retention by Technology (Evolution)",
            ],
        }

        #! Get queries to check if response is ok
        queries_response = self.get_queries_script_and_status_response()
        self.set_responses_with_updated_data(msisdn, date_from, date_to)

        responses_status = {}

        if queries_response["no_error_requests"]:
            queries = queries_response["no_error_requests"]

            for query in queries:
                for key, model in self.responses_model.items():
                    if query["query_script"] == model:
                        # responses_status[key] == "OK" if query["status"] >= 200 or query["status"] <= 299 else "NOK"
                        responses_status[key] = True

        if queries_response["error_requests"]:
            queries = queries_response["error_requests"]

            for query in queries:
                for key, model in self.responses_model.items():
                    if query["query_script"] == model:
                        # responses_status[key] == "OK" if query["status"] >= 200 or query["status"] <= 299 else "NOK"
                        responses_status[key] = False

        if queries_response["pending_requests"]:
            queries = queries_response["pending_requests"]

            for query in queries:
                for key, model in self.responses_model.items():
                    if query["query_script"] == model:
                        # responses_status[key] == "OK" if query["status"] >= 200 or query["status"] <= 299 else "NOK"
                        responses_status[key] = False

        return responses_status

    def subscribers_tables_and_charts_status(self, msisdn, date_from, date_to):
        tables_and_your_queries = {
            "User and Device Information": ["getFilterSigRegional"],
            "Detailed User Sessions during Selected Time Period - KBs": [
                "getUserSessionsDetails"
            ],
            "Indicator Percentage by Technology": ["getIndicatorData", "getFailResumeByUC"],
            "Summary of Failure Quantities by UC": ["getIndicatorData", "getFailResumeByUC"],
            "Cells Used by The User during Selected Time Period - KBs": [
                "getLocationsInfo",
                "getCellsUsedbyUser"
            ],
            "Map of Cells Used by The User": ["getLocationsInfo", "getCellsUsedbyUser"],
            "Distribution of Sessions by Technology by hour - KBs": [
                "getSessionsGroupedTime",
                "getTotalTrafficByTechLine",
            ],
            "Downlink Data Volume by Technology (Evolution) - KBs": [
                "getSessionsGroupedTime",
                "getTotalTrafficByTechLine",
            ],
            "Uplink Data Volume by Technology (Evolution) - KBs": [
                "getSessionsGroupedTime",
                "getTotalTrafficByTechLine",
            ],
            "(%) Data Flow - Data Volume Proportion by Technology (Evolution)": [
                "getSessionsGroupedTime",
                "getTotalTrafficByTechLine",
            ],
            "(%) Retention by Technology (Evolution)": [
                "getSessionsGroupedTime",
                "getTotalTrafficByTechLine",
            ],
        }

        # Obtendo os nomes das funções com seus respectivos status
        request_status = self.subscriber_responses_identifier(
            msisdn, date_from, date_to)

        response = {}
        if request_status:
            # Iteration by tables and charts
            for topic, queries_names in tables_and_your_queries.items():

                boolean_status = True

                for query_name in queries_names:
                    boolean_status = boolean_status and request_status[query_name]

                # Checking if the query_name is in the topic, that is, if this
                # table needs that query to show
                response[topic] = boolean_status

        return response

    def insert_text_on_text_input_and_click_in_onption_selection(self, xpath, text):
        web_element = self.driver.find_element(
            By.XPATH, xpath)
        # Removing disabled attribute to add or change value on field without error
        self.driver.execute_script(
            "arguments[0].removeAttribute('disabled')", web_element)
        web_element.send_keys(text)
        time.sleep(0.5)
        try:
            OPTION_SELECTION = self.driver.find_element(
                By.XPATH, f"//span[contains(@class, 'mat-option-text') and contains(text(),'{text}')]")
            # *  //span[contains(@class, 'mat-option-text') and contains(text(),'SP')]
            OPTION_SELECTION.click()
        except NoSuchElementException:
            return

    def insert_text_on_text_input(self, xpath, text):
        web_element = self.driver.find_element(
            By.XPATH, xpath)
        web_element.send_keys(text)

    def insert_date_on_date_field(
        self, xpath_date_from, xpath_date_to, date_from, date_to
    ):
        FROM_DATE_FIELD = self.driver.find_element(
            By.XPATH, xpath_date_from)
        self.driver.execute_script(
            "arguments[0].removeAttribute('disabled')", FROM_DATE_FIELD)
        # Date format mm/dd/yyyy
        FROM_DATE_FIELD.send_keys(date_from)
        # Removing disabled attribute to add or change value on date inputs
        TO_DATE_FIELD = self.driver.find_element(
            By.XPATH, xpath_date_to)
        # Removing disabled attribute to add or change value on date inputs
        self.driver.execute_script(
            "arguments[0].removeAttribute('disabled')", TO_DATE_FIELD)
        # Date format mm/dd/yyyy
        TO_DATE_FIELD.send_keys(date_to)

    def click_on_button(self, xpath):
        web_element = self.driver.find_element(
            By.XPATH, xpath)
        web_element.click()
