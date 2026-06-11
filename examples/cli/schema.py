from typewall import w

User = w.object({"name": w.str().min(2), "age": w.int().min(0)})
