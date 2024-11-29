VSMBB Automation
Process queue

Page - Subscribers


[x] - Measure total automation runtime
[x] - Measure total execution time for opening the driver
[ ] - Measure chrome driver opening time
[ ] - Inject Javascript script to monitor requests pending responses
[ ] - Start counter
[ ] - Request the opening of the Subscribers page
[ ] - Measure total page loading time (Measuring by completion of requests)
[ ] - Insert filters and measure loading data time in filters fields
[ ] - Analyze API requests, which ones have status 200 and which ones gave an error
[ ] - Get a report on filter loading times:
        - If there is any error;
        - Request response time
[ ] - Analyze and associate requests with each filter field to know which field each request is from and find out which query searches for data from each field and populates it
[ ] - 

#Mapped tables and charts

TABELAS:

User and Device Information ----------------------------   getUserGrouped

Summary of Failure Quantities by UC --------------------   getIndicatorData
                                                           getFailResumeByUC

Cells Used by The User during Selected Time Period - KBs - getLocationsInfo 
                                                           getCellsUsedbyUser

Distribution of Sessions by Technology by hour - KBs ----------- getSessionsGroupedTime getTotalTrafficByTechLine

Detailed User Sessions during Selected Time Period - KBs ------- getUserSessionsDetails

Resume Sessions by Technology and Cause for Reclosing ---------- 

Gráficos:

Indicator Percentage by Technology ----------------------------- getIndicatorData
                                                                 getFailResumeByUC
Downlink Data Volume by Technology (Evolution) - KBs ----------- getSessionsGroupedTime 
                                                                 getTotalTrafficByTechLine
Uplink Data Volume by Technology (Evolution) - KBs ------------- getSessionsGroupedTime getTotalTrafficByTechLine
(%) Data Flow - Data Volume Proportion by Technology (Evolution) getSessionsGroupedTime 
                                                                 getTotalTrafficByTechLine
(%) Retention by Technology (Evolution) ------------------------ getSessionsGroupedTime 
                                                                 getTotalTrafficByTechLine

Mapas:

Map of Cells Used by The User ---------------------------------- getLocationsInfo 
                                                                 getCellsUsedbyUser

# Mapped queries

ASSINANTES:

--------------------------------------------------------
***************** QUERY SEM FUNÇÃO *********************
--------------------------------------------------------

getFilterSigRegional = '{"query":"\\nSELECT\\n  \\"sig_regional\\"\\nFROM \\"celulas\\"\\nWHERE \\"__time\\" BETWEEN TIMESTAMP \'2024-11-16 00:00:00\' AND TIMESTAMP \'2001-11-17 23:59:59\'\\nGROUP BY \\"sig_regional\\"\\n","context":{}}'

--------------------------------------------------------
******************** IDENTIFICAR ***********************
--------------------------------------------------------

TABELAS:
User and Device Information

getUserGrouped = '{"query":"\\nSELECT\\n  \\"__time\\" as \\"__time\\",\\n  \\"msisdn\\",\\n  \\"imsi\\",\\n  \\"desc_fabricante\\",\\n  \\"modelo\\",\\n  \\"tac_tecnologia\\",\\n  \\"desc_modelo\\"\\nFROM \\"cem-enrichment\\"\\nWHERE \\"msisdn\\" = \'5511942837639\' AND \\"__time\\" BETWEEN \'2024-11-16 00:00:00\' AND \'2024-11-17 23:59:59\' AND \\"apn\\" NOT LIKE \'ims%\'\\nORDER BY \\"__time\\" DESC LIMIT 1\\n","context":{}}'

--------------------------------------------------------
******************** IDENTIFICAR ***********************
--------------------------------------------------------

TABELAS:

Detailed User Sessions during Selected Time Period - KBs

getUserSessionsDetails = '{"query":"\\nSELECT\\n  \\"__time\\" as time_second,\\n  \\"tecnologia\\" AS tecnologia,\\n  \\"cellname\\",\\n  \\"municipio\\",\\n  \\"uf\\",\\n  \\"sig_regional\\",\\n  \\"causeforrecclosing\\",\\n  \\"banda\\",\\n  \\"setor\\",\\n  \\"datavolumeuplink\\" as totalUplinkg,\\n  \\"datavolumedownlink\\" as totalDownlinkg,\\n  \\"duration\\" as dur_total,\\n  \\"diagnostics\\"\\nFROM \\"cem-enrichment\\"\\nWHERE \\"msisdn\\" = \'5511942837639\'\\n  AND \\"__time\\" BETWEEN \'2024-11-16 00:00:00\' AND \'2024-11-17 23:59:59\'\\n  AND \\"apn\\" not like \'ims%\'\\nORDER BY \\"__time\\" ASC\\nlimit 10000\\n","context":{}}'

