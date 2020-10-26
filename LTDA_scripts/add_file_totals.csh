foreach n(1 2 3 4 5 6)
    ls -l rootfiles/AllEvents-Run"$n"-OnPeak-R24 | awk '{print $5}' | awk '{total = total + $1}END{print total}'
end

