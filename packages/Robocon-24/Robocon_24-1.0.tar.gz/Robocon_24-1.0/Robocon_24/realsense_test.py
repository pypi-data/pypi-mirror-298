import cv2
import numpy as np
import pyrealsense2 as rs
import Robocon_24

def run_yolo():
    
    W = 640
    H = 480

    # Create a pipeline object
    pipeline = rs.pipeline()

    # Configure the pipeline to stream color and depth data
    config = rs.config()
    config.enable_stream(rs.stream.color, W, H, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, W, H, rs.format.z16, 30)

    # Start the pipeline
    profile = pipeline.start(config)
    align_to = rs.stream.color
    align = rs.align(align_to)


    try:
        while True:
            # Wait for frames from the pipeline
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)

            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()

            if not color_frame:
                continue

            color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.08), cv2.COLORMAP_JET)

            results_silo, result_image = Robocon_24.decision_maker(image_input_def=color_image, our_ball=0)
            print(results_silo)

            cv2.imshow("Result", result_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Stop the pipeline and release resources
        pipeline.stop()
        cv2.destroyAllWindows()

run_yolo()