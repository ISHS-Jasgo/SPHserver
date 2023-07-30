import math
import numpy as np
from sklearn import neighbors
import rotation as rt

PARTICLE_MASS = 70
ISOTROPIC_EXPONENT = 20
BASE_DENSITY = 1
SMOOTHING_LENGTH = 5
DYNAMIC_VISCOSITY = 0.1
DAMPING_COEFFICIENT = - 0.9
CONSTANT_FORCE = np.array([[0.0, -9.8]])

TIME_STEP_LENGTH = 0.01
N_TIME_STEPS = 5

# (315 M) / (64 π L⁹)
# NORMALIZATION_DENSITY = (
#         (315 * PARTICLE_MASS) / (64 * np.pi * SMOOTHING_LENGTH ** 9)
# )
NORMALIZATION_DENSITY = 4 * PARTICLE_MASS / (np.pi * SMOOTHING_LENGTH ** 8)
# (− (45 M) / (π L⁶))
# NORMALIZATION_PRESSURE_FORCE = (
#         -(45 * PARTICLE_MASS) / (np.pi * SMOOTHING_LENGTH ** 6)
# )
NORMALIZATION_PRESSURE_FORCE = (-10) * PARTICLE_MASS / (np.pi * SMOOTHING_LENGTH ** 5)
# (45 μ M) / (π L⁶)
# NORMALIZATION_VISCOUS_FORCE = (
#         (45 * DYNAMIC_VISCOSITY * PARTICLE_MASS) / (np.pi * SMOOTHING_LENGTH ** 6)
# )
NORMALIZATION_VISCOUS_FORCE = 40 * DYNAMIC_VISCOSITY * PARTICLE_MASS / (np.pi * SMOOTHING_LENGTH ** 5)


def SPH(MAX_PARTICLES=1000, DOMAIN_WIDTH=40, DOMAIN_HEIGHT=80):

    DOMAIN_X_LIM = np.array([
        SMOOTHING_LENGTH,
        DOMAIN_WIDTH - SMOOTHING_LENGTH
    ])
    DOMAIN_Y_LIM = np.array([
        SMOOTHING_LENGTH,
        DOMAIN_HEIGHT - SMOOTHING_LENGTH
    ])

    n_particles = 0
    forceList = []
    result_force = []

    positions = np.zeros((n_particles, 2))
    velocities = np.zeros_like(positions)

    for iter in range(N_TIME_STEPS):
        if n_particles < MAX_PARTICLES:
            # new_positions = np.array([
            #     [DOMAIN_WIDTH/6 + np.random.rand(), DOMAIN_Y_LIM[1]],
            #     [DOMAIN_WIDTH/6*2 + np.random.rand(), DOMAIN_Y_LIM[1]],
            #     [DOMAIN_WIDTH/6*3 + np.random.rand(), DOMAIN_Y_LIM[1]],
            #     [DOMAIN_WIDTH/6*4 + np.random.rand(), DOMAIN_Y_LIM[1]],
            #     [DOMAIN_WIDTH/6*5 + np.random.rand(), DOMAIN_Y_LIM[1]],
            # ])
            n_positions = []
            for _ in range(MAX_PARTICLES):
                # random position between DOMAIN_X_LIM[0] and DOMAIN_X_LIM[1]
                x = np.random.rand() * (DOMAIN_X_LIM[1] - DOMAIN_X_LIM[0]) + DOMAIN_X_LIM[0]
                # random position between DOMAIN_Y_LIM[0] and DOMAIN_Y_LIM[1]
                y = np.random.rand() * (DOMAIN_Y_LIM[1] - DOMAIN_Y_LIM[0]) + DOMAIN_Y_LIM[0]
                n_positions.append([x, y])
            new_positions = np.array(n_positions)
            # create new_velocities with shape (n_particles, 2)
            new_velocities = np.zeros_like(new_positions)
            # set y velocity of new_velocities to 5
            # new_velocities[:, 1] = -10
            # set x velocity of new_velocities to random value between -1 and 1
            # new_velocities[:, 0] = np.random.rand(1000) * 2 - 1

            n_particles += MAX_PARTICLES

            positions = np.concatenate((positions, new_positions), axis=0)
            velocities = np.concatenate((velocities, new_velocities), axis=0)
        try:
            neighbor_ids, distances = neighbors.KDTree(
                positions,
            ).query_radius(
                positions,
                SMOOTHING_LENGTH,
                return_distance=True,
                sort_results=True,
            )
        except ValueError:
            continue

        densities = np.zeros(n_particles)

        for i in range(n_particles):
            for j_in_list, j in enumerate(neighbor_ids[i]):
                densities[i] += NORMALIZATION_DENSITY * (
                        SMOOTHING_LENGTH ** 2 - distances[i][j_in_list] ** 2
                ) ** 3

        pressures = ISOTROPIC_EXPONENT * (densities - BASE_DENSITY)

        forces = np.zeros_like(positions)

        # clear elements
        neighbor_ids = [np.delete(x, 0) for x in neighbor_ids]
        distances = [np.delete(x, 0) for x in distances]

        for i in range(n_particles):
            for j_in_list, j in enumerate(neighbor_ids[i]):
                forces[i] += NORMALIZATION_PRESSURE_FORCE * (
                    - (positions[j] - positions[i])
                ) / distances[i][j_in_list] * (pressures[j] + pressures[i]) / (2 * densities[j]) * (
                                     SMOOTHING_LENGTH - distances[i][j_in_list]) ** 2
                rotate_angle = rt.random_angle_with_normal_distribution()
                forces[i] = rt.rotate_matrix(rotate_angle) @ forces[i]

                forces[i] += NORMALIZATION_VISCOUS_FORCE * (velocities[j] - velocities[i]) / densities[j] * (
                        SMOOTHING_LENGTH - distances[i][j_in_list])
                # forces[i] += CONSTANT_FORCE[0] * densities[i]

        velocities += TIME_STEP_LENGTH * forces / densities[:, np.newaxis]
        positions += TIME_STEP_LENGTH * velocities

        out_of_left_boundary = positions[:, 0] < DOMAIN_X_LIM[0]
        out_of_right_boundary = positions[:, 0] > DOMAIN_X_LIM[1]
        out_of_bottom_boundary = positions[:, 1] < DOMAIN_Y_LIM[0]
        out_of_top_boundary = positions[:, 1] > DOMAIN_Y_LIM[1]

        velocities[out_of_left_boundary, 0] *= DAMPING_COEFFICIENT
        positions[out_of_left_boundary, 0] = DOMAIN_X_LIM[0]

        velocities[out_of_right_boundary, 0] *= DAMPING_COEFFICIENT
        positions[out_of_right_boundary, 0] = DOMAIN_X_LIM[1]

        velocities[out_of_bottom_boundary, 1] *= DAMPING_COEFFICIENT
        positions[out_of_bottom_boundary, 1] = DOMAIN_Y_LIM[0]

        velocities[out_of_top_boundary, 1] *= DAMPING_COEFFICIENT
        positions[out_of_top_boundary, 1] = DOMAIN_Y_LIM[1]

        for force in forces:
            forceList.append(math.sqrt(force[0] ** 2 + force[1] ** 2))

        print(f"Max force: {np.max(forceList)}")
        result_force.append(np.max(forceList))

    return {
        "force": np.mean(result_force),
    }


def main():
    SPH(1000, 20, 50)


if __name__ == '__main__':
    main()