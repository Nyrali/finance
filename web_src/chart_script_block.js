const transactions = __TRANSACTIONS__;
const labels = __LABELS__;
const categories = __CATEGORIES__;
const rawData = __DATA__;
const PALETTES = __PALETTES__;
let darkMode = false;
let currentPalette = "default";
let selectedLabels = new Set();

function getPalette(name) {
  return PALETTES[name] || PALETTES["default"];
}

function getDatasets(paletteName) {
  const colors = getPalette(paletteName);
  return categories.map(function(cat, i) {
    return {
      label: cat,
      data: rawData.map(function(row) { return row[cat] || 0 }),
      backgroundColor: colors[i % colors.length],
      stack: 'total'
    };
  });
}

function updateChartVisibility() {
  chart.data.datasets.forEach(function(ds, i) {
    chart.getDatasetMeta(i).hidden = selectedLabels.size > 0 && !selectedLabels.has(ds.label);
  });
  chart.update();
}

function createChartConfig(dark, datasets) {
  return {
    type: 'bar',
    data: {
      labels: labels,
      datasets: datasets
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            font: { size: 20 },
            color: dark ? '#eee' : '#000'
          },
          onClick: function(e, legendItem) {
            e.native.stopPropagation();
            const label = legendItem.text;
            if (selectedLabels.has(label)) {
              selectedLabels.delete(label);
            } else {
              selectedLabels.add(label);
            }
            updateChartVisibility();
          }
        },
        title: {
          display: true,
          text: 'Monthly Debit by Category',
          font: { size: 26 },
          color: dark ? '#eee' : '#000'
        },
        tooltip: {
          bodyFont: { size: 20 },
          titleFont: { size: 22 },
          backgroundColor: dark ? '#333' : '#fff',
          titleColor: dark ? '#fff' : '#000',
          bodyColor: dark ? '#eee' : '#000',
          borderColor: dark ? '#888' : '#ccc',
          borderWidth: 1
        }
      },
      scales: {
        x: {
          stacked: true,
          ticks: {
            font: { size: 22 },
            color: dark ? '#eee' : '#000'
          },
          grid: {
            color: dark ? '#555' : '#ccc'
          }
        },
        y: {
          stacked: true,
          ticks: {
            font: { size: 20 },
            color: dark ? '#eee' : '#000'
          },
          grid: {
            color: dark ? '#555' : '#ccc'
          }
        }
      },
      onClick: __ONCLICK__
    }
  };
}

const ctx = document.getElementById('debitChart').getContext('2d');
let chart = new Chart(ctx, createChartConfig(darkMode, getDatasets(currentPalette)));
updateChartVisibility();

document.getElementById("toggle-theme").addEventListener("click", function() {
  darkMode = !darkMode;
  document.body.classList.toggle("dark-mode", darkMode);
  document.body.style.background = darkMode ? 'var(--bg-color-dark)' : 'var(--bg-color-light)';
  document.body.style.color = darkMode ? 'var(--text-color-dark)' : 'var(--text-color-light)';
  chart.destroy();
  chart = new Chart(ctx, createChartConfig(darkMode, getDatasets(currentPalette)));
  updateChartVisibility();
});

document.getElementById("palette-picker").addEventListener("change", function(e) {
  currentPalette = e.target.value;
  chart.destroy();
  chart = new Chart(ctx, createChartConfig(darkMode, getDatasets(currentPalette)));
  updateChartVisibility();
});

document.body.addEventListener("click", function(e) {
  if (!e.target.closest('.chart-container') && selectedLabels.size > 0) {
    selectedLabels.clear();
    updateChartVisibility();
  }
});
