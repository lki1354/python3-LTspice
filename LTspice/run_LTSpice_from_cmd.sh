#!/bin/bash

if [ $# = "2" ]; then
  echo "Your command line contains $# arguments and the simulation starts"
	SIM_FILE="$1"
	SIM_OUT="$2"
	#SIM="tempRun"
	SIM=$(echo $SIM_FILE | cut -f1 -d.)
	echo $SIM

	LTSpice_dir="~/.wine/drive_c/Program Files/LTC/LTspiceXVII/"
	LTSpice_cmd="./XVIIx64.exe -Run -b"
	#SIM_FILE="$SIM.$SIM_TYPE"

	cd "$LTSpice_dir"
	mkdir "$SIM"
	cp "$SIM_FILE" "$SIM/" 
	$LTSpice_cmd "$SIM/$SIM_FILE"
	cp "$SIM/$SIM.log" "$SIM_OUT"
	rm -rf "$SIM"

else
    echo "Your command line contains not 2 arguments"
fi
