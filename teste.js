// ! Essa forma coleta apenas as requisições que já foram concluídas

const allRequestsCompleted = () => {
	const permorfance =
		window.performance ||
		window.mozPerformance ||
		window.msPerformance ||
		window.webkitPerformance ||
		{};

	const entries = permorfance.getEntriesByType("resource");
	return entries.filter((entry) => {
		return (
			(entry.initiatorType === "xmlhttprequest" && entry.duration) ||
			(entry.initiatorType === "fetch" && entry.duration)
		);
	}).length;
};

window.performance.getEntries("resource")[78];
window.performance
	.getEntries("resource")
	.map((request, i) => console.log(request.name, i, request.duration));

// Script para analisar as requests do VSMBB concluídas

window.performance.getEntries("resource").map((entry, i) => {
	if (
		entry.name ===
		"https://cem-connection-service-telco-webapplications-prod.apps.ocp-01.tdigital-vivo.com.br/consulta-api"
	) {
		console.log(i, entry.duration);
	}
});
