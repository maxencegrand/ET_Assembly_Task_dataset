# Users Data

User data is stored in two files:

* *dataset/user-mobile.csv* for users with experience of mobile configuration
* *dataset/user-stationary.csv* for users with experience of stationary configuration

User data contains the following information:

* User ID
* User position, i.e. whether the user does the experience sitting or standing
* if the user wears glasses or contact lenses
* Some calibration data. This part differs between mobile and stationary users
* For each figure, a Boolean indicates whether assembly data is available

## Mobile Users


| id       | position | glasses | eye0 | eye1 | screen | pupil | car | tb | house | sc | tc | tsb |
|----------|----------|---------|------|------|--------|-------|-----|----|-------|----|----|-----|
| 69907732 | sitting  | 1       | 0    | 1    | 1      | 3     | 1   | 1  | 1     | 1  | 1  | 1   |
| 6184491  | sitting  | 0       | 1    | 1    | 3      | 2     | 1   | 1  | 1     | 1  | 1  | 1   |


## Stationary Users
| id       | position | glasses | fovio | tobii | car | tb | house | sc | tc | tsb |
|----------|----------|---------|-------|-------|-----|----|-------|----|----|-----|
| 32322786 | sitting  | 0       | 2     | 2     | 1   | 1  | 1     | 1  | 1  | 1   |
| 6581999  | sitting  | 1       | 3     | 3     | 1   | 1  | 1     | 1  | 1  | 1   |