# Albion Experiment Methodology

Live experiments use the Albion Online Data Project Asia/East REST host:

```text
https://east.albion-online-data.com
```

The initial city set is Bridgewatch, Caerleon, Fort Sterling, Lymhurst, Martlock, and Thetford. Experiments request quality 1 unless stated otherwise.

Policy comparisons use one fetched snapshot per matrix. The same observations are replayed through each policy so changing live market data does not distort the comparison.

All current results are gross only. No transaction fees, listing fees, travel cost, transport capacity, route risk, or execution behavior is included.

Live requests are engineering experiments, not CI tests. Unit tests use local servers, static JSON fixtures, and fake clients.
