import pandas as pd

# Load both files
df1 = pd.read_csv('archive/phase1/clause_mates_phase1_export.csv')
df2 = pd.read_csv('clause_mates_phase2_export.csv')

print('Phase 1 columns:', len(df1.columns))
print('Phase 2 columns:', len(df2.columns))
print()

print('Column order comparison:')
p1_cols = list(df1.columns)
p2_cols = list(df2.columns)

for i, (c1, c2) in enumerate(zip(p1_cols, p2_cols)):
    if c1 != c2:
        print(f'{i:2d}: {c1:35s} | {c2}  <- DIFFERENT')
    else:
        print(f'{i:2d}: {c1:35s} | {c2}')

print('\nColumns in Phase 1 but not Phase 2:')
for col in p1_cols:
    if col not in p2_cols:
        print(f'  - {col}')

print('\nColumns in Phase 2 but not Phase 1:')
for col in p2_cols:
    if col not in p1_cols:
        print(f'  - {col}')
