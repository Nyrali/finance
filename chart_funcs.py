import json
import pandas as pd
from pathlib import Path


def assemble_chart_html_from_parts(
    labels,
    categories,
    data_matrix,
    transactions_json,
    palettes,
    output_path,
    html_head_path="web_src/chart_head.html",
    html_body_top_path="web_src/chart_body_top.html",
    html_body_bottom_path="web_src/chart_body_bottom.html",
    js_handler_path="web_src/chart_onclick_handler.js",
    js_script_block_path="web_src/chart_script_block.js",
):
    # Load HTML parts
    head = Path(html_head_path).read_text(encoding="utf-8")
    body_top = Path(html_body_top_path).read_text(encoding="utf-8")
    body_bottom = Path(html_body_bottom_path).read_text(encoding="utf-8")

    # Load JS parts
    onclick_handler = Path(js_handler_path).read_text(encoding="utf-8")
    script_template = Path(js_script_block_path).read_text(encoding="utf-8")

    # Create palette <option> tags
    palette_options = "".join(
        f'<option value="{name}">{name.replace("_", " ").title()}</option>'
        for name in palettes
    )

    # Inject palette options into body_top
    body_top = body_top.replace("__PALETTE_OPTIONS__", palette_options)

    # Container height
    container_height = f"{max(800, 50 * len(labels))}px"
    head = head.replace("__HEIGHT__", container_height)

    # Prepare JSON replacements
    script = (
        script_template.replace(
            "__TRANSACTIONS__", json.dumps(transactions_json, ensure_ascii=False)
        )
        .replace("__LABELS__", json.dumps(labels, ensure_ascii=False))
        .replace("__CATEGORIES__", json.dumps(categories, ensure_ascii=False))
        .replace("__DATA__", json.dumps(data_matrix, ensure_ascii=False))
        .replace("__PALETTES__", json.dumps(palettes, ensure_ascii=False))
        .replace("__ONCLICK__", onclick_handler.strip())
    )

    # Join all parts
    final_html = head + body_top + "<script>\n" + script + "\n</script>\n" + body_bottom
    return final_html


def generate_chart_with_templates(
    df, categories, output_file="D:/finance/chart_from_templates.html", opacity=0.90
):
    try:
        # Normalize categories
        norm_categories = normalize_categories(df, categories)

        # Prepare pivoted and sorted data
        pivoted = prepare_pivoted_data(df, norm_categories)
        sorted_df, labels = sort_categories(pivoted)

        # Export inputs
        data_matrix = sorted_df.to_dict(orient="records")
        transactions = json.loads(export_transaction_data(df, norm_categories))
        palettes = get_color_palettes(opacity=opacity)

        # Assemble HTML from parts
        final_html = assemble_chart_html_from_parts(
            labels=labels,
            categories=sorted_df.columns.tolist(),
            data_matrix=data_matrix,
            transactions_json=transactions,
            palettes=palettes,
            output_path=output_file,
        )

        # Save output
        Path(output_file).write_text(final_html, encoding="utf-8")
        print(f"✅ Chart successfully saved to {output_file}")

    except Exception as e:
        print(f"❌ Failed to generate chart: {e}")


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
