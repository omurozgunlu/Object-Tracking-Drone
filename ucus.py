from __future__ import print_function
import time
from dronekit import connect, VehicleMode, mavutil
import math
import pickle



def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,  # time_boot_ms (not used)
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0, 0, 0,  # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z,  # x, y, z velocity in m/s
        0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    # send command to vehicle on 1 Hz cycle
    for x in range(0, duration):
        vehicle.send_mavlink(msg)


vehicle = connect("127.0.0.1:14551", wait_ready=True)
derece = vehicle.heading
derece1 = math.fmod((-derece + 90), 360)
radian = 2 * math.pi * derece1 / 360

arm_and_takeoff(10)
vehicle.airspeed=5
vehicle.groundspeed=5
while True:
    with open("paylasim.pkl", "rb") as f:
        xd = pickle.load(f)
        #time.sleep(3)
        
    a_e = xd[0]+1
    a_n = xd[1]+1
    dist_x = math.fabs(a_e - 160)
    dist_y = math.fabs(a_n - 240)
    disx=math.pow(dist_x,2)
    disy=math.pow(dist_y,2)
    distance=disx+disy
    dis=math.sqrt(distance)
    oran=dist_y/dis
    aci=math.acos(oran)
    radian_aci=aci*360/(2*math.pi)
    
    
    
    
    hedef = math.fmod((-radian_aci + 90), 360)
    radian_2 = 2 * math.pi * hedef / 360
    radian_3=90-radian_2
    #print(radian_2)
    print("aci:",aci)
    print("hedef aci:",hedef)
    print("radian_2:",radian_3)
    
    
    if a_e > 160:
        if a_n<120:
            v_n = math.sin(radian - radian_3)
            v_e = math.cos(radian - radian_3)
            v_N=v_n*2
            v_E=v_e*2
            send_ned_velocity(v_N,v_E,0,3)
            print (" plus ")
            #print (v_N)
        elif a_n>120:
            v_n = math.sin(radian - radian_3)
            v_e = math.cos(radian - radian_3)
            v_N=-v_n*2
            v_E=v_e*2
            send_ned_velocity(v_N,v_E,0,3)
            print (" minus ")
            #print (-v_N)
    elif  a_e < 160:
        
        if a_n<120:
            v_n = math.sin(radian - radian_3)
            v_e = math.cos(radian - radian_3)
            v_N=v_n*2
            v_E=-v_e*2
            send_ned_velocity(v_N,v_E,0,3)
            print (" plus ")
            #print (v_N)
        elif a_n>120:
            v_n = math.sin(radian - radian_3)
            v_e = math.cos(radian - radian_3)
            v_N=-v_n*2
            v_E=-v_e*2
            send_ned_velocity(v_N,v_E,0,3)
            print (" minus ")
            #print (-v_N)
            #print (radian_3)
    elif (a_e > 140 and a_e < 180 and a_n > 100 and a_n < 140):
        send_ned_velocity(0,0,0,3)
        print("Position Hold")
  
    #print("going to target")
    elif vehicle.mode == VehicleMode("POSHOLD"):
        break
    else:
        send_ned_velocity(0,0,0,3)
    #send_ned_velocity(v_N,v_E,0,3)
    
    time.sleep(3)
vehicle.mode=VehicleMode("RTL")
time.sleep(3)
vehicle.close()
    
        
        





