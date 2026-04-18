# Python Data Manipulation Summary

Compact study notes from our pandas practice. The emphasis is on patterns that come up in interview-style data tasks: ranking, joins, filtering, reshaping, missing data, and mutation behavior.

Main ideas:
- Use `merge` for SQL-style joins and `concat` for stacking objects.
- Use `melt` for wide-to-long and `pivot` for long-to-wide.
- Prefer boolean filtering for row conditions; use `drop(..., inplace=True)` only when you truly want to mutate the passed object.
- Be explicit about tie handling with `rank(method=...)`.
- Watch pandas indexing: `series[1]` can be label-based, while `series.iloc[1]` is positional.

## 1. Mental Models To Keep Straight

- A `DataFrame` is mutable. If a function changes columns or rows in place, the caller sees it.
- Rebinding a local variable like `df = df[...]` does not change the caller's object.
- In pandas, the most common workflow is: `filter -> reshape/join -> aggregate -> clean names/index`.
- Prefer explicitness in interviews: clear column references, deterministic tie-breaking, and readable reshaping.

## 2. Ranking, Ties, and Nth Values

Typical use cases:
- second-highest salary
- highest salary per department
- keep ties or break ties intentionally

```python
employee = pd.DataFrame(
    {
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Cara", "Dan", "Eli"],
        "departmentId": [10, 10, 10, 20, 20],
        "salary": [120, 120, 90, 150, 130],
    }
)

employee["dense_rank"] = (
    employee.groupby("departmentId")["salary"]
    .rank(method="dense", ascending=False)
)

employee_sorted = employee.sort_values(
    ["departmentId", "salary", "name"],
    ascending=[True, False, True],
).copy()

employee_sorted["first_rank"] = (
    employee_sorted.groupby("departmentId")["salary"]
    .rank(method="first", ascending=False)
)

top2 = employee["salary"].drop_duplicates().nlargest(2)
second_highest_salary = top2.iloc[1] if len(top2) == 2 else None
```

Notes:
- `rank(method="dense")`: ties share the same rank, and ranks stay consecutive.
- `rank(method="first")`: ties are broken by row order. Sort first if you want a deterministic tiebreaker like alphabetical name.
- `drop_duplicates().nlargest(2)` is a clean way to get the second distinct highest value.
- Use `.iloc[1]`, not `[1]`, when you mean the second element by position.
- After operations like `nlargest`, the Series may keep original index labels, so `[1]` can look for label `1` instead of row position `1`.

## 3. Merge vs Concat

- `merge` = SQL join on keys.
- `concat` = stack or align objects along rows or columns.
- `merge` takes DataFrames as separate arguments.
- `concat` usually takes a list.

```python
department = pd.DataFrame(
    {
        "id": [10, 20, 30],
        "name": ["Analytics", "Economics", "Research"],
    }
)

employee_dep = employee.merge(
    department,
    left_on="departmentId",
    right_on="id",
    how="left",
    suffixes=("_emp", "_dept"),
)

anti_join = employee.merge(
    department,
    left_on="departmentId",
    right_on="id",
    how="left",
    indicator=True,
)
anti_join = anti_join[anti_join["_merge"] == "left_only"][employee.columns]

stacked = pd.concat([employee.head(2), employee.tail(2)], axis=0)
```

Notes:
- Left join in pandas: `left_df.merge(right_df, ..., how="left")`.
- Left anti-join pattern: use `indicator=True`, then keep `_merge == "left_only"`.
- `suffixes=(...)` only affects overlapping column names, not every column.
- If you want to rename every column, use `add_prefix`, `add_suffix`, or `rename` before the merge.
- `pd.concat([df1, df2])` is the common list-taking operation, not `merge`.

## 4. Missing Data, Filtering, and Mutation

Most of the time, row removal is easier with boolean filtering than with `drop`.

```python
people = pd.DataFrame(
    {
        "id": [3, 1, 2, 4],
        "email": ["a@example.com", "a@example.com", "b@example.com", None],
        "salary": [80, 120, 95, np.nan],
    }
)

filtered = people[people["salary"].notna()]
missing_salary_rows = people[people["salary"].isna()]

people_kept_smallest_id = people.sort_values("id").drop_duplicates(subset="email")

def remove_low_salary_inplace(df):
    df.drop(df.index[df["salary"] < 100], inplace=True)

people_copy = people.copy()
remove_low_salary_inplace(people_copy)
```

Notes:
- `df[condition]` or `df.loc[condition]` filters rows and returns a new object.
- `df.drop(indexes, inplace=True)` mutates the original DataFrame object.
- `.loc` helps select rows or columns or assign values. It does not delete rows by itself.
- `isna()` and `notna()` are the standard missing-value checks.
- Pattern to keep the smallest `id` per duplicate email:
  - `sort_values("id")`
  - `drop_duplicates(subset="email")`
  Because `drop_duplicates` keeps the first occurrence by default.

## 5. Reshaping: `melt` and `pivot`

This is the pandas equivalent of going between wide and long table shapes.

```python
products = pd.DataFrame(
    {
        "product_id": [0, 1],
        "product_name": ["product_a", "product_b"],
        "store1": [95, 70],
        "store2": [100, None],
        "store3": [105, 80],
    }
)

products_melted = products.melt(
    id_vars=["product_id", "product_name"],
    value_vars=["store1", "store2", "store3"],
    var_name="store",
    value_name="price",
)

products_melted = products_melted[products_melted["price"].notna()].reset_index(drop=True)

products_wide = (
    products_melted
    .pivot(index=["product_id", "product_name"], columns="store", values="price")
    .reset_index()
    .rename_axis(columns=None)
)
```

Notes:
- `melt` is for wide to long.
- `pivot` is for long to wide.
- In `melt`, `var_name` stores the old column names and `value_name` stores the cell contents.
- If you omit `value_vars`, pandas uses every column not listed in `id_vars`.
- `pivot` requires unique combinations of index and column pairs. If duplicates exist, use `pivot_table` with an aggregation.
- `reset_index()` after `pivot` gives you a fresh integer index. If you care about restoring the exact original index later, save it before melting.

## 6. Quick Reference

Ranking and nth values:
- `s.drop_duplicates().nlargest(2)`
- `groupby(col)[target].rank(method="dense", ascending=False)`
- `groupby(col)[target].rank(method="first", ascending=False)`

Merge and join patterns:
- `df1.merge(df2, on="key", how="left")`
- `df1.merge(df2, ..., indicator=True)` then `_merge == "left_only"` for anti-join
- `pd.concat([df1, df2], axis=0)` for stacking

Filtering and missing data:
- `df[df["col"] >= value]`
- `df["col"].isna()` and `df["col"].notna()`
- `df.drop(df.index[condition], inplace=True)` if you truly want to mutate the passed object

Reshaping:
- `df.melt(id_vars=[...], var_name="...", value_name="...")`
- `df.pivot(index=..., columns=..., values=...)`
- `df.pivot_table(...)` when duplicates require aggregation

Indexing reminders:
- `series.iloc[1]` = second element by position
- `series[1]` may be label-based, so be careful after sorting or `nlargest`

Interview style reminders:
- Prefer readable transformations over clever but fragile ones.
- If ties matter, say how you handle them.
- If mutation matters, be explicit about whether you are editing in place or returning a new object.
