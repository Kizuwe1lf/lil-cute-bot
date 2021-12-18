git clone https://github.com/ppy/osu-tools
git clone https://github.com/ppy/osu

mv osu/osu.Game.Rulesets.Osu osu-tools/
mv osu/osu.Game.Rulesets.Taiko osu-tools/
mv osu/osu.Game.Rulesets.Mania osu-tools/
mv osu/osu.Game.Rulesets.Catch osu-tools/

sudo rm -r osu
rm my_files/pp_calculator -r