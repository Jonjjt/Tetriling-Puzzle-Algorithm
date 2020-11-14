# ####################################################
# DE2-COM2 Computing 2
# Individual project
#
# Title: MAIN
# Author: Jonathan Tang
# ####################################################

import utils  # it might be helpful to use 'utils.py' 
import numpy as np
from copy import deepcopy # copy 'target' to avoid modifying it

def Tetris(target):
    def count_neighbours(target, r, c): #count neighbours of each occupied square
        neighbour_count = 0 #initialise neighbour count
        try:
            if target[r+1][c] == 1:
                neighbour_count += 1
        except IndexError:
            pass
        try:
            if target[r-1][c] == 1:
                neighbour_count += 1
        except IndexError:
            pass
        try:    
            if target[r][c+1] == 1:
                neighbour_count += 1
        except IndexError:
            pass
        try:    
            if target[r][c-1] == 1:
                neighbour_count += 1
        except IndexError:
            pass
        neighbour_count_matrix[r][c] = neighbour_count
        return neighbour_count_matrix[r][c]

    def check_piece_validity(target, r, c): #check for pieces that fit in the target area
        valid_pieces = [] #create list for valid pieces
        for shape_id in range(4, 20): #check each of 16 shapes with ids 4-19
            shape = utils.generate_shape(shape_id) #define shape from utils as a linear transformation using 4 coordinate pairs
            piece = [[y + r, x + c] for [y, x] in shape] #define piece as 4 coordinate pairs
            #check piece validity
            valid = False #set default piece validity
            piece_neighbour_counts = [] #create list for neighbour count for each occupied square of a piece
            for j, k in piece: #for each coordinate
                if j < 0 or j >= height or k < 0 or k >= width: #no negative numbers otherwise will look from end of list
                    break
                else:
                    if target[j][k] == 1: #check if the coordinate square is occupied
                        piece_neighbour_counts.append(neighbour_count_matrix[j][k])
                        if piece.index([j, k]) == 3:
                            valid = True
                    else:
                        break #one of the squares is not occupied, go to next piece
            if valid:
                valid_pieces.append([piece, shape_id, sum(piece_neighbour_counts)]) #store valid shape ids
        sorted(valid_pieces, key=lambda piece: piece[2])
        return valid_pieces

    def place_piece(S, loop, neighbour_count_matrix, best_piece, best_piece_id):
        # best_piece_index = neighbour_count_list.index(min(neighbour_count_list))
        # best_piece, best_piece_id = valid_pieces[best_piece_index][0], valid_pieces[best_piece_index][1]
        for [j, k] in best_piece: #for each square in best piece
            S[j][k] = (best_piece_id, count) #enter piece id and count
            loop[j][k] = 0
            neighbour_count_matrix[j][k] = 0
            try:
                if neighbour_count_matrix[j+1][k] != 0:
                    neighbour_count_matrix[j+1][k] -= 1
            except IndexError:
                pass
            try:
                if neighbour_count_matrix[j-1][k] != 0:
                    neighbour_count_matrix[j-1][k] -= 1
            except IndexError:
                pass
            try:    
                if neighbour_count_matrix[j][k+1] != 0:
                    neighbour_count_matrix[j][k+1] -= 1
            except IndexError:
                pass
            try:    
                if neighbour_count_matrix[j][k-1] != 0:
                    neighbour_count_matrix[j][k-1] -= 1
            except IndexError:
                pass
        return S, loop, neighbour_count_matrix

    def unplace(S, loop, neighbour_count_matrix, best_piece, best_piece_id, target):
        for [j, k] in best_piece: #for each square in best piece
            S[j][k] = (0, 0) #revert piece id and count
            loop[j][k] = 1
            neighbour_count_matrix[j][k] = count_neighbours(target, j, k)
        return S, loop, neighbour_count_matrix

    def find_empty(loop):
        for r in range(height): #iterate through each row
            for c in range(width): #iterate through each column
                if loop[r][c] == 1:
                    return r, c
        return None
    def solve(loop, target):
        global count
        try:
            r, c = find_empty(loop)
        except TypeError:
            return True
        valid_pieces = check_piece_validity(loop, r, c) #check for valid pieces
        if len(valid_pieces) > 0: #check if there are valid pieces
            for best_piece, best_piece_id, score in valid_pieces:
                place_piece(S, loop, neighbour_count_matrix, best_piece, best_piece_id) #place piece
                count += 1
                if solve(loop, target): #if the next iteration places a piece
                    return True
                unplace(S, loop, neighbour_count_matrix, best_piece, best_piece_id, target) #unplace piece and revert neighbour counts
                count -= 1
        return False
    
    #backtracking algorithm, no errors in each row?
    height, width = len(target), len(target[0]) #define height and width of the target area
    S = [[(0, 0) for c in range(width)] for r in range(height)] #create an empty solution matrix
    loop = deepcopy(target) #create a copy of the target that updates with the solution
    neighbour_count_matrix = deepcopy(target) #create a copy of the target that stores the neighbour count for each occupied square
    #count neighbours of each occupied square in target
    for r in range(height): #iterate through each row
            for c in range(width): #iterate through each column
                if target[r][c] == 1:
                    count_neighbours(target, r, c)
    global count
    count = 1
    solve(loop, target)
    return S