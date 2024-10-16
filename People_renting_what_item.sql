SELECT Rentals.Name, Rentals.Item, Rentals.Returned_Date
FROM Rentals
WHERE Rentals.Returned_Date IS NULL
