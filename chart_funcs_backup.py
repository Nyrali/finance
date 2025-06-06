import json
import pandas as pd


def get_color_palettes(opacity=0.85):
    def rgba(r, g, b):
        return f"rgba({r}, {g}, {b}, {opacity})"

    return {
        "default": [
            rgba(54, 162, 235),
            rgba(255, 99, 132),
            rgba(255, 206, 86),
            rgba(75, 192, 192),
            rgba(153, 102, 255),
            rgba(255, 159, 64),
            rgba(201, 203, 207),
            rgba(0, 204, 102),
            rgba(255, 102, 255),
            rgba(102, 255, 255),
            rgba(0, 0, 0),
            rgba(240, 100, 100),
            rgba(100, 240, 100),
            rgba(100, 100, 240),
        ],
        "forest": [
            rgba(253, 216, 167),
            rgba(150, 128, 108),
            rgba(136, 107, 85),
            rgba(46, 75, 71),
            rgba(35, 50, 45),
        ],
        "pastel": [
            rgba(255, 179, 186),
            rgba(255, 223, 186),
            rgba(255, 255, 186),
            rgba(186, 255, 201),
            rgba(186, 225, 255),
        ],
        "autumn_night": [
            rgba(171, 74, 31),  # rust orange
            rgba(105, 61, 34),  # deep brown
            rgba(200, 152, 106),  # warm tan
            rgba(57, 89, 78),  # forest green
            rgba(11, 61, 62),  # teal
            rgba(48, 11, 28),  # dark burgundy
            rgba(18, 19, 24),  # near-black navy
        ],
        "lake_forest": [
            rgba(162, 181, 104),  # #A2B568
            rgba(105, 116, 49),  # #697431
            rgba(71, 93, 46),  # #475D2E
            rgba(53, 75, 41),  # #354B29 - added
            rgba(21, 40, 47),  # #15282F
            rgba(17, 70, 67),  # #114643
            rgba(3, 99, 92),  # #03635C - added
            rgba(6, 129, 118),  # #068176
        ],
        "flavors": [
            rgba(0, 66, 66),  # pine
            rgba(0, 133, 156),  # proud
            rgba(0, 120, 79),  # basil
            rgba(159, 141, 50),  # butch
            rgba(133, 82, 160),  # dessert
            rgba(239, 71, 130),  # femme
            rgba(252, 64, 36),  # spicy
            rgba(248, 153, 29),  # honey
            rgba(240, 158, 125),  # peach
            rgba(187, 197, 171),  # sage
        ],
        "ocean_breeze": [
            rgba(28, 52, 100),  # Deep Navy
            rgba(3, 69, 105),  # Midnight Blue
            rgba(35, 91, 121),  # Steel Blue
            rgba(8, 108, 162),  # Cerulean
            rgba(60, 157, 208),  # Sky Blue
            rgba(120, 190, 220),  # Light Blue
            rgba(180, 220, 240),  # Pale Blue
            rgba(220, 240, 250),  # Ice Blue
        ],
        "forest_canopy": [
            rgba(34, 49, 34),  # Dark Forest Green
            rgba(85, 107, 47),  # Olive Drab
            rgba(107, 142, 35),  # Olive Green
            rgba(154, 205, 50),  # Yellow Green
            rgba(139, 69, 19),  # Saddle Brown
            rgba(160, 82, 45),  # Sienna
            rgba(210, 180, 140),  # Tan
            rgba(245, 222, 179),  # Wheat
        ],
        "vibrant_spectrum": [
            rgba(255, 0, 0),  # Red
            rgba(255, 127, 0),  # Orange
            rgba(255, 255, 0),  # Yellow
            rgba(0, 255, 0),  # Green
            rgba(0, 0, 255),  # Blue
            rgba(75, 0, 130),  # Indigo
            rgba(148, 0, 211),  # Violet
            rgba(255, 20, 147),  # Deep Pink
        ],
        "policy_focus": [
            rgba(157, 94, 89),  # červenohnědá
            rgba(199, 163, 70),  # hořčičná
            rgba(110, 145, 123),  # zelenošedá
            rgba(77, 142, 160),  # šedomodrá
            rgba(228, 190, 141),  # písková
            rgba(142, 86, 75),  # cihlová
            rgba(176, 129, 50),  # tmavá hořčice
            rgba(89, 118, 107),  # tmavá zeleň
            rgba(62, 91, 110),  # ocelově modrá
        ],
        "block_segments": [
            rgba(58, 123, 179),  # modrá
            rgba(60, 190, 173),  # tyrkysová
            rgba(245, 189, 68),  # žlutá
            rgba(237, 108, 76),  # cihlově oranžová
            rgba(255, 153, 71),  # jasná oranžová
            rgba(42, 99, 138),  # tmavě modrá
            rgba(82, 180, 175),  # světle tyrkysová
            rgba(255, 203, 92),  # světle žlutá
            rgba(242, 132, 90),  # korálově oranžová
        ],
        "treemap_blues": [
            rgba(251, 181, 84),  # světle oranžová
            rgba(255, 203, 119),  # krémová žlutá
            rgba(139, 213, 212),  # aqua
            rgba(97, 186, 199),  # tyrkys
            rgba(52, 144, 172),  # modrozelená
            rgba(26, 102, 145),  # tmavší modrá
            rgba(20, 79, 120),  # hluboká modrá
            rgba(15, 61, 94),  # námořnická
            rgba(8, 44, 72),  # inkoustová
        ],
    }


