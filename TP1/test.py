from algorithms.utils import print_results

data = [
    ["Strassen", "8x8", 64, 0.00441924123, "n^3"], 
    ["Strassen", "8x8", 64, 0.00441924123, "n^3"], 
    ["Strassen", "8x8", 64, 0.00441924123, "n^3"], 
    ["Conventional", "4x4", 24, 0.00441924123, "n^3"], 
    ["Conventional", "4x4", 32, 0.543254325, "1"], 
    ["Conventional", "4x4", 32, 0.4231432155, "1"], 
    ["Conventional", "4x4", 32, 0.1432213231, "1"]
]

print_results(data)