import cv2

def visualizeTracking(tracked_objs):
	# Code for visualizing tracking output (should make this a separate function later on)
	for tracked_obj in tracked_objs.values():
		id = float(tracked_obj["name"])
		color = (int((id%1)*255), int((id*100%1)*255), int((id*10000%1)*255))
		current_pos = tracked_obj["history"][str(tracked_obj["lastUpdate"])]
		current_pos = [int(elem) for elem in current_pos]
		image = cv2.rectangle(image, (current_pos[0], current_pos[1]), (current_pos[2], current_pos[3]), color, 2)
		for i in range(len(list(tracked_obj["history"]))-1):
			pos_c = tracked_obj["history"][list(tracked_obj["history"])[i]]
			pos_n = tracked_obj["history"][list(tracked_obj["history"])[i+1]]

			midpoint_c = (int((pos_c[0] + pos_c[2])/2),int((pos_c[1] + pos_c[3])/2))
			midpoint_n = (int((pos_n[0] + pos_n[2])/2),int((pos_n[1] + pos_n[3])/2))

			image = cv2.line(image, midpoint_c, midpoint_n, color, 2)
	cv2.imwrite("../frame" + str(frame_index) + ".jpg", image)