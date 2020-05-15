from random import *

num_steps = 1000
num_dimensions = 3
init_location = 0
end_locations = [init_location for i in range(num_dimensions)]
print("Initial locations: ", end_locations)

# Iterate through the number of steps
for i in range(0, num_steps):
    # For ever step, iterate through each dimension
    for j in range(0, num_dimensions):

        r = randint(0, 1)
        if (r == 0):
            end_locations[j] -= 1
        elif (r == 1):
            end_locations[j] += 1
        # print("step(i) =",i , " \tdimension(j) =", j, " \tr =", r, " \tlocation =", end_locations[j], " \tall locations =", end_locations)

print("Steps taken: ", num_steps, "\nEnd locations: ", end_locations)