--------------------------------------------------------
******************** IDENTIFICAR ***********************
--------------------------------------------------------

GRÁFICOS:

Indicator Percentage by Technology

TABELAS:

Summary of Failure Quantities by UC

getIndicatorData = '{"query":"\\n    SELECT\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" ELSE 0 END))*100,2) as porc_Uplink_2g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" ELSE 0 END))*100,2) as porc_Uplink_3g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" ELSE 0 END))*100,2) as porc_Uplink_4g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" ELSE 0 END))*100,2) as porc_Uplink_5g,\\n\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_Downlink_2g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_Downlink_3g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_Downlink_4g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_Downlink_5g,\\n\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_total_2g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_total_3g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_total_4g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_total_5g,\\n\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'02\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_2g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'01\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_3g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_4g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'10\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_5g\\nFROM \\"cem-enrichment\\"\\nWHERE msisdn = \'5511942837639\'\\n AND \\"__time\\" BETWEEN \'2024-11-16 00:00:00\' AND \'2024-11-17 23:59:59\'\\n AND \\"apn\\" not like \'ims%\'\\n  ","context":{}}'

--------------------------------------------------------
******************** IDENTIFICAR ***********************
--------------------------------------------------------

TABELAS:

getTotalTrafficByTechLine = '{"query":"\\nSELECT\\nTIME_FLOOR(__time, \'PT1H\') as floor_1_hour,\\nSUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total2g,\\nSUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total3g,\\nSUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total4g,\\nSUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total5g,\\n\\nSUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumedownlink\\" ELSE 0 END) as downloadTotalLinkByTech_2g,\\nSUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumedownlink\\" ELSE 0 END) as getDownloadLinkByTech_3g,\\nSUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as downloadTotalLinkByTech_4g,\\nSUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumedownlink\\" ELSE 0 END) as getDownloadLinkByTech_5g,\\n\\nSUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\" ELSE 0 END) as upLinkTotalLinkByTech_2g,\\nSUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\" ELSE 0 END) as getUpLinkByTech_3g,\\nSUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as upLinkTotalLinkByTech_4g,\\nSUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" ELSE 0 END) as getUpLinkByTech_5g,\\n\\nSUM(case when \\"rattype\\" = \'02\' then 1 else 0 end) as ses_2g,\\nSUM(case when \\"rattype\\" = \'01\' then 1 else 0 end) as ses_3g,\\nSUM(case when \\"rattype\\" = \'06\' then 1 else 0 end) as ses_4g_lte,\\nSUM(case when \\"rattype\\" = \'08\' then 1 else 0 end) as ses_4g_iot,\\nSUM(case when \\"rattype\\" IN (\'06\',\'08\') then 1 else 0 end) as ses4gTotal,\\nSUM(case when \\"rattype\\" = \'10\' then 1 else 0 end) as ses5gTotal,\\nSUM(CASE WHEN \\"rattype\\" in (\'01\', \'02\', \'06\', \'10\') THEN 1 ELSE 0 END) AS ses_total,\\nROUND((CAST(SUM(case when \\"rattype\\" = \'02\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_2g,\\nROUND((CAST(SUM(case when \\"rattype\\" = \'01\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_3g,\\nROUND((CAST(SUM(case when \\"rattype\\" = \'06\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g_lte,\\nROUND((CAST(SUM(case when \\"rattype\\" = \'08\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g_iot,\\nROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g,\\nROUND((CAST(SUM(case when \\"rattype\\" = \'10\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_5g,\\n\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_escoamento_2g,\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_escoamento_3g,\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_escoamento_4g,\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_escoamento_5g,\\n\\nROUND((CAST(SUM(case when \\"rattype\\" IN (\'02\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_2g,\\nROUND((CAST(SUM(case when \\"rattype\\" IN (\'01\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_3g,\\nROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_4g,\\nROUND((CAST(SUM(case when \\"rattype\\" IN (\'10\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_retencao_5g,\\n\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_Downlink_4g,\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumedownlink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumedownlink\\" ELSE 0 END))*100,2) as porc_Downlink_5g,\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" ELSE 0 END))*100,2) as porc_Uplink_4g,\\nROUND((CAST(SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" ELSE 0 END) as float)/SUM(CASE WHEN rattype IN (\'01\', \'02\', \'06\', \'08\', \'10\') THEN \\"datavolumeuplink\\" ELSE 0 END))*100,2) as porc_Uplink_5g,\\nSUM(duration) as dur_total,\\n\\nSUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumedownlink\\" ELSE 0 END) as total_downlink_2g,\\nSUM(CASE WHEN rattype IN (\'01\') THEN  \\"datavolumedownlink\\" ELSE 0 END) as total_downlink_3g,\\nSUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as total_downlink_4g,\\nSUM(CASE WHEN rattype IN (\'10\') THEN  \\"datavolumedownlink\\" ELSE 0 END) as total_downlink_5g,\\nSUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\"  ELSE 0 END) as total_uplink_2g,\\nSUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\"  ELSE 0 END) as total_uplink_3g,\\nSUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as total_uplink_4g,\\nSUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" ELSE 0 END) as total_uplink_5g\\n\\nFROM \\"cem-enrichment\\"\\nWHERE \\"msisdn\\" = \'5511942837639\' AND (TIMESTAMP \'2024-11-16 00:00:00\' <= \\"__time\\" AND \\"__time\\" < TIMESTAMP \'2024-11-17 23:59:59\') AND \\"apn\\" not like \'ims%\'\\nGROUP BY 1\\n","context":{}}'

