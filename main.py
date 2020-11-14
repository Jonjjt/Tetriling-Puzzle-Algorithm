# ####################################################
# DE2-COM2 Computing 2
# Individual project
#
# Title: MAIN
# Author: Jonathan Tang
# ####################################################

import utils
import numpy as np

#the_forbidden_pieces = {1,2,3} #Forbidden shapeIDs
#target, perfect_solution = utils.generate_target(width=10, height=10, density=0.7, forbidden_pieces=the_forbidden_pieces) # NOTE: it is recommended to keep density below 0.8

def Tetris(target):
    #place pieces top to bottom left to right one at a time(greedy algorithm), using number of neighbouring blocks to determine what block to place
    #Analyse target to find number of neighbouring blocks for each tile, use neighbour scores to determine piece placement
    def neighbour_count(target): #target can be initial target or updated area
        #create empty matrix for neighbour count
        C = np.zeros((height, width))
        #start by define length of rows and cols
        #check each coordinate
        for r in range(height):
            for c in range(width):
                #create a default count of neighbouring blocks
                score = 0
                #Find blocks that aren't blank
                if target[r][c] != 0:
                    #check for neighbours within bounds height - 1 and width - 1 and 0
                    if r + 1 <= height - 1:
                        if target[r+1][c] != 0:
                            score += 1
                    if r - 1 >= 0:
                        if target[r-1][c] != 0:
                            score += 1
                    if c + 1 <= width - 1:
                        if target[r][c+1] != 0:
                            score += 1
                    if c - 1 >= 0:
                        if target[r][c-1] != 0:
                            score += 1
                    C[r][c] = score
        return C

    #check for valid pieces
    def check_piece_validity(C):
        #create list for valid pieces
        valid_pieces = []
        #check each of 16 shapes with ids 4-19
        for shape_id in range(4, 20):
            #define shape from utils as a linear transformation using 4 coordinate pairs
            shape = utils.generate_shape(shape_id)
            #define piece as 4 coordinate pairs
            piece = [[y + r, x + c] for [y, x] in shape]
            # check piece validity
            #set default piece validity
            valid = True
            #check validity
            for [i, j] in piece:
                #all values outside bounds are invalid
                if i < 0 or i >= height or j < 0 or j >= width:
                    valid = False
                if valid == True:
                    #if the value is 0 for a given coordinate within a piece it is invalid.
                    if C[i][j] == 0:
                        valid = False
            #store valid shape ids
            if valid == True:
                valid_pieces.append([r, c, shape_id])
        return valid_pieces

    def check_piece_score(C, valid_pieces):
        #score valid pieces based on neighbour count of each block it occupies
        #create dict of placable pieces
        placable = {}
        prev_coord = None
        for n in valid_pieces:
            #create list for neighbour counts
            scoring = []
            shape = utils.generate_shape(n[2]) 
            piece = [[y + n[0], x + n[1]] for [y, x] in shape]
            #find neighbour count values to sum
            for i in piece:
                scoring.append(C[i[0]][i[1]])
            shape_score = sum(scoring)
            #store lowest shape scores based on coordinates
            coord = n[0], n[1]
            if prev_coord != coord: #check if the coordinates are the same
                prev_shape_score = [20]
                if prev_shape_score[0] > shape_score:
                    placable[n[0], n[1]] = [shape_score, n[2]]
                    prev_shape_score = [shape_score, n[2]]
            if prev_coord == coord:
                if prev_shape_score[0] > shape_score:
                    placable[n[0], n[1]] = [shape_score, n[2]]
                    prev_shape_score = [shape_score, n[2]]
            prev_coord = coord
        return placable
    
    #create a function to update immediate neighbours to placed pieces in order to not run neighbour_count through every coordinate after every piece is placed
    def update_neighbour(C, r, c):
        C[r][c] = 0
        if r + 1 <= height - 1:
            if C[r+1][c] != 0:
                C[r+1][c] -= 1
        if r - 1 >= 0:
            if C[r-1][c] != 0:
                C[r-1][c] -= 1
        if c + 1 <= width - 1:
            if C[r][c+1] != 0:
                C[r][c+1] -= 1
        if c - 1 >= 0:
            if C[r][c-1] != 0:
                C[r][c-1] -= 1
        return C
    
    #create a function to place pieces into the solution matrix
    def place_piece(C, placable, S, count):
        for n in placable: #where n is the coordinate pair of a placable piece
            shape = utils.generate_shape(placable[n][1]) 
            piece = [[y + n[0], x + n[1]] for [y, x] in shape]
            for i in piece:
                S[i[0]][i[1]] = (placable[n][1], count)
                C = update_neighbour(C, i[0], i[1])
        return S, C
    
    
    #define height and width of the target area
    height, width = len(target), len(target[0])
    #create empty solution matrix
    S = [[(0, 0) for c in range(0, width)] for r in range(0, height)]
    #create count variable for piece number
    count = 0
    #x as a temp variable for target
    x = target
    #initial run
    C_t = neighbour_count(x)
    #looping
    #check each coordinate
    for r in range(height):
        for c in range(width):
            valid_pieces_t = check_piece_validity(C_t)
            placable_t = check_piece_score(C_t, valid_pieces_t)
            count += 1
            S, C_t = place_piece(C_t, placable_t, S, count)
    return S
