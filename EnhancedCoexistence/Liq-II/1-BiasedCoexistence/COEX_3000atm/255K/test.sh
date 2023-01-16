START=$(date)
sleep 1
END=$(date)
Time_diff_in_secs=$(($(date -d "$END" +%s) - $(date -d "$START" +%s)))
if [ "$Time_diff_in_secs" -le "300" ]; then
    echo Run exited premeaturely, no resubmission!
    exit
fi