--------------------------------------------------------
******************** IDENTIFICAR ***********************
--------------------------------------------------------

TABELAS:

getFailResumeByUC = '{"query":"\\n       SELECT\\nsum(totalUplinkg+totalDownlinkg) as Total_Traffic,\\nROUND((CAST(sum(total4g) as float)/sum(totalUplinkg+totalDownlinkg))*100,2) as Escoamento_4G,\\nROUND((CAST(sum(dur_4g) as float)/sum(dur_total))*100,2) as Reten_4G,\\nROUND((CAST(sum(total2g) as float)/sum(totalUplinkg+totalDownlinkg))*100,2) as Escoamento_2G,\\nROUND((CAST(sum(dur_2g) as float)/sum(dur_total))*100,2) as Reten_2G,\\n \\nROUND((CAST(sum(total3g) as float)/sum(totalUplinkg+totalDownlinkg))*100,2) as Escoamento_3G,\\nROUND((CAST(sum(dur_3g) as float)/sum(dur_total))*100,2) as Reten_3G,\\n \\nROUND((CAST(sum(total4g) as float)/sum(totalUplinkg+totalDownlinkg))*100,2) as Escoamento_4G,\\nROUND((CAST(sum(dur_4g) as float)/sum(dur_total))*100,2) as Reten_4G,\\n \\nROUND((CAST(sum(total5g) as float)/sum(totalUplinkg+totalDownlinkg))*100,2) as Escoamento_5G,\\nROUND((CAST(sum(dur_5g) as float)/sum(dur_total))*100,2) as Reten_5G,\\nCOUNT(1) as Total_Hours,\\nCOUNT(CASE when porc_ses_4g < 95 and perc_cnn < 70 and ses_total > 10 then 1 else null end) as UCpingPong,\\nCOUNT(CASE when porc_ses_4g < 95 and perc_cnn > 70 then 1 else null end) as UCGapService,\\nCOUNT(CASE when porc_ses_4g > 95 and perc_cnn > 70 and ses_total > 10 then 1 else null end) as UCDropSession,\\nCOUNT(CASE when porc_ses_4g > 95 and perc_cnn > 70 and ses_total < 10 then 1 else null end) as UCConectaNoNavega,\\nROUND((CAST(COUNT(CASE when porc_ses_4g < 95 and perc_cnn < 70 and ses_total > 10 then 1 else null end) as float)/COUNT(1))*100,2) as Porc_UCpingPong,\\nROUND((CAST(COUNT(CASE when porc_ses_4g < 95 and perc_cnn > 70 then 1 else null end) as float)/COUNT(1))*100,2) as Porc_UCGapService,\\nROUND((CAST(COUNT(CASE when porc_ses_4g > 95 and perc_cnn > 70 and ses_total > 10 then 1 else null end) as float)/COUNT(1))*100,2) as Porc_UCDropSession,\\nROUND((CAST(COUNT(CASE when porc_ses_4g > 95 and perc_cnn > 70 and ses_total < 10 then 1 else null end) as float)/COUNT(1))*100,2) as Porc_UCConectaNoNavega,\\nsum(ses_total) as Total_Sessions,\\nSUM(cnn) as CnN_Sessions,\\nROUND((CAST(SUM(cnn)as float)/sum(ses_total))*100,2) as Porc_CnN_Sessions,\\nsum(abnormal_R) as abnormal_Releases,\\nROUND((CAST(sum(abnormal_R) as float)/sum(ses_total))*100,2) as Porc_abnR_Sessions\\nFROM (\\nSELECT\\n TIME_FLOOR(\\"__time\\", \'PT1H\') AS \\"__time\\",\\n sum(CASE\\n   WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\')  AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\'\\n THEN 1 ELSE 0 END) as cnn,\\n ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\')  AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\' THEN 1 ELSE 0 END) as float)/COUNT(1))*100,2) as perc_cnn,\\n SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total4g,\\n SUM(CASE WHEN rattype IN (\'02\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total2g,\\n  SUM(CASE WHEN rattype IN (\'01\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total3g,\\n    SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total5g,\\n\\n\\n SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplinkg,\\n SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlinkg,\\n SUM(CASE WHEN \\"rattype\\" in (\'01\', \'02\', \'06\', \'10\') THEN 1 ELSE 0 END) AS ses_total,\\n ROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g,\\n SUM(case when \\"rattype\\" IN (\'06\', \'08\') then \\"duration\\" else 0 end) as dur_4g,\\n  SUM(case when \\"rattype\\" IN (\'10\') then \\"duration\\" else 0 end) as dur_5g,\\n\\n  SUM(case when \\"rattype\\" IN (\'02\') then \\"duration\\" else 0 end) as dur_2g,\\n    SUM(case when \\"rattype\\" IN (\'01\') then \\"duration\\" else 0 end) as dur_3g,\\n\\n SUM(duration) as dur_total,\\n COUNT(CASE when \\"causeforrecclosing\\" = \'04 - abnormalRelease\' then 1 else null end) as abnormal_R\\nFROM \\"cem-enrichment\\"\\nWHERE msisdn = \'5511942837639\'\\n AND \\"__time\\" BETWEEN \'2024-11-16 00:00:00\' AND \'2024-11-17 23:59:59\'\\n AND \\"apn\\" not like \'ims%\'\\n GROUP BY 1)\\n  ","context":{}}'

