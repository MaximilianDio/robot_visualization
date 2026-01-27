"""
Shared video generation utilities.

This module provides common functionality for video generation and
frame processing used across visualization tools.
"""

from typing import Tuple
import cv2
import numpy as np


def calculate_fps_from_timestamps(time_ms: np.ndarray) -> float:
    """
    Calculate FPS from timestamp array.

    Args:
        time_ms: Array of timestamps in milliseconds

    Returns:
        Calculated FPS
    """
    if len(time_ms) < 2:
        return 30.0  # Default fallback

    t_end = time_ms[-1]
    fps = len(time_ms) / (t_end / 1000.0)
    return fps


def add_timestamp_to_frame(
    frame: np.ndarray,
    timestamp_ms: float,
    position: Tuple[int, int] = (20, 30),
    font_scale: float = 1.0,
    color: Tuple[int, int, int] = (255, 255, 255),
    thickness: int = 1
) -> np.ndarray:
    """
    Add timestamp overlay to frame.

    Args:
        frame: Input frame
        timestamp_ms: Timestamp in milliseconds
        position: Text position (x, y)
        font_scale: Font scale factor
        color: Text color (BGR)
        thickness: Text thickness

    Returns:
        Frame with timestamp overlay
    """
    formatted_timestamp = f"{int(timestamp_ms):04d}"
    cv2.putText(
        frame,
        f"Time: {formatted_timestamp} ms",
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness,
        cv2.LINE_AA,
    )
    return frame


def create_video_writer(
    output_path: str,
    fps: float,
    frame_size: Tuple[int, int],
    fourcc: str = "mp4v"
) -> cv2.VideoWriter:
    """
    Create a configured video writer.

    Args:
        output_path: Path to output video file
        fps: Frames per second
        frame_size: Frame dimensions (width, height)
        fourcc: Video codec fourcc code

    Returns:
        Configured VideoWriter instance
    """
    fourcc_code = cv2.VideoWriter_fourcc(*fourcc)
    return cv2.VideoWriter(output_path, fourcc_code, fps, frame_size)


def interpolate_frame_count(
    current_time: float,
    previous_time: float,
    mean_fps: float
) -> int:
    """
    Calculate number of frames to repeat based on time delta.

    Args:
        current_time: Current timestamp
        previous_time: Previous timestamp
        mean_fps: Mean frames per second

    Returns:
        Number of frames to repeat
    """
    dt = (current_time - previous_time) / 1000.0  # Convert to seconds
    return max(1, int(round(dt * mean_fps)))


def display_frame(
    window_name: str,
    frame: np.ndarray,
    wait_time: int = 1
):
    """
    Display frame in OpenCV window.

    Args:
        window_name: Name of the display window
        frame: Frame to display
        wait_time: Wait time in milliseconds
    """
    cv2.imshow(window_name, frame)
    cv2.waitKey(wait_time)


def close_all_windows():
    """Close all OpenCV windows."""
    cv2.destroyAllWindows()