# Initial Live Scan

The first live scan queried `T4_BAG`, quality 1, across six Asia markets with:

```text
max quote age: 2 hours
max timestamp skew: 30 minutes
```

No fresh gross opportunity qualified.

The diagnostic output explained the result:

- Fort Sterling had fresh bid and ask sides.
- Lymhurst had fresh bid and ask sides.
- Bridgewatch quotes were approximately 11 hours old.
- Martlock had a stale ask and no bid.
- Caerleon and Thetford had no sides.

Among fresh markets, no sell bid exceeded another fresh market's ask. This was a valid result, not a detector failure. It established quote coverage and freshness as the first practical constraint.