--------------------------------------------------------
***************** QUERY SEM FUNÇÃO *********************
--------------------------------------------------------

getInfoUserVip = '{"query":"SELECT * FROM \\"assinantes_vips\\" WHERE \\"msisdn\\" = \'5511942837639\' ","context":{}}'

--------------------------------------------------------
******************** IDENTIFICAR ***********************
--------------------------------------------------------

TABELAS:

Cells Used by The User during Selected Time Period - KBs

GRÁFICOS:


getCellsUsedbyUser = '{"query":"\\nSELECT\\n msisdn,\\n rattype,\\n cellname,\\n municipio,\\n banda,\\n setor,\\n  sum(CASE\\n   WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\')  AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\'\\n THEN 1 ELSE 0 END) as cnn,\\n ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\' THEN 1 ELSE 0 END) as float)/COUNT(1))*100,2) as perc_cnn,\\n\\n SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total4g,\\n SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplink,\\n SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlink,\\n sum(\\"datavolumeuplink\\" + \\"datavolumedownlink\\") as \\"totalDataVolume\\",\\n\\n SUM(CASE WHEN \\"rattype\\" in (\'01\', \'02\', \'06\', \'10\') THEN 1 ELSE 0 END) AS ses_total,\\n\\n SUM(duration) as dur_total\\nFROM \\"cem-enrichment\\"\\nWHERE \\"msisdn\\" = \'5511942837639\' AND (TIMESTAMP \'2024-11-16 00:00:00\' <= \\"__time\\" AND \\"__time\\" < TIMESTAMP \'2024-11-17 23:59:59\') AND \\"apn\\" not like \'ims%\'\\nGROUP BY 1,2,3,4,5,6\\norder by totalDataVolume desc\\n","context":{}}'

