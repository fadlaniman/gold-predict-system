Chart.defaults.color = '#A89878';

const rawData = window.chartData;
const predictResult = window.predicted;
const historicalPrediction = window.historicalPrediction;


// =====================================
// HISTORICAL DATA
// =====================================

const actualGold = historicalPrediction.actual;
const predictedGold = historicalPrediction.predicted;


// =====================================
// HELPER FORMAT DATE
// =====================================

function formatDate(date) {
    return new Date(date).toLocaleDateString('id-ID', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    });
}


// =====================================
// LABELS (FULL HISTORICAL)
// =====================================

const labels = rawData.map(row =>
    formatDate(row['Periode'])
);


// =====================================
// DEBUG (PASTIKAN LAST DATE BENAR)
// =====================================

console.log("LAST RAW DATE:", rawData[rawData.length - 1]['Periode']);
console.log("LAST LABEL:", labels[labels.length - 1]);


// =====================================
// SAFE ALIGNMENT (ANTI MISSING DATA)
// =====================================

const minLength = Math.min(
    labels.length,
    actualGold.length,
    predictedGold.length
);

const safeLabels = labels.slice(-minLength);
const safeActual = actualGold.slice(-minLength);
const safePredicted = predictedGold.slice(-minLength);


// =====================================
// FORECAST LABELS (FUTURE)
// =====================================

const lastDate =
    new Date(rawData[rawData.length - 1]['Periode']);

const forecastLabels =
    predictResult.map((_, index) => {

        const nextDate = new Date(lastDate);
        nextDate.setDate(nextDate.getDate() + index + 1 );

        return formatDate(nextDate);
    });


// =====================================
// GOLD CHART (ACTUAL VS PREDICTED)
// =====================================

new Chart(document.getElementById('goldChart'), {

    type: 'line',

    data: {

        labels: safeLabels,

        datasets: [

            // =================================
            // ACTUAL GOLD (SOLID)
            // =================================
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
                pointBorderWidth: 0,

                borderDash: []
            },

            // =================================
            // PREDICTED GOLD (DASHED)
            // =================================
            {
                label: 'Predicted Gold',

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

        scales: {

            x: {
                ticks: {
                    color: '#A89878',
                    maxRotation: 45,
                    minRotation: 45,

                    callback: function(value) {
                        return this.getLabelForValue(value);
                    }
                },

                grid: {
                    color: 'rgba(255,255,255,0.04)'
                }
            },

            y: {
                ticks: {
                    color: '#A89878',

                    callback: function(value) {
                        return 'Rp ' +
                            new Intl.NumberFormat('id-ID').format(value);
                    }
                },

                grid: {
                    color: 'rgba(255,255,255,0.04)'
                }
            }
        },

        elements: {
            line: {
                capBezierPoints: true
            }
        }
    }
});


// =====================================
// FORECAST CHART (FUTURE ONLY)
// =====================================

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
                labels: {
                    color: '#A89878'
                }
            }
        },

        scales: {

            x: {
                ticks: {
                    color: '#A89878',
                    maxRotation: 45,
                    minRotation: 45,

                    callback: function(value) {
                        return this.getLabelForValue(value);
                    }
                },

                grid: {
                    color: 'rgba(255,255,255,0.05)'
                }
            },

            y: {
                ticks: {
                    color: '#A89878',

                    callback: function(value) {
                        return 'Rp ' +
                            new Intl.NumberFormat('id-ID').format(value);
                    }
                },

                grid: {
                    color: 'rgba(255,255,255,0.05)'
                }
            }
        }
    }
});


// =====================================
// TOGGLE DATASET TABLE
// =====================================

const toggleBtn =
    document.getElementById('toggleTableBtn');

const tableContainer =
    document.getElementById('tableContainer');

toggleBtn.addEventListener('click', () => {

    tableContainer.classList.toggle('active');

    toggleBtn.innerText =
        tableContainer.classList.contains('active')
            ? 'Sembunyikan Dataset'
            : 'Lihat Semua Dataset';
});