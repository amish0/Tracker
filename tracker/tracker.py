
import numpy as np
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory

from tracker.Sort_Tracker.Sort import Sort
from tracker.Bot_Tracker.bot_sort import BoTSORT
from tracker.BYTE_Tracker.byte_tracker import BYTETracker

from tracker.basic_utils.loadyaml import load_yaml

TRACKER_MAP = {'bytetrack': BYTETracker, 'botsort': BoTSORT, 'sort': Sort}


class Tracker:
    """Tracker class for multi object tracking with some modifications to the original Sort class"""

    def __init__(self, tracker_type: str = 'sort') -> None:
        """@brief Tracker class
           @details will initialize the tracker with the given tracker_type and tracker parameters from corresponding yaml file
           @param tracker_type type of tracker to be used
        """
        if isinstance(tracker_type, str) and tracker_type in TRACKER_MAP.keys():
            if tracker_type == 'bytetrack':
                print("loading bytetrack.yaml")
                self.parm = load_yaml(ROOT / "cfg/bytetrack.yaml")
                print("bytetrack.yaml loaded")
                print("bytetrack.yaml: ", self.parm)
                self.tracker_type = tracker_type
            elif tracker_type == 'botsort':
                print("loading botsort.yaml")
                self.parm = load_yaml(ROOT / "cfg/botsort.yaml")
                print("botsort.yaml loaded")
                print("botsort.yaml: ", self.parm)
                self.tracker_type = tracker_type
            elif tracker_type == 'sort':
                print("loading sort.yaml")
                self.parm = load_yaml(ROOT / "cfg/sort.yaml")
                print("sort.yaml loaded")
                print("sort.yaml: ", self.parm)
                self.tracker_type = tracker_type
            else:
                print("tracker_type must be string and in {}".format(TRACKER_MAP.keys()))
                print("using default parameters and default tracker_type: sort")
                self.parm = None
                self.tracker_type = tracker_type

            if self.parm is None:
                self.parm = {'max_age': 1, 'min_hits': 3, 'iou_threshold': 0.3}
                print("sort.yaml not found, using default parameters")
            self.tracker = TRACKER_MAP[tracker_type](**self.parm)
        else:
            print("tracker_type must be string and in {}".format(TRACKER_MAP.keys()))

    # def update(self, detections: (list, np.ndarray))->any:
    #     """@brief update the tracker with new detections
    #        @details update the tracker with new detections
    #        @param detections new detections in the format [[x1, y1, x2, y2, score, class_id], ...]
    #        @return updated bounding boxes in the format [[x1, y1, x2, y2, score, class_id, track_id], ...] if tracker is not initalized it will return None
    #     """
    #     if isinstance(detections, list):
    #         detections = np.array(detections)
    #     if hasattr(self, 'tracker'):
    #         return self.tracker.update(detections)
    #     else:
    #         print("tracker not init")
    #         return None

    def update(self, detections, img: np.ndarray = None)->any:
        """@brief update the tracker with new detections
           @details update the tracker with new detections
           @param detections new detections in the format
                if tracker_type == 'bytetrack' or tracker_type == 'botsort':
                    detections: Result class with following attributes
                        class Result:
                            def __init__(self) -> None:
                                self.xyxy = None
                                self.conf = None
                                self.cls = None
                    img: np.ndarray image
                
                if tracker_type == 'sort':
                    detections: new detections in the format
                    detections: [[x1, y1, x2, y2, score, class_id], ...]
           @return updated bounding boxes in the format [[x1, y1, x2, y2, track_id, score, class_id], ...] if tracker is not initalized it will return None
        """
        if hasattr(self, 'tracker'):
            if self.tracker_type == 'bytetrack' or self.tracker_type == 'botsort':
                if img is None:
                    print("img is required for bytetrack and botsort")
                    return None
                else:
                    return self.tracker.update(detections, img)
            else:
                if isinstance(detections, list):
                    detections = np.array(detections)
                elif isinstance(detections, np.ndarray):
                    pass
                else:
                    print("detections must be list or np.ndarray")
                    return None
                return self.tracker.update(detections)
        else:
            print("tracker not init")
            return None

    def __call__(self, detections, img=None):
        """@brief update the tracker with new detections
           @details update the tracker with new detections
           @param detections parameters in the format 
                if tracker_type == 'bytetrack' or tracker_type == 'botsort':
                    detections: Result class with following attributes
                        class Result:
                            def __init__(self) -> None:
                                self.xyxy = None
                                self.conf = None
                                self.cls = None
                    img: np.ndarray image
                
                if tracker_type == 'sort':
                    detections: new detections in the format
                    detections: [[x1, y1, x2, y2, score, class_id], ...]
           @return updated bounding boxes in the format [[x1, y1, x2, y2, track_id, score, class_id], ...] if tracker is not initalized it will return None"""
        return self.update(detections, img)

    def check_parameters(self):
        print(self.parm)


class MuliCameraTracker:
    """@brief MultiCameraTracker class
       @details his class will initialize the tracker with the given tracker_type,
       and a set of tracker id (each tracker id will be associated with each camera) 
       and tracker parameters from `yaml` file.
       """
    # TODO: add multi camera tracker
    pass

if __name__ == "__main__":
    object_tracker = Tracker('sort')
    print("test case started")
    print("test case 1")
    test = object_tracker([[0.1, 0.2, 0.3, 0.4, 0.5, 0], [0.2, 0.3, 0.4, 0.5, 0.6, 1]])
    for *xyxy, ID, conf, cls in test:
        print("xyxy: ", xyxy)
        print("conf: ", conf)
        print("cls: ", cls)
        print("ID: ", ID)
        print("\n")
    print("test case ended")
    