--------------------------------------------------------
******************** IDENTIFICAR ***********************
--------------------------------------------------------

GRÁFICOS

TABELAS:

Distribution of Sessions by Technology by hour - KBs

getSessionsGroupedTime = '{"query":"\\nSELECT\\n TIME_FLOOR(\\"__time\\", \'PT1H\') AS \\"__time\\",\\n sum(CASE\\n   WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\')  AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\'\\n THEN 1 ELSE 0 END) as cnn,\\n ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\' THEN 1 ELSE 0 END) as float)/COUNT(1))*100,2) as perc_cnn,\\n SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total4g,\\n SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total5g,\\n SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlink4g,\\n SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlink5g,\\n SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplink4g,\\n SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplink5g,\\n SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplinkg,\\n SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlinkg,\\n SUM(case when \\"rattype\\" = \'02\' then 1 else 0 end) as ses_2g,\\n SUM(case when \\"rattype\\" = \'01\' then 1 else 0 end) as ses_3g,\\n SUM(case when \\"rattype\\" = \'06\' then 1 else 0 end) as ses_4g_lte,\\n SUM(case when \\"rattype\\" = \'08\' then 1 else 0 end) as ses_4g_iot,\\n SUM(case when \\"rattype\\" IN (\'06\',\'08\') then 1 else 0 end) as ses4gTotal,\\n SUM(case when \\"rattype\\" = \'10\' then 1 else 0 end) as ses5gTotal,\\n SUM(CASE WHEN \\"rattype\\" in (\'01\', \'02\', \'06\', \'10\') THEN 1 ELSE 0 END) AS ses_total,\\n ROUND((CAST(SUM(case when \\"rattype\\" = \'02\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_2g,\\n ROUND((CAST(SUM(case when \\"rattype\\" = \'01\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_3g,\\n ROUND((CAST(SUM(case when \\"rattype\\" = \'06\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g_lte,\\n ROUND((CAST(SUM(case when \\"rattype\\" = \'08\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g_iot,\\n ROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g,\\n ROUND((CAST(SUM(case when \\"rattype\\" = \'10\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_5g,\\n SUM(case when \\"rattype\\" = \'02\' then \\"duration\\" else 0 end) as dur_2g,\\n SUM(case when \\"rattype\\" = \'01\' then \\"duration\\" else 0 end) as dur_3g,\\n SUM(case when \\"rattype\\" = \'06\' then \\"duration\\" else 0 end) as dur_4g_lte,\\n SUM(case when \\"rattype\\" = \'08\' then \\"duration\\" else 0 end) as dur_4g_iot,\\n SUM(case when \\"rattype\\" IN (\'06\', \'08\') then \\"duration\\" else 0 end) as dur_4g,\\n SUM(case when \\"rattype\\" = \'10\' then \\"duration\\" else 0 end) as dur_5g,\\n ROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_duration_4g,\\n ROUND((CAST(SUM(case when \\"rattype\\" IN (\'10\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_duration_5g,\\n SUM(duration) as dur_total\\nFROM \\"cem-enrichment\\"\\nWHERE msisdn = \'5511942837639\'\\n AND \\"__time\\" BETWEEN \'2024-11-16 00:00:00\' AND \'2024-11-17 23:59:59\'\\n AND \\"apn\\" not like \'ims%\'\\nGROUP BY 1\\nORDER BY 1\\n","context":{}}'

--------------------------------------------------------
******************** IDENTIFICAR ***********************
--------------------------------------------------------

TABELAS:
Cells Used by The User during Selected Time Period - KBs

MAPA:
Map of Cells Used by The User

