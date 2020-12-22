# CamShift

A simple application to track objects in videos or via webcam using python and opencv. For detailed explanation check out my [blog]().

## How to run?

### 1. Create virtual environment

```shell
python3 -m venv venv
```

#### macOS
```shell
source venv/bin/activate
```

#### Windows
```shell
.\venv\Scripts\activate
```

### 2. Install required dependencies

```shell
pip3 install -r requirements.txt
```

### 3. Execute

```shell
python3 -m track
```

Press `i` to get into input-mode and set the coordinates of the object you want to track.
Once the coordinates are marked, press enter and the model will try to track the object. Note that the model may not be that accurate.
