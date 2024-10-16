SELECT Rentals.Name, Items.Item, Items.Type
FROM Items, Rentals
WHERE Items.Type = "Toy"
AND Items.Item = Rentals.Item