getLocationsInfo = '{"query":"\\nSELECT\\n   \\n   \\"cellname\\",\\n    \\"rattype\\",\\n   \\"num_lat_dec\\",\\n   \\"num_lon_dec\\",\\n   \\"sigla_site\\",\\n   SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total4g,\\n   SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as total5g,\\n   ROUND((CAST(SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\')  AND \\"datavolumeuplink\\" = 0 AND \\"datavolumedownlink\\" = 0 AND \\"duration\\" > 30 AND \\"duration\\" < 600 AND \\"causeforrecclosing\\" != \'17 - timeLimit\'  THEN 1 ELSE 0 END) as float)/COUNT(1))*100,2) as perc_cnn,\\n\\n   SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlink4g,\\n   SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlink5g,\\n\\n   SUM(CASE WHEN rattype IN (\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplink4g,\\n   SUM(CASE WHEN rattype IN (\'10\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplink5g,\\n   SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumeuplink\\" ELSE 0 END) as totalUplink,\\n   SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumedownlink\\" ELSE 0 END) as totalDownlink,\\n\\n   SUM(CASE WHEN rattype IN (\'01\',\'02\',\'10\',\'06\',\'08\') THEN \\"datavolumeuplink\\" + \\"datavolumedownlink\\" ELSE 0 END) as totalDataVolume,\\n\\n   SUM(case when \\"rattype\\" = \'02\' then 1 else 0 end) as ses_2g,\\n   SUM(case when \\"rattype\\" = \'01\' then 1 else 0 end) as ses_3g,\\n   SUM(case when \\"rattype\\" = \'06\' then 1 else 0 end) as ses_4g_lte,\\n   SUM(case when \\"rattype\\" = \'08\' then 1 else 0 end) as ses_4g_iot,\\n   SUM(case when \\"rattype\\" IN (\'06\',\'08\') then 1 else 0 end) as ses4gTotal,\\n   SUM(case when \\"rattype\\" = \'10\' then 1 else 0 end) as ses5gTotal,\\n   SUM(CASE WHEN \\"rattype\\" in (\'01\', \'02\', \'06\', \'10\') THEN 1 ELSE 0 END) AS ses_total,\\n   ROUND((CAST(SUM(case when \\"rattype\\" = \'02\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_2g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" = \'01\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_3g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" = \'06\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g_lte,\\n   ROUND((CAST(SUM(case when \\"rattype\\" = \'08\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g_iot,\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_4g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" = \'10\' then 1 else 0 end) as float)/SUM(1))*100,2) as porc_ses_5g,\\n   SUM(case when \\"rattype\\" = \'02\' then \\"duration\\" else 0 end) as dur_2g,\\n   SUM(case when \\"rattype\\" = \'01\' then \\"duration\\" else 0 end) as dur_3g,\\n   SUM(case when \\"rattype\\" = \'06\' then \\"duration\\" else 0 end) as dur_4g_lte,\\n   SUM(case when \\"rattype\\" = \'08\' then \\"duration\\" else 0 end) as dur_4g_iot,\\n   SUM(case when \\"rattype\\" IN (\'06\', \'08\') then \\"duration\\" else 0 end) as dur_4g,\\n   SUM(case when \\"rattype\\" = \'10\' then \\"duration\\" else 0 end) as dur_5g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'06\', \'08\') then duration else 0 end) as float)/SUM(duration))*100,2) as porc_duration_4g,\\n   ROUND((CAST(SUM(case when \\"rattype\\" IN (\'10\') then 1 else 0 end) as float)/SUM(duration))*100,2) as porc_duration_5g,\\n   SUM(duration) as dur_total\\nFROM \\"cem-enrichment\\"\\nWHERE \\"__time\\" BETWEEN \'2024-11-16 00:00:00\' AND \'2024-11-17 23:59:59\'\\n AND  msisdn = \'5511942837639\'\\n AND \\"apn\\" not like \'ims%\'\\nGROUP BY 1,2,3,4,5\\nORDER BY \\"cellname\\" DESC\\n","context":{}}'

--------------------------------------------------------
******************** IDENTIFICAR ***********************
--------------------------------------------------------

######### OBTER A QUERY EM STRING PELO VS CODE #########

