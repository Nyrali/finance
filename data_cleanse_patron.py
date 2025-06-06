
import pandas as pd

def remove_refund_pairs(df, days=20):
    df = df.reset_index(drop=False)
    df = df.copy()

    debits = df[df['amount'] < 0].copy()
    credits = df[df['amount'] > 0].copy()

    debits['abs_amount'] = debits['amount'].abs().round(2)
    credits['abs_amount'] = credits['amount'].round(2)

    # Sort for predictable matching
    debits.sort_values(by='booking_date', inplace=True)
    credits.sort_values(by='booking_date', inplace=True)

    used_debit_ids = set()
    used_credit_ids = set()

    for i, credit in credits.iterrows():
        potential_matches = debits[
            (debits['counter_acc_name'] == credit['counter_acc_name']) &
            (debits['abs_amount'] == credit['abs_amount']) &
            (~debits['index'].isin(used_debit_ids)) &
            (abs((credit['booking_date'] - debits['booking_date']).dt.days) <= days)
        ]

        if not potential_matches.empty:
            match = potential_matches.iloc[0]
            used_debit_ids.add(match['index'])
            used_credit_ids.add(credit['index'])

    to_remove = list(used_debit_ids.union(used_credit_ids))
    return df[~df['index'].isin(to_remove)]

# Remove unwanted transactions based on counter account name
def remove_unwanted_transactions(df, name_list):
    return df[~df['counter_acc_name'].str.lower().isin([name.lower() for name in name_list])]

def patron_data_cleanse (df):
    # Rename columns
    df.rename(columns={
        'Odesláno': 'booking_date',
        'Částka': 'amount',
        'Měna': 'currency',
        'Název kategorie': 'category',
        'Číslo protiúčtu': 'counter_acc',
        'Název účtu příjemce': 'counter_acc_name'
    }, inplace=True)

    # Convert category to lowercase
    df['category'] = df['category'].str.strip().str.lower()

    # Parse date and extract year/month
    df['booking_date'] = pd.to_datetime(df['booking_date'], format='%d.%m.%Y', errors='coerce')
    df['year'] = df['booking_date'].dt.year
    df['month'] = df['booking_date'].dt.month
    df['year_month'] = df['booking_date'].dt.to_period('M').astype(str)

    # Clean and convert amount
    df['amount'] = (
        df['amount']
        .astype(str)
        .str.replace('\xa0', '', regex=False)  # remove non-breaking space
        .str.replace(',', '.', regex=False)    # fix decimal separator
        .astype(float)
    )

    # Create debit and credit columns
    df['debit'] = df['amount'].where(df['amount'] < 0, 0).abs()
    df['credit'] = df['amount'].where(df['amount'] > 0, 0)
        
    exclude_names = [
        "MARTINKOVÁ TEREZA",              
    ]

    df = remove_unwanted_transactions(df, exclude_names)

    # Map specific counter_acc_name values to new categories
    category_mapping_counter_acc_name = {
        "907 GECO VAM DEKUJE HRADEC KRA": "Zábava a volný čas",
        "Vytvarne potreby U tuk": "ostatní - zábava a relax",
        " VYTVARNE POTREBY U TUKA": "ostatní - zábava a relax",
        "E.M.P. Merchandising Hand": "ostatní - zábava a relax"   
    }

    df['category'] = df['counter_acc_name'].map(category_mapping_counter_acc_name).fillna(df['category'])

    # Map specific counter_acc values to new categories
    category_mapping_counter_acc = {
        "5132099033/0800": "nájem",
        "5720517369/0800": "nájem",
        "5332283003/5500": "nájem",
        "8436104966/5500": "nájem"

    }

    df['category'] = df['counter_acc'].map(category_mapping_counter_acc).fillna(df['category'])

    # Final category normalization
    df['category'] = df['category'].str.strip().str.lower()
        
    df = remove_refund_pairs(df, days=20)

    df['category'] = df['category'].astype(str)

    df = df[df['category'].isin([c.lower() for c in df["category"].unique()])]

    category_merge_map = {
        # ✅ Bydlení
        'bydlení': 'Bydlení',
        'domácnost': 'Bydlení',
        'nájem': 'Bydlení',
        'internet': 'Bydlení',

        # ✅ Jídlo a restaurace
        'jídlo a pití': 'Restaurace / potraviny',
        'jídlo': 'Restaurace / potraviny',

        # ✅ Doprava
        'auto': 'Doprava',
        'benzín': 'Doprava',
        'doprava': 'Doprava',

        # ✅ Zábava a volný čas
        'zábava': 'Zábava a volný čas',
        'elektronika': 'Zábava a volný čas',
        'služby': 'Zábava a volný čas',
        'hotely': 'Zábava a volný čas',
        'domácí mazlíčci': 'Zábava a volný čas',
        

        # ✅ Oblečení a styl
        'oblečení': 'Oblečení a styl',
        'krása a zdraví': 'Oblečení a styl',

        # ✅ Jiné finanční výdaje
        'instituce': 'Jiné finanční výdaje',
        'bankomat': 'Jiné finanční výdaje',
        'spoření': 'Jiné finanční výdaje',
        'cigarety': 'Jiné finanční výdaje',
        'splátky': 'Jiné finanční výdaje',
        'pojištění': 'Jiné finanční výdaje',

        # ✅ Výplata (zachováme jako výnos, zvlášť pokud pracuješ s kredity)
        'výplata': 'Výplata / Příjem',

        # fallback se ošetří později
    }

    # Apply
    df['category_high_lvl'] = df['category'].replace(category_merge_map)
    df = df[df["debit"] > 0]
   

    return df
