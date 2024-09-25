import polars as pl

def help():
    print("""Dear User,

Thank you for choosing the NotificationList package. We sincerely appreciate your support.

Should you require any assistance or have any questions, please do not hesitate to reach out to Ranjeet Aloriya at ranjeet.aloriya@gmail.com. We are here to help!

Best regards,
Ranjeet Aloriya""")
    
def initial_unqid(file_path):
    df = pl.read_csv(file_path, encoding="latin", infer_schema_length=0)
    df = df.with_columns([pl.col(col).alias(col.upper()) for col in df.columns])
    df = df.select([pl.col(col).str.to_uppercase().alias(col) if df.schema[col] == pl.Utf8 else pl.col(col) for col in df.columns])
    df = df.sort(by=['FIRST NAME', 'LAST NAME', 'MIDDLE NAME'])
    df = df.with_columns((pl.arange(1, len(df) + 1)).alias("S N")).select(["S N"] + df.columns)
    df = df.with_columns(
        pl.concat_str(
            [
                pl.col("FIRST NAME").fill_null(""),
                pl.col("LAST NAME").fill_null(""),
            ],
            separator=" ",
        ).alias("FIRST LAST"),
    )
    df = df.with_columns(
        pl.concat_str(
            [
                pl.col("FIRST NAME").fill_null(""),
                pl.col("MIDDLE NAME").fill_null(""),
                pl.col("LAST NAME").fill_null(""),
            ],
            separator=" ",
        ).alias("FULL NAME"),
    )
    df = df.with_columns(pl.col("FIRST LAST").str.replace_all(r'[^a-zA-Z]', ' '))
    df = df.with_columns(pl.col("FULL NAME").str.replace_all(r'[^a-zA-Z]', ' '))
    df = df.with_columns(pl.col("FIRST LAST").str.split(" ").list.unique().list.sort().list.join(" ").alias("FIRST LAST"))
    df = df.with_columns(pl.col("FULL NAME").str.split(" ").list.unique().list.sort().list.join(" ").alias("FULL NAME"))
    df = df.with_columns(pl.col("FIRST LAST").str.replace_all(r' ', ''))
    df = df.with_columns(pl.col("FULL NAME").str.replace_all(r' ', ''))
    df = df.join(df.group_by("FIRST LAST").agg(pl.col("S N").alias("FIRST_LAST")), on = "FIRST LAST")
    df = df.join(df.group_by("FULL NAME").agg(pl.col("S N").alias("FULL_NAME")), on = "FULL NAME")
    df = df.with_columns(((pl.col("FIRST_LAST").list.concat(pl.col("FULL_NAME")).list.unique())).alias("id"))
    id_to_group = {}
    unique_id_counter = 1
    for ids in df['id']:
        group_id = next((id_to_group[id] for id in ids if id in id_to_group), None)

        if not group_id:
            group_id = f"UNQ_{unique_id_counter:05}"
            unique_id_counter += 1

        for id in ids:
            id_to_group[id] = group_id
    df = df.with_columns(pl.col("S N").replace_strict(id_to_group).alias("UNIQUE ID"))
    df = df.drop(["S N", "FIRST LAST", "FULL NAME", "FIRST_LAST", "FULL_NAME", "id"])
    df = df.sort('UNIQUE ID')
    serial_numbers = pl.arange(1, df.height + 1).cast(pl.Utf8)
    df = df.with_columns(serial_numbers.alias("S N")).select(["S N"] + df.columns)
    df = df.select(["S N", "UNIQUE ID"] + [col for col in df.columns if col not in ["S N", "UNIQUE ID"]])
    return df