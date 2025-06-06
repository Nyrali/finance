(e, activeEls) => {
  const popup = document.getElementById("popup");
  popup.style.display = "none";
  if (!activeEls.length) return;

  const el = activeEls[0];
  const cat = chart.data.datasets[el.datasetIndex].label.toLowerCase();
  const month = chart.data.labels[el.index];
  const filtered = transactions.filter(t => t.year_month === month && t.category_high_lvl === cat);

  let msg = "📅 " + month + "\n📂 " + cat + "\n\n";

  if (filtered.length === 0) {
    msg = "No transactions found.";
  } else {
    filtered.forEach(t => {
      const rawName = t.counter_acc_name || "";
      const rawNumber = t.counter_acc || "";
      const name = rawName.toLowerCase() !== 'nan' && rawName.trim() !== '' ? rawName : "📭 neznámý příjemce";
      const number = rawNumber.toLowerCase() !== 'nan' && rawNumber.trim() !== '' ? rawNumber : "❓ neznámé číslo účtu";
      const category = t.category && t.category.toLowerCase() !== 'nan' ? t.category : "📁 neznámá kategorie";

      msg += "• " + t.booking_date + " 📉 " + t.debit + " Kč\n  " +
             category + "\n  " +
             name + " (" + number + ")\n\n";
    });
  }

  popup.innerText = msg;
  popup.style.left = e.native.clientX + 20 + "px";
  popup.style.top = e.native.clientY + 20 + "px";
  popup.style.backgroundColor = darkMode ? "#333" : "#fff";
  popup.style.color = darkMode ? "#eee" : "#000";
  popup.style.borderColor = darkMode ? "#999" : "#444";
  popup.style.display = "block";
}
