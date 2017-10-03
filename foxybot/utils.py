

async def find(predicate, seq):
    for element in seq:
        if predicate(element):
            return element
    return None