def normalize_categories(df, categories):
    if "category_high_lvl" not in df.columns:
        raise KeyError("Missing 'category_high_lvl' column in the dataframe.")
    df["category_high_lvl"] = (
        df["category_high_lvl"].astype(str).str.strip().str.lower()
    )
    return [c.lower().strip() for c in categories]


def prepare_pivoted_data(df, categories):
    filtered = df[df["category_high_lvl"].isin(categories)]
    grouped = (
        filtered.groupby(["year_month", "category_high_lvl"])["debit"]
        .sum()
        .reset_index()
    )
    return grouped.pivot(
        index="year_month", columns="category_high_lvl", values="debit"
    ).fillna(0)


def sort_categories(pivoted):
    base_order = [
        "bydlení",
        "zdraví a pojištění",
        "restaurace / fast food",
        "potraviny (supermarket)",
        "doprava",
        "zábava a volný čas",
        "oblečení a styl",
        "ostatní nákupy",
        "jiné finanční výdaje",
    ]
    sorted_rows, index_labels = [], []
    for idx, row in pivoted.iterrows():
        non_zero_cols = row[row > 0].index.tolist()
        fixed_present = [cat for cat in base_order if cat in non_zero_cols]
        remaining = [cat for cat in non_zero_cols if cat not in fixed_present]
        remaining_sorted = row[remaining].sort_values(ascending=False).index.tolist()
        row_order = fixed_present + remaining_sorted
        sorted_row = row.reindex(
            row_order + [col for col in pivoted.columns if col not in row_order],
            fill_value=0,
        )
        sorted_rows.append(sorted_row)
        index_labels.append(idx)
    sorted_df = pd.DataFrame(sorted_rows, index=index_labels)
    # if want ascending false turn on
    # sorted_df = sorted_df.sort_index(ascending=False)
    return sorted_df, sorted_df.index.tolist()


def export_transaction_data(df, categories):
    display_cols = [
        "year_month",
        "booking_date",
        "debit",
        "category_high_lvl",
        "counter_acc_name",
        "counter_acc",
        "category",
    ]
    filtered = df[df["category_high_lvl"].isin(categories)]
    displayed = filtered[display_cols].copy()
    for col in ["year_month", "booking_date", "counter_acc_name", "counter_acc"]:
        displayed[col] = displayed[col].astype(str)
    return json.dumps(displayed.to_dict(orient="records"), ensure_ascii=False)


def build_chart_onclick_handler():
    return """
(e, activeEls) => {
  const popup = document.getElementById("popup");
  popup.style.display = "none";
  if (!activeEls.length) return;

  const el = activeEls[0];
  const cat = chart.data.datasets[el.datasetIndex].label.toLowerCase();
  const month = chart.data.labels[el.index];
  const filtered = transactions.filter(t => t.year_month === month && t.category_high_lvl === cat);

  let msg = "📅 " + month + "\\n📂 " + cat + "\\n\\n";

  if (filtered.length === 0) {
    msg = "No transactions found.";
  } else {
    filtered.forEach(t => {
      const rawName = t.counter_acc_name || "";
      const rawNumber = t.counter_acc || "";
      const name = rawName.toLowerCase() !== 'nan' && rawName.trim() !== '' ? rawName : "📭 neznámý příjemce";
      const number = rawNumber.toLowerCase() !== 'nan' && rawNumber.trim() !== '' ? rawNumber : "❓ neznámé číslo účtu";
      const category = t.category && t.category.toLowerCase() !== 'nan' ? t.category : "📁 neznámá kategorie";

      msg += "• " + t.booking_date + " 📉 " + t.debit + " Kč\\n  " +
             category + "\\n  " +
             name + " (" + number + ")\\n\\n";
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
"""


