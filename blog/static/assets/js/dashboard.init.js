var options = {
    series: [{ name: "series1", data: [1, , 2, 10, 20, , 30, 40, 45, 50, 55, 60, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 90, 140, 70, 145, 157, 150] }],
    chart: { height: 320, type: "line", toolbar: "false", dropShadow: { enabled: !0, color: "#000", top: 18, left: 7, blur: 8, opacity: 0.2 } },
    dataLabels: { enabled: !1 },
    colors: ["#556ee6"],
    stroke: { curve: "smooth", width: 3 },
    xaxis: {
        type: 'numeric',
        min: 1,
        max: 30,

    }
},
    chart = new ApexCharts(document.querySelector("#line-chart"), options);
chart.render();
options = { series: [56, 38, 26], chart: { type: "donut", height: 262 }, labels: ["Series A", "Series B", "Series C"], colors: ["#556ee6", "#34c38f", "#f46a6a"], legend: { show: !1 }, plotOptions: { pie: { donut: { size: "70%" } } } };
(chart = new ApexCharts(document.querySelector("#donut-chart"), options)).render();
var radialoptions1 = {
    series: [37],
    chart: { type: "radialBar", width: 60, height: 60, sparkline: { enabled: !0 } },
    dataLabels: { enabled: !1 },
    colors: ["#556ee6"],
    plotOptions: { radialBar: { hollow: { margin: 0, size: "60%" }, track: { margin: 0 }, dataLabels: { show: !1 } } },
},
    radialchart1 = new ApexCharts(document.querySelector("#radialchart-1"), radialoptions1);
radialchart1.render();
var radialoptions2 = {
    series: [72],
    chart: { type: "radialBar", width: 60, height: 60, sparkline: { enabled: !0 } },
    dataLabels: { enabled: !1 },
    colors: ["#34c38f"],
    plotOptions: { radialBar: { hollow: { margin: 0, size: "60%" }, track: { margin: 0 }, dataLabels: { show: !1 } } },
},
    radialchart2 = new ApexCharts(document.querySelector("#radialchart-2"), radialoptions2);
radialchart2.render();
var radialoptions3 = {
    series: [54],
    chart: { type: "radialBar", width: 60, height: 60, sparkline: { enabled: !0 } },
    dataLabels: { enabled: !1 },
    colors: ["#f46a6a"],
    plotOptions: { radialBar: { hollow: { margin: 0, size: "60%" }, track: { margin: 0 }, dataLabels: { show: !1 } } },
},
    radialchart3 = new ApexCharts(document.querySelector("#radialchart-3"), radialoptions3);
radialchart3.render();
