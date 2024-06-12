# COMPENG 2DX3 Deliverable 2 Code
# Caylia Bonnick
# Student Number: 400373187
# April 1, 2024

import serial
import time
import numpy as np
import open3d as o3d
if __name__ == "__main__":
    s = serial.Serial('COM3',baudrate=115200,timeout=10)
    #print("Opening: " + s.name)
    steps = int(input("How many steps are you taking?")) # User input for the number of steps
    f = open("2dx3bonnickc.xyz", "w")    #create a new file for writing 

    # reset the buffers of the UART port to delete the remaining data in the buffers
    s.reset_output_buffer()
    s.reset_input_buffer()


    # Send the character 's' to MCU via UART to signal MCU to start transmission
    s.write('s'.encode())

    # Loop to receive point cloud data from the serial port and write it to the file
    for i in range(30*(steps-1)):
        x = s.readline() # Read a line of data from the serial port
        coordinate=x.decode() # Decode the received data to string format
        f.write(coordinate) # Write the received data to the file
        print(coordinate) # Print the received data


    # Close the file and serial port
    f.close()
    s.close()
    
    
    #Reading the test data from the file we created        
    print("Read in the prism point cloud data (pcd)")
    pcd = o3d.io.read_point_cloud("2dx3bonnickc.xyz", format="xyz")

    #Seeing what the point cloud data looks like numerically       
    print("PCD array:")
    print(np.asarray(pcd.points))

    # Visualize the 3D rendering of the point cloud       
    print("Visualizing the 3D rendering: ")
    o3d.visualization.draw_geometries([pcd])


    # Create a line set to connect vertices in the point cloud    
    yz_slice_vertex = []
    for x in range(0,30*(steps-1)):
        yz_slice_vertex.append([x])

    #Defining coordinates to connect lines in each yz slice        
    lines = []  
    for x in range(0,30*(steps-1),30): #loop that iterates over the range of 0 to
        #30*(steps-1) with a step size of 30 over each yz slice
        lines.append([yz_slice_vertex[x], yz_slice_vertex[x + 1]])
        lines.append([yz_slice_vertex[x + 1], yz_slice_vertex[x + 2]])
        lines.append([yz_slice_vertex[x + 2], yz_slice_vertex[x + 3]])
        lines.append([yz_slice_vertex[x + 3], yz_slice_vertex[x + 4]])
        lines.append([yz_slice_vertex[x + 4], yz_slice_vertex[x + 5]])
        lines.append([yz_slice_vertex[x + 5], yz_slice_vertex[x + 6]])
        lines.append([yz_slice_vertex[x + 6], yz_slice_vertex[x + 7]])
        lines.append([yz_slice_vertex[x + 7], yz_slice_vertex[x + 8]])
        lines.append([yz_slice_vertex[x + 8], yz_slice_vertex[x + 9]])
        lines.append([yz_slice_vertex[x + 9], yz_slice_vertex[x + 10]])
        lines.append([yz_slice_vertex[x + 10], yz_slice_vertex[x + 11]])
        lines.append([yz_slice_vertex[x + 11], yz_slice_vertex[x + 12]])
        lines.append([yz_slice_vertex[x + 12], yz_slice_vertex[x + 13]])
        lines.append([yz_slice_vertex[x + 13], yz_slice_vertex[x + 14]])
        lines.append([yz_slice_vertex[x + 14], yz_slice_vertex[x + 15]])
        lines.append([yz_slice_vertex[x + 15], yz_slice_vertex[x + 16]])
        lines.append([yz_slice_vertex[x + 16], yz_slice_vertex[x + 17]])
        lines.append([yz_slice_vertex[x + 17], yz_slice_vertex[x + 18]])
        lines.append([yz_slice_vertex[x + 18], yz_slice_vertex[x + 19]])
        lines.append([yz_slice_vertex[x + 19], yz_slice_vertex[x + 20]])
        lines.append([yz_slice_vertex[x + 20], yz_slice_vertex[x + 21]])
        lines.append([yz_slice_vertex[x + 21], yz_slice_vertex[x + 22]])
        lines.append([yz_slice_vertex[x + 22], yz_slice_vertex[x + 23]])
        lines.append([yz_slice_vertex[x + 23], yz_slice_vertex[x + 24]])
        lines.append([yz_slice_vertex[x + 24], yz_slice_vertex[x + 25]])
        lines.append([yz_slice_vertex[x + 25], yz_slice_vertex[x + 26]])
        lines.append([yz_slice_vertex[x + 26], yz_slice_vertex[x + 27]])
        lines.append([yz_slice_vertex[x + 27], yz_slice_vertex[x + 28]])
        lines.append([yz_slice_vertex[x + 28], yz_slice_vertex[x + 29]])
        lines.append([yz_slice_vertex[x + 29], yz_slice_vertex[x]])

   #Defining coordinates to connect lines between current and next yz slice
