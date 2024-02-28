user=$1
setup=$2
position=$3

echo "User = $user Setup = $setup Position = $position"

raw_data=../raw_data/$setup/$position/$user
dataset=../dataset/$setup/$position
dataviz=../dataviz/$setup/$position
if [ -d "$raw_data" ]; then

  mkdir $dataset/$user
  for figure in car tb house sc tc tsb
  do
    mkdir -p $dataset/$user/$figure
    mkdir -p $dataviz/$user/$figure
    gnome-terminal -e "python3 event_annotation.py -path ../raw_data -user $user -figure $figure -setup $setup -position $position" &
    gnome-terminal --wait -e "python3 instruction_annotation.py -path ../raw_data -user $user -figure $figure -setup $setup -position $position"
  done
else
  echo "$raw_data doesn't exist."
  exit 1
fi
