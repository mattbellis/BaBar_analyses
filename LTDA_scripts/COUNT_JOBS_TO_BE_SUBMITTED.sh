#!/bin/bash
# Count the jobs that will be submitted by the sub_*.sh files, grouped by
# dataset (SP-1005, SP-1235, OnPeak data, ...) and summed over all runs.
#
# Usage:
#   ./count_jobs.sh                 # every dataset, one line each
#   ./count_jobs.sh -r              # also break each dataset down by run
#   ./count_jobs.sh -v              # also list every file
#   ./count_jobs.sh SP-1237 OnPeak  # only files matching these patterns
#
# Point it elsewhere with:  DIR=submission_scripts/other_analysis ./count_jobs.sh

dir="${DIR:-submission_scripts/bnv_analysis_lam0lamc}"
#dir="${DIR:-submission_scripts/bnv_analysis_lam0lam0}"

by_run=0
verbose=0
while getopts "rv" opt; do
    case "$opt" in
        r) by_run=1 ;;
        v) verbose=1 ;;
        *) echo "usage: $0 [-r] [-v] [pattern ...]" >&2; exit 1 ;;
    esac
done
shift $((OPTIND - 1))

declare -A total runs
order=()

for f in "$dir"/sub_*.sh; do
    [ -e "$f" ] || continue
    base=$(basename "$f")

    # dataset: SP-#### if present, otherwise the peak label from the data files
    if [[ $base =~ sub_(SP-[0-9]+)- ]]; then
        ds="${BASH_REMATCH[1]}"
    elif [[ $base =~ -(OnPeak|OffPeak)- ]]; then
        ds="Data-${BASH_REMATCH[1]}"
    else
        ds="unknown"
    fi

    # if patterns were given, keep only files matching one of them
    if [ $# -gt 0 ]; then
        keep=0
        for p in "$@"; do
            [[ $base == *"$p"* ]] && keep=1 && break
        done
        [ $keep -eq 1 ] || continue
    fi

    [[ $base =~ -(Run[0-9]+)- ]] && run="${BASH_REMATCH[1]}" || run="Run?"

    n=$(grep -c '^bsub' "$f")

    [ -n "${total[$ds]}" ] || order+=("$ds")
    total[$ds]=$(( ${total[$ds]:-0} + n ))
    runs[$ds/$run]=$(( ${runs[$ds/$run]:-0} + n ))

    [ $verbose -eq 1 ] && printf "    %6d  %s\n" "$n" "$base"
done

if [ ${#order[@]} -eq 0 ]; then
    echo "no matching sub_*.sh files in $dir" >&2
    exit 1
fi

grand=0
printf "%-14s %8s\n" "DATASET" "JOBS"
printf "%-14s %8s\n" "-------" "----"
while read -r ds; do
    printf "%-14s %8d\n" "$ds" "${total[$ds]}"
    if [ $by_run -eq 1 ]; then
        for key in "${!runs[@]}"; do
            [[ $key == "$ds/"* ]] && echo "${key#*/} ${runs[$key]}"
        done | sort -V | while read -r run n; do
            printf "  %-12s %8d\n" "$run" "$n"
        done
    fi
    grand=$((grand + total[$ds]))
done < <(printf '%s\n' "${order[@]}" | sort -V)

printf "%-14s %8s\n" "-------" "----"
printf "%-14s %8d\n" "TOTAL" "$grand"
