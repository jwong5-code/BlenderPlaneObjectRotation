import matplotlib.pyplot as plt
from math import sin, cos, radians
import sys
'''
Student Author Name: Joshua Wong
Project 2
Fall 2022
COMP 313: Computer Graphics
Professor Schiffer
'''

# Holds the coord values
octa_x = []
octa_y = []
octa_z = []
real = []

# Holds the coordinate values in point vector lists.
octa_points = []

# Holds the enumerated vertices, but after decrementing to make them zero-based.
octa_f = []

rotd_x_coords = []
rotd_y_coords = []
rotd_z_coords = []
rotd_sequence_coords = []

def importObj():

    # Import the OBJ
    file = open('Triangular.obj')

    # Fills the list to become 2d matrices (list of lists) of point vectors and coord lists
    list_of_lines = file.readlines()
    for line in list_of_lines:
        if line[0] == 'v':
            #print(line)
            line_v = line.strip('v \n')
            #print(line_v)
            pnt_vect = line_v.split(' ')

            for index, str in enumerate(pnt_vect):
                pnt_vect[index] = float(str)

            print('pnt_vect', pnt_vect)
            octa_points.append(pnt_vect)
            octa_x.append(pnt_vect[0])
            octa_y.append(pnt_vect[1])
            octa_z.append(pnt_vect[2])

        # Creates the face list
        if line[0] == 'f':

            line_f = line.strip('f \n')
            face = line_f.split(' ')
            for index, str_num in enumerate(face):
                face[index] = int(str_num) - 1
            print(face)
            octa_f.append(face)

    '''
    print('octa_x')
    print(octa_x)
    print('octa_y')
    print(octa_y)
    print('octa_z')
    print(octa_z)
    '''
    print('octa_f')
    print(octa_f)
    print('octa_points')
    print(octa_points)

    pass

def rotx(center_vector, point_vector, angle):

    angle = radians(angle)

    rotx_mat = [
                [1,          0,           0],
                [0, cos(angle), -sin(angle)],
                [0, sin(angle), cos(angle) ]
              ]

    xprod = rotx_mat[0][0] * point_vector[0] + rotx_mat[0][1] * point_vector[1] + rotx_mat[0][2] * point_vector[2]
    yprod = rotx_mat[1][0] * point_vector[0] + rotx_mat[1][1] * point_vector[1] + rotx_mat[1][2] * point_vector[2]
    zprod = rotx_mat[2][0] * point_vector[0] + rotx_mat[2][1] * point_vector[1] + rotx_mat[2][2] * point_vector[2]

    xg = xprod + center_vector[0]
    yg = yprod + center_vector[1]
    zg = zprod + center_vector[2]

    return [xg, yg, zg]


def roty(center_vector, point_vector, angle):

    angle = radians(angle)

    roty_mat = [
                [ cos(angle), 0, sin(angle)],
                [0,           1,          0],
                [-sin(angle), 0, cos(angle)]
               ]

    xprod = roty_mat[0][0] * point_vector[0] + roty_mat[0][1] * point_vector[1] + roty_mat[0][2] * point_vector[2]
    yprod = roty_mat[1][0] * point_vector[0] + roty_mat[1][1] * point_vector[1] + roty_mat[1][2] * point_vector[2]
    zprod = roty_mat[2][0] * point_vector[0] + roty_mat[2][1] * point_vector[1] + roty_mat[2][2] * point_vector[2]

    xg = xprod + center_vector[0]
    yg = yprod + center_vector[1]
    zg = zprod + center_vector[2]

    return [xg, yg, zg]

def rotz(center_vector, point_vector, angle):

    angle = radians(angle)

    rotz_mat = [
                [cos(angle), -sin(angle),  0],
                [sin(angle),  cos(angle),  0],
                [          0,           0, 1]
               ]

    xprod = rotz_mat[0][0] * point_vector[0] + rotz_mat[0][1] * point_vector[1] + rotz_mat[0][2] * point_vector[2]
    yprod = rotz_mat[1][0] * point_vector[0] + rotz_mat[1][1] * point_vector[1] + rotz_mat[1][2] * point_vector[2]
    zprod = rotz_mat[2][0] * point_vector[0] + rotz_mat[2][1] * point_vector[1] + rotz_mat[2][2] * point_vector[2]

    xg = xprod + center_vector[0]
    yg = yprod + center_vector[1]
    zg = zprod + center_vector[2]

    return [xg, yg, zg]

