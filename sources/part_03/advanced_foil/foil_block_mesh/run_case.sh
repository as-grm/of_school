#!/bin/bash


usage()
{
    echo "usage: run_case.sh -a {0,1,2,3,5,10,15,20} "
}

path=$(pwd)
case=simpleFoam

# clean case
cd $path/$case
./Allclean


no_args="true"
U_file=0/U

while getopts a: flag
do
    case "${flag}" in
        a) 
            angle=${OPTARG}
            if [ $angle = 0 ]; then
                sed -e s/"^internalField.*"/"internalField   uniform (60 0 0);"/g \
                $U_file > temp.$$
                mv temp.$$ $U_file
            elif [ $angle = 1 ]; then
                sed -e s/"^internalField.*"/"internalField   uniform (59.99086 1.04714 0);"/g \
                $U_file > temp.$$
                mv temp.$$ $U_file
            elif [ $angle = 2 ]; then
                sed -e s/"^internalField.*"/"internalField   uniform (59.96345 2.09397 0);"/g \
                $U_file > temp.$$
                mv temp.$$ $U_file
            elif [ $angle = 3 ]; then
                sed -e s/"^internalField.*"/"internalField   uniform (59.91777 3.14016 0);"/g \
                $U_file > temp.$$
                mv temp.$$ $U_file
            elif [ $angle = 5 ]; then
                sed -e s/"^internalField.*"/"internalField   uniform (59.77168 5.22935 0);"/g \
                $U_file > temp.$$
                mv temp.$$ $U_file
            elif [ $angle = 10 ]; then
                sed -e s/"^internalField.*"/"internalField   uniform (59.08847 10.41889 0);"/g \
                $U_file > temp.$$
                mv temp.$$ $U_file
            elif [ $angle = 15 ]; then
                sed -e s/"^internalField.*"/"internalField   uniform (57.95555 15.52914 0);"/g \
                $U_file > temp.$$
                mv temp.$$ $U_file
            elif [ $angle = 20 ]; then
                sed -e s/"^internalField.*"/"internalField   uniform (56.38156 20.52121 0);"/g \
                $U_file > temp.$$
                mv temp.$$ $U_file
            else
                echo "Angle should be 0,1,2,3,5,10,15 or 20 degrees!"
                exit 1
            fi
            ;;
        *) 
            usage
            exit 1
            ;;
    esac
    no_args="false"
done

[[ "$no_args" == "true" ]] && { usage; exit 1; }

shift $((OPTIND-1))

if [ -z "${case}" ] || [ -z "${angle}" ]; then
    usage
    exit 1
fi

echo "Running case: simpleFoam";
echo "Foil angle: $angle [deg]";
cd $path/$case
./Allrun $case

#foamMonitor -l -r 1 $case/postProcessing/residuals/0/residuals.dat
