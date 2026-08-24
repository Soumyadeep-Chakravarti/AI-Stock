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
total_transport_time = trip_count * trip_time
full_trip_profit = net_profit_per_unit * units_per_trip
full_trip_profit_per_hour = full_trip_profit / trip_time
total_profit = net_profit_per_unit * quantity
realization_profit_per_hour = total_profit / total_transport_time
```

`full_trip_profit_per_hour` describes a fully loaded cycle. `realization_profit_per_hour` describes completing the requested quantity, including the time spent on a partial final trip. They are equal only when quantity divides evenly by capacity.

`TransportAdjustedOpportunity` preserves the underlying net opportunity and reports both rates, requested quantity, capacity-limited trip size, trip count, total transport time, and total profit.

No static city-route configuration is included. Cycle time depends on mount, loadout, route, player behavior, return-trip assumptions, and eventually risk policy. A later empirical `RouteProfile` should be based on recorded runs rather than invented constants.

Transport risk, loss probability, route danger, capacity by item weight, and slippage remain outside v1.
