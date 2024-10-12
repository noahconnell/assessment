SELECT Rentals.Name, Items.Item
FROM Items, Rentals
WHERE Items.Item = Rentals.Item
