foreach dir($*)
    foreach decay('pmu' 'pe' 'nmu' 'ne' 'pnu')
        python merge_a_bunch_of_dataframes.py $dir/"$decay"/*.h5
    end
end

