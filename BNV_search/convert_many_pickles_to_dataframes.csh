foreach dir($*)
    foreach decay('pmu' 'pe' 'nmu' 'ne' 'pnu')
        python convert_pickle_to_dataframe.py $dir/"$decay"/*.pkl
    end
end