getResumeByTecnologyCauseforrecclosing = `\nSELECT\n"tecnologia",\n"causeforrecclosing" as Cause_of_Closing,\n sum(CASE\n   WHEN rattype IN ('01','02','10','06','08')  AND "datavolumeuplink" = 0 AND "datavolumedownlink" = 0 AND "duration" > 30\n THEN 1 ELSE 0 END) as ConnectionnoNavigation,\n ROUND((CAST(SUM(CASE WHEN rattype IN ('01','02','10','06','08') AND "datavolumeuplink" = 0 AND "datavolumedownlink" = 0 AND "duration" > 30 THEN 1 ELSE 0 END) as float)/COUNT(1))*100,2) as Perc_ConnectionnoNavigation,\n SUM(CASE WHEN rattype IN ('01','02','10','06','08') THEN "datavolumeuplink" ELSE 0 END) as Uplink_Traffic,\n SUM(CASE WHEN rattype IN ('01','02','10','06','08') THEN "datavolumedownlink" ELSE 0 END) as Downlink_Traffic,\n SUM(CASE WHEN rattype IN ('01','02','10','06','08') THEN "datavolumedownlink"+"datavolumeuplink" ELSE 0 END) as Total_Traffic,\n SUM(CASE WHEN "rattype" in ('01', '02', '06', '10') THEN 1 ELSE 0 END) AS Total_Sessions,\n SUM(duration) as Total_Duration\nFROM "cem-enrichment"\nWHERE msisdn = '5511942837639'\n AND "__time" BETWEEN '2024-11-19T16:00:00' AND '2024-11-19T16:59:59.000'\n AND "apn" not like 'ims%'\n GROUP BY 1,2\n order by 1 desc\n`




getUserGrouped
getTotalTrafficByTech 
getTotalTrafficByTechLine
getSessionsInformationsByUser
getSessionsInformationsByUserPercDuration
getSessionsInformationsByUser4G
getSessionsInformationsByUser5G
getCellsUsedbyUser
getSessionsGroupedTime2
getSessionsGroupedTime
getUserSessionsDetails
getLocationsInfoOneCell
getParamCellNameInterRATHandoverUseCases
getParamCellName
getParamTecnologia
getParamBandaTabelaCem
getParamBanda
getFilterSigRegionalTabelaCem
getFilterSigRegional
getFilterUF2
getFilterUF
getFilterCountryTabelaCem
getFilterCountry
getFilterNomeTabelaCem
getFilterNome
getFilterTecTabelaCem
getFilterTec
getFilterBandTabelaCem
getFilterBand
getTopCellsByusersCnnTabelaCem
getTopCellsByusersCnn2
getTopCellsByusersCnn
getTopCellsByusersCnn1Dia
getTopCellsByusersCnnOneCell
getTopCellsByusersCnnOneCellNaoValidado
getTopCellsByusersCnnGroupByTabelaCem
getTopCellsByusersCnnGroupBy
getTopCellsByusersCnnGrafic
getTopCellWithSubscribersInterTabelaCelulas
getTopCellWithSubscribersInter
getTopCellWithSubscribersInterUmDia
getTopCellWithSubscribersInterOneCell
getTopCellWithSubscribersInterTabelaCem
getTopCellWithSubscribersInterGroupByTabelaCem
getTopCellWithSubscribersInterGroupBy = "";
getTopCellWithSubscribersInterGrafic
getTopCellDataVolumeTabelaCem
getDataVolumeGroupByTabelaCem
getTopCellDataVolumeTabelaCelulas
getTopCellDataVolume
getTopCellDataVolume1Dia
getTopCellDataVolumeOneCell
getDataVolumeGroupBy
getTopCellDataVolumeGrafic
getCellMapDashTabelaCem
getCellMapDash2Celulas
getCellMapDash2
getCellMapDash
getCellMapDashOneCellTabelaCem
getCellMapDashOneCell
getCellMapGroupByTabelaCem
getCellMapGroupBy
getAverageDataVolumeUf
getAverageDataVolumeCity
getAverageDataVolumeTec
getAverageDataVolumeBand
getCellRetetion
getCellRetetionGroupBy
getCellDataFlowTabelaCelulas
getCellDataFlow
getCellDataFlowOneCell
getCellDataFlowGroupByTabelaCem
getCellDataFlowGroupBy
getCellDataFlowGrafic
getFailResumeByUC
getIndicatorData
getVipsMainKpisAgg
getVipsMainKpis
getVipsMainKpisByCell
getVipsMainKpisCount
getVipsCellsUsedByUser2g3g4g5g
getAffectedCells
getExecutiveVisionResumeTabelaCem
getExecutiveVisionResume2
getExecutiveVisionResume
getExecutiveVisionAffectedCells
getExecutiveVisionAffectedCells2
getExecutiveVisionAffectedCellsMap
getExecutiveVisionAffectedCellsMapShared
getExecutiveVisionAffectedCellsMapShared11
apiUrl = "https://cem-connection-service-telco-webapplications-prod.apps.ocp-01.tdigital-vivo.com.br/consulta-api";