def plot_shape(center_vector, x_angle, y_angle, z_angle, rot_seq):

    # GRID SETUP FOR SEQUENTIAL COMBINED ROTATIONS
    figure, axes = plt.subplots()
    axes.set_aspect(1)
    plt.axis([-20, 20, -20, 20])
    plt.axis('on')
    plt.grid(True)
    x_coords = octa_x
    y_coords = octa_y
    z_coords = octa_z

    for vert_num in range(0, len(x_coords)):
        rotd_x_coords.append(rotx(center_vector, [x_coords[vert_num], y_coords[vert_num], z_coords[vert_num]], x_angle))
        rotd_y_coords.append(roty(center_vector, [x_coords[vert_num], y_coords[vert_num], z_coords[vert_num]], y_angle))
        rotd_z_coords.append(rotz(center_vector, [x_coords[vert_num], y_coords[vert_num], z_coords[vert_num]], z_angle))

    global rotd_sequence_coords
    if rot_seq == 'RxRyRz':
        rotd_sequence_coords = rotd_x_coords

        for vert_num in range(0, len(x_coords)):
            rotd_sequence_coords[vert_num] = roty(center_vector,
                                                  [rotd_sequence_coords[vert_num][0], rotd_sequence_coords[vert_num][1],
                                                   rotd_sequence_coords[vert_num][2]], y_angle)
            rotd_sequence_coords[vert_num] = rotz(center_vector,
                                                  [rotd_sequence_coords[vert_num][0], rotd_sequence_coords[vert_num][1],
                                                   rotd_sequence_coords[vert_num][2]], z_angle)



    elif rot_seq == 'RyRxRz':
        rotd_sequence_coords = rotd_y_coords
        for vert_num in range(0, len(x_coords)):
            rotd_sequence_coords[vert_num] = rotx(center_vector,
                                                  [rotd_sequence_coords[vert_num][0], rotd_sequence_coords[vert_num][1],
                                                   rotd_sequence_coords[vert_num][2]], x_angle)
            rotd_sequence_coords[vert_num] = rotz(center_vector,
                                                  [rotd_sequence_coords[vert_num][0], rotd_sequence_coords[vert_num][1],
                                                   rotd_sequence_coords[vert_num][2]], z_angle)

    elif rot_seq == 'RzRyRx':
        rotd_sequence_coords = rotd_z_coords
        for vert_num in range(0, len(x_coords)):
            rotd_sequence_coords[vert_num] = roty(center_vector,
                                                  [rotd_sequence_coords[vert_num][0], rotd_sequence_coords[vert_num][1],
                                                   rotd_sequence_coords[vert_num][2]], y_angle)
            rotd_sequence_coords[vert_num] = rotx(center_vector,
                                                  [rotd_sequence_coords[vert_num][0], rotd_sequence_coords[vert_num][1],
                                                   rotd_sequence_coords[vert_num][2]], x_angle)

    elif rot_seq == 'RzRxRy':
        rotd_sequence_coords = rotd_z_coords
        for vert_num in range(0, len(x_coords)):
            rotd_sequence_coords[vert_num] = rotx(center_vector,
                                                  [rotd_sequence_coords[vert_num][0], rotd_sequence_coords[vert_num][1],
                                                   rotd_sequence_coords[vert_num][2]], x_angle)
            rotd_sequence_coords[vert_num] = roty(center_vector,
                                                  [rotd_sequence_coords[vert_num][0], rotd_sequence_coords[vert_num][1],
                                                   rotd_sequence_coords[vert_num][2]], y_angle)

    elif rot_seq == 'RxRzRy':
        rotd_sequence_coords = rotd_x_coords
        for vert_num in range(0, len(x_coords)):
            rotd_sequence_coords[vert_num] = rotz(center_vector,
                                                  [rotd_sequence_coords[vert_num][0], rotd_sequence_coords[vert_num][1],
                                                   rotd_sequence_coords[vert_num][2]], z_angle)
            rotd_sequence_coords[vert_num] = roty(center_vector,
                                                  [rotd_sequence_coords[vert_num][0], rotd_sequence_coords[vert_num][1],
                                                   rotd_sequence_coords[vert_num][2]], y_angle)

    elif rot_seq == 'RyRzRx':
        rotd_sequence_coords = rotd_y_coords
        for vert_num in range(0, len(x_coords)):
            rotd_sequence_coords[vert_num] = rotz(center_vector,
                                                  [rotd_sequence_coords[vert_num][0], rotd_sequence_coords[vert_num][1],
                                                   rotd_sequence_coords[vert_num][2]], z_angle)
            rotd_sequence_coords[vert_num] = rotx(center_vector,
                                                  [rotd_sequence_coords[vert_num][0], rotd_sequence_coords[vert_num][1],
                                                   rotd_sequence_coords[vert_num][2]], x_angle)

    else:
        print('The rotation sequence is invalid.')
        sys.exit()



    # Loop to plot all tris
    for face in octa_f:
        # plt.plot([0,1],[0,1], color='k')
        # vertex 0 to 1
        plt.plot([ rotd_sequence_coords[  face[0] ] [0], rotd_sequence_coords[ face[1]] [0] ],
                 [ rotd_sequence_coords[  face[0] ] [1], rotd_sequence_coords[ face[1]] [1] ],
                 color='k')
        # vertex 1 to 2
        plt.plot([ rotd_sequence_coords[  face[1] ] [0], rotd_sequence_coords[ face[2]] [0] ],
                 [ rotd_sequence_coords[  face[1] ] [1], rotd_sequence_coords[ face[2]] [1] ],
                 color='k')
        # vertex 2 to 0
        plt.plot([ rotd_sequence_coords[  face[2] ] [0], rotd_sequence_coords[ face[0]] [0] ],
                 [ rotd_sequence_coords[  face[2] ] [1], rotd_sequence_coords[ face[0]] [1] ],
                 color='k')

        pass

    plt.show()
    pass


def main():
    importObj()
    plot_shape([0,0,0], 90, 75, 145, 'RyRzRx')
    pass

main()