def build_html(
    labels, categories, data_matrix, transactions_json, palettes, opacity=0.95
):
    import json

    container_height_px = max(800, 50 * len(labels))
    palettes_json = json.dumps(palettes, ensure_ascii=False)
    palette_options = "".join(
        f'<option value="{name}">{name.replace("_", " ").title()}</option>'
        for name in palettes.keys()
    )

    onclick_handler = build_chart_onclick_handler()

    return f"""<!DOCTYPE html>
<html>
<head>
  <title>Resizable Stacked Chart</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {{
      --bg-color-light: #fff;
      --bg-color-dark: #1e1e1e;
      --text-color-light: #000;
      --text-color-dark: #eee;
    }}
    body {{
      font-family: Arial, sans-serif;
      background: var(--bg-color-light);
      color: var(--text-color-light);
      margin: 0;
      padding: 0;
      transition: background 0.4s, color 0.4s;
    }}
    .chart-container {{
      resize: both;
      overflow: auto;
      width: 90%;
      max-width: 2560px;
      height: {container_height_px}px;
      border: 2px dashed #ccc;
      margin: 20px auto;
      padding: 10px;
    }}
    body.dark-mode .chart-container {{
      border-color: #666;
    }}
    canvas {{
      width: 100% !important;
      height: 100% !important;
    }}
    #popup {{
      display: none;
      position: absolute;
      z-index: 9999;
      background: white;
      border: 2px solid #444;
      padding: 12px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      font-size: 18px;
      max-width: 500px;
      white-space: pre-wrap;
      transition: background 0.3s, color 0.3s;
    }}
    #control-bar {{
      position: fixed;
      top: 10px;
      right: 10px;
      display: flex;
      gap: 10px;
      z-index: 1000;
    }}
    #toggle-theme,
    #palette-picker {{
      background-color: #333;
      color: white;
      font-size: 16px;
      padding: 10px 16px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      transition: background 0.3s ease;
    }}
    #toggle-theme:hover,
    #palette-picker:hover {{
      background-color: #555;
    }}
    .dark-mode #toggle-theme,
    .dark-mode #palette-picker {{
      background-color: #999;
      color: #000;
    }}
  </style>
</head>
<body>
  <div id="control-bar">
    <button id="toggle-theme">&#x1F319; Dark Mode</button>
    <select id="palette-picker">
      {palette_options}🌈
    </select>
  </div>

  <h2 style="text-align:center; font-size: 28px;">📊 Monthly Debit by Category</h2>
  <div class="chart-container">
    <canvas id="debitChart"></canvas>
  </div>
  <div id="popup"></div>
  <script>
    const transactions = {transactions_json};
    const labels = {labels};
    const categories = {categories};
    const rawData = {data_matrix};
    const PALETTES = {palettes_json};
    let darkMode = false;
    let currentPalette = "default";
    let selectedLabels = new Set();

    function getPalette(name) {{
      return PALETTES[name] || PALETTES["default"];
    }}

    function getDatasets(paletteName) {{
      const colors = getPalette(paletteName);
      return categories.map((cat, i) => {{
        return {{
          label: cat,
          data: rawData.map(row => row[cat] || 0),
          backgroundColor: colors[i % colors.length],
          stack: 'total'
        }};
      }});
    }}

    function updateChartVisibility() {{
      chart.data.datasets.forEach((ds, i) => {{
        chart.getDatasetMeta(i).hidden = selectedLabels.size > 0 && !selectedLabels.has(ds.label);
      }});
      chart.update();
    }}

    function createChartConfig(dark, datasets) {{
      return {{
        type: 'bar',
        data: {{
          labels: labels,
          datasets: datasets
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              position: 'top',
              labels: {{
                font: {{ size: 20 }},
                color: dark ? '#eee' : '#000'
              }},
              onClick: function(e, legendItem) {{
                e.native.stopPropagation();
                const label = legendItem.text;
                if (selectedLabels.has(label)) {{
                  selectedLabels.delete(label);
                }} else {{
                  selectedLabels.add(label);
                }}
                updateChartVisibility();
              }}
            }},
            title: {{
              display: true,
              text: 'Monthly Debit by Category',
              font: {{ size: 26 }},
              color: dark ? '#eee' : '#000'
            }},
            tooltip: {{
              bodyFont: {{ size: 20 }},
              titleFont: {{ size: 22 }},
              backgroundColor: dark ? '#333' : '#fff',
              titleColor: dark ? '#fff' : '#000',
              bodyColor: dark ? '#eee' : '#000',
              borderColor: dark ? '#888' : '#ccc',
              borderWidth: 1
            }}
          }},
          scales: {{
            x: {{
              stacked: true,
              ticks: {{
                font: {{ size: 22 }},
                color: dark ? '#eee' : '#000'
              }},
              grid: {{
                color: dark ? '#555' : '#ccc'
              }}
            }},
            y: {{
              stacked: true,
              ticks: {{
                font: {{ size: 20 }},
                color: dark ? '#eee' : '#000'
              }},
              grid: {{
                color: dark ? '#555' : '#ccc'
              }}
            }}
          }},
          onClick: {onclick_handler}
        }}
      }};
    }}

    const ctx = document.getElementById('debitChart').getContext('2d');
    let chart = new Chart(ctx, createChartConfig(darkMode, getDatasets(currentPalette)));
    updateChartVisibility();

    document.getElementById("toggle-theme").addEventListener("click", () => {{
      darkMode = !darkMode;
      document.body.classList.toggle("dark-mode", darkMode);
      document.body.style.background = darkMode ? 'var(--bg-color-dark)' : 'var(--bg-color-light)';
      document.body.style.color = darkMode ? 'var(--text-color-dark)' : 'var(--text-color-light)';
      chart.destroy();
      chart = new Chart(ctx, createChartConfig(darkMode, getDatasets(currentPalette)));
      updateChartVisibility();
    }});

    document.getElementById("palette-picker").addEventListener("change", (e) => {{
      currentPalette = e.target.value;
      chart.destroy();
      chart = new Chart(ctx, createChartConfig(darkMode, getDatasets(currentPalette)));
      updateChartVisibility();
    }});

    document.body.addEventListener("click", (e) => {{
      if (!e.target.closest('.chart-container') && selectedLabels.size > 0) {{
        selectedLabels.clear();
        updateChartVisibility();
      }}
    }});
  </script>
</body>
</html>"""


