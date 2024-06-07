# Eye-Tracking Data During Lego Duplo Assembly

## Overview
This dataset contains ocular data collected during the assembly of figures using Lego Duplo. The data were gathered as part of a study aimed at evaluating the performance of different eye movement measurement devices in a simulated industrial context.

## Contents
The dataset includes:
- **Task Details**: Information about the assembly tasks performed, including instructions and configurations.
- **Eye-Tracking Data**: Recorded data from the eye-tracking devices during the assembly tasks.

## Task Dataset

All data are stored in the ***tasks/*** directory.

### Block Position in Stock Zone Table Documentation

First, we have the table tasks/stock.csv. This table contains the coordinates of blocks used during the assembly tasks. Each row represents a block with its corresponding x and y coordinates in the workspace:

- **block**: An identifier for each block.
- **x**: The x-coordinate of the block in the workspace.
- **y**: The y-coordinate of the block in the workspace.

### Figure Instructions Table Documentation

Each figure has a subdirectory containing the `instructions.csv` file. This file provides detailed instructions for assembling the figure using specific blocks. The table includes the coordinates for each corner of the block at different stages of placement.

#### Columns

- **id**: The instruction identifier, unique for each step in the assembly process.
- **block**: The identifier for the block to be placed or moved.
- **x0, y0**: The x and y coordinates of the first corner of the block.
- **x1, y1**: The x and y coordinates of the second corner of the block.
- **x2, y2**: The x and y coordinates of the third corner of the block.
- **x3, y3**: The x and y coordinates of the fourth corner of the block.
- **level**: The number of blocks beneath the current block. For example, `level = 0` means no block is beneath the current block.

#### Description

This table provides step-by-step instructions for assembling a figure. Each row represents a single instruction, detailing the coordinates of each corner of a block before it is placed or moved. The coordinates ensure precise placement of each block in the assembly process.

#### Notes

- The `id` column ensures that instructions are followed in the correct order.
- The `x0, y0`, `x1, y1`, `x2, y2`, and `x3, y3` columns represent the coordinates of the four corners of each block, from the top left to the bottom left.
- The `level` column indicates the number of blocks beneath the current block, which is important for understanding the vertical structure of the assembly. For example, `level = 0` means no block is beneath the current block.


## Eye-Tracking Dataset

All data are stored in the ***dataset/*** directory. The dataset is organized into directories based on the configuration of the eye-tracking devices and the participant's position during the tasks. The root directory is `dataset`, which contains subdirectories for each configuration and position, followed by a unique ID directory for each participant.

    root/
    └── dataset/
    ├── mobile/
    │ ├── sitting/
    │ │ ├── participant_id_1/
    │ │ ├── participant_id_2/
    │ │ └── ...
    │ └── standing/
    │ ├── participant_id_1/
    │ ├── participant_id_2/
    │ └── ...
    └── stationnary/
    ├── sitting/
    │ ├── participant_id_1/
    │ ├── participant_id_2/
    │ └── ...
    └── standing/
    ├── participant_id_1/
    ├── participant_id_2/
    └── ...

Each participant directory contains the following files:

- **events.csv**: Logs of different events during the assembly tasks.
- **table.csv**: Positions of the participant's gaze points recorded on the table during the tasks.
- **states.csv**: The state of the assembly table at different times during the tasks.

### events.csv

This file logs different events that occur during the assembly tasks.

##### Columns

- **timestamp**: The time at which the event occurred.
- **action**: The action type (0 for grasping a block, 1 for releasing a block).
- **block**: The identifier for the block involved in the event.
- **x0, y0**: The x and y coordinates of the first corner of the block.
- **x1, y1**: The x and y coordinates of the second corner of the block.
- **x2, y2**: The x and y coordinates of the third corner of the block.
- **x3, y3**: The x and y coordinates of the fourth corner of the block.
- **level**: The number of blocks beneath the current block.

### table.csv

This file contains the positions of the participant's gaze points recorded during the assembly tasks.

##### Columns

- **timestamp**: The time at which the gaze point was recorded.
- **x**: The x-coordinate of the gaze point.
- **y**: The y-coordinate of the gaze point.

### state.csv

This file provides the state of the assembly table at different timestamps during the tasks.

#### Columns

- **timestamp**: The time at which the state was recorded.
- For each block:
 - **x0, y0**: The x and y coordinates of the first corner of the block.
 - **x1, y1**: The x and y coordinates of the second corner of the block.
 - **x2, y2**: The x and y coordinates of the third corner of the block.
 - **x3, y3**: The x and y coordinates of the fourth corner of the block.
 - **level**: The number of blocks beneath the current block.
 - **holding**: Indicates whether the block is being held by a participant (1 for holding, 0 for not holding).

The columns are structured in a hierarchical manner to represent the positions and levels of blocks on the assembly table.
