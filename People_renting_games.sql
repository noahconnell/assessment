SELECT Rentals.Name, Items.Item, Items.Type
FROM Items, Rentals
WHERE Items.Type = "Game"
AND Items.Item = Rentals.Item
