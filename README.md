# Tracker
This package is an collection of three type of tracker. `TRACKER_MAP = {'bytetrack': BYTETracker, 'botsort': BoTSORT, 'sort': Sort}`

## Example
<details close>
<summary>Tracker class can be used to track the objects in a video.</summary> Please check the [tracker.py](tracker/tracker.py) for more details.

```bash
# import tracker
from tracker.tracker import Tracker

# Create an instance of tracker
tracker = Tracker(tracker_type = 'sort')

# detections result from object detector
dets = np.array([[0,0,10,10,0.9,1],[0,0,10,10,0.8,1],[0,0,10,10,0.7,1], ....])

# update tracker
tracking_results = tracker(dets)

# print tracking results
print(tracking_results)
```
</details>

<details close>
<summary>Class Explanation</summary>

- `Tracker`: This class will initialize the tracker with the given tracker_type and tracker parameters from [corresponding yaml](tracker/cfg/*.yaml) file. __call__ will take the detections and return the tracking results. Please check the [tracker.py](tracker/tracker.py) for more details.
    - arguments:
    
        detections parameters in the format 

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
                    detections: `[[x1, y1, x2, y2, score, class_id], ...]`

    - returns:
        - Returns the updated bounding boxes in the format `[[x1, y1, x2, y2, track_id, score, class_id], ...]` if tracker is not initalized it will return None
</details>

## Use in your own peoject
Below is the gist of how to instantiate and update the tracker. Please check the [tracker.py](tracker/tracker.py) for more details.
1. using Sort Tracker
```bash

from tracker.tracker import Tracker
# Create an instance of tracker
obj_tracker = Tracker(tracker_type = 'sort')
# get detections
...

# update SORT
track_bbs_conf_cls_ids = obj_tracker(detections)

# track_bbs_conf_cls_ids is a np array where each row contains a valid bounding box, track_id, score and class
...
```
2. Using ByteTracker and Boat Tracker using yolov5 object detector
```bash

from tracker.tracker import Tracker
# Create an instance of tracker
obj_tracker = Tracker(tracker_type = 'bytetrack')

# create class to store results of each frame
class Result:
    def __init__(self) -> None:
        self.xyxy = None
        self.conf = None
        self.cls = None
# get detections
...
...

if len(det):
    # Rescale boxes from img_size to im0 size
    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
    # detect results
    det1 = det.cpu().numpy()
    # update result class
    results.xyxy = det1[:, :4]
    results.conf = det1[:, 4]
    results.cls = det1[:, 5]
    # update Tracker
    det_S = obj_tracker(results, im0)
    if (det_S is not None) and (det_S.size != 0):
        for *xyxy, ID, conf, cls in reversed(det_S):
            # *xyxy : Bounding box
            # ID: id of each object
            # conf: confidence score
            # cls: class index
        ...
        ...
    ...
...

```

## Build setup
```
# Go to code directory
cd some_root_dir

# create build

python -m build
# or
# python setup.py sdist bdist_wheel
```
It will create build in your dist directory. if dist is not present it will create it.

## Install Packages
 
 if you have not made any build, please follow the command

 ```
 python setup.py install
 ```

 If you have created an build, please follow the instruction below
 ```
 cd dist
 pip install package_name*.whl
 ```
 Please replace "package_name*.whl" with .whl file present in dist directory

## Work from source code
Clone repo and install [requirements.txt](requirements.txt)

```bash
git https://github.com/amish0/Tracker.git
cd Tracker
pip install -r requirements.txt
```

# References
    - SORT: https://github.com/abewley/sort

    - Byte Track: https://github.com/ifzhang/ByteTrack

    - BoT-SORT: https://github.com/NirAharon/BoT-SORT
