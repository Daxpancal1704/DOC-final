
const doc = {{ doc_count|default:0 }};
const img = {{ img_count|default:0 }};
const text = {{ text_count|default:0 }};

const ai = {{ ai_count|default:0 }};
const human = {{ human_count|default:0 }};
const mixed = {{ mixed_count|default:0 }};

console.log("AI:", ai, "Human:", human, "Mixed:", mixed);

// Activity Chart
new Chart(document.getElementById('activityChart'), {
    type: 'pie',
    data: {
        labels: ['Document', 'Image', 'Text'],
        datasets: [{
            data: [doc, img, text],
            backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56']
        }]
    }
});




// Result Chart
new Chart(document.getElementById('resultChart'), {
    type: 'doughnut',
    data: {
        labels: ['AI', 'Human', 'Mixed'],
        datasets: [{
            data: [ai, human, mixed],
            backgroundColor: ['#ff4d4d', '#4CAF50', '#FFC107']
        }]
    }
});




const dates = {{ dates|safe }};
const counts = {{ counts|safe }};

new Chart(document.getElementById('weeklyChart'), {
    type: 'bar',
    data: {
        labels: dates,
        datasets: [{
            label: 'Scans',
            data: counts,
            backgroundColor: '#36A2EB'
        }]
    }
});

options: {
    plugins: {
        legend: {
            labels: {
                color: "#000",   // make legend visible
                font: {
                    size: 12
                }
            }
        }
    }
}