#  #Append pairs of vertices to the lines list

    for x in range(0,30*(steps-1)-30,30): #another loop that iterates over the range of 0 to
        #30*(steps-1) with a step size of 30 over each yz slice
        lines.append([yz_slice_vertex[x], yz_slice_vertex[x + 30]])
        lines.append([yz_slice_vertex[x + 1], yz_slice_vertex[x + 31]])
        lines.append([yz_slice_vertex[x + 2], yz_slice_vertex[x + 32]])
        lines.append([yz_slice_vertex[x + 3], yz_slice_vertex[x + 33]])
        lines.append([yz_slice_vertex[x + 4], yz_slice_vertex[x + 34]])
        lines.append([yz_slice_vertex[x + 5], yz_slice_vertex[x + 35]])
        lines.append([yz_slice_vertex[x + 6], yz_slice_vertex[x + 36]])
        lines.append([yz_slice_vertex[x + 7], yz_slice_vertex[x + 37]])
        lines.append([yz_slice_vertex[x + 8], yz_slice_vertex[x + 38]])
        lines.append([yz_slice_vertex[x + 9], yz_slice_vertex[x + 39]])
        lines.append([yz_slice_vertex[x + 10], yz_slice_vertex[x + 40]])
        lines.append([yz_slice_vertex[x + 11], yz_slice_vertex[x + 41]])
        lines.append([yz_slice_vertex[x + 12], yz_slice_vertex[x + 42]])
        lines.append([yz_slice_vertex[x + 13], yz_slice_vertex[x + 43]])
        lines.append([yz_slice_vertex[x + 14], yz_slice_vertex[x + 44]])
        lines.append([yz_slice_vertex[x + 15], yz_slice_vertex[x + 45]])
        lines.append([yz_slice_vertex[x + 16], yz_slice_vertex[x + 46]])
        lines.append([yz_slice_vertex[x + 17], yz_slice_vertex[x + 47]])
        lines.append([yz_slice_vertex[x + 18], yz_slice_vertex[x + 48]])
        lines.append([yz_slice_vertex[x + 19], yz_slice_vertex[x + 49]])
        lines.append([yz_slice_vertex[x + 20], yz_slice_vertex[x + 50]])
        lines.append([yz_slice_vertex[x + 21], yz_slice_vertex[x + 51]])
        lines.append([yz_slice_vertex[x + 22], yz_slice_vertex[x + 52]])
        lines.append([yz_slice_vertex[x + 23], yz_slice_vertex[x + 53]])
        lines.append([yz_slice_vertex[x + 24], yz_slice_vertex[x + 54]])
        lines.append([yz_slice_vertex[x + 25], yz_slice_vertex[x + 55]])
        lines.append([yz_slice_vertex[x + 26], yz_slice_vertex[x + 56]])
        lines.append([yz_slice_vertex[x + 27], yz_slice_vertex[x + 57]])
        lines.append([yz_slice_vertex[x + 28], yz_slice_vertex[x + 58]])
        lines.append([yz_slice_vertex[x + 29], yz_slice_vertex[x+59]])
 


    # Map the lines to the 3D coordinate vertices
    line_set = o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(np.asarray(pcd.points)),lines=o3d.utility.Vector2iVector(lines))

     # Visualize the point cloud data with lines       
    o3d.visualization.draw_geometries([line_set])
                                    
    
