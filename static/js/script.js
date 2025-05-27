   function switchMode(mode) {
      document.getElementById('ungrouped-section').classList.remove('visible');
      document.getElementById('grouped-section').classList.remove('visible');
      document.getElementById(mode + '-section').classList.add('visible');
    }

    function getData() {
      const mode = document.querySelector('input[name="mode"]:checked').value;
      if (mode === 'ungrouped') {
        const data = document.getElementById('ungroupedInput').value.split(',').map(Number);
        return { grouped: false, data: data };
      } else {
        const classes = document.getElementById('classIntervals').value.split(',');
        const frequencies = document.getElementById('frequencies').value.split(',').map(Number);
        return { grouped: true, classes: classes, frequencies: frequencies };
      }
    }

    function analyze() {
      const payload = getData();
      fetch('/analyze', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      })
      .then(res => res.json())
      .then(data => {
        const table = document.getElementById('resultTable');
        table.innerHTML = `<tr><th>Type</th><th>Value</th></tr>`;
        for (let key in data) {
          table.innerHTML += `<tr><td>${key}</td><td>${data[key]}</td></tr>`;
        }
      });
    }

    function generateCumulative() {
      const payload = getData();
      fetch('/cumulative', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      })
      .then(res => res.json())
      .then(data => {
        const table = document.getElementById('cumulativeTable');
        table.innerHTML = `<tr><th>Class Interval</th><th>Frequency</th><th>Cumulative Frequency</th></tr>`;
        data.forEach(row => {
          table.innerHTML += `<tr>
            <td>${row['Class Interval']}</td>
            <td>${row['Frequency']}</td>
            <td>${row['Cumulative Frequecny']}</td>
          </tr>`;
        });
      });
    }

    function generateHistogram() {
      const payload = getData();
      fetch('/histogram', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        grouped: true,
        classes: ["10-20", "20-30", "30-40"],
        frequencies: [5, 10, 6]
    })
})
.then(res => res.json())
.then(data => {
    if (data.image) {
        document.getElementById('histogram').src = 'data:image/png;base64,' + data.image;
    }
});
    }