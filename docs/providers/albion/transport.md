# Albion Transport Economics

The first transport layer is deliberately caller-configured. It does not claim that a city pair has one fixed travel time or capacity.

`TransportInputs` requires:

```text
quantity
transport_capacity
trip_time
```

`quantity` is the number of units to trade. `transport_capacity` is the maximum units carried in one trip. `trip_time` is one complete economic cycle, normally a round trip including execution time as measured by the caller.

All inputs must be greater than zero.

```text
units_per_trip = min(quantity, transport_capacity)
trip_count     = ceil(quantity / transport_capacity)
profit_per_trip = net_profit_per_unit * units_per_trip
total_profit    = net_profit_per_unit * quantity
profit_per_hour = profit_per_trip / trip_time
```

`TransportAdjustedOpportunity` preserves the underlying net opportunity and reports the requested quantity, capacity-limited trip size, trip count, per-trip profit, total profit, and hourly profit.

No static city-route configuration is included. Cycle time depends on mount, loadout, route, player behavior, return-trip assumptions, and eventually risk policy. A later empirical `RouteProfile` should be based on recorded runs rather than invented constants.

Transport risk, loss probability, route danger, capacity by item weight, and slippage remain outside v1.
