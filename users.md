# User Data
## 1. General Information
### Dataset Names:
   - **users-mobiles.csv** (Mobile eye tracking data with Pupil)
   - **userq-stationary.csv** (Stationary eye tracking data with Fovio and Tobii)
### Data Types:
   - users-mobiles: Data collected using a mobile eye tracker (Pupil).
   - userq-stationary: Data collected using stationary eye trackers (Fovio and Tobii).

## 2. Common Variables for Both Datasets
   - **id:** Unique identifier for each participant
   -  **glasses:** Indication if the participant wore glasses or contact lenses (1 for yes, 0 for no).
   - **position:** Participant's position during recording (sitting/standing).
   - **car, tb, house, sc, tc, tsb:** Binary variables indicating if the corresponding figure was recorded (1 for recorded, 0 for not recorded).

## 3. Usesr-mobile Specific Variables
   - **eye0, eye1:** Recording status for eye 0 and eye 1 (1 for recorded, 0 for not recorded).
   - **screen:** Number of sides of the screen visible to the participant.
   - **pupil:** Calibration score (0: no data, 1: severe, 2: slight, 3: no issue).

## 4. Users-stationary Specific Variables
   - **fovio:** Fovio calibration score (0: no data, 1: severe, 2: slight, 3: no issue).
   - **tobii:** Tobii calibration score (0: no data, 1: severe, 2: slight, 3: no issue).