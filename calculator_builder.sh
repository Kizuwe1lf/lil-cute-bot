dotnet build osu-tools

rm osu-tools/PerformanceCalculator/bin/Debug/net6.0/runtimes -r
mv osu-tools/PerformanceCalculator/bin/Debug/net6.0 my_files/pp_calculator

rm osu-tools -r
