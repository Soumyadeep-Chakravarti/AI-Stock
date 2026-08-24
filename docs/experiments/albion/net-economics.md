# Instant-Execution Net Economics Study

This experiment applied the default Albion instant-execution policy to a 50-item Asia snapshot:

```text
quote age: 24 hours
timestamp skew: 30 minutes
Premium: disabled
market tax: 8% of sale price
setup fee: excluded
transport economics: excluded
```

Results:

```text
Gross candidates: 43
Net-profitable candidates after tax: 14
Average gross return: 8.34%
Average net return among survivors: 7.54%
```

The 8% tax removed 29 gross candidates, confirming that gross spread is insufficient evidence of a viable trade. It did not eliminate all low-skew candidates.

Examples before transport and execution costs:

```text
T6_ORE:   Bridgewatch 751 -> Fort Sterling 883
          tax 70.64, net profit 61.36, net return 8.17%, skew 10m

T4_FIBER: Martlock 86 -> Lymhurst 120
          tax 9.60, net profit 24.40, net return 28.37%, skew 25m

T4_WOOD:  Bridgewatch 72 -> Fort Sterling 100
          tax 8.00, net profit 20.00, net return 27.78%, skew 30m
```

These values preserve exact `Decimal` tax arithmetic. Albion's integer-silver tax rounding remains unverified, so the displayed fractions are analytical values rather than a claim of exact in-game settlement. Transport, travel time, capacity, route risk, slippage, and execution behavior are still excluded.
