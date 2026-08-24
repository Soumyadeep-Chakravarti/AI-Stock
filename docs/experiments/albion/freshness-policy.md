# Freshness Policy Study

The policy matrices used a 50-item Asia snapshot across six cities and quality 1.

## Quote Age

With timestamp skew fixed at 30 minutes:

```text
Max age   >=2 usable   All 6   Median coverage   Opportunities
2h             0         0          0%                 0
6h            17         0          0%                27
12h           25         0         25%                42
24h           27         3         33%                43
48h           27         3         33%                43
```

Coverage plateaued at 24 hours for this snapshot. Increasing the limit to 48 hours added neither usable coverage nor qualifying opportunities. This supports a provisional 24-hour Asia default, not a universal constant.

## Timestamp Skew

With quote age fixed at 24 hours:

```text
Skew       Potential pairs   Opportunities
30m                 507             43
1h                  507             47
2h                  507             53
6h                  507             62
unlimited           507             91
```

Potential pairs stayed fixed because skew does not change source-side coverage. It changes temporal confidence in a candidate spread.

## Return Versus Skew

A later 24-hour snapshot with no skew limit produced this gross-return distribution:

```text
Skew bin  Opportunities  Average gross return  Maximum gross return
<=30m             43              8.34%                39.53%
30m-1h             4             11.59%                13.07%
1h-2h              6              6.27%                10.71%
2h-6h              9              9.83%                31.58%
>6h               29             13.04%                33.33%
```

Large apparent returns do not occur only at high skew: the low-skew group included a 39.53% gross return. Skew is therefore a confidence policy, not proof that a candidate is invalid. Deterministic Albion market costs are the next economics layer to evaluate before treating any gross candidate as executable.
