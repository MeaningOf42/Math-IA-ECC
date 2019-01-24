# import dependencies
import lib

def order(point):
    points = []
    i = 3
    while True:
        newPoint = i * point
        if newPoint == point:
            break
        else:
            points.append(newPoint)
            i+=1
    print([str(p) for p in points], str(newPoint))
    return len(points)

# Create FiniteFeild of integers mod 41 and use that to create the eliptic curve
# y**2 = x**3 - 3x + 15 mod 41
F = lib.FiniteFeild(263)
C = lib.Curve(F, -2,3, 6,7, 33)

# Generate all possible integer points in form (0 <= x < 41, 0 <= y < 41)
# Proceed to filter for points that lie on the curve
points = [lib.Point(C, i//F.size, i%F.size) for i in range(F.size**2)]
points = list(filter(C.isOnCurve, points))

# print the points and the order of the curve to the screen.
print(list(map((lambda p: f"{p}: {order(p)}"), points)))
print(len(points))
