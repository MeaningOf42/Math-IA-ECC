# import dependencies
import lib
import matplotlib.pyplot as plt

# Create FiniteFeild of integers mod 41 and use that to create the eliptic curve
# y**2 = x**3 - 3x + 15 mod 41
F = lib.FiniteFeild(41)
C = lib.Curve(F, -3,15, 6,7, 33)

# Generate all possible integer points in form (0 <= x < 41, 0 <= y < 41)
# Proceed to filter for points that lie on the curve
points = [lib.Point(C, i//F.size, i%F.size) for i in range(F.size**2)]
points = list(filter(C.isOnCurve, points))

# print the points and the order of the curve to the screen.
print(list(map(str, points)))
print(len(points))

# Display the points of the eliptic curve as a scatter plot.
plt.plot([point.x for point in points], [point.y for point in points], "bo")
plt.axis([0, F.size, 0, F.size])
plt.show()