def generate_resizable_stacked_chart_html_1(
    df, categories, output_file="D:/finance/chart_1.html", opacity=0.90
):
    try:
        categories = normalize_categories(df, categories)
        pivoted = prepare_pivoted_data(df, categories)
        sorted_df, sorted_labels = sort_categories(pivoted)

        transactions_json = export_transaction_data(df, categories)
        palettes = get_color_palettes(opacity=opacity)
        html = build_html(
            sorted_labels,
            sorted_df.columns.tolist(),
            sorted_df.to_dict(orient="records"),
            transactions_json,
            palettes,
        )
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Clickable stacked chart saved as {output_file}")
    except Exception as e:
        print(f"❌ Error generating chart: {e}")


def generate_resizable_stacked_chart_html(
    df,
    categories,
    template_file="D:/finance/chart_template.html",
    output_file="D:/finance/resizable_stacked_chart.html",
):
    # Step 1: Filter and aggregate
    filtered = df[df["category"].isin([c.lower() for c in categories])]
    grouped = filtered.groupby(["year_month", "category"])["debit"].sum().reset_index()

    # Step 2: Prepare labels and datasets
    labels = grouped["year_month"].unique().tolist()
    datasets = []
    colors = [
        "rgba(54, 162, 235, 0.85)",
        "rgba(255, 99, 132, 0.85)",
        "rgba(255, 206, 86, 0.85)",
        "rgba(75, 192, 192, 0.85)",
        "rgba(153, 102, 255, 0.85)",
        "rgba(255, 159, 64, 0.85)",
    ]

    for i, cat in enumerate(categories):
        values = [
            grouped[
                (grouped["year_month"] == m) & (grouped["category"] == cat.lower())
            ]["debit"].sum()
            for m in labels
        ]
        datasets.append(
            f"""{{
            label: "{cat.capitalize()}",
            data: {values},
            backgroundColor: "{colors[i % len(colors)]}",
            stack: "total"
        }}"""
        )

    # Step 3: Load template and substitute
    with open(template_file, "r", encoding="utf-8") as file:
        template = file.read()

    html = template.replace("__LABELS__", json.dumps(labels))
    html = html.replace("__DATASETS__", ",\n".join(datasets))

    # Step 4: Save to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Chart saved to: {output_file}")
