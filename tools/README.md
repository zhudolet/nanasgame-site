# Updating the playable game in /play

`play/` is the browser copy of the game from the `xmas-lights-app` repo (`game/` folder),
with Google Fonts swapped for the local fonts in `play/fonts/`, test mode switched off and
a level limit added (no ads bridge).

To refresh it after the game changes:

    cp -r play/fonts /tmp/xl-fonts
    python3 tools/build_play.py path/to/xmas-lights-app/game play /tmp/xl-fonts 10

The last number is how many levels the web demo allows (10 = District 1). Past that, the
game shows a "That's the web demo" card with a Become a tester button. Test mode is off in
the web copy. If you change the number, change `WEB` near the top of the script in
`index.html` to match.

The home page reads the level list from `play/levels/journey-levels-city.js` and talks to
the game through `window.__nl` (`openJIntro`, `openMap`, `LEVELS`, `G`). If the levels file
is renamed, update the `<script src>` near the bottom of `index.html`.
