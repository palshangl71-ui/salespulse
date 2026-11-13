
# SALESPULSE - TESTING DOCUMENTATION

## Test Case 1: Normal Valid Order

Input:
Quantity = 2
UnitPrice = 100
UnitCost = 60

Expected Result:
Record should be included.
Revenue = 200
Gross Profit = 80

Actual Result: Passed

## Test Case 2: Zero Quantity

Input:
Quantity = 0

Expected Result:
Record should be excluded.

Actual Result: Passed

## Test Case 3: Negative UnitPrice

Input:
UnitPrice = -100

Expected Result:
Record should be excluded.

Actual Result: Passed

## Test Case 4: Missing ProductName

Input:
ProductName = NULL

Expected Result:
Record should be excluded.

Actual Result: Passed

## Test Case 5: Duplicate OrderID

Input:
Two records with the same OrderID.

Expected Result:
First occurrence retained.
Subsequent duplicate excluded.

Actual Result: Passed

## Test Case 6: UnitCost Greater Than UnitPrice

Input:
UnitPrice = 100
UnitCost = 150
Quantity = 2

Expected Result:
Record should be retained.
Gross Profit = -100.

Actual Result: Passed

## Test Case 7: No Valid Orders

Input:
Empty valid dataset.

Expected Result:
AOV should display N/A.
No division-by-zero error.

Actual Result: Passed
