import numpy as np


def random_angle_with_normal_distribution():
    rand = abs(np.random.normal())
    if rand > 1:
        rand = 1
    return rand * np.pi / 2


def rotate_matrix(angle):
    return np.array([
        np.sqrt(1 - np.power(np.sin(angle), 2)), -np.sin(angle),
        np.sin(angle), np.sqrt(1 - np.power(np.sin(angle), 2))
    ]).reshape((2, 2))


def main():
    angle = random_angle_with_normal_distribution()
    print(angle / np.pi * 2)
    print(rotate_matrix(angle))
    print(rotate_matrix(angle) @ np.array([1, 0]))


if __name__ == "__main__":
    main()
