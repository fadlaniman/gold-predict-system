// ==========================================
// CONFIGURATION & GLOBAL DEFAULTS
// ==========================================
Chart.defaults.color = '#A89878';

// Konfigurasi Grid & Ticks yang sering diulang
const sharedChartScales = {
    x: {
        ticks: {
            color: '#A89878',
            maxRotation: 45,
            minRotation: 45,
            callback: function(value) {
                return this.getLabelForValue(value);
            }
        },
        grid: { color: 'rgba(255,255,255,0.04)' }
    },
    y: {
        ticks: {
            color: '#A89878',
            callback: function(value) {
                return 'Rp ' + new Intl.NumberFormat('id-ID').format(value);
            }
        },
        grid: { color: 'rgba(255,255,255,0.04)' }
    }
};

// ==========================================
// DATA INTEGRATION FROM WINDOW.FLASKDATA
// ==========================================
const dataBridge = window.flaskData || {};

const activeData = dataBridge.activeData || [];
const historicalChartData = dataBridge.historicalChartData || [];
const predictResult = dataBridge.predicted || [];
const historicalPrediction = dataBridge.historicalPrediction || { actual: [], predicted: [] };

const actualGold = historicalPrediction.actual;
const predictedGold = historicalPrediction.predicted;

// ==========================================
// HELPER FUNCTIONS
// ==========================================
function formatDate(date) {
    if (!date) return '';
    return new Date(date).toLocaleDateString('id-ID', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    });
}

// ==========================================
// PROCESSING HISTORICAL LABELS
// ==========================================
const historicalLabels = historicalChartData.map(row => formatDate(row['Periode']));
const nSteps = 30;

const safeLabels = historicalLabels.slice(nSteps);
const safeActual = actualGold;
const safePredicted = predictedGold;

// ==========================================
// PROCESSING FORECAST LABELS
// ==========================================
const targetSource = dataBridge.activeLastRow || activeData;
const lastIndex = targetSource.length - 1;
const rawLastDate = targetSource[lastIndex]?.Periode;

let lastDate = new Date();
if (rawLastDate) {
    lastDate = new Date(rawLastDate);
    if (isNaN(lastDate.getTime())) {
        const parts = String(rawLastDate).split(/[-/ T]/);
        if (parts.length >= 3) {
            lastDate = new Date(parts[0], parts[1] - 1, parts[2]);
        }
    }
}

const forecastLabels = predictResult.map((_, index) => {
    const nextDate = new Date(lastDate);
    nextDate.setDate(nextDate.getDate() + index + 1);
    return formatDate(nextDate);
});

// ==========================================
// CHART 1: ACTUAL VS FORECASTED HISTORICAL
// ==========================================
if (document.getElementById('goldChart')) {
    new Chart(document.getElementById('goldChart'), {
        type: 'line',
        data: {
            labels: safeLabels,
            datasets: [
                {
                    label: 'Actual Gold',
                    data: safeActual,
                    borderColor: '#D4AF37',
                    backgroundColor: 'transparent',
                    fill: false,
                    tension: 0.15,
                    borderWidth: 4,
                    pointRadius: 1,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#D4AF37',
                    pointBorderWidth: 0
                },
                {
                    label: 'Forecasted Gold',
                    data: safePredicted,
                    borderColor: '#FF3D00',
                    backgroundColor: 'rgba(255, 61, 0, 0.12)',
                    fill: false,
                    tension: 0.15,
                    borderWidth: 2.5,
                    borderDash: [8, 6],
                    pointRadius: 3,
                    pointHoverRadius: 7,
                    pointBackgroundColor: '#FF3D00',
                    pointBorderColor: '#FF3D00',
                    pointBorderWidth: 1.5
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#A89878',
                        usePointStyle: true,
                        padding: 20,
                        font: { size: 13 }
                    }
                },
                tooltip: {
                    backgroundColor: '#111',
                    titleColor: '#fff',
                    bodyColor: '#ddd',
                    borderColor: '#333',
                    borderWidth: 1,
                    padding: 12
                }
            },
            scales: sharedChartScales,
            elements: {
                line: { capBezierPoints: true }
            }
        }
    });
}

// ==========================================
// CHART 2: FUTURE FORECAST RESULT
// ==========================================
if (document.getElementById('forecastChart')) {
    new Chart(document.getElementById('forecastChart'), {
        type: 'line',
        data: {
            labels: forecastLabels, 
            datasets: [
                {
                    label: 'Forecast Gold',
                    data: predictResult,
                    borderColor: '#FF3D00',
                    pointBackgroundColor: '#FF3D00',
                    backgroundColor: 'rgba(255, 61, 0, 0.15)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3,
                    pointRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#A89878' }
                }
            },
            scales: sharedChartScales
        }
    });
}

// ==========================================
// DATASET TABLE INTERACTION (TOGGLE)
// ==========================================
const toggleBtn = document.getElementById('toggleTableBtn');
const tableContainer = document.getElementById('tableContainer');

if (toggleBtn && tableContainer) {
    toggleBtn.addEventListener('click', () => {
        tableContainer.classList.toggle('active');
        toggleBtn.innerText = tableContainer.classList.contains('active')
            ? 'Sembunyikan Dataset'
            : 'Lihat Semua Dataset';
    });
}