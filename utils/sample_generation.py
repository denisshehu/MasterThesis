from utils.functions import *


def sample_from_sphere(n, intrinsic_dimension, r, seed=None, ambient_dimension=None):
    np.random.seed(seed)

    points = np.random.normal(size=(n, (intrinsic_dimension + 1)))
    for point in points:
        norm = np.linalg.norm(point)
        point *= r / norm

    points = add_extra_dimensions(points, ambient_dimension)
    return points


def sample_from_ball(n, intrinsic_dimension, r, seed=None, ambient_dimension=None):
    points = sample_from_sphere(n, ((intrinsic_dimension - 1) + 2), r, seed)
    points = points[:, :-2]
    points = add_extra_dimensions(points, ambient_dimension)
    return points


def sample_from_intersecting_cones(n, intrinsic_dimension, r, angle_in_degrees, seed=None, ambient_dimension=None):
    np.random.seed(seed)

    axis = np.zeros(shape=intrinsic_dimension)
    axis[-1] = 1

    points = np.empty(shape=(0, intrinsic_dimension))
    threshold = math.cos(math.radians(angle_in_degrees))

    while points.shape[0] < n:
        seed_ = np.random.randint(np.iinfo(np.int32).max)
        points_ = sample_from_ball(n, intrinsic_dimension, r, seed_)

        for point in points_:
            cosine_similarity = np.dot(point, axis) / np.linalg.norm(point)
            if abs(cosine_similarity) >= threshold:
                points = np.row_stack((points, point))

    points = points[:n, :]
    points = add_extra_dimensions(points, ambient_dimension)
    return points


def sample_from_intersecting_planes(n1, r1, n2, r2, intrinsic_dimension, seed1=None, seed2=None,
                                    ambient_dimension=None):
    plane1 = sample_from_ball(n1, intrinsic_dimension, r1, seed1, ambient_dimension)
    plane2 = sample_from_ball(n2, intrinsic_dimension, r2, seed2, (ambient_dimension - 1))
    plane2 = np.hstack((np.zeros(shape=(plane2.shape[0], 1)), plane2))

    points = np.row_stack((plane1, plane2))
    return points


def sample_from_annulus(n, intrinsic_dimension, max_r, min_r, seed=None, ambient_dimension=None):
    np.random.seed(seed)

    points = np.empty(shape=(0, intrinsic_dimension))

    while points.shape[0] < n:
        seed_ = np.random.randint(np.iinfo(np.int32).max)
        points_ = sample_from_ball(n, intrinsic_dimension, max_r, seed_)

        for point in points_:
            norm = np.linalg.norm(point)
            if norm >= min_r:
                points = np.row_stack((points, point))

    points = points[:n, :]
    points = add_extra_dimensions(points, ambient_dimension)
    return points


def sample_from_intersecting_spheres(n1, intrinsic_dimension1, r1, n2, intrinsic_dimension2, r2, ambient_dimension,
                                     proportion=1, seed1=None, seed2=None):
    sphere1 = sample_from_sphere(n1, intrinsic_dimension1, r1, seed1, ambient_dimension)
    sphere2 = sample_from_sphere(n2, intrinsic_dimension2, r2, seed2, ambient_dimension)

    for point in sphere1:
        point[0] -= proportion * r1
    for point in sphere2:
        point[0] += proportion * r2

    points = np.row_stack((sphere1, sphere2))
    return points


def figure(n1, s1, r1, seed1, n2, s2, r2, seed2, proportion):
    intrinsic_dimension = 2
    annulus1 = sample_from_annulus(n1, intrinsic_dimension, s1, r1, seed1)
    annulus2 = sample_from_annulus(n2, intrinsic_dimension, s2, r2, seed2)

    for point in annulus2:
        point[1] += proportion * (s1 + s2)

    points = np.row_stack((annulus1, annulus2))
    return points
